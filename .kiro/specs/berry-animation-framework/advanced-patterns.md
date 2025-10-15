# Advanced Animation Patterns Specification

## Overview

This specification defines four advanced animation patterns for the Berry Animation Framework: **Noise**, **Plasma**, **Sparkle**, and **Wave**. These patterns provide sophisticated visual effects while maintaining the framework's performance standards and API consistency.

## Design Goals

### Primary Objectives
1. **Performance**: Optimized for embedded systems with limited resources
2. **Consistency**: Follow established framework patterns and conventions
3. **Flexibility**: Support both static values and dynamic value providers
4. **Quality**: Provide visually appealing, professional-grade effects
5. **Usability**: Simple API with sensible defaults and global constructors

### Technical Requirements
- Integer-only arithmetic (no floating-point operations)
- Pre-computed lookup tables for performance-critical calculations
- Memory-efficient state management
- Consistent parameter validation and handling
- Full integration with existing color provider system

## Pattern Specifications

### 1. Noise Animation

#### Purpose
Generate pseudo-random noise patterns with fractal complexity for organic, natural-looking effects.

#### Technical Approach
- **Algorithm**: Linear congruential generator with lookup table
- **Interpolation**: Linear interpolation between discrete noise values
- **Fractal Support**: Multiple octaves with configurable persistence
- **Animation**: Time-based offset progression through noise space

#### Key Parameters
- `scale` (0-255): Noise frequency/detail level
- `speed` (0-255): Animation speed
- `octaves` (1-4): Number of fractal octaves
- `persistence` (0-255): Octave amplitude decay
- `seed`: Reproducible pattern seed

#### Performance Characteristics
- **Memory**: 256-value lookup table + pixel arrays
- **CPU**: O(n × octaves) per frame where n = strip length
- **Scalability**: Linear with strip length and octave count

### 2. Plasma Animation

#### Purpose
Create classic plasma effects using sine wave interference patterns for smooth, flowing visuals.

#### Technical Approach
- **Algorithm**: Dual sine wave interference with configurable frequencies
- **Wave Generation**: Pre-computed sine lookup table with quarter-wave symmetry
- **Blend Modes**: Add, multiply, and average combination methods
- **Animation**: Time-based phase progression

#### Key Parameters
- `freq_x` (0-255): Primary wave frequency
- `freq_y` (0-255): Secondary wave frequency
- `phase_x`, `phase_y` (0-255): Wave phase offsets
- `time_speed` (0-255): Animation speed
- `blend_mode` (0-2): Wave combination method

#### Performance Characteristics
- **Memory**: 256-value sine table + pixel arrays
- **CPU**: O(n) per frame where n = strip length
- **Scalability**: Linear with strip length, independent of frequency

### 3. Sparkle Animation

#### Purpose
Generate random twinkling effects with individual pixel lifecycle management for starfield and magical effects.

#### Technical Approach
- **State Management**: Per-pixel brightness, age, and state tracking
- **Lifecycle**: Creation, aging, fading, and death phases
- **Timing**: Frame-based updates at ~30 FPS
- **Randomization**: Pseudo-random sparkle generation

#### Key Parameters
- `density` (0-255): Sparkle creation probability
- `fade_speed` (0-255): Fade-out rate
- `sparkle_duration` (0-255): Maximum sparkle lifetime
- `min_brightness`, `max_brightness` (0-255): Brightness range
- `background_color`: Non-sparkle pixel color

#### Performance Characteristics
- **Memory**: 3 arrays × strip length (colors, states, ages)
- **CPU**: O(n) per frame where n = strip length
- **Scalability**: Linear with strip length

### 4. Wave Animation

#### Purpose
Generate mathematical waveforms with configurable types, amplitude, and movement for rhythmic and geometric patterns.

#### Technical Approach
- **Wave Types**: Sine, triangle, square, sawtooth with distinct algorithms
- **Generation**: Pre-computed lookup tables for each wave type
- **Scaling**: Amplitude and center level adjustment
- **Animation**: Phase progression for wave movement

#### Key Parameters
- `wave_type` (0-3): Waveform shape
- `amplitude` (0-255): Wave intensity range
- `frequency` (0-255): Wave density
- `phase` (0-255): Pattern offset
- `wave_speed` (0-255): Movement speed
- `center_level` (0-255): Baseline intensity

#### Performance Characteristics
- **Memory**: 256-value wave table + pixel arrays
- **CPU**: O(n) per frame where n = strip length
- **Scalability**: Linear with strip length

## Implementation Architecture

### Class Hierarchy
```
animation.animation (base class)
├── NoiseAnimation
├── PlasmaAnimation
├── SparkleAnimation
└── WaveAnimation
```

### Common Patterns

#### Constructor Signature
```berry
def init(pattern_params..., strip_length, priority, duration, loop, name)
```

#### Parameter Registration
```berry
self.register_param(name, {"min": min_val, "max": max_val, "default": default_val})
```

#### Update Cycle
```berry
def update(time_ms)
  if !super(self).update(time_ms) return false end
  # Update pattern-specific state
  # Calculate colors for all pixels
  return true
end
```

#### Rendering
```berry
def render(frame, time_ms)
  if !self.is_running || frame == nil return false end
  # Copy colors to frame buffer
  return true
end
```

### Global Constructor Functions

Each pattern provides convenience constructors:
- Basic version with common parameters
- Single-color version for simple effects
- Custom version with full parameter control

Example pattern:
```berry
def pattern_basic(common_params..., strip_length, priority)
def pattern_single_color(color, common_params..., strip_length, priority)
def pattern_custom(color_source, all_params..., strip_length, priority)
```

## Integration Requirements

### Framework Integration
1. **Module Registration**: Add to `animation.be` imports
2. **Color Provider Support**: Full compatibility with all color providers
3. **Parameter System**: Use base class parameter management
4. **Value Provider Support**: Accept both static values and dynamic providers

### Testing Requirements
1. **Unit Tests**: Comprehensive test coverage for each pattern
2. **Parameter Tests**: Validation of all parameter changes
3. **Integration Tests**: Compatibility with framework systems
4. **Performance Tests**: Memory and CPU usage validation

### Documentation Requirements
1. **API Documentation**: Complete parameter and method documentation
2. **Usage Examples**: Practical code examples for common use cases
3. **Visual Guides**: Description of visual characteristics
4. **Integration Guides**: How to combine with other effects

## Performance Specifications

### Memory Usage Targets
- **Lookup Tables**: ≤ 256 bytes per pattern
- **Pixel Arrays**: 4 bytes × strip length (ARGB colors)
- **State Data**: Minimal additional per-pixel state
- **Total Overhead**: < 1KB for typical 30-pixel strip

### CPU Usage Targets
- **Update Frequency**: 30-60 FPS capability
- **Calculation Complexity**: O(n) or better per frame
- **Integer Operations**: No floating-point arithmetic
- **Lookup Table Access**: Constant-time color/wave calculations

### Scalability Requirements
- **Strip Length**: Support 1-1000 pixels efficiently
- **Multiple Instances**: Multiple patterns simultaneously
- **Parameter Changes**: Real-time parameter modification
- **Memory Scaling**: Linear growth with strip length

## Quality Assurance

### Visual Quality Standards
1. **Smoothness**: No visible artifacts or discontinuities
2. **Color Accuracy**: Proper color space handling
3. **Timing Consistency**: Stable frame rates and animation speed
4. **Parameter Response**: Immediate response to parameter changes

### Code Quality Standards
1. **Berry Compliance**: Follow Berry language constraints
2. **Framework Patterns**: Consistent with existing animations
3. **Error Handling**: Graceful handling of invalid parameters
4. **Documentation**: Complete inline and external documentation

### Testing Standards
1. **Coverage**: 100% test coverage for public APIs
2. **Edge Cases**: Testing of boundary conditions
3. **Integration**: Compatibility with all framework features
4. **Performance**: Validation of performance targets

## Future Considerations

### Extensibility
- **Custom Wave Types**: Framework for adding new wave functions
- **Noise Algorithms**: Support for different noise generation methods
- **Blend Modes**: Additional wave and color blending options
- **3D Effects**: Extension to 2D/3D coordinate systems

### Optimization Opportunities
- **SIMD Operations**: Vector processing for multiple pixels
- **GPU Acceleration**: Hardware-accelerated calculations
- **Caching**: Intelligent caching of computed values
- **Compression**: Compressed lookup tables for memory savings

### Advanced Features
- **Pattern Morphing**: Smooth transitions between pattern types
- **Harmonic Analysis**: Frequency domain pattern manipulation
- **Procedural Generation**: Algorithm-based pattern creation
- **Machine Learning**: AI-generated pattern parameters

## Implementation Status: ✅ COMPLETE

All four advanced animation patterns are fully implemented and operational:

- **Noise Animation** - Pseudo-random noise patterns with fractal complexity
- **Plasma Animation** - Classic plasma effects using sine wave interference  
- **Sparkle Animation** - Random twinkling effects with pixel lifecycle management
- **Wave Animation** - Mathematical waveforms with configurable movement

### Key Achievements
- Complete integration with framework parameter and color systems
- Integer-only arithmetic with pre-computed lookup tables for performance
- Comprehensive test coverage with working demo examples
- Full documentation and API reference
- Memory-efficient implementation suitable for embedded systems

## Conclusion

The advanced animation patterns provide sophisticated visual effects while maintaining the framework's core principles of performance, simplicity, and consistency. These patterns demonstrate the framework's extensibility and provide a rich foundation for creating complex LED animations.