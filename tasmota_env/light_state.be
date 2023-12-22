# light_state

class light_state
  static var RELAY = 0
  static var DIMMER = 1
  static var CT = 2
  static var RGB = 3
  static var RGBW = 4
  static var RGBCT = 5

  var channels                # number of channels

  var power                   # (bool) on/off state
  var reachable	              # (bool) light is reachable
  var type                    # (int) number of channels of the light
  var bri                     # (int) brightness of the light (0..255)
  var ct                      # (int) white temperature of the light (153..500)
  var sat                     # (int) saturation of the light (0..255)
  var hue                     # (int) hue of the light (0..360)
  var hue16                   # (int) hue as 16 bits (0..65535)
  var r, g, b                 # (int) Red Green Blue channels (0..255)
  var r255, g255, b255        # (int) Red Green Blue channels (0..255) at full brightness
  var x,y                     # (float) x/y color as floats (0.0 .. 1.0)
  var mode_ct, mode_rgb       # (bool) light is in RGB or CT mode

  static var _gamma_table = [
    [    1,      1 ],
    [    4,      1 ],
    [  209,     13 ],
    [  312,     41 ],
    [  457,    106 ],
    [  626,    261 ],
    [  762,    450 ],
    [  895,    703 ],
    [ 1023,   1023 ],
    [ 0xFFFF, 0xFFFF ]          # fail-safe if out of range
  ]


  def init(channels)
    self.power = false
    self.reachable = true
    self.type = channels
    self.bri = 0
    self.ct = 153
    self.sat = 255
    self.hue = 0
    self.hue16 = 0
    self.r255 = 255
    self.g255 = 255
    self.b255 = 255
    self.r = 0
    self.g = 0
    self.b = 0
    self.x = 0.5
    self.y = 0.5
    self.mode_ct = false
    self.mode_rgb = true
  end

  #
  # INTERNAL
  #
  def signal_change() end     # nop

  #
  # GAMMA
  #
  # 10 bits in, 10 bits out
  static def ledGamma10_10(v)
    return _class.ledGamma_internal(v, _class._gamma_table)
  end

  static def ledGamma8_8(v8)
    if (v8 <= 0)    return 0    end
    var v10 = tasmota.scale_uint(v8, 0, 255, 0, 1023)
    var g10 = _class.ledGamma10_10(v10)
    var g8 = tasmota.scale_uint(g10, 4, 1023, 1, 255)
    return g8
  end

  # Calculate the gamma corrected value for LEDS
  static def ledGamma_internal(v, gt_ptr)
    var from_src = 0
    var from_gamma = 0
  
    var idx = 0
    while true
      var gt = gt_ptr[idx]
      var to_src = gt[0]
      var to_gamma = gt[1]
      if (v <= to_src)
        return tasmota.scale_uint(v, from_src, to_src, from_gamma, to_gamma)
      end
      from_src = to_src
      from_gamma = to_gamma
      idx += 1
    end
  end

  def set_rgb(r,g,b)
    var maxi = (r > g && r > b) ? r : (g > b) ? g : b      #   // 0..255

    if (0 == maxi)
      r = 255
      g = 255
      b = 255
      #self.mode_ct = false
      #self.mode_rgb = true
      #setColorMode(LCM_CT);   // try deactivating RGB, setColorMode() will check if this is legal
    else
      if (255 > maxi)
        #// we need to normalize rgb
        r = tasmota.scale_uint(r, 0, maxi, 0, 255)
        g = tasmota.scale_uint(g, 0, maxi, 0, 255)
        b = tasmota.scale_uint(b, 0, maxi, 0, 255)
      end
      # addRGBMode();
    end

    self.r255 = r
    self.g255 = g
    self.b255 = b
    self.compute_rgb()
    self.RgbToHsb(r,g,b)
  end

  def RgbToHsb(r,g,b)
    #RgbToHsb(r, g, b, &hue, &sat, nullptr);
    # void RgbToHsb(uint8_t ir, uint8_t ig, uint8_t ib, uint16_t *r_hue, uint8_t *r_sat, uint8_t *r_bri) {
    var max = (r > g && r > b) ? r : (g > b) ? g : b  #   // 0..255
    var min = (r < g && r < b) ? r : (g < b) ? g : b  #   // 0..255
    var d = max - min   #   // 0..255
  
    var hue = 0   #;   // hue value in degrees ranges from 0 to 359
    var sat = 0   #;    // 0..255
    var bri = max #;  // 0..255
  
    if (d != 0)
      sat = tasmota.scale_uint(d, 0, max, 0, 255)
      if (r == max)
        hue = (g > b) ?       tasmota.scale_uint(g-b,0,d,0,60) : 360 - tasmota.scale_uint(b-g,0,d,0,60)
      elif (g == max)
        hue = (b > r) ? 120 + tasmota.scale_uint(b-r,0,d,0,60) : 120 - tasmota.scale_uint(r-b,0,d,0,60)
      else
        hue = (r > g) ? 240 + tasmota.scale_uint(r-g,0,d,0,60) : 240 - tasmota.scale_uint(g-r,0,d,0,60)
      end
      hue = hue % 360 #;    // 0..359
    end
  
    self.hue = hue
    self.hue16 = tasmota.scale_uint(hue, 0, 360, 0, 65535);
    self.sat = sat
    self.bri = bri

  end

  # convert r255 to r accodring to bri
  def compute_rgb()
    self.r = tasmota.scale_uint(self.r255, 0, 255, 0, self.bri)
    self.g = tasmota.scale_uint(self.g255, 0, 255, 0, self.bri)
    self.b = tasmota.scale_uint(self.b255, 0, 255, 0, self.bri)
  end

  def set_bri(bri)
    if (bri == nil)   bri = 0     end
    if (bri < 0)      bri = 0     end
    if (bri > 255)    bri = 255   end
    self.bri = bri
    self.compute_rgb()
  end

  def HsToRgb(hue, sat)
    #void HsToRgb(uint16_t hue, uint8_t sat, uint8_t *r_r, uint8_t *r_g, uint8_t *r_b) {
    var r = 255
    var g = 255
    var b = 255
    # // we take brightness at 100%, brightness should be set separately
    hue = hue % 360   #;  // normalize to 0..359

    if (sat > 0)
      var i = hue / 60   #;   // quadrant 0..5
      var f = hue % 60   #;   // 0..59
      var q = 255 - tasmota.scale_uint(f, 0, 60, 0, sat)   #  // 0..59
      var p = 255 - sat
      var t = 255 - tasmota.scale_uint(60 - f, 0, 60, 0, sat)

      if i == 0
          # //r = 255;
          g = t
          b = p
      elif i == 1
          r = q
          # //g = 255;
          b = p
      elif i == 2
          r = p
          # //g = 255;
          b = t
      elif i == 3
          r = p
          g = q
          # //b = 255;
      elif i == 4
          r = t
          g = p
          # //b = 255;
      else
          # //r = 255;
          g = p
          b = q
      end
      self.r = r
      self.g = g
      self.b = b
    end
  end

end
return light_state

#-

var tasmota = compile("tasmota.be","file")()()
var light_state = compile("light_state.be","file")()

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

-#
