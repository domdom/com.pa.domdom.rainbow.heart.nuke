import utils
import colorsys
import copy
import math
import random

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

## produces a 2d array of the geometric shape of a heart
# radius - radius of the round bit on top of a heart
# ds - the resolution of the beam particle in world space coordinates (remember beam particles can only do straight lines, 
#      which mean round bits need to be approximated)
def make_heart(radius, ds):
    b = radius
    a = b * 0.97
    t = 0
    # First we must compute the angles of the round bits on the heart
    y0 = math.sqrt(b**2 - (- a)**2)
    x0 = -a
    y1 = math.sin(-math.pi / 4) * b
    x1 = math.cos(-math.pi / 4) * b
    # start and end angle
    a0 = math.atan2(y1, x1)
    a1 = math.atan2(y0, x0)
    a3 = math.atan2(y0, -x0)
    # get angle in radians
    angle = a1 - a0
    s = angle * b * 2 + (a + 2 * b * math.sin(math.pi / 4)) * math.sqrt(2) * 2
    x = []
    y = []
    t = 0
    # bottom right straight part
    y.append([t, -(a + 2 * b * math.sin(math.pi / 4))])
    x.append([t, 0])
    t = (a + 2 * b * math.sin(math.pi / 4)) * math.sqrt(2) / s
    # right curvy bit
    num_points = int(math.floor(float(angle * b) / ds))
    for i in xrange(num_points):
        ang = float(i) / num_points * angle + a0
        vx = b * math.cos(ang) + a
        vy = b * math.sin(ang)
        x.append([b * (ang - a0)/ s + t, vx])
        y.append([b * (ang - a0)/ s + t, vy])
    # we are half way now
    t = 0.5
    # add middle concave point
    x.append([t, 0])
    y.append([t, y0])
    # left curvy bit
    for i in xrange(num_points):
        ang = float(i) / num_points * angle + a3
        vx = b * math.cos(ang) - a
        vy = b * math.sin(ang)
        x.append([b * (ang - a3)/ s + t, vx])
        y.append([b * (ang - a3)/ s + t, vy])

    # bottom left straight part
    y.append([1, -(a + 2 * b * math.sin(math.pi / 4))])
    x.append([1, 0])
    return (x, y, len(x))

effect_root = {
    "label": "Effect root",
    "spec": {
        "shader": "particle_add",
        "alpha": [[0, 1 ], [0.25, 1 ], [0.5, 1 ], [0.7, 1 ], [0.8, 0.1 ], [0.9, 0.01 ], [0.992, 0.0 ]]
    },
    "delay": 1,
    "offsetZ": 7.5,
    "velocityZ": 1,
    "velocity": 15,
    "drag": 0.998,
    "sizeX": 1.5,
    "lifetime": 15,
    "emissionBursts": 1,
    "bLoop": False,
    "endDistance": -1
}


base_orb = {
    "spec": {
        "shader": "particle_clip",
        "size": [[0, 0 ], [0.1, 0.5 ], [0.3, 0.75 ], [1, 1.0 ] ],
        "red": [[0.0, 1.0 ], [0.25, 0.8 ] ],
        "green": [[0.0, 1.0 ], [0.25, 0.8 ] ],
        "blue": [[0.0, 1.0 ], [0.25, 0.8 ] ], 
        "alpha": [[0.0, 1.0 ], [0.2, 0.25 ], [0.35, 0.15 ], [1.0, 0.0 ] ],
        "cameraPush": 0.5,
        "baseTexture": "/pa/effects/textures/particles/fire_puff.papa",
        "dataChannelFormat": "PositionAndColor"
    },
    "alpha": [[0, 1], [13, 1], [15, 0]],
    "type": "EMITTER",
    "red" : 1,
    "green": 1,
    "blue" : 10,
    "sizeX": 30,
    "sizeRangeX": 10,
    "emissionRate": 5,
    "rotationRange": 6.28,
    "lifetime": 0.8,
    "lifetimeRange": 0.15,
    "emitterLifetime": 15,
    "bLoop": True,
    "endDistance": -1
}
base_lines = {
    "spec": {
        "shader": "particle_add_ramp",
        "facing": "velocity",
        "sizeX": [[0, 1 ], [0.15, 1 ] ],
        "sizeY": [[0, 25 ], [0.15, 1.5 ] ],
        "red": [[0.1, 4.0 ], [0.2, 1 ] ],
        "green": [[0.1, 4.0 ], [0.2, 1 ] ],
        "blue": [[0.1, 4.0 ], [0.2, 1 ] ],
        "alpha": [[0, 1 ], [1, 0 ] ],
        "cameraPush": 1,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/flicker_ramp.papa"
    },
    "type": "EMITTER",
    "offsetRangeX": 20,
    "offsetRangeY": 20,
    "offsetRangeZ": 20,
    "velocity": 120,
    "velocityRangeX": 1,
    "velocityRangeZ": 1,
    "velocityRangeY": 1,
    "velocityRange": 50,
    "gravity": -9.8,
    "drag": [[0, 0.89 ], [0.5, 0.98 ] ],
    "sizeX": 0.5,
    "sizeRangeX": 0.3,
    "emissionRate": 65,
    "rampV": 0.5,
    "rampRangeV": 0.5,
    "lifetime": 1.5,
    "lifetimeRange": 1.0,
    "emitterLifetime": 1,
    "bLoop": True,
    "endDistance": 1000,
    "sort": "NoSort"
}
base_sparks = {
    "spec": {
        "shader": "particle_transparent",
        "facing": "velocity",
        "flipBookColumns": 4,
        "flipBookRows": 1,
        "frameCurve": [[0, 0 ], [1, 0.75 ] ],
        "flipBookRandomStart": True,
        "polyAdjustCenter": 0.5,
        "sizeX": [[0, 1 ], [1, 1.2 ] ],
        "sizeY": [[0, -1 ], [1, -1.02 ] ],
        "red": 1,
        "green": 1,
        "blue": 10,
        "alpha": [[0.5, 1.0 ], [1, 0.0 ] ],
        "baseTexture": "/pa/effects/textures/particles/metalControlCoreSpark.papa"
    },
    "type": "EMITTER",
    "offsetRangeX": 5,
    "offsetRangeY": 5,
    "offsetRangeZ": 5,
    "velocity": 0.1,
    "velocityRangeX": 1,
    "velocityRangeZ": 1,
    "velocityRangeY": 1,
    "sizeX": 3,
    "sizeRangeX": 1,
    "sizeY": 15,
    "sizeRangeY": 10,
    "lifetime": 0.4,
    "lifetimeRange": 0.125,
    "emissionRate": [[0, 50], [13, 50], [15, 0]],
    "emitterLifetime": 15,
    "bLoop": True,
    "endDistance": 1000
}

# create beam particle to be our 'field' of data points
base_beam = {
    "spec": {
        "shader": "particle_transparent",
        "shape": "beam",
        "sizeX": 1.0,
        "alpha": 0,
        "baseTexture": "/pa/effects/textures/particles/flat.papa"
    },
    "lifetime": 10,
    "emitterLifetime": 10,
    "maxParticles": 0,
    # "sizeX": [[0, 1],[1, 0]],
    "emissionBursts": 1,
    "bLoop": False,
    "endDistance": -1,
    "delay": 2
}

base_heart_particles = {
    "spec": {
        "shader": "particle_add",
        "sizeX": 0.8,
        "alpha": [[0, 0 ], [0.2, 1], [1, 0 ] ],
        "cameraPush": 10,
        "dataChannelFormat": "PositionAndColor",
        "baseTexture": "/pa/effects/textures/particles/softdot.papa"
    },
    "lifetime": 0.4,
    "lifetimeRange": 0.1,
    "type": "EMITTER",
    "offsetRangeX" : 0.0,
    "offsetRangeY" : 0.0,
    "offsetRangeZ" : 0.0,
    "velocityRangeX": 1,
    "velocityRangeY": 1,
    "velocityRangeZ": 1,
    "velocity": 0,
    "gravity" : -9.8,
    "emissionRate": 10,
    "maxParticles": 40000,
    "emitterLifetime": 1,
    "endDistance": 2000,
    "useWorldSpace": True,
    "bLoop": True
}

"""effect_root = {
    "label": "Effect root",
    "spec": {
        "shader": "particle_add",
        "alpha": [[0, 1 ], [0.25, 1 ], [0.5, 1 ], [0.7, 1 ], [0.8, 0.1 ], [0.9, 0.01 ], [0.992, 0.0 ]]
    },
    "delay": 1,
    "offsetZ": 7.5,
    "velocityZ": 1,
    "velocity": 15,
    "drag": 0.998,
    "sizeX": 1.5,
    "lifetime": 15.2,
    "emissionBursts": 1,
    "bLoop": False,
    "endDistance": -1
}"""

base_light = {
      "spec": {
        "shape": "pointlight",
        "size": [[0.1, 1 ], [0.5, 0.75 ] ],
        "red": [[0, 0.2 ], [0.75, 0.2 ] ],
        "green": [[0, 1 ], [0.75, 1 ] ],
        "blue": [[0, 1 ], [0.75, 1 ] ],
        "alpha": [[0.1, 5 ], [0.75, 1 ], [0.85, 0.1 ], [1, 0 ] ]
      },
      "type": "EMITTER",
      "offsetZ": 200,
      "sizeX": 200,
      "emissionBursts": 1,
      "lifetime": 13,
      "emitterLifetime": 1.5,
      "bLoop": False,
      "endDistance": -1
    }

sparks_field = {
    "spec": {
        "shader": "particle_transparent",
        "facing": "velocity",
        "flipBookColumns": 4,
        "flipBookRows": 1,
        "frameCurve": [[0, 0 ], [1, 0.75 ] ],
        "flipBookRandomStart": True,
        "polyAdjustCenter": 0.5,
        "sizeX": [[0, 1 ], [1, 1.2 ] ],
        "sizeY": [[0, -1 ], [1, -1.02 ] ],
        "red": 1,
        "green": 1,
        "blue": 10,
        "alpha": [[0.5, 1.0 ], [1, 0.0 ] ],
        "baseTexture": "/pa/effects/textures/particles/metalControlCoreSpark.papa"
    },
    "type": "CYLINDER_Z",
    "offsetRangeX": [[0.0, 0.0 ], [1, 50], [10, 60]],
    "offsetRangeY": [[0.0, 0.0 ], [1, 50], [10, 60]],
    "offsetRangeZ": 1,
    "velocity": 0.1,
    "velocityRangeX": 1,
    "velocityRangeZ": 1,
    "velocityRangeY": 1,
    "sizeX": 3,
    "sizeRangeX": 1,
    "sizeY": 10,
    "sizeRangeY": 5,
    "lifetime": 0.4,
    "lifetimeRange": 0.125,
    "emissionRate": [[0, 20], [13, 100], [15, 0]],
    "emitterLifetime": 10,
    "bLoop": False,
    "endDistance": 1000
}

line_implosion = {
    "spec": {
        "shader": "particle_add_ramp",
        "facing": "velocity",
        "sizeX": [[0, 1 ], [0.15, 1 ] ],
        "sizeY": [[0, 25 ], [0.15, 1.5 ] ],
        "red": [[0.1, 4.0 ], [0.2, 1 ] ],
        "green": [[0.1, 4.0 ], [0.2, 1 ] ],
        "blue": [[0.1, 4.0 ], [0.2, 1 ] ],
        "alpha": [[0, 1 ], [1, 0 ] ],
        "cameraPush": 1,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/flicker_ramp.papa"
    },
    "useArcLengthSpace": True,
    "type": "CYLINDER_Z",
    "offsetRangeX": 100,
    "offsetRangeY": 100,
    "offsetRangeZ": 10,
    "useRadialVelocityDir": True,
    "velocity": -200,
    "velocityRange": 50,
    "gravity": -9.8,
    "drag": [[0, 0.89 ], [0.5, 0.98 ] ],
    "sizeX": 0.5,
    "sizeRangeX": 0.3,
    "emissionRate": 165,
    "rampV": 0.5,
    "rampRangeV": 0.5,
    "lifetime": 1.5,
    "lifetimeRange": 1.0,
    "emitterLifetime": 1,
    "bLoop": False,
    "endDistance": 1000,
    "sort": "NoSort"
}

def make(delay):
    global base_orb
    global base_lines
    global base_sparks
    global base_light

    effects = []
    ## making the heart shape
    # for each size
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    # delay for this animation
    delay = 1

    # size of heart
    outer_size = 15.0

    # each heart will rotate 
    num_rots = 1.0
    num_rot_frames = int(num_rots * 15)
    # rotation time in seconds
    rot_time = 15.0

    heart_height = 7.5
    heart_vel_up = 15.0

    ds = 2.5

    brightness_scale = 40
    rot_time = 15.0

    num_frames = int(1 * rot_time)

    num_layers = 8

    for j in xrange(1, num_layers):

        shape_frames = []

        xy_offset = float(j) * 2 * outer_size / num_layers - outer_size

        size = math.sqrt(outer_size ** 2 - xy_offset ** 2)

        r, z, points = make_heart(size, ds)

        heart_vel_up = 15.0
        height = heart_height


        for i in xrange(num_frames):
            shape_emitter = copy.deepcopy(base_beam)

            t = float(i) / num_frames * rot_time
            dt = 1.0 / num_frames * rot_time
            drag = 0.90

            heart_vel_up *= drag

            height += heart_vel_up * dt

            shape_emitter['maxParticles'] = points

            xy_offset

            cos = math.cos(math.pi * 2 * i / float(num_frames))
            sin = math.sin(math.pi * 2 * i / float(num_frames))


            # rotate heart shape
            x1 = [[a[0], a[1] * cos + xy_offset * sin] for a in r]
            y1 = [[a[0], a[1] * sin - xy_offset * cos] for a in r]
            # vertically displace heart shape
            z1 = [[a[0], a[1] + height] for a in z]

            shape_emitter['offsetX'] = x1
            shape_emitter['offsetY'] = y1
            shape_emitter['offsetZ'] = z1

            shape_emitter['spec']['alpha'] = 0
            # shape_emitter['red'], shape_emitter['green'], shape_emitter['blue'] = rainbow(20, float(i) / num_layers, brightness_scale, 1, 1)
            # shape_emitter['spec']['red'], shape_emitter['spec']['green'], shape_emitter['spec']['blue'] = rainbow(20, float(i) / num_frames, 1, 1 / float(num_frames) / 3, 1)

            shape_emitter['delay'] = delay + t

            shape_emitter['lifetime'] = rot_time / num_frames
            shape_emitter['emitterLifetime'] = rot_time / num_frames

            # add this emitter shape to the emitter
            effects.append(shape_emitter)
            shape_frames.append(shape_emitter)

            # get index of shape emitter
            idx = len(effects) - 1

            particles = copy.deepcopy(base_heart_particles)

            particles['red'], particles['green'], particles['blue'] = rainbow(20, float(j) / num_layers + float(i) / num_frames, brightness_scale, 1, 1)
            # particles['red'], particles['green'], particles['blue'] = rainbow(20, float(i) / num_frames, brightness_scale, 1, 1)
            # particles['spec']['red'], particles['spec']['green'], particles['spec']['blue'] = rainbow(20, float(i) / num_layers, brightness_scale, 1, 1)

            particles['linkIndex'] = idx

            effects.append(particles)


        # do frame interpolation
        # duplicate first frame
        # shape_frames.insert(0, copy.deepcopy(shape_frames[0]))

        # #################################### add this pre-frame
        # effects.append(shape_frames[0])
        # # get index of shape emitter
        # idx = len(effects) - 1
        # particles = copy.deepcopy(base_heart_particles)
        # # particles['red'], particles['green'], particles['blue'] = rainbow(20, float(j) / num_layers + float(i) / num_frames, brightness_scale, 1, 1)
        # particles['red'], particles['green'], particles['blue'] = rainbow(20, 0, brightness_scale)
        # # particles['spec']['red'], particles['spec']['green'], particles['spec']['blue'] = rainbow(20, float(i) / num_layers, brightness_scale, 1, 1)
        # particles['linkIndex'] = idx
        # effects.append(particles)

        # shape_frames[0]['delay'] = delay - 1
        # # randomise the points of first frame
        # for i in xrange(len(shape_frames[0]['offsetX'])):
        #     x = math.sin(float(random.randint(0, points-1)) / points * 2 * math.pi) * outer_size * 8 * random.random()
        #     y = math.cos(float(random.randint(0, points-1)) / points * 2 * math.pi) * outer_size * 8 * random.random()
        #     z = 0

        #     shape_frames[0]['offsetX'][i][1] = x
        #     shape_frames[0]['offsetY'][i][1] = y
        #     shape_frames[0]['offsetZ'][i][1] = z

        for i in xrange(len(shape_frames) - 1):
            dt = 1.0 / num_frames * rot_time
            # if i == 0:
                # dt = 1
            cf = shape_frames[i]
            nf = shape_frames[i + 1]

            cf['velocityX'] = []
            cf['velocityY'] = []
            cf['velocityZ'] = []
            cf['velocity'] = []

            for k in xrange(len(cf['offsetX'])):
                t = cf['offsetX'][k][0]

                dx = nf['offsetX'][k][1] - cf['offsetX'][k][1]
                dy = nf['offsetY'][k][1] - cf['offsetY'][k][1]
                dz = nf['offsetZ'][k][1] - cf['offsetZ'][k][1]

                v = math.sqrt(dx * dx + dy * dy + dz * dz) / dt

                cf['velocityX'].append([t, dx])
                cf['velocityY'].append([t, dy])
                cf['velocityZ'].append([t, dz])
                cf['velocity'].append([t, v])

            nf['velocityX'] = cf['velocityX']
            nf['velocityY'] = cf['velocityY']
            nf['velocityZ'] = cf['velocityZ']
            nf['velocity'] = cf['velocity']
    ################### orb effects go last, to simplify index calculations
    effects.append(effect_root)

    idx = len(effects) - 1

    base_orb['linkIndex'] = idx
    base_sparks['linkIndex'] = idx
    base_lines['linkIndex'] = idx
    base_light['linkIndex'] = idx

    # there are two orbs
    # make the orb here
    base_orb['emissionRate'] = 3
    base_orb['delay'] = delay
    # def rainbow(n, offset=0, scale=1, revs=1, time=1):
    base_orb['red'], base_orb['green'], base_orb['blue'] = rainbow(40, 0, 10, 1, base_orb['emitterLifetime'])
    effects.append(base_orb)

    base_light['red'], base_light['green'], base_light['blue'] = rainbow(40, 0, 10, 1, base_orb['emitterLifetime'])

    base_orb = copy.deepcopy(base_orb)
    base_orb['delay'] = delay + 0.5 / base_orb['emissionRate']
    # base_orb['emitterLifetime'] = 3
    base_orb['red'], base_orb['green'], base_orb['blue'] = rainbow(40, 0.6, 8, 1, base_orb['emitterLifetime'])

    effects.append(base_orb)

    line_implosion['delay'] = 0

    line_implosion['red'], line_implosion['green'], line_implosion['blue'] = rainbow(40, 0, 10, 1, line_implosion['emitterLifetime'])
    base_lines['red'], base_lines['green'], base_lines['blue'] = rainbow(40, 0, 10, 1, base_lines['emitterLifetime'])

    base_sparks['delay'] = delay
    base_lines['delay'] = delay
    base_light['delay'] = delay

    sparks_field['delay'] = delay

    effects.append(sparks_field)

    effects.append(line_implosion)
    effects.append(base_light)
    # sparks and lines
    effects.append(base_sparks)
    effects.append(base_lines)

    return effects