import utils
import colorsys
import copy
import math
import json

from json import encoder


def float_rep(o):
    o = round(o, 3)
    return str(o)

encoder.FLOAT_REPR = float_rep



# path for the base nuke effect
# base_path = "/pa/units/land/nuke_launcher/nuke_launcher_ammo_explosion.pfx"

trail_out_path = "pa/units/air/missile_nuke/missile_nuke_trail.pfx"
nuke_out_path = "pa/units/land/nuke_launcher/nuke_launcher_ammo_explosion.pfx"
# nuke_out_path = "pa/effects/specs/ping.pfx"

# this is the base nuke effect, it comes from the game
# base_nuke = utils.load_base_json(base_path)
base_nuke = {"emitters": []}
# base_nuke = utils.load_local_json("hit.json")


base_trail = utils.load_base_json(trail_out_path)



############################################### configuration
# initial light, smoke wave
import make_init

# raising orb of light and the heart shape
import make_orb

############################################### util functions
# produces arrays of color (like a rainbow! xD)
def rainbow(n, offset=0, scale=1, revs=1, time=1):
    r = []
    g = []
    b = []
    for i in xrange(n + 1):
        t = offset + (float(i) / n) * revs
        rgb = colorsys.hsv_to_rgb(t % 1, 1, 1)
        r.append([float(i) / n * time, scale * rgb[0]])
        g.append([float(i) / n * time, scale * rgb[1]])
        b.append([float(i) / n * time, scale * rgb[2]])
    return (r, g, b)
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

    base_trail['emitters'][1]['red'], base_trail['emitters'][1]['green'], base_trail['emitters'][1]['blue'] = rainbow(40, 0, 1)

    return 0



make_effect()


# output the effect
# compressed
utils.save_local_json(base_nuke, nuke_out_path)
utils.save_local_json(base_trail, trail_out_path)
# not compressed
# utils.save_local_json(base_nuke, nuke_out_path, 3)