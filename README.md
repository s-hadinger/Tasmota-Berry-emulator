# Tasmota-Berry-emulator

This project is part of the [Tasmota](https://github.com/arendst/Tasmota) project. Since end of 2023, Tasmota introduced an [animation framework](https://tasmota.github.io/docs/Berry_Addressable-LED/#animation-framework-module-animate) for Leds based on the embedded [Berry](https://tasmota.github.io/docs/Berry/) programming languages. However iterating when building new animations requires numerous updates on the Tasmota devices and reboots.

This project is a minimal Tasmota/Berry emulator enabling to run and try animations on a laptop, without the need to iterate on an actual embedded device. The goal is to provide an animated image (animated GIF or else) to vizualize the result and iterate.

## Installation

Requirements: Pyhton 3.x, C standard compiler

### Step 1. Clone the repository

```bash
git clone https://github.com/s-hadinger/Tasmota-Berry-emulator.git
cd Tasmota-Berry-emulator
```

### Step 2. Compile Berry

```bash
make
cd ..
```

You should see something like this:

```bash
> make
[Prebuild] generate resources
[Compile] src/be_api.c
[Compile] src/be_baselib.c
[Compile] src/be_bytecode.c
[Compile] src/be_byteslib.c
[Compile] src/be_class.c
[Compile] src/be_code.c
[Compile] src/be_debug.c
[Compile] src/be_debuglib.c
[Compile] src/be_exec.c
[Compile] src/be_filelib.c
[Compile] src/be_func.c
[Compile] src/be_gc.c
[Compile] src/be_gclib.c
[Compile] src/be_globallib.c
[Compile] src/be_introspectlib.c
[Compile] src/be_jsonlib.c
[Compile] src/be_lexer.c
[Compile] src/be_libs.c
[Compile] src/be_list.c
[Compile] src/be_listlib.c
[Compile] src/be_map.c
[Compile] src/be_maplib.c
[Compile] src/be_mathlib.c
[Compile] src/be_mem.c
[Compile] src/be_module.c
[Compile] src/be_object.c
[Compile] src/be_oslib.c
[Compile] src/be_parser.c
[Compile] src/be_rangelib.c
[Compile] src/be_repl.c
[Compile] src/be_solidifylib.c
[Compile] src/be_strictlib.c
[Compile] src/be_string.c
[Compile] src/be_strlib.c
[Compile] src/be_syslib.c
[Compile] src/be_timelib.c
[Compile] src/be_undefinedlib.c
[Compile] src/be_var.c
[Compile] src/be_vector.c
[Compile] src/be_vm.c
[Compile] default/be_modtab.c
[Compile] default/be_port.c
[Compile] default/be_re_lib.c
[Compile] default/berry.c
[Compile] re1.5/backtrack.c
[Compile] re1.5/charclass.c
[Compile] re1.5/cleanmarks.c
[Compile] re1.5/compile.c
[Compile] re1.5/compilecode.c
[Compile] re1.5/dumpcode.c
[Compile] re1.5/pike.c
[Compile] re1.5/recursive.c
[Compile] re1.5/recursiveloop.c
[Compile] re1.5/sub.c
[Compile] re1.5/thompson.c
[Compile] re1.5/util.c
[Linking...]
done
```

### Step 3. Prepare the Python environnement

```bash
python3 -m venv python_env
source python_env/bin/activate
python3 -m pip install "imageio"
```

Output:

```bash
> python3 -m venv python_env
> source python_env/bin/activate
> python3 -m pip install "imageio"
[... lots of linees]
Successfully installed imageio-2.33.1 numpy-1.26.2 pillow-10.1.0
```

## How to use

Copy your animation script in directory `tasmota` and run the following:

```bash
./run_animate.be tasmota/<file>.be
python3 generate_gif.py output.jsonl
```

Example:

```bash
> ./run_animate.be tasmota/animate_demo_cylon.be
Animation exported to 'output.jsonl'
> python3 generate_gif.py output.jsonl -o cylon.gif
```

## Example

#### demo_pulse

<img src='/demo_gif/pulse.gif' height='20'>

Berry code:

```berry
import animate

var strip = Leds(5 * 5, gpio.pin(gpio.WS2812, 0))
var anim = animate.core(strip)
anim.set_back_color(0x2222AA)
var pulse = animate.pulse(0xFF4444, 2, 1)
var osc1 = animate.oscillator(-3, 26, 5000, animate.COSINE)
osc1.set_cb(pulse, pulse.set_pos)

# animate color of pulse
var palette = animate.palette(animate.PALETTE_STANDARD_TAG, 30000)
palette.set_cb(pulse, pulse.set_color)

anim.start()
```

```bash
> ./run_animate.be -d 30000 tasmota/animate_demo_pulse.be
Animation exported to 'output.jsonl'
> python3 generate_gif.py output.jsonl -o pulse.gif
```

#### demo_cylon

<img src='/demo_gif/cylon.gif' height='20'>

```berry
import animate

var strip = Leds(5 * 5, gpio.pin(gpio.WS2812, 0))
var anim = animate.core(strip)
anim.set_back_color(0x000000)
var pulse = animate.pulse(0xFF0000, 3, 2)
var osc1 = animate.oscillator(0, 23, 3000, animate.TRIANGLE)
osc1.set_cb(pulse, pulse.set_pos)

anim.start()
```

```bash
> ./run_animate.be -d 3000 tasmota/animate_demo_cylon.be
Animation exported to 'output.jsonl'
> python3 generate_gif.py output.jsonl -o cylon.gif
```
