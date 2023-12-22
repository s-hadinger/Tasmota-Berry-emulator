# Leds_frame
import Leds     # solve import

class Leds_frame : bytes
  var pixel_size

  def init(pixels)
    if (pixels < 0)   pixels = -pixels  end
    self.pixel_size = pixels
    super(self).init(pixels * (-4))
  end

  def item(i)
    return self.get(i * 4, 4)
  end

  def setitem(i, v)
    self.set(i * 4, v, 4)
  end

  def set_pixel(i, r, g, b, alpha)
    if (alpha == nil)   alpha = 0   end
    var color = ((alpha & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)
    self.setitem(i, color)
  end

  def fill_pixels(color)
    var pixels_count = self.size() / 4
    var idx = 0
    while idx < pixels_count
      self.set(idx * 4, color, 4)
      idx += 1
    end
  end

  static def blend(color_a, color_b, alpha)
    var r = (color_a >> 16) & 0xFF
    var g = (color_a >>  8) & 0xFF
    var b = (color_a      ) & 0xFF
    var r2 = (color_b >> 16) & 0xFF
    var g2 = (color_b >>  8) & 0xFF
    var b2 = (color_b      ) & 0xFF
    var r3 = tasmota.scale_uint(alpha, 0, 255, r2, r)
    var g3 = tasmota.scale_uint(alpha, 0, 255, g2, g)
    var b3 = tasmota.scale_uint(alpha, 0, 255, b2, b)
    var rgb = (r3 << 16) | (g3 << 8) | b3
    return rgb
  end

  def paste_pixels(dest_buf, bri, gamma)
    if (bri == nil)     bri = 255       end
    if (gamma == nil)   gamma = false   end
    var pixels_count = self.size() / 4
    if (pixels_count > size(dest_buf) / 3)    pixels_count = size(dest_buf) / 3   end
    if (pixels_count > 0)
      var i = 0
      while i < pixels_count
        var src_argb = Leds.apply_bri_gamma(self.get(i * 4, 4), bri, gamma)
        var src_r = (src_argb >> 16) & 0xFF
        var src_g = (src_argb >>  8) & 0xFF
        var src_b = (src_argb      ) & 0xFF
        dest_buf[i * 3 + 0] = src_g
        dest_buf[i * 3 + 1] = src_r
        dest_buf[i * 3 + 2] = src_b
        i += 1
      end
    end
  end

  def blend_pixels(fore)
    var back = self
    var dest = self
    var dest_len = size(dest)
    if (size(fore) < dest_len)    dest_len = size(fore)     end
    if (size(back) < dest_len)    dest_len = size(back)     end
    var pixels_count = dest_len / 4

    if (pixels_count > 0)
      var i = 0
      while i < pixels_count
        var back_argb = back.get(i * 4, 4)
        var fore_argb = fore.get(i * 4, 4)
        var fore_alpha = (fore_argb >> 24) & 0xFF
        var dest_rgb_new = back_argb

        if (fore_alpha == 0)          # {        // opaque layer, copy value from fore
          dest_rgb_new = fore_argb
        elif (fore_alpha == 255)      # {   // fore is transparent, use back
          # // nothing to do, dest_rgb_new = back_argb above
        else
          var back_r = (back_argb >> 16) & 0xFF
          var fore_r = (fore_argb >> 16) & 0xFF
          var back_g = (back_argb >>  8) & 0xFF
          var fore_g = (fore_argb >>  8) & 0xFF
          var back_b = (back_argb      ) & 0xFF
          var fore_b = (fore_argb      ) & 0xFF
          var dest_r_new = tasmota.scale_uint(fore_alpha, 0, 255, fore_r, back_r)
          var dest_g_new = tasmota.scale_uint(fore_alpha, 0, 255, fore_g, back_g)
          var dest_b_new = tasmota.scale_uint(fore_alpha, 0, 255, fore_b, back_b)
          dest_rgb_new = (dest_r_new << 16) | (dest_g_new << 8) | dest_b_new
        end
        dest.set(i * 4, dest_rgb_new, 4)
        i += 1
      end
    end
  end

end

return Leds_frame

# /* @const_object_info_begin
# class be_class_Leds_frame (scope: global, name: Leds_frame, super:be_class_bytes, strings: weak) {
#   pixel_size, var

#   init, closure(Leds_frame_be_init_closure)

#   item, closure(Leds_frame_be_item_closure)
#   setitem, closure(Leds_frame_be_setitem_closure)
#   set_pixel, closure(Leds_frame_be_set_pixel_closure)

#   // the following are on buffers
#   blend, static_func(be_leds_blend)
#   fill_pixels, func(be_leds_fill_pixels)
#   blend_pixels, func(be_leds_blend_pixels)
#   paste_pixels, func(be_leds_paste_pixels)
# }