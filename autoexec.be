# Command:
#   ./run_animate.be tasmota/animate_demo_pulse.be
#
# configura animation
#
var duration = 3000

var argv_index = 1

if _argv[argv_index] == '-d'
  duration = int(_argv[argv_index + 1])
  argv_index += 2
end

var animation_file = _argv[argv_index]
load(animation_file)

#
# emulate
#
var now = 0
var fname = "output.jsonl"

if (global._strip == nil)       raise "error", "global._strip is not initialized"       end

# post configure strip
global._strip.set_bri(255)          # set max brightness
global._strip.set_gamma(false)      # disable gamma

import json
var fout = open(fname, "w")
fout.write(f'{{"leds":{global._strip.pixel_count():i}}}\n')

while now < duration
  tasmota.set_millis(now)
  tasmota.fast_loop()
  
  fout.write(f'{{"t":{now:5i},"buf":"{global._strip.pixels_buffer().tohex()}"}}\n')

  now += 50   # add 50 ms step
end
fout.close()

print(f"Animation exported to '{fname}'")

