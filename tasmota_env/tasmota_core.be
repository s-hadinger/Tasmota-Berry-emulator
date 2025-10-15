# Tasmota emulator - lightweitght for Leds animation

import global

class Tasmota
  var _millis           # emulate millis from Tasmota
  var _fl               # fast_loop

  def init()
    self._millis = 1
  end

  static def scale_uint(inum, ifrom_min, ifrom_max, ito_min, ito_max)
    if (ifrom_min >= ifrom_max)
      return (ito_min > ito_max ? ito_max : ito_min)  # invalid input, return arbitrary value
    end
    
    var num = inum
    var from_min = ifrom_min
    var from_max = ifrom_max
    var to_min = ito_min
    var to_max = ito_max

    # check source range
    num = (num > from_max ? from_max : (num < from_min ? from_min : num))

    # check to_* order
    if (to_min > to_max)
      # reverse order
      num = (from_max - num) + from_min
      to_min = ito_max
      to_max = ito_min
    end

    # short-cut if limits to avoid rounding errors
    if (num == from_min) return to_min  end
    if (num == from_max) return to_max  end
    
    var result
    if ((num - from_min) < 0x8000)
      if (to_max - to_min > from_max - from_min)
        var numerator = (num - from_min) * (to_max - to_min) * 2
        result = ((numerator / (from_max - from_min)) + 1 ) / 2 + to_min
      else
        var numerator = ((num - from_min) * 2 + 1) * (to_max - to_min + 1)
        result = numerator / ((from_max - from_min + 1) * 2) + to_min
      end
    else
      var numerator = (num - from_min) * (to_max - to_min + 1)
      result = numerator / (from_max - from_min) + to_min
    end

    return (result > to_max ? to_max : (result < to_min ? to_min : result))
  end

  static def scale_int(num, from_min, from_max, to_min, to_max)
    # guard-rails
    if (from_min >= from_max)
      return (to_min > to_max ? to_max : to_min)  # invalid input, return arbitrary value
    end

    var from_offset = 0
    if (from_min < 0)
      from_offset = - from_min
    end
    var to_offset = 0
    if (to_min < 0)
      to_offset = - to_min
    end
    if (to_max < (- to_offset))
      to_offset = - to_max
    end

    return _class.scale_uint(num + from_offset, from_min + from_offset, from_max + from_offset, to_min + to_offset, to_max + to_offset) - to_offset
  end

  def millis(offset)
    return self._millis + (offset == nil ? 0 : offset)
  end

  # does nothing
  def add_driver()
  end

  def is_network_up()
    return false
  end

  def log(m, l)
    if (l == nil) || (l <= 2)     # only print for level 2 or below
      print(m)
    end
  end

  # internal debugging function
  def set_millis(m)
    self._millis = m
  end

  def time_reached(t)
    # naive implementation because the emulator will not run over 20 days
    return (t <= self._millis)
  end

  # fast_loop() is a trimmed down version of event() called at every Tasmota loop iteration
  # it is optimized to be as fast as possible and reduce overhead
  # there is no introspect, closures must be registered directly
  def fast_loop()
    var fl = self._fl
    if !fl return end     # fast exit if no closure is registered (most common case)

    # iterate and call each closure
    var i = 0
    var sz = size(fl)
    while i < sz
      # note: this is not guarded in try/except for performance reasons. The inner function must not raise exceptions
      fl[i]()
      i += 1
    end
  end

  # check that the parameter is not a method, it would require a closure instead
  def check_not_method(f)
    import introspect
    if type(f) != 'function'
      raise "type_error", "BRY: argument must be a function"
    end
    if introspect.ismethod(f) == true
      raise "type_error", "BRY: method not allowed, use a closure like '/ args -> obj.func(args)'"
    end
  end

  def add_fast_loop(cl)
    self.check_not_method(cl)
    if self._fl == nil
      self._fl = []
    end
    if type(cl) != 'function' raise "value_error", "argument must be a function" end
    global.fast_loop_enabled = 1      # enable fast_loop at global level: `TasmotaGlobal.fast_loop_enabled = true`
    self._fl.push(cl)
  end

  def remove_fast_loop(cl)
    if !self._fl return end
    var idx = self._fl.find(cl)
    if idx != nil
      self._fl.remove(idx)
    end
  end

  def sine_int(i)
    import math

    var x = i / 16384.0 * math.pi
    var y = math.sin(x)
    var r = int(y * 4096)
    return r
  end

  def delay(t)
    # do nothing in this simulation environment
  end

end

import light_state
import Leds
import Leds_frame

global.tasmota = Tasmota()
return tasmota
