# Berry Animation Simulator

A browser-based simulator for the [Berry Animation Framework](lib/libesp32/berry_animation/README.md), enabling LED strip animation development and testing directly in your web browser without hardware.

## 🌐 Try It Now

<img width="353" alt="Tasmota_Berry_LED_emulator" src="emulator_screenshot.png" />

**[Launch the Emulator](https://tasmota.github.io/docs/Tasmota-Berry-emulator/index.html)**

No installation required - runs entirely in your browser.

## About

This project is part of [Tasmota](https://github.com/arendst/Tasmota), an open-source firmware for ESP32/ESP8266 devices. Tasmota provides extensive home automation capabilities, including addressable LED strip control through the [Berry scripting language](https://berry.readthedocs.io/).

The Berry Animation Framework introduces a simplified Domain-Specific Language (DSL) for creating LED animations. This simulator compiles the Berry interpreter to WebAssembly, allowing you to develop and test animations in your browser before deploying to hardware.

## ✨ Features

- **Browser-Based** - No hardware required, runs entirely in WebAssembly
- **Real-Time Preview** - See your animations on a virtual LED strip
- **DSL Support** - Write animations using the simplified animation DSL
- **Berry Support** - Full Berry language support for advanced animations
- **Example Library** - Browse and run example animations instantly
- **APNG Export** - Export animations as animated PNG files for sharing
- **Tasmota UI** - Familiar interface matching Tasmota's web UI style

## 🎬 Animation Examples

| Rainbow Wave | Fire Effect |
|:---:|:---:|
| ![Color Pattern](docs/img/color_pattern-15fps-5s.png) | Cycling color pattern |
| ![Cylon red eye](docs/img/cylon-15fps-5s.png) | Cylon red eye |

## 🚀 Quick Start

### Using the Online Simulator

1. Open the [simulator](https://raw.githubusercontent.com/s-hadinger/Tasmota-Berry-emulator/main/dist/index.html)
2. Select an example from the Animation Library panel
3. Click "Compile & Run" to see the animation
4. Modify the code and experiment!

### Running Locally

```bash
# Clone the repository
git clone https://github.com/s-hadinger/Tasmota-Berry-emulator.git
cd Tasmota-Berry-emulator

# Open in browser (no server required)
open dist/index.html
```

## 📝 Writing Animations

The simulator includes a library of example animations - just select one from the Animation Library panel and click "Compile & Run". Here's a sample of what the DSL looks like:

```berry
# @desc Smooth color transitions using rich_palette with sine interpolation

# define a palette of rainbow colors including white with constant brightness
palette rainbow_with_white = [
  0xFC0000        # Red
  0xFF8000        # Orange
  0xFFFF00        # Yellow
  0x00FF00        # Green
  0x00FFFF        # Cyan
  0x0080FF        # Blue
  0x8000FF        # Violet
  0xCCCCCC        # White
  0xFC0000        # Red - need to add the first color at last position to ensure roll-over
]

# define a color attribute that cycles over time, cycle is 10 seconds
color rainbow_rich_color = rich_palette(colors=rainbow_with_white, period=10s, transition_type=SINE)

animation back = solid(color=rainbow_rich_color)

run back
```

## 📚 Documentation

### Animation Framework
- **[Animation Framework README](lib/libesp32/berry_animation/README.md)** - Overview and quick start
- **[DSL Reference](lib/libesp32/berry_animation/docs/DSL_REFERENCE.md)** - Complete DSL syntax
- **[Animation Classes](lib/libesp32/berry_animation/docs/ANIMATION_CLASS_HIERARCHY.md)** - Available animations

### Simulator
- **[Berry JS Module](docs/BERRY_JS_MODULE.md)** - JavaScript bridge API for Berry
- **[LED Strip API](docs/LED_STRIP_API_GUIDE.md)** - LED rendering API

### External Resources
- **[Tasmota Documentation](https://tasmota.github.io/)** - Official Tasmota docs
- **[Berry Language](https://berry.readthedocs.io/)** - Berry language reference
- **[Tasmota Berry Guide](https://tasmota.github.io/docs/Berry/)** - Berry in Tasmota

## 🛠️ Building from Source

### Prerequisites

- [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html) for WebAssembly compilation
- Make and Clang (recommended) or GCC

### Build Commands

```bash
# Full build (native + WebAssembly)
./build.sh

# Or build separately:

# Native Berry interpreter
make -C berry-lang clean
make -C berry-lang

# WebAssembly build
source emsdk/emsdk_env.sh
make -C berry-lang clean BUILD_MODE=emsdk
make -C berry-lang BUILD_MODE=emsdk
```

### Running Tests

```bash
# Run all tests
./run_all_tests.sh

# Compile all DSL examples
./compile_all_dsl_examples.sh
```

## 📁 Project Structure

```
├── dist/                    # Browser simulator files
│   ├── index.html          # Main simulator page
│   ├── berry.js            # Berry WASM module
│   └── *.js                # JavaScript modules
├── lib/libesp32/berry_animation/
│   ├── src/                # Animation framework source
│   ├── anim_examples/      # Example animations
│   ├── anim_tutorials/     # Tutorial animations
│   └── docs/               # Framework documentation
├── berry-lang/             # Berry interpreter source
├── tasmota_env/            # Tasmota emulator for local dev
├── docs/                   # Simulator documentation
└── emsdk/                  # Emscripten SDK
```

## 🤝 Contributing

Contributions are welcome! This project is part of the Tasmota ecosystem.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the simulator
5. Submit a pull request

## 📄 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

Part of the [Tasmota](https://github.com/arendst/Tasmota) project.

## 🔗 Links

- **[Tasmota GitHub](https://github.com/arendst/Tasmota)** - Main Tasmota repository
- **[Tasmota Documentation](https://tasmota.github.io/)** - Official documentation
- **[Berry Language](https://berry.readthedocs.io/)** - Berry scripting language
- **[Berry Short Manual (PDF)](https://berry.readthedocs.io/en/latest/_static/berry_short_manual.pdf)** - 8-page Berry reference

---

**Happy Animating!** 🎨✨
