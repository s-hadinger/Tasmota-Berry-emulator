# Berry Language Reference for Tasmota

Note: Compact reference for Generative AI (~4.5k tokens). For Tasmota-specific features, see `BERRY_TASMOTA.md`.

## Comments

```berry
# Line comment
#- Block
   comment -#
```

## Literals

```berry
40        # Integer
0x80      # Hex integer
3.14      # Real
1.1e-6    # Scientific notation
true false nil
'string' "string"
"a" "b"   # Concatenates to "ab"
```

Escape sequences: `\n` `\r` `\t` `\\` `\"` `\'` `\0` `\xhh` `\uXXXX`

## Identifiers

Identifiers start with underscore or letter, followed by underscores, letters, or numbers. Berry is case-sensitive.

## Keywords

```
if elif else while for def end class break continue return
true false nil var do import as try except raise static
```

## Types

**Simple:** nil, integer, real, boolean, string, function, class, instance
**Built-in classes:** list, map, range, bytes

## Variables

```berry
a = 1              # Direct assignment (creates if doesn't exist)
var a              # Declare with nil
var a = 1          # Declare with value
var a, b = 1, 2    # Multiple declarations
```

**Scope:** Variables in outermost block are global; inner blocks are local.

```berry
var i = 0          # Global
do
    var j = 'str'  # Local to this block
    print(i, j)
end
print(i)           # j not accessible here
```

## Operators

**Arithmetic:** `+` `-` `*` `/` `%` (unary `-`)
**Relational:** `<` `<=` `==` `!=` `>=` `>`
**Logical:** `&&` `||` `!` (short-circuit evaluation)
**Bitwise:** `~` `&` `|` `^` `<<` `>>`
**Assignment:** `=` `+=` `-=` `*=` `/=` `%=` `&=` `|=` `^=` `<<=` `>>=`
**Walrus:** `:=` (assigns and returns value)
**Other:** `.` (member) `[]` (subscript) `? :` (ternary) `..` (range/concat)

**String multiplication:**
```berry
"ab" * 3           # "ababab"
"s" * (n > 1)      # "s" if true, "" if false
"  " * indent      # Create indentation
```

## Control Flow

```berry
# Conditional
if condition
    # ...
elif condition2
    # ...
else
    # ...
end

# While loop
while condition
    # ...
end

# For loop with range (inclusive)
for i: 0..5
    print(i)       # 0, 1, 2, 3, 4, 5
end

# For loop with container
for item: ['a', 'b', 'c']
    print(item)
end

for key: map.keys()
    print(key, map[key])
end

# Jump statements
break              # Exit loop
continue           # Skip to next iteration
```

## Import

```berry
import math
import hardware as hw    # Alias
```

## Functions

```berry
# Named function
def add(a, b)
    return a + b
end

# Anonymous function
add = def (a, b)
    return a + b
end

# Lambda
add = / a, b -> a + b

# Variable arguments
def print_all(a, b, *args)
    print(a, b)
    for arg: args
        print(arg)
    end
end
print_all(1, 2, 3, 4)  # args = [3, 4]

# Dynamic function call
def sum(a, b, c) return a + b + c end
call(sum, 1, 2, 3)     # Calls sum(1, 2, 3)
call(sum, 1, [2, 3])   # Calls sum(1, 2, 3) - list unpacked
```

**Closures:**
```berry
def counter(start)
    var count = start
    return def()
        count += 1
        return count
    end
end
c = counter(0)
print(c())  # 1
print(c())  # 2
```

## Classes

```berry
class Person
    var name, age
    
    def init(name, age)
        self.name = name
        self.age = age
    end
    
    def greet()
        print("Hello, I'm", self.name)
    end
end

person = Person("John", 30)
person.greet()
```

**Static members:**
```berry
class MathUtils
    static var PI = 3.14159
    static def square(x)
        return x * x
    end
    
    def use_static()
        return self.PI * 2     # Instance methods access static via self
    end
end
print(MathUtils.PI)
print(MathUtils.square(5))
```

Static vars can be accessed via `self` in instance methods. Static methods receive an implicit `_class` variable to reference other class members:
```berry
class Counter
    static var count = 0
    static def increment()
        _class.count += 1      # Use _class in static methods
        return _class.count
    end
end
```

**Inheritance:**
```berry
class Student : Person
    var school
    
    def init(name, age, school)
        super(self).init(name, age)
        self.school = school
    end
    
    def greet()
        super(self).greet()
        print("I study at", self.school)
    end
end
```

**Operator overloading:**
```berry
class Vector
    var x, y
    def init(x, y) self.x = x self.y = y end
    def +(other)
        return Vector(self.x + other.x, self.y + other.y)
    end
    def tostring()
        return f"Vector({self.x}, {self.y})"
    end
end
```

## List

```berry
l = [1, 2, 3]
l[0]               # First element (1)
l[-1]              # Last element (3)
l[1..3]            # Slice from 1 to 3 inclusive
l[1..]             # From index 1 to end
l[0..-2]           # All except last

l.push(4)          # Append
l.pop()            # Remove and return last
l.pop(1)           # Remove and return at index
l.insert(1, x)     # Insert at index
l.remove(1)        # Remove at index
l.resize(5)        # Resize (fills with nil)
l.clear()

l.size()
l.find(x)          # Index of first occurrence, or nil
l.concat()         # Join as string (no separator)
l.concat(", ")     # Join as string with separator
[1, 2] == [1, 2]   # true (list comparison)
l.reverse()
l.copy()           # Shallow copy
l + [4, 5]         # Concatenate (new list)
l .. 4             # Append in place

for i: l.keys()    # Iterate over indices
    print(i, l[i])
end
```

## Map

```berry
m = {"key": "value"}
m["key"]                   # Access (raises if missing)
m.find("key")              # Returns nil if missing
m.find("key", "default")   # With default value
m["new"] = "val"           # Set
m.insert("key", "val")     # Returns true if inserted, false if exists
m.remove("key")
m.size()
m.contains("key")

for k: m.keys()
    print(k, m[k])
end
```

## Range

```berry
r = 0..5                   # 0 to 5 inclusive
r = 10..                   # 10 to MAXINT (open-ended)
r.lower()                  # Lower bound
r.upper()                  # Upper bound
r.incr()                   # Increment (default 1)
r.setrange(1, 10)          # Change bounds
r.setrange(1, 10, 2)       # Change bounds and increment

for i: 0..5
    print(i)               # 0, 1, 2, 3, 4, 5
end
```

## String Operations

```berry
s = "hello"
s[0]               # "h"
s[-1]              # "o" (last)
s[1..3]            # "ell"
s[1..]             # "ello"
s[0..-2]           # "hell" (all except last)
```

## Bytes

```berry
b = bytes()            # Empty
b = bytes("1122AA")    # From hex string
b = bytes(10)          # Pre-allocated size
b = bytes(-8)          # Fixed size

b[0]                   # First byte
b[1..2]                # Slice
b[0] = 0xFF            # Set byte
b.resize(10)
b.clear()

# Structured read/write
b.get(0, 2)            # Read 2 bytes unsigned (little endian)
b.get(0, -2)           # Read 2 bytes unsigned (big endian)
b.geti(0, 2)           # Read 2 bytes signed
b.set(0, 0x1234, 2)    # Write 2-byte value
b.add(0x1234, 2)       # Append 2-byte value

# Conversion
b.tohex()              # To hex string
b.asstring()           # To raw string
b.tob64()              # To base64
b.fromhex("AABB")
b.fromstring("Hi")
b.fromb64("SGVsbG8=")
```

## File I/O

```berry
f = open("file.txt", "r")  # Read mode
content = f.read()         # Read entire file
line = f.readline()        # Read one line
data = f.readbytes()       # Read as bytes
f.close()

f = open("file.txt", "w")  # Write mode
f.write("Hello")
f.write(bytes("AABB"))
f.flush()
f.close()

f.seek(10)                 # Move to position
f.tell()                   # Current position
f.size()                   # File size
```

## String Module

```berry
import string

string.count("hello", "l")          # 2
string.find("hello", "lo")          # 3 (or -1 if not found)
string.split("a,b,c", ",")          # ["a", "b", "c"]
string.split("hello", 2)            # ["he", "llo"]

string.byte("A")                    # 65
string.char(65)                     # "A"

string.toupper("hello")             # "HELLO"
string.tolower("HELLO")             # "hello"

string.tr("hello", "el", "ip")      # "hippo"
string.replace("hello", "ll", "xx") # "hexxo"

string.startswith("hello", "he")         # true
string.startswith("hello", "HE", true)   # true (case-insensitive)
string.endswith("hello", "lo")           # true
string.endswith("hello", "LO", true)     # true (case-insensitive)
string.escape("hello\n")                 # Escape for C strings

string.format("Val: %d", 42)
f"Value: {x}"                       # f-string
f"Value: {x:.2f}"                   # With format spec
f"{x=}"                             # Debug format
```

## Math Module

```berry
import math

# Constants
math.pi  math.inf  math.nan  math.imin  math.imax

# Basic
math.abs(-5)           # 5
math.floor(3.7)        # 3
math.ceil(3.2)         # 4
math.round(3.5)        # 4
math.min(1, 2, 3)      # 1
math.max(1, 2, 3)      # 3

# Exponential/logarithmic
math.sqrt(16)          # 4
math.pow(2, 3)         # 8
math.exp(1)            # e
math.log(x)            # Natural log
math.log10(100)        # 2

# Trigonometric (radians)
math.sin(x)  math.cos(x)  math.tan(x)
math.asin(x) math.acos(x) math.atan(x) math.atan2(y, x)

# Conversion
math.deg(rad)          # Radians to degrees
math.rad(deg)          # Degrees to radians

# Random
math.srand(seed)
math.rand()

# Checks
math.isinf(x)  math.isnan(x)
```

## JSON Module

```berry
import json

data = json.load('{"name": "John"}')   # Parse (returns nil on error)
if data == nil
    print("Invalid JSON")
end

json_str = json.dump(obj)              # Compact
json_str = json.dump(obj, "format")    # Pretty print
```

## OS Module

```berry
import os

os.getcwd()
os.chdir("/path")
os.mkdir("/path")
os.remove("/path")
os.listdir()
os.listdir("/path")
os.system("command")
os.exit()

os.path.exists(path)
os.path.isfile(path)
os.path.isdir(path)
os.path.split("/path/file.txt")    # ["/path", "file.txt"]
os.path.splitext("file.txt")       # ["file", ".txt"]
os.path.join("dir", "file.txt")    # "dir/file.txt"
```

## Global Module

```berry
import global

global()                   # List all global variables
global.contains("name")    # Check if exists
global.var_name            # Get value
global.var_name = 42       # Set value
global.("dynamic_name")    # Dynamic access
```

## Introspect Module

```berry
import introspect

introspect.members(obj)        # List of members
introspect.get(obj, "attr")    # Get attribute
introspect.set(obj, "attr", v) # Set attribute
introspect.name(obj)           # Get name
introspect.ismethod(fn)        # Check if method
introspect.module("math")      # Dynamic import
```

## Exception Handling

**Standard exceptions:** `assert_failed`, `index_error`, `io_error`, `key_error`, `runtime_error`, `stop_iteration`, `syntax_error`, `unrealized_error`, `type_error`

```berry
# Raise
raise "my_error"
raise "my_error", "message"

# Catch specific
try
    # risky code
except "my_error"
    # handle
end

# Catch with variables
try
    # risky code
except "my_error" as e, msg
    print(e, msg)
end

# Catch multiple types
try
    # risky code
except "error1", "error2" as e, msg
    # handle either
end

# Catch all
try
    # risky code
except ..
    # handle any exception
end

# Assertions
assert(condition)
assert(condition, "message")
```

**Note:** Many functions return `nil` on error instead of raising exceptions (e.g., `json.load`, `map.find`, `list.find`). Check return values accordingly.
