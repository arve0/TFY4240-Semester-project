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

# constants from wikipedia
earthRadius = 12
sunEarthRadius = 150e6
magnetosphere = 65          # http://en.wikipedia.org/wiki/Magnetosphere
sunRadius = 109*earthRadius # http://en.wikipedia.org/wiki/Sun

# Create grid
n = 13. # 0.5x number of steps
steps = earthRadius / n
x,y,z = np.mgrid[-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps]
r,x_hat,y_hat,z_hat = makeRcoordinates(x,y,z)

# Calculate B-field
m = np.array([0,0,2])
mr = calcMdotRhat(m, x_hat, y_hat, z_hat)
bx, by, bz = calcBfield(r, x_hat, y_hat, z_hat, m, mr)

# Remove data no longer in use
del m, mr, x_hat, y_hat, z_hat

# Plot
fig = figure(1, size=(400, 400), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0)) # figure with white background
fig.scene.y_plus_view() # see from Y-axis
fig.scene.camera.roll(90) # roll north to point upwards
fig.scene.show_axes = True
#quiver3d(x,y,z,bx,by,bz)
flow(x,y,z,bx,by,bz,integration_direction='both')
streamline = engine.scenes[0].children[0].children[0].children[0].children[0]
streamline.seed.widget.phi_resolution = 5
streamline.seed.widget.theta_resolution = 10
streamline.seed.widget.center = array([-0.        , -0.46153846, -0.46153846])
streamline.seed.widget.center = array([-0.        ,  0.        , -0.46153846])
streamline.seed.widget.center = array([-0.,  0.,  0.])
streamline.seed.widget.center = array([-0.,  0.,  0.])
streamline.seed.widget.handle_direction = array([ 0.,  0.,  0.])
streamline.seed.widget.handle_direction = array([ 0.,  0.,  0.])
streamline.seed.widget.radius = 12.0
scene = engine.scenes[0]
scene.scene.camera.position = [0.0, 117.39085287969561, 0.0]
scene.scene.camera.focal_point = [0.0, 0.0, 0.0]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [2.2204460492503131e-16, 0.0, 1.0]
scene.scene.camera.clipping_range = [70.141001376808077, 178.03865934697859]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
streamline.stream_tracer.start_position = array([ 0.,  0.,  0.])
streamline.stream_tracer.progress = 1.0
streamline.stream_tracer.integration_direction = 'both'

# prevent segfautl (malloc too large) on osx
vectors = fig.children[0].children[0].children[0]
vectors.glyph.mask_points.maximum_number_of_points = 1000

# make pretier
vectors.glyph.glyph.scaling = True
vectors.glyph.glyph.range = np.array([-2.,  4.])
vectors.glyph.glyph.scale_factor = 10.0
vectors.glyph.mask_input_points = True



#mayavi.tools.pipeline.vector_field(x,y,z,bx,by,bz)

