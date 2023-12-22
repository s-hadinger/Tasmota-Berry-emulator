#
# Example for M5Stack Led Matrix
# 5 x 5 WS2812
#
import animate

var strip = Leds(5 * 5, gpio.pin(gpio.WS2812, 0))
var anim = animate.core(strip)
anim.set_back_color(0x000000)
var pulse = animate.pulse(0xFF0000, 3, 2)
var osc1 = animate.oscillator(0, 23, 3000, animate.TRIANGLE)
osc1.set_cb(pulse, pulse.set_pos)

anim.start()
