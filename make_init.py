import utils
import colorsys
import copy
import math

## produces arrays of color (like a rainbow! xD)
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

smoke_puff_upper = {
      "label": "smoke burst",
      "spec": {
        "shader": "particle_transparent_lit",
        "red": [[0.0, 25 ], [0.5, 2.5 ], [1, 0 ] ],
        "green": [[0.0, 10 ], [0.5, 1.0 ], [1, 0 ] ],
        "blue": [[0.0, 2.5 ], [0.5, 0.25 ], [1, 0 ] ],
        "size": [[0, 0.5 ], [0.01, 1 ], [1, 1.5 ] ],
        "alpha": [[0, 0 ], [0.01, 0.1 ], [1, 0 ] ],
        "cameraPush": 0.25,
        "baseTexture": "/pa/effects/textures/particles/softSmoke.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "type": "CYLINDER_Z",
      "offsetZ": 5,
      "offsetX": 20,
      "offsetY": 20,
      "useRadialVelocityDir": True,
      "velocityZ": 2,
      "velocity": 10,
      "drag": 0.996,
      "sizeX": 35,
      "sizeRangeX": 5,
      "rotationRange": 3.15,
      "rotationRateRange": 0.5,
      "emissionBursts": 20,
      "lifetime": 14,
      "lifetimeRange": 0.25,
      "delay": 1.5,
      "bLoop": False,
      "endDistance": -1
    }

smoke_wave = {
      "label": "ground smoke wave",
      "spec": {
        "shader": "particle_transparent_lit",
        "size": [[0, 0.25 ], [0.05, 1 ], [1, 1.25 ] ],
        "red": [[0.0, 25 ], [1, 0 ] ],
        "green": [[0.0, 10 ], [1, 0 ] ],
        "blue": [[0.0, 2.5 ], [1, 0 ] ],
        "alpha": [[0, 0 ], [0.05, 1 ], [0.25, 1.0 ], [1, 0 ] ],
        "cameraPush": 0.25,
        "baseTexture": "/pa/effects/textures/particles/softBrownSmoke.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "type": "CYLINDER_Z",
      "offsetX": [[0.0, 0.0 ], [0.15, 11.379 ], [0.3, 22.7545 ], [0.45, 34.123 ], [0.6, 45.4812 ], [0.75, 56.8255 ], [0.9, 68.1526 ], [1.05, 79.4588 ], [1.2, 90.7409 ], [1.35, 101.995 ], [1.5, 113.219 ] ],
      "offsetY": [[0.0, 0.0 ], [0.15, 11.379 ], [0.3, 22.7545 ], [0.45, 34.123 ], [0.6, 45.4812 ], [0.75, 56.8255 ], [0.9, 68.1526 ], [1.05, 79.4588 ], [1.2, 90.7409 ], [1.35, 101.995 ], [1.5, 113.219 ] ],
      "useArcLengthSpace": True,
      "red": [[0, 1 ], [0.2, 0.922 ], [0.4, 0.71 ], [0.6, 0.41 ], [0.8, 0.13 ], [1.5, 0 ] ], 
      "green": [[0, 1 ], [0.2, 0.922 ], [0.4, 0.71 ], [0.6, 0.41 ], [0.8, 0.13 ], [1.5, 0 ] ],
      "blue": [[0, 1 ], [0.2, 0.922 ], [0.4, 0.71 ], [0.6, 0.41 ], [0.8, 0.13 ], [1.5, 0 ] ],
      "velocityY": -1.0,
      "velocityZ": 0.25,
      "velocityRangeX": 0.1,
      "velocityRangeY": 0.1,
      "velocity": 10,
      "snapToSurface": True,
      "snapToSurfaceOffset": 0,
      "alignVelocityToSurface": True,
      "sizeX": 24,
      "accelZ": -0.2,
      "drag": 0.985,
      "alpha": [[0.5, 1 ], [1.0, 0.25 ], [1.5, 0.001 ] ],
      "emissionRate": [[0.15, 0 ], [1.5, 500 ] ],
      "maxParticles": 750,
      "rotationRange": 3.15,
      "rotationRateRange": 0.025,
      "lifetime": [[0.0, 10 ], [1.5, 8.5 ] ],
      "lifetimeRange": [[0.0, 0.5 ], [1.5, 0.25 ] ],
      "emitterLifetime": 1.5,
      "bLoop": False,
      "delay": 1.0,
      "endDistance": -1
    }

smoke_wave_mesh = {
      "label": "nuke ground smoke wave",
      "spec": {
        "shader": "meshParticle_clip_smoke_bend",
        "shape": "mesh",
        "facing": "EmitterZ",
        "red": [[0.5, 25 ], [0.75, 10 ], [1, 0 ] ],
        "green": [[0.5, 10 ], [0.75, 2.5 ], [1, 0 ] ],
        "blue": [[0.5, 2.5 ], [0.75, 0.1 ], [1, 0 ] ],
        "alpha": [[0, 2 ], [0.8, -0.1 ] ],
        "sizeX": [[0.0, 0.0696893 ], [0.05, 0.298525 ], [0.1, 0.442665 ], [0.15, 0.548785 ], [0.2, 0.631928 ], [0.25, 0.699241 ], [0.3, 0.75479 ], [0.35, 0.801152 ], [0.4, 0.840083 ], [0.45, 0.872846 ], [0.5, 0.900386 ], [0.55, 0.923436 ], [0.6, 0.942578 ], [0.65, 0.958285 ], [0.7, 0.970955 ], [0.75, 0.980926 ], [0.8, 0.988496 ], [0.85, 0.993932 ], [0.9, 0.997491 ], [0.95, 0.999423 ], [1.0, 1.0 ] ],
        "sizeY": [[0, 0 ], [0.01, 0.5 ], [0.5, 4 ], [1, 1 ] ], 
        "polyAdjustCenter": [[0.0, 0.0696893 ], [0.05, 0.298525 ], [0.1, 0.442665 ], [0.15, 0.548785 ], [0.2, 0.631928 ], [0.25, 0.699241 ], [0.3, 0.75479 ], [0.35, 0.801152 ], [0.4, 0.840083 ], [0.45, 0.872846 ], [0.5, 0.900386 ], [0.55, 0.923436 ], [0.6, 0.942578 ], [0.65, 0.958285 ], [0.7, 0.970955 ], [0.75, 0.980926 ], [0.8, 0.988496 ], [0.85, 0.993932 ], [0.9, 0.997491 ], [0.95, 0.999423 ], [1.0, 1.0 ] ],
        "papa": "/pa/effects/fbx/particles/nukeSmokeWave.papa",
        "materialProperties": {
          "DiffuseTexture": "/pa/effects/textures/particles/bumpyLightGrey.papa",
          "NormalTexture": "/pa/effects/textures/particles/bumpyCell.papa",
          "UVScale": [3.0, 0.15, 4, 0 ],
          "UVPan": [0.0, -0.5, 0, 0 ]
        }
      },
      "snapToSurface": True,
      "snapToSurfaceOffset": 0.0,
      "rampRangeV": 1,
      "velocityZ": -1,
      "velocity": 0.5,
      "rotationRange": 3.14,
      "sizeX": 4,
      "sizeY": 1.5,
      "lifetime": 15.0,
      "emissionBursts": 1,
      "bLoop": False,
      "delay": 1,
      "endDistance": -1
    }

shockwave_rings = [    {
      "label": "shockwave ring",
      "spec": {
        "shader": "meshParticle_ring_wave_add",
        "shape": "mesh",
        "facing": "EmitterZ",
        "sizeX": [[0, 0 ], [0.1, 0.185 ], [0.2, 0.344 ], [0.3, 0.48 ], [0.4, 0.597 ], [0.5, 0.697 ], [0.6, 0.782 ], [0.7, 0.854 ], [0.8, 0.914 ], [0.9, 0.962 ], [1, 1 ] ], 
        "sizeY": [[0, 0 ], [1, 1 ] ],
        "red": 2,
        "green": 5,
        "blue": 3.6,
        "alpha": [[0, 1 ], [0.3, 0.5 ], [0.6, 0.01 ], [1, 0 ] ], 
        "papa": "/pa/effects/fbx/particles/ringWave_highpoly.papa",
        "materialProperties": {
          "Texture": "/pa/effects/textures/particles/explosionRingEdge.papa"
        }
      },
      "sizeX": 180.0,
      "offsetZ": 10.0,
      "emissionBursts": 1,
      "rotationRange": 3.15,
      "lifetime": 1.5,
      "emitterLifetime": 4,
      "bLoop": False,
      "sort": "NoSort",
      "delay": 1.5,
      "endDistance": -1
    },
    {
      "label": "initial shockwave ring",
      "spec": {
        "shader": "particle_add",
        "facing": "EmitterZ",
        "size": [[0, 0 ], [0.1, 0.486 ], [0.2, 0.774 ], [0.3, 0.894 ], [0.4, 0.933 ], [0.5, 0.961 ], [0.6, 0.98 ], [0.7, 0.992 ], [0.8, 0.998 ], [0.9, 0.9997 ], [1, 1 ] ],
        "red": 2,
        "green": 5,
        "blue": 3.6,
        "alpha": [[0.3, 1 ], [0.46, 0.125 ], [0.8, 0 ] ], 
        "baseTexture": "/pa/effects/textures/particles/simpleExplosionRing.papa",
        "rampTexture": "/pa/effects/textures/particles/uncompressed/no_ramp.papa",
        "dataChannelFormat": "PositionAndColor"
      },
      "sizeX": 80,
      "offsetZ": 5,
      "emissionBursts": 1,
      "rotationRange": 0.5,
      "lifetime": 2.0,
      "emitterLifetime": 1,
      "bLoop": False,
      "sort": "NoSort",
      "delay": 0,
      "endDistance": -1
    },
    {
      "label": "initial flash bloom",
      "spec": {
        "shader": "particle_add_soft",
        "red": [[0.1, 1 ], [0.25, 0.5 ], [1, 0 ] ],
        "green": [[0.1, 0.4 ], [0.25, 0.125 ], [1, 0 ] ],
        "blue": [[0.1, 0.1 ], [0.25, 0.005 ], [1, 0 ] ],
        "cameraPush": 0.5,
        "baseTexture": "/pa/effects/textures/particles/softdot.papa"
      },
      "velocityZ": 1,
      "velocity": 5,
      "sizeX": 150,
      "emissionBursts": 1,
      "lifetime": 10.0,
      "bLoop": False,
      "sort": "NoSort",
      "endDistance": 3000
    },
    {
      "label": "nuke cloud stalk",
      "spec": {
        "shader": "meshParticle_clip_smoke",
        "shape": "mesh",
        "facing": "EmitterZ",
        "red": [[0.5, 25 ], [0.75, 10 ], [1, 0 ] ],
        "green": [[0.5, 10 ], [0.75, 2.5 ], [1, 0 ] ],
        "blue": [[0.5, 2.5 ], [0.75, 0.1 ], [1, 0 ] ],
        "alpha": [[0, 0.6 ], [1, 0 ] ],
        "sizeX": [[0.0, 0.0696893 ], [0.05, 0.298525 ], [0.1, 0.442665 ], [0.15, 0.548785 ], [0.2, 0.631928 ], [0.25, 0.699241 ], [0.3, 0.75479 ], [0.35, 0.801152 ], [0.4, 0.840083 ], [0.45, 0.872846 ], [0.5, 0.900386 ], [0.55, 0.923436 ], [0.6, 0.942578 ], [0.65, 0.958285 ], [0.7, 0.970955 ], [0.75, 0.980926 ], [0.8, 0.988496 ], [0.85, 0.993932 ], [0.9, 0.997491 ], [0.95, 0.999423 ], [1.0, 1.0 ] ],
        "sizeY": [[0, 0 ], [0.01, 1 ], [0.5, 5.5 ], [1, 8 ] ],
        "polyAdjustCenter": [[0.0, 0.0696893 ], [0.05, 0.298525 ], [0.1, 0.442665 ], [0.15, 0.548785 ], [0.2, 0.631928 ], [0.25, 0.699241 ], [0.3, 0.75479 ], [0.35, 0.801152 ], [0.4, 0.840083 ], [0.45, 0.872846 ], [0.5, 0.900386 ], [0.55, 0.923436 ], [0.6, 0.942578 ], [0.65, 0.958285 ], [0.7, 0.970955 ], [0.75, 0.980926 ], [0.8, 0.988496 ], [0.85, 0.993932 ], [0.9, 0.997491 ], [0.95, 0.999423 ], [1.0, 1.0 ] ],
        "papa": "/pa/effects/fbx/particles/nukeCone.papa",
        "materialProperties": {
          "DiffuseTexture": "/pa/effects/textures/particles/bumpyLightGrey.papa",
          "NormalTexture": "/pa/effects/textures/particles/bumpyCell.papa",
          "UVScale": [1, 0.4, 4, 0 ],
          "UVPan": [0.0, -1.0, 0, 0 ]
        }
      },
      "snapToSurface": True,
      "snapToSurfaceOffset": -1.0,
      "rampRangeV": 1,
      "offsetZ": -1,
      "velocityZ": -1,
      "velocity": 0.5,
      "rotationRange": 3.14,
      "sizeX": 6.0,
      "sizeY": 1.75,
      "lifetime": 14.0,
      "emissionBursts": 1,
      "bLoop": False,
      "delay": 1,
      "endDistance": -1
    },
    {
      "label": "nuke dome",
      "spec": {
        "shader": "meshParticle_clip_smoke",
        "shape": "mesh",
        "facing": "EmitterZ",
        "red": [[0.5, 50 ], [0.75, 20 ], [1, 0 ] ],
        "green": [[0.5, 20 ], [0.75, 5 ], [1, 0 ] ],
        "blue": [[0.5, 5 ], [0.75, 0.2 ], [1, 0 ] ],
        "alpha": [[0.5, 0.4 ], [1, 0 ] ],
        "size": [[0, 0 ], [0.01, 1 ], [1, 3 ] ],
        "polyAdjustCenter": [[0, 0 ], [0.1, 0.185 ], [0.2, 0.344 ], [0.3, 0.48 ], [0.4, 0.597 ], [0.5, 0.697 ], [0.6, 0.782 ], [0.7, 0.854 ], [0.8, 0.914 ], [0.9, 0.962 ], [1, 1 ] ],
        "papa": "/pa/effects/fbx/particles/nukeDome.papa",
        "materialProperties": {
          "DiffuseTexture": "/pa/effects/textures/particles/bumpyLightGrey.papa",
          "NormalTexture": "/pa/effects/textures/particles/bumpyCell.papa",
          "UVScale": [1, 0.5, 4, 0 ],
          "UVPan": [0.0, -1.0, 0, 0 ]
        }
      },
      "rampRangeV": 1,
      "offsetZ": 7.5,
      "velocityZ": 1,
      "velocity": 15,
      "drag": 0.998,
      "rotationRange": 3.14,
      "sizeX": 1.5,
      "lifetime": 15.0,
      "emissionBursts": 1,
      "bLoop": False,
      "delay": 1,
      "endDistance": -1
    }
]

base_init_flash = {
      "label": "ball flash",
      "spec": {
        "shader": "particle_clip",
        "shape": "mesh",
        "facing": "EmitterZ",
        "red": 10,
        "green": 3,
        "blue": 9,
        "alpha": [[0.65, 1.1 ], [1, 0 ] ], "sizeX": [[0, 0 ], [0.1, 0.486 ], [0.2, 0.774 ], [0.3, 0.894 ], [0.4, 0.933 ], [0.5, 0.961 ], [0.6, 0.98 ], [0.7, 0.992 ], [0.8, 0.998 ], [0.9, 0.9997 ], [1, 1 ] ],
        "papa": "/pa/effects/fbx/particles/sphere_24sides.papa",
        "materialProperties": {
          "Texture": "/pa/effects/textures/particles/nuke_shell_clip.papa"
        }
      },
      "offsetZ": 9,
      "velocityZ": 1,
      "velocity": 0.1,
      "sizeX": 50,
      "lifetime": 1.75,
      "emissionBursts": 1,
      "bLoop": False,
      "endDistance": 5000
    }

# global light source

base_light = {
      "spec": {
        "shape": "pointlight",
        "size": [[0.1, 1 ], [0.5, 0.75 ] ],
        "red": [[0, 0.2 ], [0.75, 0.2 ] ],
        "green": [[0, 1 ], [0.75, 1 ] ],
        "blue": [[0, 1 ], [0.75, 1 ] ],
        "alpha": [[0.1, 5 ], [0.75, 1 ], [0.85, 0.1 ], [1, 0 ] ]
      },
      "velocityZ": 1,
      "velocity": 0.5,
      "offsetZ": 10.0,
      "sizeX": 200,
      "emissionBursts": 1,
      "lifetime": 13,
      "emitterLifetime": 1.5,
      "bLoop": False,
      "endDistance": -1
    }


def make(delay):
	global smoke_puff_upper, smoke_wave, shockwave_rings, base_light, base_init_flash


	smoke_wave['spec']['red'], smoke_wave['spec']['green'], smoke_wave['spec']['blue'] = rainbow(40, 0.4, 20)
	base_light['spec']['red'], base_light['spec']['green'], base_light['spec']['blue'] = rainbow(40, 0, 20)


	smoke_wave_mesh['spec']['red'], smoke_wave_mesh['spec']['green'], smoke_wave_mesh['spec']['blue'] = rainbow(40, 0.1, 50)
	 # = base_init_flash['spec']['red'], base_init_flash['spec']['green'], base_init_flash['spec']['blue']

	 # = base_light['spec']['red'], base_light['spec']['red'], base_light['spec']['red']

	effects = []

	effects.append(base_light)
	effects.append(base_init_flash)

	# effects.append(smoke_puff_upper)
	effects.append(smoke_wave)
	effects.append(smoke_wave_mesh)
	effects.extend(shockwave_rings)

	return effects