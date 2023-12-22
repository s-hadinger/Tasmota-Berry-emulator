#!/usr/bin/env -S ./berry -s -g
#
# autoexec.be
#
# auto-load all Tasmota environment and run code

# add `tasmota_env` in the path for importing modules
# we do it through an anonymous function to not pollute the global namespace
(def ()
  import sys
  var path = sys.path()
  path.push('./tasmota_env')
  path.push('./tasmota')
end)()      # last `()` calls the anonymous function immediately

# import common modules that are auto-imported in Tasmota
import global

# import all Tasmota emulator stuff
import load
import gpio
import light_state
import Leds
import tasmota
import animate

# compile and run `autoexec.be`
(def ()
  var code = compile("autoexec.be", "file")
  code()
end)()
