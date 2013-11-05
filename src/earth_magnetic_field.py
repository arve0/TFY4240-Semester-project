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

def cartesianCoordinates(r,theta,phi):
    '''Returns cartesian coordinates to correpsonding spherical coordinates r,theta,phi'''
    size = r.size * theta.size * phi.size
    x = np.zeros(size)
    y = np.zeros(size)
    z = np.zeros(size)
    pos = 0
    for i in range(r.size):
        for j in range(theta.size):
            for k in range(phi.size):
                x[pos] = r[i] * np.sin(theta[j]) * np.cos(phi[k])
                y[pos] = r[i] * np.sin(theta[j]) * np.sin(phi[k])
                z[pos] = r[i] * np.cos(theta[j])
                pos += 1
    return x, y, z
                

def calculateBfield(r,theta,phi):
    import numpy as np
    m = np.array([0,0,2])
    r_hat = np.zeros(3)
    r_hat[0] = np.cos(phi)*np.sin(theta)
    r_hat[1] = np.sin(phi)*np.sin(theta)
    r_hat[2] = np.cos(theta)
    m_dot_r_hat = 0
    for i in range(3):
        m_dot_r_hat += m[i]*r_hat[i]
    B=np.zeros(3)
    for i in range(3):
        B[i]=(3*m_dot_r_hat*r_hat[i]-m[i])/r**3
    return B

def bFieldMgrid(r,theta,phi):
    Bx=np.zeros(r.shape)
    By=np.zeros(r.shape)
    Bz=np.zeros(r.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            for k in range(x.shape[2]):
                Bx[i,j,k],By[i,j,k],Bz[i,j,k]=calculateBfield(r[i,j,k], theta[i,j,k], phi[i,j,k])
    Bx[np.isinf(Bx)] = np.nan
    By[np.isinf(By)] = np.nan
    Bz[np.isinf(Bz)] = np.nan
    return Bx, By, Bz

def bFieldLinspace(r,theta,phi):
    '''Calculate B-field for coordinates made with linspace'''
    size = r.size*theta.size*phi.size
    Bx = np.zeros(size)
    By = np.zeros(size)
    Bz = np.zeros(size)
    pos = 0
    for i in range(r.size):
        for j in range(theta.size):
            for k in range(phi.size):
                Bx[pos], By[pos], Bz[pos] = calculateBfield(r[i], theta[j], phi[k])
                pos += 1
    return Bx, By, Bz

#def calcCircle2D(radius):
#    iterations = 100
#    x = np.zeros(iterations)
#    y = np.zeros(iterations)
#    z = np.zeros(iterations)
#    for i in range(iterations):
        


# constants from wikipedia
earthRadius = 6371
sunEarthRadius = 150e6
magnetosphere = 65          # http://en.wikipedia.org/wiki/Magnetosphere
sunRadius = 109*earthRadius # http://en.wikipedia.org/wiki/Sun
# x axis towards sun
# y in same direction as earths trajectory
# z perpendicular to earth-sun ellipse

n = 13 # number of points to calculate in each coordinate

# method 1 - mgrid
#x,y,z = np.mgrid[-2*earthRadius:2*earthRadius:earthRadius/n,-2*earthRadius:2*earthRadius:earthRadius/n,-2*earthRadius:2*earthRadius:earthRadius/n]
#r,theta,phi = sphericalCoordinates(x,y,z)
#bx,by,bz = bFieldMgrid(x,y,z)

# method 2 - spherical coordinates
r = np.linspace(earthRadius,2*earthRadius,n)
theta = np.linspace(0,2*np.pi,n)
phi = np.array([0]) # xy-plane
x,y,z = cartesianCoordinates(r,theta,phi)
bx,by,bz = bFieldLinspace(r,theta,phi)

# method 3 - ogrid
#steps = earthRadius / n
#x,y,z = np.ogrid[-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps,-2*earthRadius:2*earthRadius:steps]

# Plot
fig = figure(1, size=(400, 400), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0)) # figure with white background
fig.scene.y_plus_view() # see from Y-axis
fig.scene.camera.roll(90) # roll north to point upwards
fig.scene.show_axes = True
quiver3d(x,y,z,bx,by,bz)
#mayavi.tools.pipeline.vector_field(x,y,z,bx,by,bz)

