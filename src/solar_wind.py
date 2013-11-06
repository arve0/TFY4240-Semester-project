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
    return np.array([ bx, by, bz ])

def solarWind(x0,y0,z0,v0):
    # constants
    m = np.array([-2*np.sin(13./180*np.pi),0,2*np.cos(13./180*np.pi)]) # rot tilt ~23deg, mag tilt ~10deg from rot -> ~13deg from z-axis
    k = 2 # q/m
    # Initial conditions
    n = 6000 # number of iterations
    v = np.zeros((n, 3))
    x = np.zeros(n)
    y = np.zeros(n)
    z = np.zeros(n)
    v[0] = v0 # initial speed
    x[0] = x0 # initial position
    y[0] = y0
    z[0] = z0
    dt = 1
    # F = q (v x B), F = ma, v = v0 + a*dt
    # a = q/m (v x B) = k(vxB)
    # -> v = v0 + k(vxB)dt
    # r = r + v*dt = r + v0*dt + k(vxB)*dt^2

    for i in range(n-1):
        r, x_hat, y_hat, z_hat = makeRcoordinates(x[i],y[i],z[i])
        mr = calcMdotRhat(m, x_hat, y_hat, z_hat)
        B = calcBfield(r, x_hat, y_hat, z_hat, m, mr)
        vxB = k*np.cross(v[i],B)
        v[i+1] = v[i] + vxB*dt
        x[i+1] = x[i] + v[i,0]*dt
        y[i+1] = y[i] + v[i,1]*dt
        z[i+1] = z[i] + v[i,2]*dt

    surface = plot3d(x,y,z)
    #visibility
    surface.actor.mapper.scalar_range = np.array([ 0.,  1.])
    surface.actor.mapper.scalar_visibility = True
    surface.actor.property.specular_color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.diffuse_color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.ambient_color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.point_size = 10.0

#x0=25
#y0=0
#z0=-25
#for i in range(np.absolute(2*z0)):
#    solarWind(x0,y0,z0+i)
v0 = np.array([-1e-2,0,-1e-2])
for i in range(15):
    for j in range(15):
        solarWind(15,i,j,v0)
