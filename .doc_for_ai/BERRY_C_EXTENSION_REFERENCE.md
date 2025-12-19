# Berry C Extension Reference

Note: Compact reference for Generative AI (~3.5k tokens). Covers FFI (Foreign Function Interface) for writing C extensions that interact with the Berry VM.

## Virtual Machine Basics

```c
#include "berry.h"

bvm *vm = be_vm_new();           // Create VM (loads standard library)
be_loadstring(vm, "print('Hi')"); // Compile source string
be_pcall(vm, 0);                 // Execute (protected call)
be_vm_delete(vm);                // Destroy VM
```

**Loading source code:**
```c
be_loadstring(vm, code);                    // From string (macro)
be_loadbuffer(vm, "name", buf, len);        // From buffer
be_loadfile(vm, "file.be");                 // From file
```

**Error codes (berrorcode):** `BE_OK`, `BE_IO_ERROR`, `BE_SYNTAX_ERROR`, `BE_EXEC_ERROR`, `BE_MALLOC_FAIL`, `BE_EXIT`

## Virtual Stack

Arguments and return values pass through a virtual stack. Index `1` is first argument (bottom), `-1` is top.

```
Stack: [arg1][arg2][arg3]...
Index:   1     2     3    (absolute, from bottom)
        -3    -2    -1    (relative, from top)
```

**Stack operations:**
```c
int be_top(bvm *vm);                    // Get stack size (arg count)
void be_pop(bvm *vm, int n);            // Pop n values
void be_remove(bvm *vm, int index);     // Remove value at index
int be_absindex(bvm *vm, int index);    // Convert to absolute index
void be_stack_require(bvm *vm, int n);  // Ensure n free slots
```

## Type Checking

```c
int be_isnil(bvm *vm, int index);
int be_isbool(bvm *vm, int index);
int be_isint(bvm *vm, int index);
int be_isreal(bvm *vm, int index);
int be_isnumber(bvm *vm, int index);    // int or real
int be_isstring(bvm *vm, int index);
int be_isfunction(bvm *vm, int index);  // closure, native func, or native closure
int be_isclosure(bvm *vm, int index);   // Berry closure
int be_isntvclos(bvm *vm, int index);   // Native closure
int be_isclass(bvm *vm, int index);
int be_isinstance(bvm *vm, int index);
int be_islist(bvm *vm, int index);
int be_ismap(bvm *vm, int index);
int be_iscomptr(bvm *vm, int index);    // C pointer
int be_isbytes(bvm *vm, int index);     // bytes instance
```

## Getting Values from Stack

```c
bint be_toint(bvm *vm, int index);              // Integer (calls toint() on instance)
breal be_toreal(bvm *vm, int index);            // Float
bbool be_tobool(bvm *vm, int index);            // Bool (converts per Berry rules, calls tobool())
const char* be_tostring(bvm *vm, int index);    // String (converts in place, calls tostring())
void* be_tocomptr(bvm *vm, int index);          // C pointer
const void* be_tobytes(bvm *vm, int index, size_t *len);  // bytes buffer + length
```

**Type info:**
```c
const char* be_typename(bvm *vm, int index);    // "int", "string", "function", etc.
const char* be_classname(bvm *vm, int index);   // Class name for instance/class
int be_strlen(bvm *vm, int index);              // String length (faster than strlen)
```

## Pushing Values to Stack

```c
void be_pushnil(bvm *vm);
void be_pushbool(bvm *vm, int b);
void be_pushint(bvm *vm, bint i);
void be_pushreal(bvm *vm, breal r);
void be_pushstring(bvm *vm, const char *str);           // Null-terminated
void be_pushnstring(bvm *vm, const char *str, size_t n); // With length
const char* be_pushfstring(bvm *vm, const char *fmt, ...); // Formatted (%d %f %g %s %c %p %%)
void be_pushvalue(bvm *vm, int index);                  // Copy value at index
void be_pushcomptr(bvm *vm, void *ptr);                 // C pointer
void* be_pushbytes(bvm *vm, const void *buf, size_t len); // bytes buffer (copied)
void be_pushntvfunction(bvm *vm, bntvfunc f);           // Native function
void be_pushntvclosure(bvm *vm, bntvfunc f, int nupvals); // Native closure
void be_pushclass(bvm *vm, const char *name, const bnfuncinfo *lib);
void be_pusherror(bvm *vm, const char *msg);            // Push error and return
```

## Native Functions

Native functions have signature `int func(bvm *vm)` and use macros to return:

```c
static int my_add(bvm *vm)
{
    int argc = be_top(vm);  // Get argument count
    if (argc >= 2 && be_isnumber(vm, 1) && be_isnumber(vm, 2)) {
        breal a = be_toreal(vm, 1);
        breal b = be_toreal(vm, 2);
        be_pushreal(vm, a + b);
        be_return(vm);      // Return top of stack
    }
    be_return_nil(vm);      // Return nil on error
}
```

**Return macros:**
```c
be_return(vm);      // Return value at top of stack
be_return_nil(vm);  // Return nil
```

**Register at runtime:**
```c
be_regfunc(vm, "myadd", my_add);  // Register as global function
```

## Container Operations

**Create containers:**
```c
void be_newlist(bvm *vm);   // Push new list (internal BE_LIST type)
void be_newmap(bvm *vm);    // Push new map (internal BE_MAP type)
```

**Access containers:**
```c
void be_getindex(bvm *vm, int index);   // Get container[top], push result
void be_setindex(bvm *vm, int index);   // Set container[top-1] = top
int be_data_size(bvm *vm, int index);   // Element count (-1 if not container)
void be_data_push(bvm *vm, int index);  // Append top to list
void be_data_insert(bvm *vm, int index); // Insert key-value (top-1, top)
void be_data_remove(bvm *vm, int index); // Remove by key (top)
void be_data_resize(bvm *vm, int index); // Resize list to top
```

**Example: Create list with value:**
```c
be_newlist(vm);
be_pushint(vm, 100);
be_data_push(vm, -2);  // Append 100 to list
be_pop(vm, 1);         // Pop the integer
```

## Instance Operations

```c
void be_getmember(bvm *vm, int index, const char *k);  // Push instance.k
void be_setmember(bvm *vm, int index, const char *k);  // instance.k = top
void be_getglobal(bvm *vm, const char *name);          // Push global variable
void be_getsuper(bvm *vm, int index);                  // Push parent class/object
```

**Instantiate a class:**
```c
be_getglobal(vm, "list");   // Push class
be_newlist(vm);             // Push data
be_call(vm, 1);             // Call constructor with 1 arg
be_pop(vm, 1);              // Pop argument
be_return(vm);              // Return instance
```

## Iterators

```c
bbool be_pushiter(bvm *vm, int index);      // Push iterator for container
int be_iter_next(bvm *vm, int index);       // Advance iterator, returns 0/1/2
int be_iter_hasnext(bvm *vm, int index);    // Check if more elements
```

## Native Closures (Upvalues)

```c
void be_getupval(bvm *vm, int index, int pos);  // Push upvalue at pos
void be_setupval(bvm *vm, int index, int pos);  // Set upvalue at pos to top
```

## Reference Stack (Avoid Recursion)

```c
int be_refcontains(bvm *vm, int index);  // Check if object in ref stack
void be_refpush(bvm *vm, int index);     // Push object to ref stack
void be_refpop(bvm *vm);                 // Pop from ref stack
```

## Calling Berry Functions

```c
be_call(bvm *vm, int argc);   // Call function at stack[-(argc+1)] with argc args
be_pcall(bvm *vm, int argc);  // Protected call (catches errors)
```

## Compile-Time Construction (coc tool)

The `coc` tool generates C code for constant objects (classes, modules, maps) from declarations in source comments.

**Declaration block format:**
```c
/* @const_object_info_begin
type object_name (attributes) {
    member_fields
}
@const_object_info_end */
#include "../generate/be_fixed_object_name.h"
```

**Types:** `class`, `module`, `map`, `vartab`

**Attributes:**
- `scope: local` (static) or `scope: global` (extern)
- `name: ClassName` (for classes)
- `strings: weak` (weak string references for linker optimization)

**Member value types:**
```c
var                     // Auto-incrementing int (for member variable indices)
func(c_function)        // Native function pointer (instance method, receives self)
static_func(c_function) // Native static function (no self, called on class)
closure(solidified_fn)  // Pre-compiled bytecode
nil()                   // nil value
int(value)              // Integer constant
real(value)             // Real constant
comptr(c_ptr)           // C pointer
class(be_class_xxx)     // Class reference
module(be_module_xxx)   // Module reference
ctype_func(mapping)     // berry_mapping integration
```

**Example class:**
```c
/* @const_object_info_begin
class be_class_map (scope: global, name: map) {
    .data, var
    init, func(m_init)
    tostring, func(m_tostring)
    size, func(m_size)
}
@const_object_info_end */
#include "../generate/be_fixed_be_class_map.h"
```

**Example module:**
```c
/* @const_object_info_begin
module math (scope: global) {
    sin, func(m_sin)
    cos, func(m_cos)
    pi, real(M_PI)
}
@const_object_info_end */
#include "../generate/be_fixed_math.h"
```

**Example built-in table:**
```c
/* @const_object_info_begin
vartab m_builtin (scope: local) {
    assert, func(l_assert)
    print, func(l_print)
    list, class(be_class_list)
}
@const_object_info_end */
```

**Build command:**
```bash
tools/coc/coc -o generate src default -c default/berry_conf.h
```

## Key Types

```c
typedef struct bvm bvm;           // VM state (opaque)
typedef int (*bntvfunc)(bvm*);    // Native function pointer
typedef long long bint;           // Berry integer (configurable)
typedef double breal;             // Berry real (float if BE_SINGLE_FLOAT)

typedef struct {
    const char *name;
    bntvfunc function;
} bnfuncinfo;                     // For batch registration
```

## Complete Native Function Example

```c
#include "berry.h"

// Native function: add two numbers
static int l_add(bvm *vm)
{
    int argc = be_top(vm);
    if (argc == 2 && be_isnumber(vm, 1) && be_isnumber(vm, 2)) {
        if (be_isint(vm, 1) && be_isint(vm, 2)) {
            bint a = be_toint(vm, 1);
            bint b = be_toint(vm, 2);
            be_pushint(vm, a + b);
        } else {
            breal a = be_toreal(vm, 1);
            breal b = be_toreal(vm, 2);
            be_pushreal(vm, a + b);
        }
        be_return(vm);
    }
    be_return_nil(vm);
}

// Native function: create list with initial value
static int l_make_list(bvm *vm)
{
    be_getglobal(vm, "list");  // Push list class
    be_newlist(vm);            // Create internal list
    be_pushint(vm, 100);       // Value to add
    be_data_push(vm, -2);      // Append to list
    be_pop(vm, 1);             // Pop the integer
    be_call(vm, 1);            // Call list constructor
    be_pop(vm, 1);             // Pop argument
    be_return(vm);             // Return list instance
}

// Registration
void register_functions(bvm *vm)
{
    be_regfunc(vm, "add", l_add);
    be_regfunc(vm, "make_list", l_make_list);
}
```
