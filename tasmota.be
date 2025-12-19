#!/usr/bin/env -S ./berry -s -g
#
# autoexec.be
#
# auto-load all Tasmota environment and run code

# add `tasmota_env` in the path for importing modules
# we do it through an anonymous function to not pollute the global namespace
do
  import sys
  var path = sys.path()
  path.push('./tasmota_env')
end

# import common modules that are auto-imported in Tasmota
import global
do
  global.global = global
  # import global as global_inner
  # global_inner.global = global_inner
end

# import all Tasmota emulator stuff
do
  import load
  global.load = load
end

global.tasmota = nil    # make sure it's visible in global scope

import gpio
global.gpio = gpio
import light_state
global.light_state = light_state
import Leds
global.Leds = Leds
import tasmota_core as tasmota
global.tasmota = tasmota

return tasmota
