import utils
import colorsys
import copy
import math

from json import encoder


def float_rep(o):
    o = round(o, 3)
    return str(o)

encoder.FLOAT_REPR = float_rep



# path for the base nuke effect
# base_path = "/pa/units/land/nuke_launcher/nuke_launcher_ammo_explosion.pfx"

out_path = "pa/units/land/nuke_launcher/nuke_launcher_ammo_explosion.pfx"
# out_path = "pa/effects/specs/ping.pfx"

# this is the base nuke effect, it comes from the game
# base_nuke = utils.load_base_json(base_path)
base_nuke = {"emitters": []}
# base_nuke = utils.load_local_json("hit.json")


############################################### configuration
# initial light, smoke wave
import make_init

# raising orb of light and the heart shape
import make_orb

############################################### util functions

#######################################################################################


#####################################################################################################
def make_effect():
    base_effects = base_nuke['emitters']
    # call other effects here
    def add(effects):
        index_offset = len(base_effects)
        for effect in effects:
            if 'linkIndex' in effect:
                effect['linkIndex'] = effect['linkIndex'] + index_offset
            base_effects.append(effect)

    add(make_init.make(0))
    add(make_orb.make(0))

    return 0



make_effect()


# output the effect
# compressed
utils.save_local_json(base_nuke, out_path)
# not compressed
# utils.save_local_json(base_nuke, out_path, 3)