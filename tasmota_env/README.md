This directory contains the files needed to emulate the Tasmota minimal environment.

Use `import tasmota` to trigger loading of all required components

## Browser Environment Detection

When running in the browser (via the Berry WASM simulator), the global `__JS__` flag is set to `true` during initialization. Berry code can use this to detect if it's running in a browser environment:

```berry
if global.contains("__JS__")
  # Running in browser simulator
  print("Running in browser")
else
  # Running on actual ESP32 hardware
  print("Running on ESP32")
end
```

This allows you to write code that works in both environments, with conditional logic for browser-specific features or hardware-specific operations.
