#!/usr/bin/env python
'A model of the earth and its magnetic field, with earth center as origin.'

import numpy as np
import mayavi
from mayavi.mlab import *


def sphericalCoordinates(x,y,z):
    '''Returns three arrays with r, theta, phi, containing spherical coordinates corresponding to input x, y, z'''
    xy = x**2+y**2
    r = np.sqrt(xy+z**2)
    theta = np.arctan2(np.sqrt(xy),z)
    phi = np.arctan2(y, x)
    return r, theta, phi

def makeRcoordinates(x,y,z):
    '''Makes r length and r^hat from coordinates'''
    r = np.sqrt(x**2 + y**2 + z**2)
    x_hat = x / r
    y_hat = y / r
    z_hat = z / r
    return r, x_hat, y_hat, z_hat

# constants from wikipedia
earthRadius = 6371
sunEarthRadius = 150e6
magnetosphere = 65          # http://en.wikipedia.org/wiki/Magnetosphere
sunRadius = 109*earthRadius # http://en.wikipedia.org/wiki/Sun

# method 3 - ogrid
n = 10 # 0.5x number of steps
steps = earthRadius / n
x,y,z = np.ogrid[-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps]
#r,theta,phi = sphericalCoordinates(x,y,z)
r,x_hat,y_hat,z_hat = makeRcoordinates(x,y,z)

# Plot
#fig = figure(1, size=(400, 400), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0)) # figure with white background
#fig.scene.y_plus_view() # see from Y-axis
#fig.scene.camera.roll(90) # roll north to point upwards
#fig.scene.show_axes = True
#quiver3d(x,y,z,bx,by,bz)
#mayavi.tools.pipeline.vector_field(x,y,z,bx,by,bz)

