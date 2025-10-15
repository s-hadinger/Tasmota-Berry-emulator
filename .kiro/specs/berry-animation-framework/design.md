# Berry Animation Framework - Architecture Overview

## Overview

The Berry Animation Framework provides a powerful, lightweight system for controlling addressable LED strips in Tasmota. The framework uses a **unified pattern-animation architecture** with a focus on simplicity, performance, and extensibility for embedded systems.

## Core Design Principles

### 1. Unified Architecture
- **`Animation` extends `Pattern`**: Eliminates artificial distinctions
- **Infinite Composition**: Animations can use other animations as base patterns
- **Consistent API**: Same interface for all visual elements

### 2. Performance First
- **Single AnimationEngine**: Unified management with 66% fewer objects
- **Optimized for Embedded**: Minimal memory usage and CPU overhead
- **Integer Arithmetic**: Uses `tasmota.scale_uint()` for efficient calculations

### 3. Declarative DSL
- **Intuitive Syntax**: Natural language for describing animations
- **Transpiled to Berry**: Generates optimized native code
- **Extensible**: User-defined functions and custom effects

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Animation DSL                            │
│  color red = #FF0000                                        │
│  animation pulse_red = pulse(solid(red), 2s, 50%, 100%)    │
│  run pulse_red                                              │
└─────────────────────┬───────────────────────────────────────┘
                      │ Transpiles to
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Berry Code                                │
│  var engine = animation.create_engine(strip)               │
│  var pulse_red = animation.pulse(...)                      │
│  engine.add_animation(pulse_red).start()                   │
└─────────────────────┬───────────────────────────────────────┘
                      │ Executes on
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                Animation Engine                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ Animation 1 │ │ Animation 2 │ │ Animation N │          │
│  │ Priority: 10│ │ Priority: 5 │ │ Priority: 1 │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│                      │                                      │
│                      ▼                                      │
│  ┌─────────────────────────────────────────────────────────┤
│  │              Frame Buffer                               │
│  │  [R][G][B] [R][G][B] [R][G][B] ... [R][G][B]          │
│  └─────────────────────┬───────────────────────────────────┘
└────────────────────────┼─────────────────────────────────────┘
                         │ Updates via fast_loop
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   LED Strip                                 │
│  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●● │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### AnimationEngine
The central controller that manages all animations:
- **Unified Management**: Single object handles all animation lifecycle
- **Priority-Based Layering**: Higher priority animations render on top
- **Automatic Blending**: Smooth opacity-based blending between layers
- **Performance Optimized**: Integrated rendering pipeline for efficiency

### Pattern (Base Class)
Foundation for all visual elements:
- **Spatial Color Generation**: `get_color_at(pixel, time_ms)`
- **Priority & Opacity**: For layering and blending
- **Lifecycle Management**: Start, stop, update, render methods
- **Parameter System**: Static and dynamic parameter support

### Animation (Extends Pattern)
Adds temporal behavior to patterns:
- **Duration & Looping**: Time-based animation control
- **Progress Tracking**: Animation completion percentage
- **Infinite Composition**: Can use other animations as base patterns

### Value Providers
Dynamic parameters that change over time:
- **Static Values**: Regular integers, colors, etc.
- **Oscillators**: Sine, triangle, square, sawtooth waves
- **Color Providers**: Palette-based color generation
- **Custom Providers**: User-defined dynamic values

## Animation Types

### Basic Animations
- **`solid(color)`** - Static color fill
- **`pulse(pattern, period, min, max)`** - Brightness pulsing
- **`breathe(color, period)`** - Smooth breathing effect

### Palette-Based Animations
- **`rich_palette_animation(palette, period, easing, brightness)`** - Color cycling
- **Color palettes** - Smooth transitions between defined colors
- **Predefined palettes** - Rainbow, fire, ocean effects

### Position-Based Animations
- **`pulse_position_animation(color, pos, size, fade)`** - Localized pulse
- **`comet_animation(color, tail_length, speed)`** - Moving comet
- **`twinkle_animation(color, density, speed)`** - Twinkling stars

### Motion Effects
- **Fire simulation** - Realistic flame effects
- **Moving patterns** - Shift, bounce, rotate effects
- **Particle systems** - Complex multi-element animations

## DSL Features

### Declarative Syntax
```dsl
# Define colors and palettes
color red = #FF0000
palette fire = [(0, black), (128, red), (255, yellow)]

# Create animations with natural syntax
animation fire_effect = rich_palette_animation(fire, 3s, smooth, 255)
animation pulse_red = pulse(solid(red), 2s, 20%, 100%)

# Compose complex effects
animation complex = pulse(shift_left(fire_effect, 300ms), 4s, 70%, 100%)

# Create sequences
sequence demo {
  play fire_effect for 10s
  wait 1s
  play pulse_red for 5s
  repeat 3 times:
    play complex for 3s
    wait 500ms
}

run demo
```

### Advanced Features
- **Nested Function Calls**: `pulse(shift_left(gradient(red, orange), 200ms), 2s)`
- **User-Defined Functions**: Custom Berry functions callable from DSL
- **Event System**: Interactive animations responding to triggers
- **Property Assignment**: `animation.priority = 10`, `animation.opacity = 200`

## Event System

### Reactive Animations
```dsl
# Define animations
animation normal_glow = solid(blue)
animation flash_white = pulse(solid(white), 500ms, 80%, 100%)

# Event handlers
on button_press: flash_white
on timer(10s): normal_glow

# Main animation
run normal_glow
```

### Event Types
- **Hardware Events**: Button presses, sensor triggers
- **Timer Events**: Scheduled activations
- **Custom Events**: User-defined triggers
- **System Events**: Startup, shutdown, state changes

## Performance Characteristics

### Memory Efficiency
- **Unified Objects**: 66% reduction in core objects vs. traditional architectures
- **Shared Resources**: Value providers reused across animations
- **Optimized Buffers**: Minimal frame buffer allocations
- **Garbage Collection Friendly**: Reduced object creation/destruction

### CPU Optimization
- **Integer Arithmetic**: Uses `tasmota.scale_uint()` for fast calculations
- **Integrated Rendering**: Single-pass rendering pipeline
- **Priority-Based Updates**: Only active animations consume CPU
- **Fast Loop Integration**: Smooth 200Hz update rate with Tasmota

### Scalability
- **LED Count**: Efficiently handles 30-300+ LEDs
- **Animation Count**: Optimal with 1-5 simultaneous animations
- **Complexity**: Supports deep nesting and composition
- **Real-time**: Maintains smooth performance under load

## Extensibility

### User Functions
```berry
# Define custom function in Berry
def my_breathing_effect(color, period)
  return animation.pulse(animation.solid(color), period, 50, 255)
end

# Register for DSL use
animation.register_user_function("breathing", my_breathing_effect)

# Use in DSL
# animation calm = breathing(blue, 4s)
```

### Custom Animations
```berry
# Extend base classes
class MyCustomAnimation : animation.animation
  def get_color_at(pixel, time_ms)
    # Custom color generation logic
    return my_calculated_color
  end
end
```

### Plugin Architecture
- **Modular Design**: Core framework + optional effects
- **Clean Interfaces**: Well-defined extension points
- **Backward Compatibility**: New features don't break existing code

## Integration with Tasmota

### Fast Loop Integration
- **200Hz Updates**: Smooth animation updates via `fast_loop`
- **Non-blocking**: Animations don't interfere with Tasmota operations
- **Resource Aware**: Adapts to system load automatically

### LED Strip Support
- **Multiple Types**: WS2812, SK6812, APA102 support
- **GPIO Flexibility**: Any available GPIO pin
- **Power Management**: Efficient LED control with brightness limiting

### Berry Integration
- **Native Performance**: Compiled Berry code execution
- **Memory Management**: Integrates with Berry's garbage collector
- **Error Handling**: Robust exception handling and recovery

## Design Benefits

### For Users
- **Easy to Learn**: Natural DSL syntax with intuitive commands
- **Powerful**: Complex effects with simple declarative code
- **Reliable**: Robust error handling and comprehensive validation
- **Interactive**: Event-driven responsive animations with priority system

### For Developers
- **Clean Architecture**: Well-separated concerns with unified Pattern-Animation hierarchy
- **Extensible**: Easy to add new effects through base class extension
- **Testable**: Comprehensive test suite with high coverage
- **Maintainable**: Clear code structure and extensive documentation

### For Embedded Systems
- **Memory Efficient**: Minimal RAM usage with unified object architecture
- **CPU Optimized**: Fast execution with integer arithmetic and lookup tables
- **Real-time**: Consistent 30+ FPS performance under load
- **Scalable**: Efficient handling from 10 to 1000+ LEDs

This architecture provides a complete foundation for sophisticated LED animations while maintaining optimal performance for embedded systems.