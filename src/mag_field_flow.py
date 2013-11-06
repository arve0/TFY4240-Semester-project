#!/usr/bin/env python
'A model of the earth and its magnetic field, with earth center as origin.'

from __future__ import division # avoid integer division
import numpy as np
import mayavi
from mayavi.mlab import *

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

# Constants
earthRadius = 10      # outer core about 5e3km below surface -> ratio m/r~0.2
m = np.array([-2*np.sin(13./180*np.pi),0,2*np.cos(13./180*np.pi)]) # rot tilt ~23deg, mag tilt ~10deg from rot -> ~13deg from z-axis

# Create grid
n = 13 # 0.5x number of steps
steps = earthRadius / n
x,y,z = np.mgrid[-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps]
r,x_hat,y_hat,z_hat = makeRcoordinates(x,y,z)

# create earth
theta, phi = np.mgrid[0:np.pi:11j, 0:np.pi*2:21j]
ex = earthRadius * np.sin(theta) * np.cos(phi)
ey = earthRadius * np.sin(theta) * np.sin(phi)
ez = earthRadius * np.cos(theta)


# Calculate B-field
mr = calcMdotRhat(m, x_hat, y_hat, z_hat)
bx, by, bz = calcBfield(r, x_hat, y_hat, z_hat, m, mr)

# Remove data no longer in use
del m, mr, x_hat, y_hat, z_hat

# Plot
fig = figure(size=(720,720))
# B-field
streamline = flow(x, y, z, bx, by, bz)
streamline.stream_tracer.start_position = np.array([ 0.,  0.,  0.])
streamline.stream_tracer.progress = 1.0
streamline.stream_tracer.integration_direction = 'both'

# earth
mesh(ex, ey, ez, color=(0, 0, 0))
# viewing
fig.scene.background = (1,1,1) # white background
fig.scene.y_plus_view()   # see from Y-axis
fig.scene.camera.roll(90) # roll north to point upwards
fig.scene.show_axes = True
fig.scene.camera.zoom(1.3)


# prevent segfautl (malloc too large) on osx
vectors = fig.children[0].children[0].children[0]
vectors.glyph.mask_points.maximum_number_of_points = 1800

# make pretier
vectors.glyph.glyph.scaling = True
vectors.glyph.glyph.range = np.array([  1.00000000e-05,   1.00000000e-03])
vectors.glyph.glyph.scale_factor = 3.0
vectors.glyph.mask_points.proportional_maximum_number_of_points = True
vectors.glyph.mask_points.generate_vertices = True
vectors.glyph.mask_input_points = True

# save pictures for animation, dont run at default
def createAnimation():
    for i in range(360):
        fig.scene.camera.azimuth(1)
        filename = `i` + '.png'
        savefig(filename, size=(720,720))
def createAnimation2():
    for i in range(360,720):
        fig.scene.camera.elevation(1)
        fig.scene.camera.orthogonalize_view_up() # http://public.kitware.com/pipermail/vtkusers/2003-July/018794.html
        filename = `i` + '.png'
        savefig(filename, size=(720,720))
