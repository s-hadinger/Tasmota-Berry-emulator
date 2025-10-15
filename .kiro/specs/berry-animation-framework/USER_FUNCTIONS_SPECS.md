# User-Defined Functions for Animation DSL

This document explains how to create and use user-defined functions with the Animation DSL.

## Overview

The Animation DSL supports calling user-defined functions that are written in Berry and registered with the animation module. This allows you to create reusable, complex animation effects that can be called from DSL code just like built-in functions.

## How It Works

1. **Write functions in Berry** - Create your custom animation functions using the full power of Berry
2. **Register functions** - Register your functions with the animation module
3. **Use in DSL** - Call your functions from DSL code just like built-in functions

## Creating User Functions

### 1. Write Your Function in Berry

```berry
# Example: Custom breathing effect - engine must be first parameter
def my_breathing_effect(engine, base_color, period)
  # Create a pulse animation with the specified color and period
  var pulse_anim = animation.pulse_animation(engine)
  pulse_anim.color = base_color
  pulse_anim.min_brightness = 50
  pulse_anim.max_brightness = 255
  pulse_anim.period = period
  return pulse_anim
end
```

### 2. Register Your Function

```berry
# Register the function with the animation module
animation.register_user_function("breathing", my_breathing_effect)
```

### 3. Use in DSL

```dsl
strip length 60
color blue = #0000FF

# Call your user-defined function - engine is automatically passed as first argument
animation calm_breathing = breathing(blue, 4s)

sequence demo {
  play calm_breathing for 10s
}

run demo
```

**Important**: The DSL transpiler automatically passes `engine` as the first argument to all user functions. Your function signature must include `engine` as the first parameter, but DSL users don't need to provide it when calling the function.

## Function Registration API

### `animation.register_user_function(name, func)`
Registers a Berry function to be available in DSL.

- **name**: String - The name to use in DSL (no namespace prefix needed)
- **func**: Function - The Berry function to register

### `animation.is_user_function(name)`
Checks if a function is registered as a user function.

- **name**: String - Function name to check
- **Returns**: Boolean - True if the function is registered

### `animation.get_user_function(name)`
Gets a registered user function.

- **name**: String - Function name to get
- **Returns**: Function or nil - The registered function, or nil if not found

### `animation.list_user_functions()`
Lists all registered user function names.

- **Returns**: List - Array of registered function names

## Example User Functions

### Simple Color Effect
```berry
def solid_with_brightness(engine, color, brightness_percent)
  # Convert percentage to 0-255 range
  var brightness = int(tasmota.scale_uint(brightness_percent, 0, 100, 0, 255))
  var solid_anim = animation.solid_animation(engine)
  solid_anim.color = color
  solid_anim.brightness = brightness
  return solid_anim
end

animation.register_user_function("bright_solid", solid_with_brightness)
```

```dsl
animation bright_red = bright_solid(red, 80%)
```

### Complex Pattern Generator
```berry
def fire_effect(engine, intensity, speed_ms)
  var color_provider = animation.rich_palette(engine)
  color_provider.palette = animation.PALETTE_FIRE
  color_provider.cycle_period = speed_ms
  color_provider.easing = 1
  
  var fire_anim = animation.filled(engine)
  fire_anim.color_provider = color_provider
  fire_anim.brightness = intensity
  return fire_anim
end

animation.register_user_function("fire", fire_effect)
```

```dsl
animation flames = fire(200, 300ms)
```

### Multi-Parameter Function
```berry
def sparkle_effect(engine, base_color, sparkle_color, density_percent)
  var density = int(tasmota.scale_uint(density_percent, 0, 100, 0, 255))
  var sparkle_anim = animation.twinkle_animation(engine)
  sparkle_anim.color = sparkle_color
  sparkle_anim.density = density
  sparkle_anim.speed = 500
  return sparkle_anim
end

animation.register_user_function("sparkle", sparkle_effect)
```

```dsl
animation sparkles = sparkle(blue, white, 15%)
```

## Advanced Usage

### Nested Function Calls
User functions work seamlessly with nested function calls:

```dsl
# User function inside built-in function
animation complex = fade(breathing(red, 2s), 3s)

# Built-in function inside user function (if the user function supports it)
animation layered = overlay(fire(200, 300ms), sparkle(white, black, 10%))
```

### Function Composition
User functions can call other user functions:

```berry
def complex_effect(base_color, speed)
  # Call another user function
  var breathing_anim = animation.get_user_function("breathing")(base_color, speed)
  # Add additional processing
  return breathing_anim
end

animation.register_user_function("complex", complex_effect)
```

### Using Animation Framework Features
User functions have access to all animation framework features:

```berry
def rainbow_pulse(speed, pulse_period)
  # Use built-in palette
  var rainbow_palette = animation.PALETTE_RAINBOW
  var provider = animation.rich_palette(rainbow_palette, speed, 1, 255)
  var base_anim = animation.filled(provider, 0, 0, true, "rainbow")
  
  # Add pulsing effect (this is conceptual - actual implementation may vary)
  return base_anim
end

animation.register_user_function("rainbow_pulse", rainbow_pulse)
```

## Best Practices

### 1. Function Naming
- Use descriptive names that clearly indicate the function's purpose
- Avoid conflicts with built-in function names
- Use snake_case or camelCase consistently

### 2. Parameter Handling
- Accept parameters in logical order (color, then timing, then modifiers)
- Use meaningful parameter names
- Handle edge cases gracefully

### 3. Return Values
- Always return an animation object that can be used in DSL
- Ensure returned animations are properly configured
- Document what your function returns

### 4. Error Handling
- Use Berry's exception handling for error conditions
- Provide meaningful error messages
- Fail gracefully when possible

### 5. Documentation
- Comment your functions clearly
- Document parameter types and ranges
- Provide usage examples

## File Organization

### Recommended Structure
```
user_functions.be          # Main user functions file
user_functions/
  ├── effects.be          # Effect-based functions
  ├── patterns.be         # Pattern generators
  ├── utilities.be        # Helper functions
  └── examples.be         # Example functions
```

### Loading User Functions
```berry
# In your main script or initialization
import "user_functions" as user_funcs  # Registers all functions

# Or load specific modules
import "user_functions/effects" as effects
import "user_functions/patterns" as patterns
```

## Limitations

1. **No DSL Syntax**: Functions must be written in Berry, not DSL
2. **Registration Required**: Functions must be explicitly registered
3. **No Automatic Discovery**: The DSL transpiler doesn't automatically find Berry functions
4. **Runtime Registration**: Functions must be registered before DSL compilation
5. **No Type Checking**: Parameter types are not validated (follows Berry's dynamic typing)

## Troubleshooting

### Function Not Found
```
Error: Unknown function 'my_function'
```
- Ensure the function is registered with `animation.register_user_function()`
- Check that the registration happens before DSL compilation
- Verify the function name matches exactly (case-sensitive)

### Generated Code Issues
```
Error: Function call failed
```
- Check that your function returns a valid animation object
- Ensure all parameters are handled correctly
- Verify that your function doesn't have syntax errors

### Import Issues
```
Error: Cannot import user_functions
```
- Ensure the user_functions.be file is in the correct location
- Check that all dependencies are available
- Verify file permissions and accessibility

## Complete Example

Here's a complete example showing how to create and use user functions:

**user_functions.be:**
```berry
import animation

def breathing_effect(base_color, period)
  var black = 0xFF000000
  var gradient_pattern = animation.gradient(engine)
  gradient_pattern.colors = [black, base_color, black]
  var pulse_anim = animation.pulse_animation(engine)
  pulse_anim.source = gradient_pattern
  pulse_anim.period = period
  return pulse_anim
end

def fire_effect(intensity, speed)
  var fire_palette = animation.PALETTE_FIRE
  var provider = animation.rich_palette(fire_palette, speed, 1, intensity)
  return animation.filled(provider, 0, 0, true, "fire")
end

animation.register_user_function("breathing", breathing_effect)
animation.register_user_function("fire", fire_effect)
```

**main.be:**
```berry
import animation
import "user_functions" as user_funcs

var dsl_code = 
  "strip length 60\n" +
  "color red = #FF0000\n" +
  "color blue = #0000FF\n" +
  "\n" +
  "animation red_breathing = breathing(red, 4s)\n" +
  "animation blue_fire = fire(200, 300ms)\n" +
  "\n" +
  "sequence demo {\n" +
  "  play red_breathing for 10s\n" +
  "  play blue_fire for 8s\n" +
  "}\n" +
  "\n" +
  "run demo"

var berry_code = animation_dsl.compile(dsl_code)
var compiled_func = compile(berry_code)
compiled_func()  # Execute the animation
```

This system provides a powerful way to extend the DSL with custom functionality while keeping the DSL syntax clean and simple.