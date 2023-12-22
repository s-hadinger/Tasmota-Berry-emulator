# mimick module `animate`

animate = module("animate")

# for solidification

load("tasmota_env/animate_0.be")
load("tasmota_env/animate_1_core.be")
load("tasmota_env/animate_2_animate_effects.be")
load("tasmota_env/animate_9_module.be")

animate.core = global.Animate_core    # make it available as `animate()`
animate.pulse = global.Animate_pulse

import Leds_frame
animate.frame = Leds_frame

# Palettes
# animate.palette.ptr_to_palette(animate.PALETTE_RAINBOW_WHITE).tostring(200)
animate.PALETTE_RAINBOW_WHITE = bytes('50FF000030FF000050FFA50030FFA50050FFFF0030FFFF005000FF003000FF00500000FF300000FF50FF00FF30FF00FF50FFFFFF30FFFFFF00FF0000')
animate.PALETTE_STANDARD_TAG = bytes('40FF000040FFA50040FFFF004000FF00400000FF40FF00FF40EE44A500FF0000')
animate.PALETTE_STANDARD_VAL = bytes('00FF00002AFFA50055FFFF007F00FF00AA0000FFD4FF00FFFFFF0000')
animate.PALETTE_SATURATED_TAG = bytes('40FF000040FFA50040FFFF004000FF00400000FF40FF00FF00FF0000')
animate.PALETTE_ib_44 = bytes('00D6181040E3734EFFEFCE8C')
animate.PALETTE_Fire_1 = bytes('00FF000080FF8000FFFFFF00')
animate.PALETTE_bhw1_sunconure = bytes('0061F04EA1F6891EFFF62D1E')
animate.PALETTE_bhw4_089 = bytes('00AE341C1CE09A8535EBD0CE4FF9D0766DE45F3284E3A574A3E28343B8FCD576C9FCA97DE0FFC265FFD75023')

return animate
