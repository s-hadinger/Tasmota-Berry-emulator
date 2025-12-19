# Berry JavaScript Module (`import js`)

## Overview

The `js` module provides a JavaScript interop bridge for Berry code running in a WebAssembly environment. It enables Berry code to call JavaScript functions, access browser properties, and interact with browser APIs. This module is only available when Berry is compiled with Emscripten for WebAssembly.

**Module Name:** `js`  
**Platform:** WebAssembly (Emscripten) only  
**Source:** `berry-lang/src/be_jslib.c`

## Quick Start

```berry
import js

# Call JavaScript functions
js.call("console.log", "Hello from Berry!")
result = js.call("Math.pow", 2, 8)  # Returns 256

# Access JavaScript properties
js.set("window.myVar", 42)
value = js.get("window.myVar")  # Returns 42

# Log to browser console
js.log("Debug message")
```

## Core Functions

### `js.call(function_name, ...args)`

Call any JavaScript function by name with optional arguments.

**Parameters:**
- `function_name` (string) - Name of the JavaScript function to call. Supports nested properties (e.g., `"Math.pow"`, `"console.log"`)
- `...args` (any) - Zero or more arguments to pass to the function

**Returns:** The result of the JavaScript function call, converted to a Berry value

**Examples:**

```berry
import js

# Call function with no arguments
random = js.call("Math.random")  # Returns a number between 0 and 1

# Call function with arguments
power = js.call("Math.pow", 2, 10)  # Returns 1024
max = js.call("Math.max", 5, 10, 3)  # Returns 10

# Call nested functions
js.call("console.log", "Hello!")
js.call("console.warn", "Warning message")

# Call custom JavaScript functions
js.call("myCustomFunction", "arg1", 42, true)
```

**Type Conversion:**

Berry values are automatically converted to JavaScript types:
- `nil` → `null`
- `bool` → `boolean`
- `int` → `number`
- `real` → `number`
- `string` → `string`

JavaScript return values are converted back to Berry:
- `null` / `undefined` → `nil`
- `boolean` → `bool`
- `number` → `int` or `real`
- `string` → `string`

---

### `js.get(property_path)`

Get a JavaScript property value by path.

**Parameters:**
- `property_path` (string) - Property path using dot notation (e.g., `"window.myVar"`, `"document.title"`)

**Returns:** The property value, converted to a Berry value

**Examples:**

```berry
import js

# Get simple properties
title = js.get("document.title")
url = js.get("window.location.href")

# Get nested properties
width = js.get("window.innerWidth")
height = js.get("window.innerHeight")

# Get custom properties
config = js.get("window.myConfig")
```

**Note:** Returns `nil` if the property doesn't exist.

---

### `js.set(property_path, value)`

Set a JavaScript property value by path.

**Parameters:**
- `property_path` (string) - Property path using dot notation
- `value` (any) - Value to set (will be converted to JavaScript type)

**Returns:** `nil`

**Examples:**

```berry
import js

# Set simple properties
js.set("window.myVar", 42)
js.set("window.myString", "Hello")
js.set("window.myBool", true)

# Set nested properties (parent must exist)
js.set("window.config.enabled", true)
js.set("window.config.count", 100)
```

**Note:** The parent object must exist. Setting `"window.foo.bar"` will fail if `window.foo` doesn't exist.

---

### `js.log(...messages)`

Log messages to the JavaScript console with `[Berry]` prefix.

**Parameters:**
- `...messages` (any) - One or more values to log (converted to strings)

**Returns:** `nil`

**Examples:**

```berry
import js

# Log simple messages
js.log("Debug message")
js.log("Value:", 42)

# Log variables
var x = 100
js.log("x =", x)

# Log formatted strings
js.log(f"Result: {x * 2}")
```

**Console Output:**
```
[Berry] Debug message
[Berry] Value: 42
[Berry] x = 100
[Berry] Result: 200
```

---

## LED Strip Functions

These functions integrate Berry animations with the browser-based LED strip visualization.

### `js.frame_buffer_display(hex_string)`

Display a frame buffer on the HTML5 canvas.

**Parameters:**
- `hex_string` (string) - Hexadecimal representation of the frame buffer in ARGB format (from `bytes.tohex()`)

**Returns:** `nil`

**Usage:**

```berry
import js

# Create frame buffer (30 LEDs, ARGB format)
var pixels = bytes()
pixels.resize(30 * 4)

# Set pixel colors (ARGB: 0xAARRGGBB)
var i = 0
while i < 30
  var offset = i * 4
  pixels.set(offset, 0xFF)      # Alpha
  pixels.set(offset + 1, 0xFF)  # Red
  pixels.set(offset + 2, 0x00)  # Green
  pixels.set(offset + 3, 0x00)  # Blue
  i += 1
end

# Display on canvas
js.frame_buffer_display(pixels.tohex())
```

**Note:** This function calls the global JavaScript function `renderLEDStrip(hexString)` which must be defined in your HTML page.

---

### `js.get_strip_size()`

Get the current LED strip size from the JavaScript UI.

**Parameters:** None

**Returns:** (int) Number of LEDs in the strip

**Usage:**

```berry
import js

var num_leds = js.get_strip_size()
js.log(f"Strip has {num_leds} LEDs")

# Create frame buffer with correct size
var pixels = bytes()
pixels.resize(num_leds * 4)
```

**Note:** This function calls the global JavaScript function `getStripSize()` which must be defined in your HTML page.

---

### `js.get_brightness()`

Get the brightness level from the JavaScript UI.

**Parameters:** None

**Returns:** (int) Brightness percentage (0-200, where 100 = normal)

**Usage:**

```berry
import js

var brightness = js.get_brightness()
js.log(f"Brightness: {brightness}%")

# Apply brightness to colors
var color = 0xFFFF0000  # Red
var adjusted = apply_brightness(color, brightness)
```

**Note:** This function calls the global JavaScript function `getBrightness()` which must be defined in your HTML page.

---

### `js.get_fader(num)`

Get a fader value from the JavaScript UI.

**Parameters:**
- `num` (int) - Fader number (1-8)

**Returns:** (int) Fader value (0-100)

**Usage:**

```berry
import js

# Get fader values
var speed = js.get_fader(1)
var intensity = js.get_fader(2)

js.log(f"Speed: {speed}, Intensity: {intensity}")

# Use in animation
var delay_ms = 1000 / speed
```

**Note:** This function calls the global JavaScript function `getFaderValue(num)` which must be defined in your HTML page.

---

## JavaScript-to-Berry Execution API

These functions are exported from the WASM module for JavaScript to call. They enable JavaScript to execute Berry code and interact with the Berry VM.

### `berry_execute(source_code)`

Execute Berry source code from JavaScript.

**JavaScript Usage:**

```javascript
// Execute Berry code
const result = Module.ccall('berry_execute', 'number', ['string'], [
    'import js\njs.log("Hello from Berry!")'
]);

if (result === 0) {
    console.log('Execution successful');
} else {
    console.error('Execution failed with code:', result);
}
```

**Returns:** `0` on success, error code on failure

---

### `berry_execute_result(source_code)`

Execute Berry code and return the result as JSON.

**JavaScript Usage:**

```javascript
// Execute expression and get result
const resultPtr = Module.ccall('berry_execute_result', 'number', ['string'], [
    '2 + 2'
]);

if (resultPtr !== 0) {
    const resultJson = Module.UTF8ToString(resultPtr);
    const result = JSON.parse(resultJson);
    console.log('Result:', result);  // 4
    Module._free(resultPtr);
}
```

**Returns:** Pointer to JSON-encoded result string (caller must free), or `NULL` on error

---

### `berry_call_global(function_name)`

Call a global Berry function by name with no arguments.

**JavaScript Usage:**

```javascript
// Call Berry function
const result = Module.ccall('berry_call_global', 'number', ['string'], [
    'my_function'
]);

if (result === 0) {
    console.log('Function called successfully');
}
```

**Returns:** `0` on success, error code on failure

---

### `berry_call_global_args(function_name, args_json)`

Call a global Berry function with JSON-encoded arguments.

**JavaScript Usage:**

```javascript
// Call Berry function with arguments
const argsJson = JSON.stringify([10, 20, "hello"]);
const resultPtr = Module.ccall('berry_call_global_args', 'number', 
    ['string', 'string'], ['my_function', argsJson]);

if (resultPtr !== 0) {
    const resultJson = Module.UTF8ToString(resultPtr);
    const result = JSON.parse(resultJson);
    console.log('Result:', result);
    Module._free(resultPtr);
}
```

**Returns:** Pointer to JSON-encoded result string (caller must free), or `NULL` on error

---

### `berry_get_global(variable_name)`

Get a global Berry variable value as JSON.

**JavaScript Usage:**

```javascript
// Get Berry global variable
const resultPtr = Module.ccall('berry_get_global', 'number', ['string'], [
    'my_variable'
]);

if (resultPtr !== 0) {
    const resultJson = Module.UTF8ToString(resultPtr);
    const value = JSON.parse(resultJson);
    console.log('Variable value:', value);
    Module._free(resultPtr);
}
```

**Returns:** Pointer to JSON-encoded value (caller must free), or `NULL` if not found

---

### `berry_set_global(variable_name, value_json)`

Set a global Berry variable from JSON value.

**JavaScript Usage:**

```javascript
// Set Berry global variable
const valueJson = JSON.stringify(42);
const result = Module.ccall('berry_set_global', 'number', 
    ['string', 'string'], ['my_variable', valueJson]);

if (result === 0) {
    console.log('Variable set successfully');
}
```

**Returns:** `0` on success, error code on failure

---

### `tasmota_millis()`

Get milliseconds since Berry VM initialization (emulates `tasmota.millis()`).

**JavaScript Usage:**

```javascript
// Get elapsed time
const millis = Module.ccall('tasmota_millis', 'number', [], []);
console.log('Elapsed time:', millis, 'ms');
```

**Returns:** (int) Milliseconds since VM initialization

**Berry Usage:**

```berry
# This is typically called internally by tasmota.millis()
# but can be accessed directly if needed
var elapsed = tasmota_millis()
```

---

## Required JavaScript Functions

When using the `js` module in your HTML page, you must define these global JavaScript functions:

### `writeOutputText(text)`

Called by Berry's `print()` function to display output.

```javascript
window.writeOutputText = function(text) {
    console.log(text);
    // Or append to a textarea, div, etc.
};
```

---

### `waitLineText()`

Called by Berry's `input()` function to get user input.

```javascript
window.waitLineText = function() {
    // Return a promise that resolves to user input
    return Promise.resolve('');
};
```

---

### `renderLEDStrip(hexString)`

Called by `js.frame_buffer_display()` to render LED colors.

```javascript
window.renderLEDStrip = function(hexString) {
    if (window.ledStripAPI) {
        window.ledStripAPI.renderLEDStrip(hexString);
    }
};
```

---

### `getStripSize()`

Called by `js.get_strip_size()` to get the LED count.

```javascript
window.getStripSize = function() {
    if (window.ledStripAPI) {
        return window.ledStripAPI.getStripSize();
    }
    return 30;  // Default
};
```

---

### `getBrightness()`

Called by `js.get_brightness()` to get the brightness level.

```javascript
window.getBrightness = function() {
    const slider = document.getElementById('brightness');
    return slider ? parseInt(slider.value, 10) : 100;
};
```

---

### `getFaderValue(num)`

Called by `js.get_fader(num)` to get fader values.

```javascript
window.getFaderValue = function(num) {
    const fader = document.getElementById('fader' + num);
    return fader ? parseInt(fader.value, 10) : 50;
};
```

---

## Complete Example

### Berry Code

```berry
import js

# Initialize
var num_leds = js.get_strip_size()
js.log(f"Initializing with {num_leds} LEDs")

# Create frame buffer
var pixels = bytes()
pixels.resize(num_leds * 4)

# Animation loop function
def update_animation()
    var brightness = js.get_brightness()
    var speed = js.get_fader(1)
    
    # Update pixel colors based on time
    var time = tasmota.millis()
    var i = 0
    while i < num_leds
        var hue = (i * 360 / num_leds + time / 10) % 360
        var color = hsv_to_rgb(hue, 100, brightness)
        
        var offset = i * 4
        pixels.set(offset, (color >> 24) & 0xFF)      # Alpha
        pixels.set(offset + 1, (color >> 16) & 0xFF)  # Red
        pixels.set(offset + 2, (color >> 8) & 0xFF)   # Green
        pixels.set(offset + 3, color & 0xFF)          # Blue
        
        i += 1
    end
    
    # Display on canvas
    js.frame_buffer_display(pixels.tohex())
end

# Helper function
def hsv_to_rgb(h, s, v)
    # HSV to RGB conversion
    # Returns ARGB color (0xAARRGGBB)
    # ... implementation ...
end
```

### JavaScript Code

```javascript
// Load Berry WASM module
const berryVM = new BerryVM();

// Wait for module to be ready
berryVM.waitReady().then(() => {
    // Execute Berry initialization code
    berryVM.execute(`
        import js
        js.log("Berry VM initialized")
    `);
    
    // Start animation loop
    function animationLoop() {
        // Call Berry update function
        Module.ccall('berry_call_global', 'number', ['string'], [
            'update_animation'
        ]);
        
        requestAnimationFrame(animationLoop);
    }
    
    animationLoop();
});
```

---

## Error Handling

All `js` module functions handle errors gracefully:

- **Invalid arguments:** Raises a Berry exception with `type_error`
- **JavaScript errors:** Logged to console, returns `nil` or default value
- **Missing functions:** Logged to console, returns `nil`

**Example:**

```berry
import js

try
    result = js.call("nonExistentFunction")
    # result will be nil
catch ..
    js.log("Error occurred")
end
```

---

## Performance Considerations

### Data Transfer

- **Small data:** Direct JSON serialization is efficient
- **Large buffers:** Use `tohex()` for frame buffers (avoids JSON overhead)
- **Frequent calls:** Cache values when possible

### Best Practices

```berry
# Good: Cache strip size
var num_leds = js.get_strip_size()

# Bad: Query every frame
def update()
    var num_leds = js.get_strip_size()  # Avoid!
    # ...
end
```

---

## Limitations

1. **Platform-specific:** Only available in WebAssembly builds
2. **Synchronous only:** All calls are synchronous (no async/await)
3. **Type conversion:** Complex JavaScript objects are not fully supported
4. **Memory management:** Caller must free returned strings from C functions

---

## Build Configuration

To use the `js` module, Berry must be compiled with Emscripten:

```bash
# Activate Emscripten SDK
source emsdk/emsdk_env.sh

# Build Berry for WebAssembly
make -C berry-lang clean BUILD_MODE=emsdk
make -C berry-lang BUILD_MODE=emsdk
```

The Makefile must export the required functions:

```makefile
EXPORTED_FUNCTIONS = [
    "_main",
    "_berry_execute",
    "_berry_execute_result",
    "_berry_call_global",
    "_berry_call_global_args",
    "_berry_get_global",
    "_berry_set_global",
    "_tasmota_millis",
    "_malloc",
    "_free"
]

EXPORTED_RUNTIME_METHODS = [
    "ccall",
    "cwrap",
    "UTF8ToString",
    "stringToUTF8",
    "lengthBytesUTF8"
]
```

---

## Related Documentation

- **[LED Strip API Guide](LED_STRIP_API_GUIDE.md)** - JavaScript LED rendering API
- **[Berry Language Reference](https://berry.readthedocs.io/en/latest/_static/berry_short_manual.pdf)** - Berry syntax and features (8 pages PDF)
- **[Tasmota Berry Guide](https://tasmota.github.io/docs/Berry/)** - Tasmota-specific Berry features

---

## Troubleshooting

### "js module not found"

**Cause:** Berry not compiled with Emscripten, or module not registered

**Solution:** Ensure you're using the WebAssembly build of Berry

---

### "Function not found" errors

**Cause:** Required JavaScript functions not defined

**Solution:** Define all required global functions (`renderLEDStrip`, `getStripSize`, etc.)

---

### Type conversion issues

**Cause:** Complex JavaScript objects not supported

**Solution:** Use simple types (numbers, strings, booleans) or JSON serialization

---

### Memory leaks

**Cause:** Not freeing returned strings from C functions

**Solution:** Always call `Module._free(ptr)` after using returned pointers in JavaScript

```javascript
const resultPtr = Module.ccall('berry_get_global', 'number', ['string'], ['myVar']);
if (resultPtr !== 0) {
    const resultJson = Module.UTF8ToString(resultPtr);
    Module._free(resultPtr);  // Important!
    const value = JSON.parse(resultJson);
}
```

---

## License

Part of the Berry Animation Framework for Tasmota.  
See project LICENSE file for details.
