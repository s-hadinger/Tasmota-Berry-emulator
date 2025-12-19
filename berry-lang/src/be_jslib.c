/********************************************************************
** Berry JavaScript Bridge Module for WebAssembly
** 
** This module provides JavaScript interop for Berry code running
** in a WebAssembly environment. It enables Berry code to call
** JavaScript functions, access properties, and interact with
** browser APIs.
**
** Part of the Berry Animation Framework Browser Simulator.
********************************************************************/
#include "berry.h"
#include "be_object.h"
#include "be_exec.h"
#include "be_vm.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#if defined(__EMSCRIPTEN__)

#include <emscripten.h>

/* strdup is not part of C99, provide our own implementation */
static char* js_strdup(const char* s)
{
    if (!s) return NULL;
    size_t len = strlen(s) + 1;
    char* copy = (char*)malloc(len);
    if (copy) {
        memcpy(copy, s, len);
    }
    return copy;
}

/*******************************************************************************
 * JavaScript function implementations using EM_JS
 * These provide the Berry-to-JavaScript bridge
 * Full implementations will be added in task 3.1
 ******************************************************************************/

/* Call a JavaScript function by name with JSON-encoded arguments
 * Returns a pointer to a JSON-encoded result string (caller must free) */
EM_JS(char*, js_call_impl, (const char* func_name_ptr, const char* args_json_ptr), {
    try {
        var funcName = UTF8ToString(func_name_ptr);
        var argsJson = UTF8ToString(args_json_ptr);
        var args = [];
        
        // Try to parse as JSON array, but if it fails, treat as single string argument
        if (argsJson) {
            try {
                args = JSON.parse(argsJson);
                if (!Array.isArray(args)) {
                    args = [args];
                }
            } catch (parseErr) {
                // Not valid JSON - treat as single string argument
                args = [argsJson];
            }
        }
        
        // Resolve function by name (supports nested properties like "Math.pow")
        var parts = funcName.split('.');
        var func = globalThis;
        for (var i = 0; i < parts.length; i++) {
            func = func[parts[i]];
            if (func === undefined) {
                console.error("JS call error: function not found:", funcName);
                return 0;
            }
        }
        
        if (typeof func === 'function') {
            var result = func.apply(null, args);
            // Handle undefined result (void functions) - convert to null for JSON
            if (result === undefined) {
                result = null;
            }
            var resultJson = JSON.stringify(result);
            var len = lengthBytesUTF8(resultJson) + 1;
            var ptr = _malloc(len);
            stringToUTF8(resultJson, ptr, len);
            return ptr;
        }
        return 0;
    } catch (e) {
        console.error("JS call error:", e);
        return 0;
    }
});

/* Get a JavaScript property value by path (e.g., "window.myVar")
 * Returns a pointer to a JSON-encoded value string (caller must free) */
EM_JS(char*, js_get_impl, (const char* prop_path_ptr), {
    try {
        var propPath = UTF8ToString(prop_path_ptr);
        var parts = propPath.split('.');
        var value = globalThis;
        for (var i = 0; i < parts.length; i++) {
            value = value[parts[i]];
            if (value === undefined) {
                return 0;
            }
        }
        var resultJson = JSON.stringify(value);
        var len = lengthBytesUTF8(resultJson) + 1;
        var ptr = _malloc(len);
        stringToUTF8(resultJson, ptr, len);
        return ptr;
    } catch (e) {
        console.error("JS get error:", e);
        return 0;
    }
});

/* Set a JavaScript property value by path
 * value_json is the JSON-encoded value to set */
EM_JS(void, js_set_impl, (const char* prop_path_ptr, const char* value_json_ptr), {
    try {
        var propPath = UTF8ToString(prop_path_ptr);
        var valueJson = UTF8ToString(value_json_ptr);
        var value = JSON.parse(valueJson);
        
        var parts = propPath.split('.');
        var obj = globalThis;
        for (var i = 0; i < parts.length - 1; i++) {
            obj = obj[parts[i]];
            if (obj === undefined) {
                console.error("JS set error: path not found:", propPath);
                return;
            }
        }
        obj[parts[parts.length - 1]] = value;
    } catch (e) {
        console.error("JS set error:", e);
    }
});

/* Log a message to the JavaScript console */
EM_JS(void, js_log_impl, (const char* message_ptr), {
    var message = UTF8ToString(message_ptr);
    console.log("[Berry]", message);
});

/*******************************************************************************
 * Helper functions
 ******************************************************************************/

/* Convert Berry value at stack index to JSON string
 * Caller must free the returned string
 * For non-JSON types (functions, classes, etc.), returns a string representation */
static char* berry_to_json(bvm *vm, int index)
{
    if (be_isnil(vm, index)) {
        return js_strdup("null");
    } else if (be_isbool(vm, index)) {
        return js_strdup(be_tobool(vm, index) ? "true" : "false");
    } else if (be_isint(vm, index)) {
        char buf[32];
        snprintf(buf, sizeof(buf), "%lld", (long long)be_toint(vm, index));
        return js_strdup(buf);
    } else if (be_isreal(vm, index)) {
        char buf[32];
        snprintf(buf, sizeof(buf), "%g", (double)be_toreal(vm, index));
        return js_strdup(buf);
    } else if (be_isstring(vm, index)) {
        const char* str = be_tostring(vm, index);
        size_t len = strlen(str);
        /* Allocate for quotes and escaping (worst case: all chars escaped) */
        char* json = (char*)malloc(len * 2 + 3);
        if (!json) return js_strdup("null");
        
        char* p = json;
        *p++ = '"';
        for (size_t i = 0; i < len; i++) {
            char c = str[i];
            if (c == '"' || c == '\\') {
                *p++ = '\\';
            }
            *p++ = c;
        }
        *p++ = '"';
        *p = '\0';
        return json;
    } else {
        /* For functions, classes, instances, and other non-JSON types,
         * use Berry's tostring conversion to get a readable representation
         * like "<function: 0x12345678>" */
        be_tostring(vm, index);
        const char* str = be_tostring(vm, index);
        size_t len = strlen(str);
        /* Return as JSON string */
        char* json = (char*)malloc(len + 3);
        if (!json) return js_strdup("null");
        snprintf(json, len + 3, "\"%s\"", str);
        return json;
    }
}

/* Parse JSON string and push Berry value onto stack
 * Returns 1 on success, 0 on failure */
static int json_to_berry(bvm *vm, const char* json)
{
    if (!json || !*json) {
        be_pushnil(vm);
        return 1;
    }
    
    /* Simple JSON parsing - will be expanded in task 2.2 */
    if (strcmp(json, "null") == 0 || strcmp(json, "undefined") == 0) {
        be_pushnil(vm);
        return 1;
    } else if (strcmp(json, "true") == 0) {
        be_pushbool(vm, 1);
        return 1;
    } else if (strcmp(json, "false") == 0) {
        be_pushbool(vm, 0);
        return 1;
    } else if (json[0] == '"') {
        /* String value - remove quotes */
        size_t len = strlen(json);
        if (len >= 2 && json[len-1] == '"') {
            be_pushnstring(vm, json + 1, len - 2);
            return 1;
        }
    } else {
        /* Try to parse as number */
        char* endptr;
        double d = strtod(json, &endptr);
        if (endptr != json && *endptr == '\0') {
            /* Check if it's an integer */
            bint i = (bint)d;
            if ((double)i == d) {
                be_pushint(vm, i);
            } else {
                be_pushreal(vm, (breal)d);
            }
            return 1;
        }
    }
    
    /* Default: push as string */
    be_pushstring(vm, json);
    return 1;
}

/*******************************************************************************
 * Timing functions for tasmota.millis() emulation
 ******************************************************************************/

/* Get current time in milliseconds from JavaScript performance.now() */
EM_JS(double, js_performance_now, (void), {
    return performance.now();
});

/* Start time for millis() calculation - set when VM is initialized */
static double g_start_time_ms = 0;

/* Initialize the timing system - called when VM is set up */
static void init_timing(void)
{
    g_start_time_ms = js_performance_now();
}

/*******************************************************************************
 * Global VM pointer for JavaScript-to-Berry execution API
 * This is set when the Berry VM is initialized and used by exported functions
 ******************************************************************************/
static bvm *g_vm = NULL;

/* Set the global VM pointer - called from Berry initialization */
void berry_set_vm(bvm *vm)
{
    g_vm = vm;
    /* Initialize timing when VM is set up */
    init_timing();
}

/* Get the global VM pointer */
bvm* berry_get_vm(void)
{
    return g_vm;
}

/*******************************************************************************
 * JavaScript-to-Berry Execution API
 * These functions are exported via Emscripten for JavaScript to call
 ******************************************************************************/

/* Execute Berry source code string
 * Returns: 0 on success, error code on failure
 * Error messages are sent to console via js_log_impl */
EMSCRIPTEN_KEEPALIVE
int berry_execute(const char* source_code)
{
    if (!source_code || !g_vm) {
        js_log_impl("Error: No source code or VM not initialized");
        return -1;
    }
    
    /* Use be_loadbuffer to compile the source code */
    int res = be_loadbuffer(g_vm, "browser", source_code, strlen(source_code));
    if (res != BE_OK) {
        /* Compilation error - error message on stack */
        const char* err = be_tostring(g_vm, -1);
        char msg[256];
        snprintf(msg, sizeof(msg), "Compilation error: %s", err ? err : "unknown");
        js_log_impl(msg);
        be_pop(g_vm, 1);
        return res;
    }
    
    /* Execute the compiled code */
    res = be_pcall(g_vm, 0);
    if (res != BE_OK) {
        /* Runtime error */
        const char* err = be_tostring(g_vm, -1);
        char msg[256];
        snprintf(msg, sizeof(msg), "Runtime error: %s", err ? err : "unknown");
        js_log_impl(msg);
        be_pop(g_vm, 1);
        return res;
    }
    
    be_pop(g_vm, 1); /* Pop result */
    return BE_OK;
}

/* Try to compile as "return (expr)" to get expression result
 * Returns BE_OK if successful, error code otherwise */
static int try_return_expr(bvm *vm, const char* source_code)
{
    int res;
    const char* wrapped = be_pushfstring(vm, "return (%s)", source_code);
    int idx = be_absindex(vm, -1);
    res = be_loadbuffer(vm, "browser", wrapped, strlen(wrapped));
    be_remove(vm, idx); /* remove the wrapped source string */
    return res;
}

/* Execute Berry source code and return result as JSON
 * Returns: JSON-encoded result string (caller must free), or NULL on error
 * If result is nil, returns "null" JSON string
 * Error messages are sent to console via js_log_impl
 * 
 * This function first tries to wrap the code as "return (code)" to capture
 * expression results (like the REPL does). If that fails with a syntax error,
 * it falls back to executing the code as-is. */
EMSCRIPTEN_KEEPALIVE
char* berry_execute_result(const char* source_code)
{
    int res;
    
    if (!source_code || !g_vm) {
        js_log_impl("Error: No source code or VM not initialized");
        return NULL;
    }
    
    /* First, try to compile as "return (expr)" to capture expression results */
    res = try_return_expr(g_vm, source_code);
    
    if (res != BE_OK) {
        /* If wrapping failed with syntax error, try compiling as-is */
        if (be_getexcept(g_vm, res) == BE_SYNTAX_ERROR) {
            be_pop(g_vm, 2); /* pop exception values (error message + exception) */
            res = be_loadbuffer(g_vm, "browser", source_code, strlen(source_code));
            if (res != BE_OK) {
                /* Compilation error - error message on stack */
                const char* err = be_tostring(g_vm, -1);
                char msg[256];
                snprintf(msg, sizeof(msg), "Compilation error: %s", err ? err : "unknown");
                js_log_impl(msg);
                be_pop(g_vm, 2); /* pop exception values */
                return NULL;
            }
        } else {
            /* Other error (not syntax) - report it */
            const char* err = be_tostring(g_vm, -1);
            char msg[256];
            snprintf(msg, sizeof(msg), "Compilation error: %s", err ? err : "unknown");
            js_log_impl(msg);
            be_pop(g_vm, 2); /* pop exception values */
            return NULL;
        }
    }
    
    /* Execute the compiled code */
    res = be_pcall(g_vm, 0);
    if (res != BE_OK) {
        /* Runtime error */
        const char* err = be_tostring(g_vm, -1);
        char msg[256];
        snprintf(msg, sizeof(msg), "Runtime error: %s", err ? err : "unknown");
        js_log_impl(msg);
        be_pop(g_vm, 2); /* pop exception values */
        return NULL;
    }
    
    /* Convert result to JSON */
    char* result = berry_to_json(g_vm, -1);
    be_pop(g_vm, 1); /* Pop result */
    return result;
}

/* Call a global Berry function by name with no arguments
 * Returns: 0 on success, error code on failure */
EMSCRIPTEN_KEEPALIVE
int berry_call_global(const char* function_name)
{
    if (!function_name || !g_vm) {
        js_log_impl("Error: No function name or VM not initialized");
        return -1;
    }
    
    /* Get the global function */
    if (!be_getglobal(g_vm, function_name)) {
        char msg[128];
        snprintf(msg, sizeof(msg), "Function not found: %s", function_name);
        js_log_impl(msg);
        return -1;
    }
    
    /* Check if it's callable */
    if (!be_isfunction(g_vm, -1) && !be_isclosure(g_vm, -1)) {
        be_pop(g_vm, 1);
        char msg[128];
        snprintf(msg, sizeof(msg), "Not a function: %s", function_name);
        js_log_impl(msg);
        return -1;
    }
    
    /* Call with no arguments */
    int res = be_pcall(g_vm, 0);
    if (res != BE_OK) {
        const char* err = be_tostring(g_vm, -1);
        char msg[256];
        snprintf(msg, sizeof(msg), "Call error in %s: %s", function_name, err ? err : "unknown");
        js_log_impl(msg);
        be_pop(g_vm, 1);
        return res;
    }
    
    be_pop(g_vm, 1); /* Pop result */
    return BE_OK;
}

/* Call a global Berry function with JSON-encoded arguments
 * Returns: JSON-encoded result string (caller must free), or NULL on error */
EMSCRIPTEN_KEEPALIVE
char* berry_call_global_args(const char* function_name, const char* args_json)
{
    if (!function_name || !g_vm) {
        js_log_impl("Error: No function name or VM not initialized");
        return NULL;
    }
    
    /* Get the global function */
    if (!be_getglobal(g_vm, function_name)) {
        char msg[128];
        snprintf(msg, sizeof(msg), "Function not found: %s", function_name);
        js_log_impl(msg);
        return NULL;
    }
    
    /* Check if it's callable */
    if (!be_isfunction(g_vm, -1) && !be_isclosure(g_vm, -1)) {
        be_pop(g_vm, 1);
        char msg[128];
        snprintf(msg, sizeof(msg), "Not a function: %s", function_name);
        js_log_impl(msg);
        return NULL;
    }
    
    /* Parse JSON arguments array and push onto stack */
    int argc = 0;
    if (args_json && args_json[0] == '[') {
        /* Simple JSON array parsing - parse each element */
        const char* p = args_json + 1; /* Skip '[' */
        while (*p && *p != ']') {
            /* Skip whitespace */
            while (*p == ' ' || *p == '\t' || *p == '\n' || *p == ',') p++;
            if (*p == ']') break;
            
            /* Find end of this value */
            const char* start = p;
            int depth = 0;
            int in_string = 0;
            while (*p) {
                if (*p == '"' && (p == start || *(p-1) != '\\')) {
                    in_string = !in_string;
                } else if (!in_string) {
                    if (*p == '[' || *p == '{') depth++;
                    else if (*p == ']' || *p == '}') {
                        if (depth == 0) break;
                        depth--;
                    }
                    else if (*p == ',' && depth == 0) break;
                }
                p++;
            }
            
            /* Extract and parse this value */
            size_t len = p - start;
            char* value = (char*)malloc(len + 1);
            memcpy(value, start, len);
            value[len] = '\0';
            
            /* Trim trailing whitespace */
            while (len > 0 && (value[len-1] == ' ' || value[len-1] == '\t' || value[len-1] == '\n')) {
                value[--len] = '\0';
            }
            
            json_to_berry(g_vm, value);
            free(value);
            argc++;
        }
    }
    
    /* Call the function */
    int res = be_pcall(g_vm, argc);
    if (res != BE_OK) {
        const char* err = be_tostring(g_vm, -1);
        char msg[256];
        snprintf(msg, sizeof(msg), "Call error in %s: %s", function_name, err ? err : "unknown");
        js_log_impl(msg);
        be_pop(g_vm, 1);
        return NULL;
    }
    
    /* Convert result to JSON */
    char* result = berry_to_json(g_vm, -1);
    be_pop(g_vm, 1);
    return result;
}

/* Get a global Berry variable value as JSON
 * Returns: JSON-encoded value (caller must free), or NULL if not found */
EMSCRIPTEN_KEEPALIVE
char* berry_get_global(const char* variable_name)
{
    if (!variable_name || !g_vm) {
        js_log_impl("Error: No variable name or VM not initialized");
        return NULL;
    }
    
    /* Get the global variable */
    if (!be_getglobal(g_vm, variable_name)) {
        /* Variable not found - return null JSON */
        return js_strdup("null");
    }
    
    /* Convert to JSON */
    char* result = berry_to_json(g_vm, -1);
    be_pop(g_vm, 1);
    return result;
}

/* Set a global Berry variable from JSON value
 * Returns: 0 on success, error code on failure */
EMSCRIPTEN_KEEPALIVE
int berry_set_global(const char* variable_name, const char* value_json)
{
    if (!variable_name || !g_vm) {
        js_log_impl("Error: No variable name or VM not initialized");
        return -1;
    }
    
    /* Parse JSON value and push onto stack */
    json_to_berry(g_vm, value_json);
    
    /* Set as global variable */
    be_setglobal(g_vm, variable_name);
    be_pop(g_vm, 1);
    
    return BE_OK;
}

/*******************************************************************************
 * Tasmota Emulation API
 * These functions emulate Tasmota functionality for browser execution
 ******************************************************************************/

/* tasmota_millis() - Get milliseconds since Berry VM initialization
 * Returns: milliseconds as integer (increments by 1 per millisecond)
 * Uses JavaScript performance.now() for high-resolution timing
 * This emulates tasmota.millis() for browser-based animation timing */
EMSCRIPTEN_KEEPALIVE
int tasmota_millis(void)
{
    double now = js_performance_now();
    double elapsed = now - g_start_time_ms;
    /* Return as integer milliseconds */
    return (int)elapsed;
}

/*******************************************************************************
 * Module functions
 ******************************************************************************/

/* js.call(func_name, ...) - Call a JavaScript function
 * func_name: string - Name of the function (e.g., "Math.pow", "console.log")
 * ...: any - Arguments to pass to the function
 * Returns: the result of the JavaScript function call */
static int m_js_call(bvm *vm)
{
    int argc = be_top(vm);
    if (argc < 1 || !be_isstring(vm, 1)) {
        be_raise(vm, "type_error", "js.call() requires function name as first argument");
    }
    
    const char* func_name = be_tostring(vm, 1);
    
    /* Build JSON array of all arguments (starting from index 2) */
    char* args_json;
    if (argc <= 1) {
        args_json = js_strdup("[]");
    } else {
        /* Calculate total size needed */
        size_t total_len = 2; /* for [ and ] */
        char** arg_jsons = (char**)malloc((argc - 1) * sizeof(char*));
        
        for (int i = 2; i <= argc; i++) {
            arg_jsons[i - 2] = berry_to_json(vm, i);
            total_len += strlen(arg_jsons[i - 2]);
            if (i > 2) total_len++; /* for comma */
        }
        
        args_json = (char*)malloc(total_len + 1);
        char* p = args_json;
        *p++ = '[';
        
        for (int i = 0; i < argc - 1; i++) {
            if (i > 0) *p++ = ',';
            size_t len = strlen(arg_jsons[i]);
            memcpy(p, arg_jsons[i], len);
            p += len;
            free(arg_jsons[i]);
        }
        
        *p++ = ']';
        *p = '\0';
        free(arg_jsons);
    }
    
    /* Call JavaScript */
    char* result = js_call_impl(func_name, args_json);
    free(args_json);
    
    /* Parse result and push to Berry stack */
    if (result) {
        json_to_berry(vm, result);
        free(result);
    } else {
        be_pushnil(vm);
    }
    
    be_return(vm);
}

/* js.get(prop_path) - Get a JavaScript property value
 * prop_path: string - Property path (e.g., "window.myVar", "document.title")
 * Returns: the property value */
static int m_js_get(bvm *vm)
{
    if (be_top(vm) < 1 || !be_isstring(vm, 1)) {
        be_raise(vm, "type_error", "js.get() requires property path as string");
    }
    
    const char* prop_path = be_tostring(vm, 1);
    char* result = js_get_impl(prop_path);
    
    if (result) {
        json_to_berry(vm, result);
        free(result);
    } else {
        be_pushnil(vm);
    }
    
    be_return(vm);
}

/* js.set(prop_path, value) - Set a JavaScript property value
 * prop_path: string - Property path (e.g., "window.myVar")
 * value: any - Value to set */
static int m_js_set(bvm *vm)
{
    if (be_top(vm) < 2 || !be_isstring(vm, 1)) {
        be_raise(vm, "type_error", "js.set() requires property path and value");
    }
    
    const char* prop_path = be_tostring(vm, 1);
    char* value_json = berry_to_json(vm, 2);
    
    js_set_impl(prop_path, value_json);
    free(value_json);
    
    be_return_nil(vm);
}

/* js.log(...) - Log messages to the JavaScript console
 * ...: any - Values to log (converted to strings) */
static int m_js_log(bvm *vm)
{
    int argc = be_top(vm);
    
    if (argc == 0) {
        js_log_impl("");
        be_return_nil(vm);
    }
    
    /* Convert first argument to string and log */
    be_tostring(vm, 1);
    const char* msg = be_tostring(vm, 1);
    js_log_impl(msg);
    
    be_return_nil(vm);
}

/* js.frame_buffer_display(hex_string) - Display frame buffer on canvas
 * hex_string: string - Hexadecimal representation of frame buffer (from tohex())
 * This function is called by Berry to push pixel data to JavaScript for rendering */
static int m_js_frame_buffer_display(bvm *vm)
{
    if (be_top(vm) < 1 || !be_isstring(vm, 1)) {
        be_raise(vm, "type_error", "js.frame_buffer_display() requires hex string");
    }
    
    const char* hex_string = be_tostring(vm, 1);
    
    /* Call JavaScript to render the frame buffer */
    js_call_impl("renderLEDStrip", hex_string);
    
    be_return_nil(vm);
}

/* js.get_strip_size() - Get the LED strip size in pixels
 * Returns: the number of LEDs in the strip (or 0 if not configured) */
static int m_js_get_strip_size(bvm *vm)
{
    /* Call JavaScript to get the strip size */
    char* result = js_call_impl("getStripSize", "[]");
    
    if (result) {
        json_to_berry(vm, result);
        free(result);
    } else {
        be_pushint(vm, 0);
    }
    
    be_return(vm);
}

/* js.get_brightness() - Get the brightness level from JavaScript UI
 * Returns: brightness percentage (0-200, 100 = normal) */
static int m_js_get_brightness(bvm *vm)
{
    /* Call JavaScript to get the brightness */
    char* result = js_call_impl("getBrightness", "[]");
    
    if (result) {
        json_to_berry(vm, result);
        free(result);
    } else {
        be_pushint(vm, 100);  /* Default to 100% if not configured */
    }
    
    be_return(vm);
}

/* js.get_fader(num) - Get a fader value from JavaScript UI
 * num: int - Fader number (1-8)
 * Returns: fader value (0-100) */
static int m_js_get_fader(bvm *vm)
{
    if (be_top(vm) < 1 || !be_isint(vm, 1)) {
        be_raise(vm, "type_error", "js.get_fader() requires fader number (1-8)");
    }
    
    int fader_num = be_toint(vm, 1);
    
    /* Build JSON array with fader number */
    char args[16];
    snprintf(args, sizeof(args), "[%d]", fader_num);
    
    /* Call JavaScript to get the fader value */
    char* result = js_call_impl("getFaderValue", args);
    
    if (result) {
        json_to_berry(vm, result);
        free(result);
    } else {
        be_pushint(vm, 50);  /* Default to 50 if not configured */
    }
    
    be_return(vm);
}

/*******************************************************************************
 * Module definition
 ******************************************************************************/

#if !BE_USE_PRECOMPILED_OBJECT
/* Runtime module registration (non-precompiled) */
be_native_module_attr_table(js) {
    be_native_module_function("call", m_js_call),
    be_native_module_function("get", m_js_get),
    be_native_module_function("set", m_js_set),
    be_native_module_function("log", m_js_log),
    be_native_module_function("frame_buffer_display", m_js_frame_buffer_display),
    be_native_module_function("get_strip_size", m_js_get_strip_size),
    be_native_module_function("get_brightness", m_js_get_brightness),
    be_native_module_function("get_fader", m_js_get_fader),
};

be_define_native_module(js, NULL);
#else
/* Precompiled module definition (used by coc tool) */
/* @const_object_info_begin
module js (scope: global) {
    call, func(m_js_call)
    get, func(m_js_get)
    set, func(m_js_set)
    log, func(m_js_log)
    frame_buffer_display, func(m_js_frame_buffer_display)
    get_strip_size, func(m_js_get_strip_size)
    get_brightness, func(m_js_get_brightness)
    get_fader, func(m_js_get_fader)
}
@const_object_info_end */
#include "../generate/be_fixed_js.h"
#endif

#endif /* __EMSCRIPTEN__ */
