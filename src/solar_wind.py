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

def particleTrajectory(x0,y0,z0,v0,k,maxIterations):
    '''Calculate particle trajectory, with starting posistion x0,y0,z0, starting velocity v0, numerical factor k (k*(vxB)), and maximum number of iterations.'''
    # constants
    m = np.array([-2*np.sin(13./180*np.pi),0,2*np.cos(13./180*np.pi)]) # rot tilt ~23deg, mag tilt ~10deg from rot -> ~13deg from z-axis
    limit = 1+np.max(np.abs([x0,y0,z0])) # max x,y or z coordinate
    dt = 50/720/np.linalg.norm(v0) # from -25 to 25, at 720 pixels, expect resolution ~50/720=v0*dt
    # arrays for particle trajectory
    v = np.zeros((maxIterations, 3))
    x = np.zeros(maxIterations)
    y = np.zeros(maxIterations)
    z = np.zeros(maxIterations)
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
    
    for i in range(maxIterations-1):
        r, x_hat, y_hat, z_hat = makeRcoordinates(x[i],y[i],z[i])
        mr = calcMdotRhat(m, x_hat, y_hat, z_hat)
        B = calcBfield(r, x_hat, y_hat, z_hat, m, mr)
        vxB = k * np.cross(v[i],B)
        v[i+1] = v[i] + vxB*dt
        x[i+1] = x[i] + v[i,0]*dt
        y[i+1] = y[i] + v[i,1]*dt
        z[i+1] = z[i] + v[i,2]*dt
        x_max = np.abs(x[i+1])
        y_max = np.abs(y[i+1])
        z_max = np.abs(z[i+1])
        if (x_max > limit or y_max > limit or z_max > limit):
            # dont continue when particle "get lost"
            #print 'Breaking with position: ' + `x_max`, `y_max`, `z_max` #debug
            x=x[0:i+1]
            y=y[0:i+1]
            z=z[0:i+1]
            v=v[0:i+1]
            break
    #print 'Iteration numer: ' + `i`
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
    v_last = np.linalg.norm(v[-1])
    v_first = np.linalg.norm(v[0])
    v_diff = v_first - v_last
    v_diff_percent = v_diff / v_first * 100
    print 'Percentage difference in start/end velocity: ' + `v_diff_percent` + '%'
    return surface, i # also return i, such that we can control animation calculations better

def trajectoryAnimation():
    x0 = 25
    start = -25      # y0,z0
    v0 = 400/6371*10 # v=400km/s, rEarth=6371km, rEarth is 10 in mgrid.py
    k = 2e2
    it = 6      # number of points in grid
    maxIterations = 10000   # max iterations
    step = 10

    # create pictures to animate particle trajectory
    imageName = 0

    for i in range(-1,2): #several starting points
        y0 = 5*i
        for j in range(2):
            z0 = -25 + 5*j
            for stop in range(100,maxIterations,step):
                r = (x0**2 + y0**2 + z0**2)**0.5
                r_hat = np.array([ x0/r, y0/r, z0/r ])
                v = -r_hat*v0 # direction straight at earth
                surface, num = particleTrajectory(x0,y0,z0,v,k,stop)
                if (num != stop-2):
                    #print 'num, stop: ' + `num`, `stop` #debug
                    break # we do not need to generate more pictures, particle out of bound
                savefig(`imageName` + '.png',size=(720,720))
                imageName+=1
                surface.remove()
                fig.scene.camera.elevation(1)
                fig.scene.camera.orthogonalize_view_up() # http://public.kitware.com/pipermail/vtkusers/2003-July/018794.html

def xTowards():
    '''Plot all trajectories in yz-plane, where x=25'''
    x0 = 25
    start = -25      # y0,z0
    v0 = 400/6371*10 # v=400km/s, rEarth=6371km, rEarth is 10 in mgrid.py
    k = 2e2
    it = 4      # number of points in grid
    maxIterations = 10000   # max iterations
    step = 10

    # plot all trajectories
    for i in range(it): #several starting points
        for j in range(it):
            y0 = start + 50*i/it
            z0 = start + 50*j/it
            r = (x0**2 + y0**2 + z0**2)**0.5
            r_hat = np.array([ x0/r, y0/r, z0/r ])
            v = -r_hat*v0 # direction straight at earth
            surface, num = particleTrajectory(x0,y0,z0,v,k,maxIterations)

def xStraigth():
    '''Plot all trajectories in yz-plane, where x=25'''
    x0 = 25
    start = -25      # y0,z0
    v0 = 400/6371*10 # v=400km/s, rEarth=6371km, rEarth is 10 in mgrid.py
    k = 2e2
    it = 4      # number of points in grid
    maxIterations = 10000   # max iterations
    step = 10

    # plot all trajectories
    for i in range(it): #several starting points
        for j in range(it):
            y0 = start + 50*i/it
            z0 = start + 50*j/it
            v = np.array([-v0,0,0])
            surface, num = particleTrajectory(x0,y0,z0,v,k,maxIterations)

def zStraight():
    '''Plot all trajectories in yz-plane, where x=25'''
    x0 = 25
    start = -25      # y0,z0
    v0 = 400/6371*10 # v=400km/s, rEarth=6371km, rEarth is 10 in mgrid.py
    k = 2e2
    it = 4      # number of points in grid
    maxIterations = 10000   # max iterations
    step = 10

    # plot all trajectories
    for i in range(it): #several starting points
        for j in range(it):
            y0 = start + 50*i/it
            z0 = start + 50*j/it
            v = np.array([0,0,-v0])
            surface, num = particleTrajectory(z0,y0,x0,v,k,maxIterations)
                
                
# create earth
earthRadius = 10
theta, phi = np.mgrid[0:np.pi:11j, 0:np.pi*2:21j]
ex = earthRadius * np.sin(theta) * np.cos(phi)
ey = earthRadius * np.sin(theta) * np.sin(phi)
ez = earthRadius * np.cos(theta)
fig = figure(size=(720,720))
fig.scene.background = (1,1,1) # white background
fig.scene.y_plus_view()   # see from Y-axis
fig.scene.camera.elevation(45)
fig.scene.camera.azimuth(10)
fig.scene.show_axes = True
earthSurface = mesh(ex, ey, ez, color=(0, 0, 0))
