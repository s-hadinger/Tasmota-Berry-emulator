import tasmota
def log(m,l) tasmota.log(m,l) end
import animation
import animation_dsl
import user_functions

# Test with very simple DSL code
var simple_dsl = 

# "set strip_len = strip_length()\n"
# "set lin = LINEAR\n"
# "set lin2 = 1 + LINEAR\n"


"template animation cylon_eye {"
  "param eye_color type color default red\n"
  "param back_color type color default transparent\n"
  "param duration min 0 max 1h default 10s\n"
"}\n"

"\n"

# "template animation shutter_central {\n"
#   "param colors type palette\n"
#   # "param duration type time\n"
#   "param duration type time min 0 max 3600 default 5 nillable true\n"
  
#   "set strip_len = strip_length()\n"
#   "set shutter_size = sawtooth(min_value = 0, max_value = strip_len, duration = duration)"

#   "animation shutter_seq = beacon_animation(\n"
#   ")\n"

#   "run shutter_seq\n"
# "}\n"
# "animation my_shutter = shutter_central(duration=2)\n"
# "run my_shutter"

# "set t_ms = 3ms\n"
# "set t_s = 5s\n"
# "set t_m = 10m\n"
# "set t_h = 1h\n"
# "set t_opa = 90%\n"

# "set r1 = rand_demo()\n"
# "set r2 = rand_demo(12)\n"
# "set r3 = rand_demo(4 + 5)\n"
# "set r4 = rand_demo(strip_len)\n"
# "set r5 = rand_demo(strip_len + 1)\n"
# "set r6 = rand_demo(strip_len.is_running)\n"

# "set az = abs(strip_len / 4)\n"
# "set az2 = strip_len.is_running\n"
# "set az3 = strip_len\n"
# "set x = 3s\n"
# "set xy = strip_length()\n"
# "set xx = (0 + 3*4)\n"

# "color space_blue = 0xFF000066\n"
# "animation a = solid(color=0x112233)\n"
# "a.color = space_blue\n"

# "set xshutter = 3s\n"
# "set shutter_size = sawtooth(min_value = strip_len, max_value = strip_len / 2 + 1, duration = xshutter)\n"
# "shutter_size.min_value = rand_demo()\n"
# "shutter_size.max_value = strip_len\n"
# "shutter_size.max_value = strip_length()\n"
# "shutter_size.min_value = strip_len / 2\n"
# "animation test = pulsating_animation(color=0xFF0000FF, min_brightness=(0+1))\n"


# "palette col1 = [red, orange, yellow, green, blue, indigo, white]\n"


# "set zz = strip_len - 2\n"
# #Fails
# # "set s2 = strip_length() + strip_length()\n"
# "set z1 = x\n" +
# "set m1 = x + 1\n"
# "set m2 = 1 + x\n"
# "sequence tt {\n"
# "restart shutter_size\n"
# "}\n"
# "set z2 = x + x\n"
# "set z3 = sawtooth()\n"
# "set z4 = linear(min_value=10, max_value=20)\n"
# "set y = x + 4\n"


# "sequence seq1 repeat forever {\n"
#   "repeat col1.palette_size times {\n"
#       'log("begin 1")\n'
#       "restart shutter_size\n"
#       "col1.next = 1\n"
#     "}\n"
#     "}\n"

# "sequence seq2 repeat forever {\n"
#   "repeat col1.palette_size + 1 times {\n"
#       'log("begin 1")\n'
#       "restart shutter_size\n"
#       "col1.next = 1\n"
#     "}\n"
#     "}\n"

# "sequence seq3 repeat forever {\n"
#   "repeat 7 times {\n"
#       'log("begin 1")\n'
#       "restart shutter_size\n"
#       "col1.next = 1\n"
#     "}\n"
#     "}\n"

# "sequence seq4 repeat forever {\n"
#   "repeat 7 + 2 times {\n"
#       'log("begin 1")\n'
#       "restart shutter_size\n"
#       "col1.next = 1\n"
#     "}\n"
#     "}\n"

# "sequence seq5 repeat forever {\n"
#   "repeat strip_len times {\n"
#       'log("begin 1")\n'
#       "restart shutter_size\n"
#       "col1.next = 1\n"
#     "}\n"
#     "}\n"

# FAILS
# "animation test_anim = solid(color=red)\n"
# "test_anim.opacity = strip_length() / 2\n"

# "\n"
# "palette fire_color = [ 0x800000, 0xFF0000, 0xFF4500, 0xFFFF00 ]\n"
# "set eye_pos = cosine_osc(min_value = -1, max_value = strip_len - 2, duration = 6s)\n"
# "animation eye_mask = beacon_animation(color = white, back_color = transparent, pos = eye_pos, beacon_size = 4, slew_size = 2, priority = 5)\n"

# "animation fire_pattern = palette_gradient_animation(\n"
# "  color_source = fire_color\n"
# "  spatial_period = strip_len / 4\n"
# "  opacity = eye_mask\n"
# ")\n"
# "run fire_pattern\n"

# "template templ {\n"
# "  param duration\n"
# "  param duration_not_used\n"
# "  set x = duration\n"
# "}\n"

# "palette pal_x = [red, orange, yellow, green, blue, indigo, white]\n"
# "set duration_x = 3s\n"
# "set duration_dyn = sawtooth(min_value = strip_len, max_value = strip_len / 2 + 1, duration = duration_x)\n"
# "color col_x = color_cycle(palette=pal_x, cycle_period=0)\n"
# "animation shutter_x = beacon_animation()\n"
# "sequence shutter_seq repeat forever {\n"
# "  repeat col_x.palette_size times {\n"
# # "  repeat duration_dyn times {\n"
# "  restart shutter_x\n"
# "  play shutter_x for duration_x\n"
# "  col_x.next = 1\n"
# "  }\n"
# "}\n"

def compile2(source)
  var lexer = animation_dsl.create_lexer(source)
  var transpiler = animation_dsl.SimpleDSLTranspiler(lexer)
  var berry_code = transpiler.transpile()
  print(transpiler.get_symbol_table_report())
  
  return berry_code
end

try
  var result = compile2(simple_dsl)
  print("Success!")
  print("Generated code:")
  print(result)
except .. as e, msg
  print("Error:", e)
  print("Message:", msg)
  import debug
  debug.traceback()
end