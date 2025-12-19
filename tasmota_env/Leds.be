# Leds


class Leds
  static var WS2812_GRB = 1
  static var SK6812_GRBW = 2

  var gamma       # if true, apply gamma (true is default)
  var leds        # number of leds
  var bri         # implicit brightness for this led strip (0..255, default is 50% = 127)

  var _buf
  var _typ
  # leds:int = number of leds of the strip
  # gpio:int (optional) = GPIO for NeoPixel. If not specified, takes the WS2812 gpio
  # typ:int (optional) = Type of LED, defaults to WS2812 RGB
  # rmt:int (optional) = RMT hardware channel to use, leave default unless you have a good reason 
  def init(leds, gpio_phy, typ, rmt)   # rmt is optional
    self.gamma = false    # force no gamma for __JS__
    
    # In browser mode, get strip size from JavaScript if not explicitly provided
    if leds == nil && global.contains('__JS__')
      import js
      var js_size = int(js.get_strip_size())
      if js_size > 0
        leds = js_size
      end
    end
    
    self.leds = (leds != nil) ? int(leds) : 30
    self.bri = 255        # force 255 for __JS__

    # fake buffer
    self._buf = bytes(self.leds).resize(self.leds * 3)
    self._typ = typ
    # if no GPIO, abort
    # if gpio_phy == nil
    #   raise "valuer_error", "no GPIO specified for neopixelbus"
    # end

    # initialize the structure
    self.ctor(self.leds, gpio_phy, typ, rmt)

    # if self._p == nil raise "internal_error", "couldn't not initialize noepixelbus" end

    # call begin
    self.begin()

    # emulator-specific
    global._strip = self    # record the current strip object

  end

  # set bri (0..255)
  # set bri (0..511)
  def set_bri(bri)
    if (bri < 0)    bri = 0   end
    if (bri > 511)  bri = 511 end
    self.bri = bri
  end
  def get_bri()
    # If running in browser, get brightness from JavaScript UI
    # JavaScript brightness is 0-200 where 100 = normal (255 in Berry)
    # We scale: 0 -> 0, 100 -> 255, 200 -> 510 (allows overexpose)
    # Note: we map to 0-510 (not 0-511) so that 100 maps exactly to 255
    if global.contains('__JS__')
      import js
      var js_bri = int(js.get_brightness())
      # Scale: js_bri 0-200 maps to 0-510 so that 100 -> 255 exactly
      return tasmota.scale_uint(js_bri, 0, 200, 0, 510)
    end
    return self.bri
  end

  def set_gamma(gamma)
    self.gamma = bool(gamma)
  end
  def get_gamma()
    return self.gamma
  end

  # assign RMT
  static def assign_rmt(gpio_phy)
  end

  def clear()
    self.clear_to(0x000000)
    self.show()
  end

  def ctor(leds, gpio_phy, typ, rmt)
    if typ == nil
      typ = self.WS2812_GRB
    end
    self._typ = typ
    # if rmt == nil
    #   rmt = self.assign_rmt(gpio_phy)
    # end
    # self.call_native(0, leds, gpio_phy, typ, rmt)
  end
  def begin()
  end
  def show()
    # Display frame buffer to JavaScript (browser only)
    # This sends the LED strip pixel data to JavaScript for rendering
    if global.contains('__JS__')
      import js
      js.frame_buffer_display(self._buf.tohex())
    end
  end
  def can_show()
    return true
  end
  def is_dirty()
    return true
  end
  def dirty()
  end

  # push_pixels
  #
  # Pushes a bytes() buffer of 0xAARRGGBB colors, without bri nor gamma correction
  # 
  def push_pixels_buffer_argb(pixels)
    var i = 0
    while i < self.pixel_count()
      self.set_pixel_color(i, pixels.get(i * 4, 4))
      i += 1
    end
  end

  def pixels_buffer(old_buf)
    return self._buf
  end
  def pixel_size()
    return self.call_native(7)
  end
  def pixel_count()
    # If running in browser, get strip size from JavaScript
    if global.contains('__JS__')
      import js
      var js_size = int(js.get_strip_size())
      if js_size > 0
        return js_size
      end
    end
    return self.leds
    # return self.call_native(8)
  end
  def length()
    return self.pixel_count()
  end
  def pixel_offset()
    return 0
  end
  def clear_to(col, bri)
    if (bri == nil)   bri = self.get_bri()    end
    var rgb = self.to_gamma(col, bri)
    var buf = self._buf
    var r = (rgb >> 16) & 0xFF
    var g = (rgb >>  8) & 0xFF
    var b = (rgb      ) & 0xFF
    var i = 0
    while i < self.leds
      buf[i * 3 + 0] = r
      buf[i * 3 + 1] = g
      buf[i * 3 + 2] = b
      i += 1
    end
  end
  def set_pixel_color(idx, col, bri)
    if (bri == nil)   bri = self.get_bri()    end
    var rgb = self.to_gamma(col, bri)
    var buf = self._buf
    var r = (rgb >> 16) & 0xFF
    var g = (rgb >>  8) & 0xFF
    var b = (rgb      ) & 0xFF
    buf[idx * 3 + 0] = r
    buf[idx * 3 + 1] = g
    buf[idx * 3 + 2] = b
    #self.call_native(10, idx, self.to_gamma(col, bri))
  end
  def get_pixel_color(idx)
    var r = self._buf[idx * 3 + 0]
    var g = self._buf[idx * 3 + 1]
    var b = self._buf[idx * 3 + 2]
    return (r << 16) | (g << 8) | b
    # return self.call_native(11, idx)
  end

  # apply gamma and bri
  def to_gamma(rgb, bri255)
    if (bri255 == nil)   bri255 = self.bri    end
    return self.apply_bri_gamma(rgb, bri255, self.gamma)
  end

  # `segment`
  # create a new `strip` object that maps a part of the current strip
  def create_segment(offset, leds)
    if int(offset) + int(leds) > self.leds || offset < 0 || leds < 0
      raise "value_error", "out of range"
    end

    # inner class
    class Leds_segment
      var strip
      var offset, leds
    
      def init(strip, offset, leds)
        self.strip = strip
        self.offset = int(offset)
        self.leds = int(leds)
      end
    
      def clear()
        self.clear_to(0x000000)
        self.show()
      end
    
      def begin()
        # do nothing, already being handled by physical strip
      end
      def show(force)
        # don't trigger on segment, you will need to trigger on full strip instead
        if bool(force) || (self.offset == 0 && self.leds == self.strip.leds)
          self.strip.show()
        end
      end
      def can_show()
        return self.strip.can_show()
      end
      def is_dirty()
        return self.strip.is_dirty()
      end
      def dirty()
        self.strip.dirty()
      end
      def pixels_buffer()
        return nil
      end
      def pixel_size()
        return self.strip.pixel_size()
      end
      def pixel_offset()
        return self.offset
      end
      def pixel_count()
        return self.leds
      end
      def clear_to(col, bri)
        if (bri == nil)   bri = self.bri    end
        self.strip.call_native(9, self.strip.to_gamma(col, bri), self.offset, self.leds)
        # var i = 0
        # while i < self.leds
        #   self.strip.set_pixel_color(i + self.offset, col, bri)
        #   i += 1
        # end
      end
      def set_pixel_color(idx, col, bri)
        if (bri == nil)   bri = self.bri    end
        self.strip.set_pixel_color(idx + self.offset, col, bri)
      end
      def get_pixel_color(idx)
        return self.strip.get_pixel_color(idx + self.offseta)
      end
    end

    return Leds_segment(self, offset, leds)

  end

  def create_matrix(w, h, offset)
    offset = int(offset)
    w = int(w)
    h = int(h)
    if offset == nil   offset = 0 end
    if w * h + offset > self.leds || h < 0 || w < 0 || offset < 0
      raise "value_error", "out of range"
    end

    # inner class
    class Leds_matrix
      var strip
      var offset
      var h, w
      var alternate     # are rows in alternate mode (even/odd are reversed)
      var pix_buffer
      var pix_size
    
      def init(strip, w, h, offset)
        self.strip = strip
        self.offset = offset
        self.h = h
        self.w = w
        self.alternate = false

        self.pix_buffer = self.strip.pixels_buffer()
        self.pix_size = self.strip.pixel_size()
      end
    
      def clear()
        self.clear_to(0x000000)
        self.show()
      end
    
      def begin()
        # do nothing, already being handled by physical strip
      end
      def show(force)
        # don't trigger on segment, you will need to trigger on full strip instead
        if bool(force) || (self.offset == 0 && self.w * self.h == self.strip.leds)
          self.strip.show()
          self.pix_buffer = self.strip.pixels_buffer(self.pix_buffer)  # update buffer after show()
        end
      end
      def can_show()
        return self.strip.can_show()
      end
      def is_dirty()
        return self.strip.is_dirty()
      end
      def dirty()
        self.strip.dirty()
      end
      def pixels_buffer()
        return self.strip.pixels_buffer()
      end
      def pixel_size()
        return self.pix_size
      end
      def pixel_count()
        return self.w * self.h
      end
      def pixel_offset()
        return self.offset
      end
      def clear_to(col, bri)
        if (bri == nil)   bri = self.bri    end
        self.strip.call_native(9, self.strip.to_gamma(col, bri), self.offset, self.w * self.h)
      end
      def set_pixel_color(idx, col, bri)
        if (bri == nil)   bri = self.bri    end
        self.strip.set_pixel_color(idx + self.offset, col, bri)
      end
      def get_pixel_color(idx)
        return self.strip.get_pixel_color(idx + self.offseta)
      end

      # setbytes(row, bytes)
      # sets the raw bytes for `row`, copying at most 3 or 4 x col  bytes
      def set_bytes(row, buf, offset, len)
        var h_bytes = self.h * self.pix_size
        if (len > h_bytes)  len = h_bytes end
        var offset_in_matrix = (self.offset + row) * h_bytes
        self.pix_buffer.setbytes(offset_in_matrix, buf, offset, len)
      end

      # Leds_matrix specific
      def set_alternate(alt)
        self.alternate = alt
      end
      def get_alternate()
        return self.alternate
      end

      def set_matrix_pixel_color(x, y, col, bri)
        if (bri == nil)   bri = self.bri    end
        if self.alternate && x % 2
          # reversed line
          self.strip.set_pixel_color(x * self.w + self.h - y - 1 + self.offset, col, bri)
        else
          self.strip.set_pixel_color(x * self.w + y + self.offset, col, bri)
        end
      end
    end

    return Leds_matrix(self, w, h, offset)

  end

  static def matrix(w, h, gpio, rmt)
    var strip = Leds(w * h, gpio, rmt)
    var matrix = strip.create_matrix(w, h, 0)
    return matrix
  end


  static def blend_color(color_a, color_b, alpha)
    var transparency = (color_b >> 24) & 0xFF
    if (alpha != nil)
      transparency = 255 - alpha
    end
    # remove any transparency
    color_a = color_a & 0xFFFFFF
    color_b = color_b & 0xFFFFFF

    if (transparency == 0) #     // color_b is opaque, return color_b
      return color_b
    end
    if (transparency >= 255) #{  // color_b is transparent, return color_a
      return color_a
    end
    var r = tasmota.scale_uint(transparency, 0, 255, (color_b >> 16) & 0xFF, (color_a >> 16) & 0xFF)
    var g = tasmota.scale_uint(transparency, 0, 255, (color_b >>  8) & 0xFF, (color_a >>  8) & 0xFF)
    var b = tasmota.scale_uint(transparency, 0, 255, (color_b      ) & 0xFF, (color_a      ) & 0xFF)

    var rgb = (r << 16) | (g << 8) | b
    return rgb
  end

  static def apply_bri_gamma(color_a, bri255, gamma)
    if (bri255 == nil)   bri255 = 255       end
    if (bri255 == 0) return 0x000000     end              # if bri is zero, short-cut
    var r = (color_a >> 16) & 0xFF
    var g = (color_a >>  8) & 0xFF
    var b = (color_a      ) & 0xFF

    # Apply brightness scaling
    # bri255 0-255: scale down (0=off, 255=full)
    # bri255 256-510: scale up (overexpose, capped at 255 per channel)
    if (bri255 < 255)
      # Scale down
      r = tasmota.scale_uint(bri255, 0, 255, 0, r)
      g = tasmota.scale_uint(bri255, 0, 255, 0, g)
      b = tasmota.scale_uint(bri255, 0, 255, 0, b)
    elif (bri255 > 255)
      # Scale up (overexpose) - bri255 256-510 maps to 1.0x-2.0x multiplier
      r = tasmota.scale_uint(bri255, 255, 510, r, r * 2)
      g = tasmota.scale_uint(bri255, 255, 510, g, g * 2)
      b = tasmota.scale_uint(bri255, 255, 510, b, b * 2)
      # Cap at 255
      if (r > 255)  r = 255  end
      if (g > 255)  g = 255  end
      if (b > 255)  b = 255  end
    end

    if gamma
      import light_state
      r = light_state.ledGamma8_8(r)
      g = light_state.ledGamma8_8(g)
      b = light_state.ledGamma8_8(b)
    end
    var rgb = (r << 16) | (g << 8) | b
    return rgb
  end

  
end

return Leds
