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

def particleTrajectory(x0,y0,z0,v0,k,n):
    # constants
    m = np.array([-2*np.sin(13./180*np.pi),0,2*np.cos(13./180*np.pi)]) # rot tilt ~23deg, mag tilt ~10deg from rot -> ~13deg from z-axis
    #n = 10000 # max number of iterations (if not out of bounds)
    limit = np.max(np.abs([x0,y0,z0]))+1 # max x,y or z coordinate
    dt = 50/720/np.linalg.norm(v0) # from -25 to 25, at 720 pixels, expect resolution ~50/720=v0*dt
    # arrays for particle trajectory
    v = np.zeros((n, 3))
    x = np.zeros(n)
    y = np.zeros(n)
    z = np.zeros(n)
    # Initial conditions
    v[0] = v0 # initial speed
    x[0] = x0 # initial position
    y[0] = y0
    z[0] = z0
    # F = q (v x B), F = ma, v = v0 + a*dt
    # a = q/m (v x B) = k(vxB)
    # -> v = v0 + k(vxB)dt
    # r = r + v*dt = r + v0*dt + k(vxB)*dt^2

    #print 'Limit:' + `limit` #debug
    
    for i in range(n-1):
        r, x_hat, y_hat, z_hat = makeRcoordinates(x[i],y[i],z[i])
        mr = calcMdotRhat(m, x_hat, y_hat, z_hat)
        B = calcBfield(r, x_hat, y_hat, z_hat, m, mr)
        vxB = k * np.cross(v[i],B)
        v[i+1] = v[i] + vxB*dt
        x[i+1] = x[i] + v[i,0]*dt
        y[i+1] = y[i] + v[i,1]*dt
        z[i+1] = z[i] + v[i,2]*dt
        x_max = np.max(np.abs(x))
        y_max = np.max(np.abs(y))
        z_max = np.max(np.abs(z))
        if (x_max > limit or y_max > limit or z_max > limit):
            # dont continue when particle "get lost"
            #print 'Breaking with position: ' + `x_max`, `y_max`, `z_max` #debug
            x=x[0:i]
            y=y[0:i]
            z=z[0:i]
            v=v[0:i]
            break
    print 'Iteration numer: ' + `i`
    # plot
    surface = plot3d(x,y,z)
    #visibility
    surface.actor.mapper.scalar_range = np.array([ 0.,  1.])
    surface.actor.mapper.scalar_visibility = True
    surface.actor.property.specular_color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.diffuse_color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.ambient_color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.color = (1.0, 0.7250934615091172, 0.0)
    surface.actor.property.point_size = 2.0
    surface.actor.property.representation = 'points'
    # debug
    #print 'First: ' + `x[0]`, `y[0]`, `z[0]` 
    #print 'Last: ' + `x[-1]`, `y[-1]`, `z[-1]`
    v_last = np.linalg.norm(v[-2])
    v_first = np.linalg.norm(v[0])
    v_diff = v_first - v_last
    v_diff_percent = v_diff / v_first * 100
    print 'Percentage difference in start/end velocity: ' + `v_diff_percent` + '%'
    return surface

x0 = 25
z0 = -25
y0 = 0
start = -25      # y0,z0
v0 = 400/6371*10 # v=400km/s, rEarth=6371km, rEarth is 10 in mgrid.py
k = 2e2
it = 6      # number of points in grid
n = 10000   # max iterations
step = 10

# do several trajectories to find sweet spot to start
j = 0
for i in range(100,n,step):
    j+=1
    r = (x0**2 + y0**2 + z0**2)**0.5
    r_hat = np.array([ x0/r, y0/r, z0/r ])
    v = -r_hat*v0 # direction straight at earth
    surface = particleTrajectory(x0,y0,z0,v,k,i)
    savefig(`j` + '.png')
    surface.remove()
