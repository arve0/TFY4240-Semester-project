#!/usr/bin/env python
'A model of the earth and its magnetic field, with earth center as origin.'

import numpy as np
import mayavi
from mayavi.mlab import *
from mayavi.api import Engine


def makeRcoordinates(x,y,z):
    '''Makes r length and r^hat from coordinates'''
    r = np.sqrt(x**2 + y**2 + z**2)
    x_hat = x / r
    y_hat = y / r
    z_hat = z / r
    return r, x_hat, y_hat, z_hat

def calcMdotRhat(m, x_hat, y_hat, z_hat):
    '''Calculates m dot r^hat'''
    mr = m[0]*x_hat + m[1]*y_hat + m[2]*z_hat
    return mr

def calcBfield(r, x_hat, y_hat, z_hat, m, mr):
    '''Calculate B-field from r^-3*(3*(m dot r^hat)*r^hat - m)'''
    bx = r**-3*(3*mr*x_hat-m[0])
    by = r**-3*(3*mr*y_hat-m[1])
    bz = r**-3*(3*mr*z_hat-m[2])
    # where r=0, B=0 (origin)
    bx[np.isnan(bx)] = 0
    by[np.isnan(by)] = 0
    bz[np.isnan(bz)] = 0
    return bx, by, bz

earthRadius = 12

# Create grid
n = 13. # 0.5x number of steps
steps = earthRadius / n
x,y,z = np.mgrid[-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps]
r,x_hat,y_hat,z_hat = makeRcoordinates(x,y,z)

# create earth
theta, phi = np.mgrid[0:np.pi:11j, 0:np.pi*2:11j]
ex = earthRadius * np.sin(theta) * np.cos(phi)
ey = earthRadius * np.sin(theta) * np.sin(phi)
ez = earthRadius * np.cos(theta)


# Calculate B-field
m = np.array([0,0,2])
mr = calcMdotRhat(m, x_hat, y_hat, z_hat)
bx, by, bz = calcBfield(r, x_hat, y_hat, z_hat, m, mr)

# Remove data no longer in use
del m, mr, x_hat, y_hat, z_hat

# Plot
clf()
fig = figure(size=(720,720))
fig.scene.background = (1,1,1) # white background
fig.scene.y_plus_view()   # see from Y-axis
fig.scene.camera.roll(90) # roll north to point upwards
fig.scene.show_axes = True
# B-field
quiver3d(x, y, z, bx, by, bz)
# earth
mesh(ex, ey, ez, color=(0, 0, 0))


# prevent segfautl (malloc too large) on osx
vectors = fig.children[0].children[0].children[0]
vectors.glyph.mask_points.maximum_number_of_points = 1000

# make pretier
vectors.glyph.glyph.scaling = True
vectors.glyph.glyph.range = np.array([-2.,  4.])
vectors.glyph.glyph.scale_factor = 10.0
vectors.glyph.mask_input_points = True

# save pictures for animation
def createAnimation():
    for i in range(360):
        fig.scene.camera.azimuth(1)
        filename = `i` + '.png'
        savefig(filename, size=(720,720))
