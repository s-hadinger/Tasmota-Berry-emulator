# LED Strip API Guide

## Overview

The LED Strip API provides a clean, reusable way to expose JavaScript functions to Berry code for LED strip visualization and control. This module handles ALL canvas management including sizing, pixel dimensions, and rendering logic.

## Architecture

### Files

- **`dist/led-strip-api.js`** - Core API module that manages LED strip rendering and canvas sizing
- **`dist/index.html`** - Main simulator using the consolidated API

### How It Works

1. **Initialization**: The page calls `window.ledStripAPI.init(config)` to set up the API
2. **Canvas Management**: The API handles all canvas sizing based on LED count and pixel size mode
3. **Berry Integration**: Berry code calls `js.frame_buffer_display(hexString)` and `js.get_strip_size()`
4. **JavaScript Bridge**: The `js` module in Berry (defined in `be_jslib.c`) calls the global functions:
   - `window.renderLEDStrip(hexString)` → calls `ledStripAPI.renderLEDStrip()`
   - `window.getStripSize()` → calls `ledStripAPI.getStripSize()`

## Usage

### Basic Setup

```html
<!-- Load LED Strip API before Berry -->
<script src="led-strip-api.js"></script>

<!-- Load Berry modules and VM -->
<script src="virtual-fs.js"></script>
<script src="berry-modules.js"></script>
<script src="berry-vm.js"></script>
<script async src="berry.js"></script>

<!-- Initialize in your page -->
<script>
window.addEventListener('DOMContentLoaded', function() {
    // Initialize the LED Strip API with consolidated canvas management
    window.ledStripAPI.init({
        stripLength: 30,           // Number of LEDs
        pixelSizeMode: 'medium',   // 'small', 'medium', or 'large'
        ledSpacing: 2,             // Gap between LEDs in pixels
        reversed: false,           // false = L→R, true = R→L
        maxCanvasWidth: 700,       // Maximum canvas width
        canvasId: 'led-canvas',    // Canvas element ID
        backgroundColor: '#1a1a1a' // Background color
    });
});
</script>
```

### Configuration Options

```javascript
window.ledStripAPI.init({
    stripLength: 30,           // (optional) Number of LEDs, default: 30
    pixelSize: 10,             // (optional) Pixel size in pixels, default: 10
    pixelSizeMode: 'medium',   // (optional) Size mode: 'small', 'medium', 'large'
    ledSpacing: 2,             // (optional) Gap between LEDs, default: 2
    reversed: false,           // (optional) Render direction, default: false (L→R)
    maxCanvasWidth: 700,       // (optional) Max canvas width, default: 700
    canvasId: 'ledCanvas',     // (optional) Canvas element ID, default: 'ledCanvas'
    backgroundColor: '#1a1a1a',// (optional) Background color, default: '#1a1a1a'
    enablePerformanceMonitoring: true, // (optional) Enable FPS tracking, default: false
    onRender: function(colors) {
        // (optional) Callback when frame buffer is rendered
        // colors: array of ARGB color values
    },
    onPerformanceUpdate: function(metrics) {
        // (optional) Callback for performance metrics (called every second)
        // metrics: { fps: number, lastFrameTime: number }
        console.log('FPS:', metrics.fps);
    }
});
```

### Pixel Size Modes

The API supports three pixel size modes that automatically adapt based on LED count:

| Mode | Base Size | Min | Max | Best For |
|------|-----------|-----|-----|----------|
| `small` | 4px | 2px | 8px | Large LED counts (100+) |
| `medium` | 10px | 4px | 16px | Standard LED counts (30-100) |
| `large` | 16px | 8px | 24px | Small LED counts (<30) |

The actual pixel size is calculated to fit within the `maxCanvasWidth` constraint while staying within the mode's min/max range.

### Berry Code Example

```berry
import animation

# Create a frame buffer
var fb = animation.frame_buffer(30)

# Set some colors
var i = 0
while i < 30
  fb.set_pixel_color(i, 0xFFFF0000)  # Red
  i += 1
end

# Create LED strip and copy colors
var strip = Leds(30)
var j = 0
while j < 30
  strip.set_pixel_color(j, fb.get_pixel_color(j))
  j += 1
end

# Display on canvas
strip.show()

# Get strip size
var size = js.get_strip_size()
print("Strip size:", size)
```

## API Reference

### Initialization

#### `window.ledStripAPI.init(config)`

Initialize the LED Strip API with configuration.

**Parameters:**
- `config` (Object, optional) - See Configuration Options above

**Returns:** `true` if successful, `false` if canvas not found

### Rendering

#### `window.ledStripAPI.renderLEDStrip(hexString)`

Render LED strip from hex color string. Called by Berry via `js.frame_buffer_display()`.

**Parameters:**
- `hexString` (string): Hex string with 6 chars per color (RRGGBB format, no alpha)

**Returns:** `true` on success, `false` on error

#### `window.ledStripAPI.clear()`

Clear the canvas with the background color.

### Strip Size Management

#### `window.ledStripAPI.getStripSize()`

Get the configured LED strip size. Called by Berry via `js.get_strip_size()`.

**Returns:** (number) Number of LEDs in the strip

#### `window.ledStripAPI.setStripSize(length)`

Set the LED strip size. Automatically recalculates pixel size if using mode-based sizing.

**Parameters:**
- `length` (number): New strip length (1-300)

### Brightness Control

#### `window.ledStripAPI.getBrightness()`

Get the current brightness level. Called by Berry via `js.get_brightness()`.

**Returns:** (number) Brightness percentage (0-200, where 100 = normal)

#### `window.ledStripAPI.setBrightness(brightness)`

Set the brightness level. This value is read by Berry's `Leds.get_bri()` method.

**Parameters:**
- `brightness` (number): Brightness percentage (0-200, where 100 = normal, >100 = overexpose)

### Pixel Size Management

#### `window.ledStripAPI.setPixelSize(size)`

Set the pixel size directly. Clears the pixel size mode.

**Parameters:**
- `size` (number): Pixel size in pixels (minimum 1)

#### `window.ledStripAPI.setPixelSizeMode(mode)`

Set the pixel size mode. Automatically calculates optimal pixel size.

**Parameters:**
- `mode` (string): 'small', 'medium', or 'large'

#### `window.ledStripAPI.calculatePixelSize(mode, ledCount)`

Calculate pixel size based on mode and LED count.

**Parameters:**
- `mode` (string): 'small', 'medium', or 'large'
- `ledCount` (number): Number of LEDs

**Returns:** (number) Calculated pixel size in pixels

#### `window.ledStripAPI.getPixelSize()`

Get the current pixel size.

**Returns:** (number) Current pixel size in pixels

#### `window.ledStripAPI.getPixelSizeMode()`

Get the current pixel size mode.

**Returns:** (string|null) Current mode or null if set directly

### Display Options

#### `window.ledStripAPI.setReversed(reversed)`

Set whether the LED strip is reversed (right-to-left).

**Parameters:**
- `reversed` (boolean): true for R→L, false for L→R

#### `window.ledStripAPI.setMaxCanvasWidth(maxWidth)`

Set the maximum canvas width for responsive sizing.

**Parameters:**
- `maxWidth` (number): Maximum width in pixels

### Utility Methods

#### `window.ledStripAPI.getCanvasDimensions()`

Get the current canvas dimensions.

**Returns:** (Object) `{ width: number, height: number }`

#### `window.ledStripAPI.setPixelColor(index, color)`

Set a single pixel color directly (for testing/debugging).

**Parameters:**
- `index` (number): LED index (0-based)
- `color` (number): 32-bit ARGB color value

### Performance Monitoring

#### `window.ledStripAPI.setPerformanceMonitoring(enabled)`

Enable or disable performance monitoring.

**Parameters:**
- `enabled` (boolean): Whether to enable FPS tracking

#### `window.ledStripAPI.getPerformanceMetrics()`

Get current performance metrics.

**Returns:** (Object) `{ fps: number, lastFrameTime: number }`

#### `window.ledStripAPI.getFPS()`

Get current frames per second.

**Returns:** (number) Current FPS (updated every second)

#### `window.ledStripAPI.resetPerformanceMetrics()`

Reset all performance counters.

## Integration with Berry's `js` Module

The LED Strip API works seamlessly with Berry's `js` module (defined in `be_jslib.c`):

```berry
# Call JavaScript functions from Berry
js.frame_buffer_display(hex_string)  # Renders the frame buffer
js.get_strip_size()                  # Gets the strip size
js.get_brightness()                  # Gets the brightness (0-200, 100 = normal)
js.call("functionName", arg1, arg2)  # Call any JS function
js.get("propertyPath")               # Get any JS property
js.set("propertyPath", value)        # Set any JS property
```

### Brightness Integration

The brightness slider in the UI (0-200 range) is automatically connected to Berry's `Leds` class:

1. **JavaScript Side**: When the brightness slider changes, `ledStripAPI.setBrightness(value)` is called
2. **Berry Side**: `Leds.get_bri()` calls `js.get_brightness()` when running in browser mode
3. **Scaling**: JavaScript brightness 0-200 maps to Berry brightness 0-511 using `tasmota.scale_uint()`
   - 0 → 0 (off)
   - 100 → 255 (normal)
   - 200 → 511 (overexpose/boost)

```berry
# Berry code automatically uses UI brightness
var strip = Leds(30)
var bri = strip.get_bri()  # Returns 0-511 based on UI slider
```

## Animation Loop Integration

The animation loop (`AnimationLoop` class in `animation-loop.js`) drives Berry animations by calling the global `_fast_loop()` function at each tick (60 FPS target).

### How It Works

1. **JavaScript Animation Loop**: Uses `requestAnimationFrame` for smooth 60 FPS rendering
2. **Berry _fast_loop()**: A global Berry function defined in `tasmota_core.be` when running in browser mode (`__JS__ = true`)
3. **tasmota.fast_loop()**: Called by `_fast_loop()`, iterates through all registered fast_loop closures
4. **Animation Engine**: Registers its `on_tick()` method as a fast_loop closure when `engine.run()` is called

### The _fast_loop() Function

The `_fast_loop()` function is automatically defined in `tasmota_core.be` when Berry detects it's running in a browser:

```berry
# Defined in tasmota_core.be when __JS__ is true
if global.contains("__JS__")
  global._fast_loop = def ()
    tasmota.fast_loop()
  end
end
```

### JavaScript Animation Loop Configuration

```javascript
// Initialize animation loop with Berry integration
var animationLoop = new AnimationLoop({
    targetFPS: 60,              // Target 60 frames per second
    useBerryFastLoop: true,     // Enable calling Berry's _fast_loop()
    onFrame: function() {
        // Optional JavaScript callback (runs alongside Berry)
    },
    onFPSUpdate: function(fps, metrics) {
        // Called every second with FPS and performance metrics
        console.log('FPS:', fps);
        console.log('Avg frame time:', metrics.avgFrameTime, 'ms');
    },
    onError: function(errorMessage, errorCount) {
        // Called when Berry execution error occurs
        console.error('Berry error:', errorMessage);
    }
});

// Start the animation loop
animationLoop.start();

// Stop the animation loop
animationLoop.stop();
```

### Animation Loop API

| Method | Description |
|--------|-------------|
| `start()` | Start the animation loop |
| `stop()` | Stop the animation loop |
| `toggle()` | Toggle running state |
| `getIsRunning()` | Check if loop is running |
| `getFPS()` | Get current FPS |
| `getMetrics()` | Get performance metrics |
| `setTargetFPS(fps)` | Set target FPS (1-120) |
| `setBerryFastLoopEnabled(enabled)` | Enable/disable Berry calls |
| `setFrameCallback(callback)` | Set JavaScript frame callback |
| `setFPSCallback(callback)` | Set FPS update callback |
| `setErrorCallback(callback)` | Set error callback |

### Performance Metrics

The animation loop tracks detailed performance metrics:

```javascript
var metrics = animationLoop.getMetrics();
// {
//   fps: 60.0,           // Current frames per second
//   avgFrameTime: 2.5,   // Average frame execution time (ms)
//   maxFrameTime: 5.0,   // Maximum frame time in last second
//   minFrameTime: 1.0    // Minimum frame time in last second
// }
```

### Error Handling

The animation loop handles Berry execution errors gracefully:

- Errors are logged to console (first error and every 60th error)
- Error callback is called with error message and count
- After 10 consecutive errors, the animation loop stops automatically
- Error information is available via `getErrorInfo()`

## Examples

### Example 1: Dynamic Configuration

```javascript
// Initialize with medium pixel size
window.ledStripAPI.init({
    stripLength: 30,
    pixelSizeMode: 'medium',
    canvasId: 'led-canvas'
});

// Later, change to large pixels
window.ledStripAPI.setPixelSizeMode('large');

// Or set pixel size directly
window.ledStripAPI.setPixelSize(20);

// Change strip size (pixel size auto-adjusts if using mode)
window.ledStripAPI.setStripSize(60);
```

### Example 2: Responsive Canvas

```javascript
// The API automatically constrains canvas width
window.ledStripAPI.init({
    stripLength: 100,
    pixelSizeMode: 'medium',
    maxCanvasWidth: 600,  // Canvas won't exceed 600px
    canvasId: 'led-canvas'
});

// Pixel size is automatically reduced to fit
console.log('Pixel size:', window.ledStripAPI.getPixelSize());
```

### Example 3: Custom Rendering Callback

```javascript
window.ledStripAPI.init({
    stripLength: 60,
    pixelSizeMode: 'medium',
    canvasId: 'myCanvas',
    onRender: function(colors) {
        // Update UI with color information
        document.getElementById('colorCount').textContent = colors.length;
        
        // Log color values
        console.log('Colors:', colors.map(c => '0x' + c.toString(16)));
    }
});
```

## Benefits

1. **Consolidated**: All canvas management in one place
2. **Reusable**: Use the same API in multiple HTML pages
3. **Responsive**: Automatic pixel size adaptation based on LED count
4. **Clean**: Separates LED rendering logic from page-specific code
5. **Extensible**: Easy to add new functions or callbacks
6. **Testable**: Can be tested independently of Berry code
7. **Maintainable**: Single source of truth for LED rendering

## Troubleshooting

### "Canvas element not found"

Make sure:
1. Your HTML has a `<canvas>` element with the correct ID
2. The canvas element exists before calling `init()`
3. The `canvasId` parameter matches your canvas element ID

### Berry can't find `js.get_strip_size()`

Make sure:
1. `led-strip-api.js` is loaded before `berry.js`
2. The global functions `renderLEDStrip` and `getStripSize` are defined
3. Berry's `js` module is properly initialized

### Colors not rendering correctly

Check:
1. Hex string format is correct (RRGGBB, 6 chars per color, no alpha)
2. Canvas context is available
3. No JavaScript errors in browser console

### Pixel size not changing

If using `setPixelSizeMode()`:
- The pixel size is calculated based on LED count and max canvas width
- Check `getPixelSize()` to see the actual calculated size
- Increase `maxCanvasWidth` if you need larger pixels

## Migration from renderer.js

If you were previously using `renderer.js` with `LEDStripRenderer`:

| Old (renderer.js) | New (led-strip-api.js) |
|-------------------|------------------------|
| `window.initLEDRenderer(...)` | `window.ledStripAPI.init(...)` |
| `window.ledRenderer.renderFromHex(hex)` | `window.ledStripAPI.renderLEDStrip(hex)` |
| `window.ledRenderer.setPixelSize(size)` | `window.ledStripAPI.setPixelSize(size)` |
| `window.ledRenderer.setReversed(rev)` | `window.ledStripAPI.setReversed(rev)` |
| `window.ledRenderer.resize(w, h)` | `window.ledStripAPI.setStripSize(w)` |

The new API also adds:
- `setPixelSizeMode()` for automatic pixel size calculation
- `calculatePixelSize()` for manual calculation
- `setMaxCanvasWidth()` for responsive constraints
- `getPixelSize()` and `getPixelSizeMode()` getters
