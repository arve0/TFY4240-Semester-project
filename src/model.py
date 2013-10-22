#!/usr/bin/env python
'A model of the earth and its magnetic field, with earth center as origin.'

import numpy
import matplotlib
matplotlib.use('pdf')         # save figures as pdf
from matplotlib import pyplot # pyplot as command



def main():
    # constants from wikipedia
    earthRadius = 6371      # http://en.wikipedia.org/wiki/Magnetosphere
    sunEarthRadius = 150e6
    magnetosphere = 65          # http://en.wikipedia.org/wiki/Magnetosphere
    sunRadius = 109*earthRadius # http://en.wikipedia.org/wiki/Sun
    # x axis towards sun
    # y in same direction as earths trajectory
    # z perpendicular to earth-sun ellipse
    phi   = numpy.linspace(0, 2*numpy.pi, 100)
    theta = numpy.linspace(0, numpy.pi, 100)
    # earth coordinates
    x = earthRadius*numpy.cos(phi)
    y = earthRadius*numpy.sin(phi)
    pyplot.plot(x, y)
    pyplot.savefig('earth')

    # B-field
    #B = numpy.arange

if __name__ == '__main__':
    main()
else:
    print "I was imported as a module!"
