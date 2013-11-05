#!/usr/bin/env python
'A model of the earth and its magnetic field, with earth center as origin.'

import numpy as np
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


# constants from wikipedia
earthRadius = 6371      # http://en.wikipedia.org/wiki/Magnetosphere
sunEarthRadius = 150e6
magnetosphere = 65          # http://en.wikipedia.org/wiki/Magnetosphere
sunRadius = 109*earthRadius # http://en.wikipedia.org/wiki/Sun
# x axis towards sun
# y in same direction as earths trajectory
# z perpendicular to earth-sun ellipse
#x,y,z = np.mgrid[-1:1:10j, -1:1:10j, 0:1]
#r,theta,phi = sphericalCoordinates(x,y,z)
n = 10
r = np.linspace(1,0,n+1)
r = r[1:n] # do not take with r=0
theta = np.linspace(0,np.pi,n)
phi = np.linspace(0,2*np.pi,2*n-1) # more points, but same steps as theta

x = np.array([])
y = np.array([])
z = np.array([])
bx = np.array([])
by = np.array([])
bz = np.array([])
for i in range(r.size):
    for j in range(theta.size):
        for k in range(phi.size):
            # positions
            x=np.append(x, r[i] * np.sin(theta[j]) * np.cos(phi[k]) )
            y=np.append(y, r[i] * np.sin(theta[j]) * np.sin(phi[k]) )
            z=np.append(z, r[i] * np.cos(theta[j]) )
            # B-field
            bx=np.append(bx, np.sin(theta[j])*np.cos(theta[j])*np.cos(phi[k])/r[i]**3)
            by=np.append(by, np.sin(theta[j])*np.cos(theta[j])*np.sin(phi[k])/r[i]**3)
            bz=np.append(bz, (np.cos(theta[j])**2-1)/r[i]**3)



# Plot
quiver3d(x,y,z,bx,by,bz)
#src = pipeline.vector_field(Bx, By, Bz)
#pipeline.vectors(src, mask_points=20, scale_factor=3.)
    

