#!/usr/bin/env -S ../../../lib/libesp32/berry/berry -s -g
#
# unit tests

# add local dir
import sys
sys.path().push(".")

# import modules
import tasmota
import light_state
import Leds_frame

# tests
assert(tasmota.scale_int(10,-500,500,5000,-5000) == -100)
assert(tasmota.scale_int(0,-500,500,5000,-5000) == 0)
assert(tasmota.scale_int(-500,-500,500,5000,-5000) == 5000)
assert(tasmota.scale_int(450,-500,500,5000,-5000) == -4500)

assert(light_state.ledGamma10_10(0) == 0)
assert(light_state.ledGamma10_10(1) == 1)
assert(light_state.ledGamma10_10(10) == 1)
assert(light_state.ledGamma10_10(45) == 3)
assert(light_state.ledGamma10_10(500) == 145)
assert(light_state.ledGamma10_10(1020) == 1016)
assert(light_state.ledGamma10_10(1023) == 1023)

print("=== All tests OK")
