from numpy import *
from mayavi.mlab import *
from mayavi.api import Engine
    
a = -10.
b = 10.
ds = 1.

x, y, z = mgrid[a:b:ds, a:b:ds, a:b:ds];

q = [1, -1, 1, 1, 1, 1, -1, -1] # set the charges
d = 1.5
qpos = [[d, d, d], # set the positions. Note: All positions are offset by 0.5 to avoid calculating charges on the grid itself (causes 0-division!)
        [d, d, -d],
        [d, -d, d],
        [d, -d, -d],
        [-d, d, d],
        [-d, d, -d],
        [-d, -d, d],
        [-d, -d, -d]]

Ex = 0 * x; # create our value arrays, filled with zeros
Ey = 0 * y;
Ez = 0 * z;

for i in range(len(q)): # calculate the charge field from each electric charge
    r = (x - qpos[i][0])**2 + (y - qpos[i][1])**2 + (z - qpos[i][2])**2
    Ex = Ex + (q[i] * (x - qpos[i][0])) / (r)**1.5
    Ey = Ey + (q[i] * (y - qpos[i][1])) / (r)**1.5
    Ez = Ez + (q[i] * (z - qpos[i][2])) / (r)**1.5

# Now, let's prepare some output

fig = figure(fgcolor=(1,1,1), bgcolor=(0,0,0)) # set the background and foreground of our scene
camera = fig.scene.camera
camera.yaw(120)

streams = []
          
for s in range(len(q)):
    fl = flow(x,y,z,Ex,Ey,Ez,seed_scale=0.3, seed_resolution=6); # create another flow object
    fl.seed.widget.center = qpos[s]; # make seed sphere surround the charge
    fl.stream_tracer.initial_integration_step = 0.01 # make small integration steps for smooth lines and to avoid ugly lines
    fl.stream_tracer.maximum_propagation = 20.0 # avoid ugly lines by limitiing propagation
    fl.stream_tracer.integration_direction = 'both' # integrate in both directions for best results
    fl.seed.widget.enabled = False # remove the widget
    fl.actor.property.opacity = 0.5 # set the line opacity to make it semi-transparent
    streams.append(fl);

print "Done."
