#! /usr/bin/env python
'This example shows basic matplotlib capabilities.'

import numpy
import matplotlib
matplotlib.use('pdf')
from matplotlib import pyplot

def make_nice_plot(xs, ys, zs, filename):
    'This function just makes a nice plot.'
    pyplot.plot(xs, ys, label='spam')
    pyplot.plot(xs, zs, label='eggs')
    legend = pyplot.legend()
    legend.draw_frame(False) # just for the looks of it
    pyplot.xlabel('$\\alpha$ value')
    pyplot.ylabel('$y$ value')
    pyplot.savefig(filename) # The filename automagically gets a .pdf suffix

def make_even_nicer_plot(xs, ys, zs, filename):
    """This one makes an even nicer plot."""
    pyplot.contourf(xs, ys, zs, 50)
    pyplot.xlabel('Whatever you want')
    pyplot.ylabel("Look at me, I'm the ylabel")
    cbar = pyplot.colorbar()
    cbar.set_label('Whatever here too')
    pyplot.xlim(xs[0, 0], xs[-1, -1])
    pyplot.ylim(ys[0, 0], ys[-1, -1])
    pyplot.savefig(filename)
    pass

def main():
    xs = numpy.linspace(0, 4 * numpy.pi, 250)
    ys = numpy.sin(xs)
    zs = numpy.cos(xs)
    make_nice_plot(xs, ys, zs, 'sincos')
    pyplot.clf() # Call between plotting commands
    # That was a curve, now let's look at a 3D plot
    xs = numpy.linspace(0, 2 * numpy.pi, 250)
    xs, ys = numpy.meshgrid(xs, xs)
    zs = numpy.sin(xs) * numpy.cos(ys)
    make_even_nicer_plot(xs, ys, zs, '3dplot')
    return 0

if __name__ == '__main__':
    main()
else:
    print "I was imported as a module!"

