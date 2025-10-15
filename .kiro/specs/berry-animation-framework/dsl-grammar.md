# Animation DSL Grammar Reference

This document provides the formal grammar specification for the Animation DSL using Extended Backus-Naur Form (EBNF).

## Current Implementation

The Animation DSL grammar is implemented using a **single-pass transpiler** that processes tokens directly and generates optimized Berry code. The grammar is designed to be:

- **Unambiguous**: Each construct has a single, clear interpretation
- **Extensible**: Easy to add new constructs while maintaining consistency
- **Human-Readable**: Natural syntax that reads like English
- **Performance-Oriented**: Generates efficient Berry code for embedded systems

This document describes the complete working grammar with all implemented features.

## Current Grammar (EBNF)

### Core Grammar ✅

```ebnf
(* Animation DSL Grammar - Current Implementation *)

(* Program Structure ✅ *)
program = { config_stmt | definition | property_assignment | sequence | execution_stmt } ;

(* Configuration Statements ✅ *)
config_stmt = strip_config | variable_assignment ;
strip_config = "strip" "length" number ;                    (* ✅ Optional, must be first if present *)
variable_assignment = "set" identifier "=" expression ;     (* ✅ Implemented *)

(* Strip properties - planned extensions ❌ *)
strip_property = "length" | "width" | "height" | "type" | "brightness" ;

(* Definitions *)
definition = color_def | animation_def ;              (* 🚧 Partial *)

color_def = "color" identifier "=" color_expression ;              (* ✅ Implemented *)
animation_def = "animation" identifier "=" animation_expression ;   (* 🚧 Basic only *)

(* Property Assignments ✅ *)
property_assignment = identifier "." identifier "=" expression ;    (* ✅ Implemented *)

(* Planned definitions ❌ *)
function_def = "function" identifier "(" [ parameter_list ] ")" "{" function_body "}" ;
zone_def = "zone" identifier "=" spatial_expression ;

(* Function Components *)
parameter_list = identifier { "," identifier } ;
function_body = { statement } [ "return" expression ] ;

(* Sequences ✅ *)
sequence = "sequence" identifier "{" sequence_body "}" ;            (* ✅ Implemented *)
sequence_body = { sequence_statement } ;                           (* ✅ Implemented *)
sequence_statement = play_stmt | simple_loop | wait_stmt ;         (* 🚧 Limited *)

(* Statements *)
play_stmt = "play" identifier [ "for" time_expression ] ;          (* ✅ Implemented *)
wait_stmt = "wait" time_expression ;                               (* ✅ Implemented *)

(* Control Flow - Current ✅ *)
simple_loop = "repeat" number "times" ":" sequence_body ;          (* ✅ Implemented *)

(* Control Flow - Planned ❌ *)
control_flow_stmt = loop_stmt | conditional_stmt | parallel_stmt | sync_stmt | choose_stmt ;

(* Planned Control Flow ❌ *)
loop_stmt = counter_loop | conditional_loop | forever_loop ;
counter_loop = "repeat" identifier "from" number "to" number ":" block ;
conditional_loop = "repeat" "while" condition ":" block ;
forever_loop = "repeat" "forever" ":" block ;

conditional_stmt = "if" condition ":" block { "elif" condition ":" block } [ "else" ":" block ] ;
parallel_stmt = "with" animation_expression [ "for" time_expression ] { modifier } ;
sync_stmt = "sync" sync_target ":" block ;
choose_stmt = "choose" "random" ":" choice_block ;

(* Control Flow Components *)
block = "{" { sequence_statement } "}" | sequence_statement ;
choice_block = "{" { choice_option } "}" ;
choice_option = sequence_statement [ "weight" number ] ;
sync_target = "every" time_expression | "to" "bpm" number ;

(* Event Handlers *)
event_handler = "on" event_name ":" event_action ;
event_name = "startup" | "shutdown" | "button_press" | "button_hold" | "motion_detected" 
           | "brightness_change" | "timer" | "time" | "sound_peak" | "network_message" 
           | identifier ;
event_action = block | "goto" identifier | "interrupt" interrupt_action | "resume" [ "after" time_expression ] ;
interrupt_action = "current" | "all" | identifier ;

(* Execution ✅ *)
execution_stmt = "run" identifier ;                                (* ✅ Implemented *)

(* Expressions *)
expression = logical_or_expr ;
logical_or_expr = logical_and_expr { "||" logical_and_expr } ;
logical_and_expr = equality_expr { "&&" equality_expr } ;
equality_expr = relational_expr { ( "==" | "!=" ) relational_expr } ;
relational_expr = additive_expr { ( "<" | "<=" | ">" | ">=" ) additive_expr } ;
additive_expr = multiplicative_expr { ( "+" | "-" ) multiplicative_expr } ;
multiplicative_expr = unary_expr { ( "*" | "/" | "%" ) unary_expr } ;
unary_expr = ( "!" | "-" | "+" ) unary_expr | primary_expr ;
primary_expr = literal | identifier | variable_ref | function_call | "(" expression ")" ;

(* Color Expressions *)
color_expression = hex_color | named_color | color_ref ;           (* 🚧 Partial *)
hex_color = "0x" hex_digit hex_digit hex_digit hex_digit hex_digit hex_digit [ hex_digit hex_digit ] ; (* ✅ Implemented *)
named_color = color_name ;                                         (* ✅ Implemented *)
color_ref = identifier ;                                           (* ✅ Implemented *)

(* Planned color formats ❌ *)
rgb_color = "rgb" "(" number "," number "," number ")" ;
hsv_color = "hsv" "(" number "," number "," number ")" ;
variable_ref = "$" identifier ;

(* Animation Expressions *)
animation_expression = animation_function | animation_ref ;        (* 🚧 Basic only *)
animation_function = "solid" "(" "color" "=" color_expression ")" ; (* ✅ Implemented with named args *)
animation_ref = identifier ;                                       (* ✅ Implemented *)

(* Planned pattern functions ❌ *)
pattern_func_advanced = "gradient" | "stripe" | "checker" | "dots" | "sparkle" 
                      | "noise" | "plasma" | "wave" | "triangle" | "sawtooth" ;
pattern_composition = pattern_expression pattern_operator pattern_expression ;
pattern_operator = "overlay" | "blend" | "mask" ;

(* Advanced Animation Functions *)
animation_function_advanced = "pulse_animation" "(" "source" "=" animation_expression "," "period" "=" time_expression ")" ; (* 🚧 Limited *)
animation_function_nested = animation_function | animation_function_advanced ; (* ✅ Nested calls supported *)

(* Planned animation functions ❌ *)
animation_func_advanced = "shift_left" | "shift_right" | "bounce" | "swing" | "rotate" 
                        | "intensity" | "hue_rotate" | "saturation" | "scale" 
                        | "jitter" | "random_sparkle" | "interference" | "particles" 
                        | "expand" | "sweep" | "move" | "fade" | "flash" | "strobe" ;
animation_composition = animation_expression animation_operator animation_expression ;
animation_operator = "with" | "then" ;

(* Spatial Expressions *)
spatial_expression = pixel_range | zone_ref | spatial_function ;
pixel_range = "pixels" pixel_spec ;
pixel_spec = number [ "-" number ] | "(" number "," number ")" [ "-" "(" number "," number ")" ] ;
zone_ref = identifier ;
spatial_function = spatial_func_name "(" [ argument_list ] ")" ;
spatial_func_name = "all" | "even" | "odd" | "random" | "center" | "edges" ;

(* Time Expressions *)
time_expression = time_literal ;                                   (* ✅ Implemented *)
time_literal = number time_unit ;                                  (* ✅ Implemented *)
time_unit = "ms" | "s" | "m" | "h" ;                              (* ✅ Implemented *)

(* Planned time features ❌ *)
time_calculation = time_expression time_operator time_expression ;
time_ref = identifier | variable_ref ;
time_operator = "+" | "-" | "*" | "/" ;

(* Modifiers *)
modifier = opacity_mod | offset_mod | spatial_mod | speed_mod | weight_mod | easing_mod ;
opacity_mod = "opacity" percentage ;
offset_mod = "offset" time_expression ;
spatial_mod = "at" spatial_expression ;
speed_mod = "speed" ( time_expression | multiplier ) ;
weight_mod = "weight" number ;
easing_mod = "ease" easing_type ;
easing_type = "linear" | "smooth" | "ease_in" | "ease_out" | "ramp" | "square" ;

(* Function Calls with Named Arguments *)
function_call = identifier "(" [ named_argument_list ] ")" ;
named_argument_list = named_argument { "," named_argument } ;
named_argument = identifier "=" expression ;

(* Conditions *)
condition = expression ;

(* Literals and Basic Types *)
literal = number | string | color_expression | time_expression | percentage | easing_type ; (* 🚧 Partial *)
number = integer | real ;                                          (* ✅ Implemented *)
integer = digit { digit } ;                                        (* ✅ Implemented *)
real = digit { digit } "." digit { digit } ;                      (* ✅ Implemented *)
string = '"' { string_char } '"' | "'" { string_char } "'" ;       (* ✅ Implemented *)
percentage = number "%" ;                                          (* ✅ Implemented *)

(* Easing Keywords ✅ *)
easing_type = "linear" | "triangle" | "smooth" | "ease_in" | "ease_out" | "ramp" | "sawtooth" | "square" ; (* ✅ Implemented *)

(* Planned literals ❌ *)
boolean = "true" | "false" ;
multiplier = number "x" ;

(* Variable References *)
variable_ref = "$" identifier ;

(* Identifiers and Names *)
identifier = ( letter | "_" ) { letter | digit | "_" } ;
color_name = "red" | "green" | "blue" | "white" | "black" | "yellow" | "orange" 
           | "purple" | "pink" | "cyan" | "magenta" | "gray" | "silver" | "gold" 
           | "brown" | "lime" | "navy" | "olive" | "maroon" | "teal" | "aqua" 
           | "fuchsia" | "transparent" ;

(* Character Classes *)
letter = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" 
       | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
       | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
       | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
hex_digit = digit | "A" | "B" | "C" | "D" | "E" | "F" | "a" | "b" | "c" | "d" | "e" | "f" ;
string_char = (* any character except quote *) ;

(* Comments and Whitespace *)
comment = "#" { (* any character except newline *) } newline ;
whitespace = " " | "\t" | "\r" | "\n" ;
newline = "\n" | "\r\n" ;

(* Values *)
value = expression ;
```

## Current vs Planned Grammar

## Currently Working Grammar

```ebnf
(* Animation DSL Grammar - Current Implementation *)

(* Program Structure *)
program = { config_stmt | definition | property_assignment | sequence | execution_stmt } ;

(* Configuration *)
config_stmt = strip_config | variable_assignment ;
strip_config = "strip" "length" number ;
variable_assignment = "set" identifier "=" expression ;

(* Definitions *)
definition = color_def | palette_def | pattern_def | animation_def ;
color_def = "color" identifier "=" color_expression ;
palette_def = "palette" identifier "=" palette_array ;
pattern_def = "pattern" identifier "=" pattern_expression ;
animation_def = "animation" identifier "=" animation_expression ;

(* Property Assignments *)
property_assignment = identifier "." identifier "=" expression ;

(* Sequences *)
sequence = "sequence" identifier "{" sequence_body "}" ;
sequence_body = { sequence_statement } ;
sequence_statement = play_stmt | wait_stmt | simple_repeat ;

play_stmt = "play" identifier [ "for" time_literal ] ;
wait_stmt = "wait" time_literal ;
simple_repeat = "repeat" number "times" ":" sequence_body ;

(* Execution *)
execution_stmt = "run" identifier ;

(* Expressions *)
color_expression = hex_color | named_color | identifier ;
pattern_expression = solid_pattern | identifier ;
animation_expression = animation_function | identifier ;
palette_array = "[" palette_entry { "," palette_entry } "]" ;
palette_entry = "(" number "," color_expression ")" ;

(* Functions *)
solid_pattern = "solid" "(" color_expression ")" ;
animation_function = animation_func_name "(" argument_list ")" ;
animation_func_name = "solid" | "rich_palette_animation" | "pulse_position_animation" 
                    | "twinkle_animation" | "comet_animation" ;

(* Basic Types *)
hex_color = "0x" hex_digit{6} | "0x" hex_digit{8} ;
time_literal = number time_unit ;
time_unit = "ms" | "s" | "m" | "h" ;
percentage = number "%" ;
number = digit+ [ "." digit+ ] ;
identifier = ( letter | "_" ) ( letter | digit | "_" )* ;
named_color = "red" | "green" | "blue" | "white" | "black" | "yellow" | "orange" 
            | "purple" | "pink" | "cyan" | "magenta" | "gray" | "transparent" ;

(* Easing Keywords *)
easing_type = "linear" | "triangle" | "smooth" | "ease_in" | "ease_out" | "ramp" | "sawtooth" | "square" ;

(* Comments *)
comment = "#" { any_char_except_newline } newline ;

(* Character Classes *)
letter = "a".."z" | "A".."Z" ;
digit = "0".."9" ;
hex_digit = digit | "A".."F" | "a".."f" ;
```

### Working DSL Example

```dsl
# Strip declaration is optional - uses Tasmota configuration if omitted
# If present, it must be the first statement

# Color definitions
color custom_red = 0xFF0000
color custom_blue = 0x0000FF

# Palette definition
palette fire_colors = [
  (0, 0x000000),
  (128, 0xFF0000),
  (255, 0xFFFF00)
]

# Animation definitions (which ARE patterns)
animation solid_red = solid(custom_red)
animation red_anim = solid(custom_red)
animation fire_anim = rich_palette_animation(fire_colors, 5s, smooth, 255)

# Property assignments
red_anim.pos = 15
red_anim.opacity = 200
red_anim.priority = 10

# Variable assignments
set brightness = 80%
set cycle_time = 3s

# Sequence with control flow
sequence demo {
  play red_anim for 3s
  wait 1s
  repeat 2 times:
    play fire_anim for 2s
    wait 500ms
}

run demo
```

### Example with Explicit Strip Length

```dsl
strip length 60  # Must be first statement if present

# Color definitions
color custom_red = 0xFF0000
# ... rest of the DSL
```


## Grammar Components

### Program Structure

The DSL program consists of statements that can appear in any order:

```ebnf
program = { config_stmt | definition | property_assignment | sequence | execution_stmt } ;
```

The transpiler processes statements sequentially, allowing flexible organization of colors, patterns, animations, and sequences.

### Configuration Statements

```ebnf
config_stmt = strip_config | variable_assignment ;
strip_config = "strip" "length" number ;
variable_assignment = "set" identifier "=" expression ;
```

Configuration statements set up the LED strip and define global variables with automatic type conversion.

**Strip Configuration Rules:**
- The `strip` declaration is **optional**
- If present, it must be the **first non-comment statement**
- If omitted, the system automatically uses Tasmota's configured strip length via `global.Leds()`

### Definitions

```ebnf
definition = color_def | palette_def | animation_def ;
color_def = "color" identifier "=" color_expression ;
palette_def = "palette" identifier "=" palette_array ;
animation_def = "animation" identifier "=" animation_expression ;
```

Definitions create reusable components that can be referenced later in the DSL.

### Color Support

```ebnf
color_expression = hex_color | named_color | identifier ;
hex_color = "0x" hex_digit{6} | "0x" hex_digit{8} ;
named_color = "red" | "green" | "blue" | "white" | "black" | ... ;
```

Colors support hex format (#RRGGBB, #AARRGGBB) and predefined named colors.

### Pattern Support

```ebnf
pattern_expression = solid_pattern | identifier ;
solid_pattern = "solid" "(" color_expression ")" ;
```

Currently only `solid(color)` patterns are implemented.

### Animation Support

```ebnf
animation_expression = animation_function | identifier ;
animation_function = animation_func_name "(" argument_list ")" ;
animation_func_name = "solid" | "rich_palette_animation" | "pulse_position_animation" 
                    | "twinkle_animation" | "comet_animation" ;
```

Several animation functions are implemented with the unified naming scheme.

### Sequence Support

```ebnf
sequence = "sequence" identifier "{" sequence_body "}" ;
sequence_body = { sequence_statement } ;
sequence_statement = play_stmt | wait_stmt | simple_repeat ;

play_stmt = "play" identifier [ "for" time_literal ] ;
wait_stmt = "wait" time_literal ;
simple_repeat = "repeat" number "times" ":" sequence_body ;
```

Sequences support basic play, wait, and simple repeat statements.

## Precedence and Associativity

### Operator Precedence (highest to lowest)

1. **Function calls** `func(args)`
2. **Unary operators** `!`, `-`, `+`
3. **Multiplicative** `*`, `/`, `%` (left associative)
4. **Additive** `+`, `-` (left associative)
5. **Relational** `<`, `<=`, `>`, `>=` (non-associative)
6. **Equality** `==`, `!=` (non-associative)
7. **Logical AND** `&&` (left associative)
8. **Logical OR** `||` (left associative)

### Statement Precedence

1. **Modifiers** bind to the nearest play statement
2. **Parallel statements** (`with`) bind to the previous play statement
3. **Control flow** has block scope

## Lexical Rules

### Keywords

Reserved words that cannot be used as identifiers:

```
strip, set, color, palette, pattern, animation, sequence, play, for, repeat, times, run, 
solid, linear, triangle, smooth, ease_in, ease_out, ramp, sawtooth, square, wait, nil, transparent, true, false
```

### Identifiers

```ebnf
identifier = ( letter | "_" ) { letter | digit | "_" } ;
```

Identifiers must start with a letter or underscore, followed by any combination of letters, digits, or underscores.

### Numbers

```ebnf
number = integer | real ;
integer = digit { digit } ;
real = digit { digit } "." digit { digit } ;
```

Numbers can be integers or floating-point values.

### Time Literals

```ebnf
time_literal = number time_unit ;
time_unit = "ms" | "s" | "m" | "h" ;
```

Time values must include a unit specifier and are automatically converted to milliseconds.

### Color Literals

```ebnf
hex_color = "0x" hex_digit{6} | "0x" hex_digit{8} ;
```

Hexadecimal colors support both RGB (#RRGGBB) and ARGB (#AARRGGBB) formats.

### Comments

```ebnf
comment = "#" { any_char_except_newline } newline ;
```

Comments start with `#` and continue to the end of the line. All comments are preserved in the generated Berry code.

## Future Grammar Extensions

The following grammar extensions are planned for future implementation:

### Advanced Pattern Functions
```ebnf
pattern_function = "gradient" | "stripe" | "checker" | "dots" | "sparkle" | "noise" | "plasma" | "wave" ;
```

### Advanced Animation Functions
```ebnf
animation_func_advanced = "shift_left" | "shift_right" | "bounce" | "rotate" | "intensity" | "hue_rotate" ;
```

### Control Flow Statements
```ebnf
conditional_stmt = "if" condition ":" block { "elif" condition ":" block } [ "else" ":" block ] ;
parallel_stmt = "with" animation_expression [ "for" time_expression ] ;
choose_stmt = "choose" "random" ":" choice_block ;
```

### Expression System
```ebnf
expression = logical_or_expr ;
variable_ref = "$" identifier ;
mathematical_expr = additive_expr { ( "+" | "-" ) additive_expr } ;
```

### User-Defined Functions
```ebnf
function_def = "function" identifier "(" parameter_list ")" "{" function_body "}" ;
```

### Event System
```ebnf
event_handler = "on" event_name ":" event_action ;
```

## Error Handling and Validation ✅

### Exception-Based Error Handling ✅

The DSL transpiler uses **exception-based error handling** for clean, consistent error management:

```berry
try
  var berry_code = animation_dsl.compile(dsl_source)
  # Use compiled code...
except "dsl_compilation_error" as e, msg
  print(f"Compilation failed: {msg}")
end
```

### Reserved Name Validation ✅

The grammar enforces validation rules to prevent naming conflicts:

#### Validation Rules

1. **DSL Keywords**: Cannot redefine reserved keywords
   - Examples: `strip`, `color`, `palette`, `animation`, `smooth`, `linear`, `play`, `for`, etc.

2. **Predefined Colors**: Cannot redefine predefined color names
   - Examples: `red`, `blue`, `green`, `white`, `black`, `yellow`, etc.

#### Error Examples

```ebnf
(* These generate validation errors *)
color red = #800000        (* Error: Cannot redefine predefined color 'red' *)
animation smooth = solid(blue)  (* Error: Cannot redefine reserved keyword 'smooth' *)
pattern strip = solid(green)    (* Error: Cannot redefine reserved keyword 'strip' *)

(* These are valid *)
color my_red = #800000     (* OK: 'my_red' is not reserved *)
animation smooth_custom = solid(blue)  (* OK: 'smooth_custom' is not reserved *)
pattern fire_strip = solid(green)     (* OK: 'fire_strip' is not reserved *)
```

### Variable Name Generation ✅

All DSL-generated Berry variables use an **underscore suffix** (`_`) to prevent conflicts:

```ebnf
(* DSL variable names are transformed during code generation *)
dsl_variable_name → berry_variable_name "_"

(* Examples *)
"red" → "red_"
"solid_red" → "solid_red_"  
"red_anim" → "red_anim_"
```

### Error Recovery

The grammar includes provisions for error recovery:

1. **Statement-level recovery**: Errors in one statement don't prevent parsing of subsequent statements
2. **Block-level recovery**: Errors within blocks are contained
3. **Expression-level recovery**: Invalid expressions can be skipped while preserving structure
4. **Reserved name recovery**: Clear suggestions for alternative names when conflicts occur

## Grammar Validation

The grammar has been validated for:

1. **Unambiguity**: No construct can be parsed in multiple ways
2. **Completeness**: All intended DSL features are covered
3. **Consistency**: Similar constructs use similar syntax patterns
4. **Extensibility**: New features can be added without breaking changes

## Implementation Notes

### Parser Implementation ✅

The grammar is implemented using a **single-pass transpiler** that efficiently processes DSL tokens and generates optimized Berry code. This approach provides:

- **High Performance**: Direct token-to-code generation without intermediate AST
- **Memory Efficiency**: Minimal memory overhead during compilation
- **Error Handling**: Exception-based error reporting with detailed messages
- **Code Quality**: Clean, readable generated Berry code with comment preservation

### Current Capabilities

1. **Complete DSL Support**: All core DSL constructs are fully implemented
2. **Nested Function Calls**: Complex nested expressions work seamlessly
3. **Advanced Features**: Property assignments, user functions, sequences
4. **Robust Error Handling**: Comprehensive validation and clear error messages

#### Left Recursion

The grammar avoids left recursion by using right-recursive rules with iteration, making it suitable for top-down parsing.

#### Ambiguity Resolution

Potential ambiguities will be resolved through:

1. **Precedence rules** for expressions
2. **Keyword precedence** over identifiers
3. **Longest match** for tokens
4. **Context-sensitive parsing** where necessary

## Summary

The Animation DSL grammar provides a clean, readable syntax for LED animations. The current implementation supports:

- **Basic DSL structure** - Strip configuration, colors, palettes, patterns, animations, sequences
- **Color definitions** - Hex colors (#RRGGBB, #AARRGGBB) and named colors
- **Palette definitions** - Custom color palettes with VRGB format conversion
- **Pattern definitions** - Currently `solid()` patterns only
- **Animation definitions** - Core animation functions with unified naming
- **Property assignments** - `animation.property = value` syntax
- **Simple sequences** - Play, wait, and repeat statements
- **Variable assignments** - `set variable = value` with type conversion
- **Comment preservation** - All DSL comments preserved in generated Berry code
- **Easing keywords** - Linear, triangle, smooth, ease_in, ease_out, ramp, sawtooth, square

The grammar is designed to be extensible, with plans for advanced pattern functions, control flow statements, user-defined functions, and event handling in future implementations.