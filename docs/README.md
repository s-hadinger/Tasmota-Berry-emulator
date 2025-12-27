# Berry Animation Framework - Documentation

This folder contains documentation for the Berry Animation Framework and related components.

## Features

- **LED Strip API** - JavaScript interface for LED visualization
- **URL Parameters API** - Share direct links to specific animation examples
- **APNG Export** - Export animations as animated PNG files for sharing

## LED Strip API Documentation

The LED Strip API provides a clean, reusable way to expose JavaScript functions to Berry code for LED strip visualization and control.

### Files

- **[LED_STRIP_API_GUIDE.md](LED_STRIP_API_GUIDE.md)** - Complete API reference and usage guide
  - Architecture overview
  - Configuration options
  - API reference with examples
  - Troubleshooting guide
  - Future enhancements

- **[LED_STRIP_API_INTEGRATION.md](LED_STRIP_API_INTEGRATION.md)** - Integration summary
  - Overview of changes made
  - Script loading order
  - API initialization in both pages
  - Benefits and dynamic configuration
  - Testing checklist

## Quick Start

### For Users

1. Read [LED_STRIP_API_GUIDE.md](LED_STRIP_API_GUIDE.md) for complete API documentation
2. See examples in `dist/test-frame-buffer.html` for practical usage
3. Check [LED_STRIP_API_INTEGRATION.md](LED_STRIP_API_INTEGRATION.md) for integration details

### For Developers

1. The core API is in `dist/led-strip-api.js`
2. Both `dist/index.html` and `dist/test-frame-buffer.html` use the API
3. Berry code calls functions via the `js` module (defined in `berry-lang/src/be_jslib.c`)

## Architecture

```
Berry Code (Berry)
    ↓
js module (be_jslib.c)
    ↓
Global Functions (window.renderLEDStrip, window.getStripSize)
    ↓
LED Strip API (dist/led-strip-api.js)
    ↓
Canvas Rendering (HTML5 Canvas)
```

## Key Features

✅ **Reusable** - Use the same API in multiple HTML pages  
✅ **Clean** - Separates LED rendering logic from page-specific code  
✅ **Extensible** - Easy to add new functions or callbacks  
✅ **Testable** - Can be tested independently of Berry code  
✅ **Maintainable** - Single source of truth for LED rendering  
✅ **Synchronized** - LED count changes are automatically propagated to Berry  

## URL Parameters API

The simulator supports loading specific examples directly via URL parameters, making it easy to share links to specific animations.

### Parameters

| Parameter | Description |
|-----------|-------------|
| `example` | Load an example by its ID |
| `ex` | Short alias for `example` |

### Usage

```
https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html?example=<example_id>
```

### Examples

| Animation | URL |
|-----------|-----|
| Simple solid color | [?example=chap_1_00_plain](https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html?example=chap_1_00_plain) |
| Twinkle stars | [?example=chap_1_30_twinkle](https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html?example=chap_1_30_twinkle) |
| Night sky | [?example=chap_2_10_sky](https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html?example=chap_2_10_sky) |
| Rainbow gradient | [?example=chap_4_10_color_pattern](https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html?example=chap_4_10_color_pattern) |
| Cylon eye | [?example=chap_5_10_template_cylon_simple](https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html?example=chap_5_10_template_cylon_simple) |
| VU meter | [?example=chap_4_30_color_pattern_meter](https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html?example=chap_4_30_color_pattern_meter) |

### Behavior

- If the example ID is valid, the animation loads and auto-runs
- If the example ID is not found, a warning is logged to the console with all available IDs
- If no parameter is provided, the default example runs

### Finding Example IDs

Example IDs follow the pattern `chap_X_YY_name` where:
- `X` is the chapter number (1-5)
- `YY` is the section number
- `name` is a descriptive identifier

You can find all available IDs by:
1. Opening the Examples panel in the simulator
2. Checking the browser console if an invalid ID is provided

## APNG Export

The simulator supports exporting animations as Animated PNG (APNG) files:

- Click "Export APNG" button while an animation is running
- Configure duration and frame rate in the export dialog
- Download the resulting `.apng` file for sharing

APNG files can be viewed in most modern browsers and image viewers, and are ideal for documentation and sharing animation previews.

## Files Involved

### Runtime Files (in `dist/`)
- `led-strip-api.js` - Core API module
- `apng-exporter.js` - APNG export functionality
- `export-ui.js` - Export UI controls
- `index.html` - Main simulator
- `test-frame-buffer.html` - Test page

### Source Files
- `berry-lang/src/be_jslib.c` - Berry's JavaScript bridge module
- `tasmota_env/Leds.be` - LED strip emulation

### Documentation (in `docs/`)
- `README.md` - This file
- `LED_STRIP_API_GUIDE.md` - Complete API reference
- `LED_STRIP_API_INTEGRATION.md` - Integration summary

## Related Documentation

For more information about the Berry Animation Framework:
- See `lib/libesp32/berry_animation/docs/` for animation framework documentation
- See `.doc_for_ai/` for AI assistant reference materials
