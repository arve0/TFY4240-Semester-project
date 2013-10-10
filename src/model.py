#!/usr/bin/env python
'A model of the earth and its magnetic field, with earth center as origin.'

import numpy
import matplotlib
matplotlib.use('pdf')         # save figures as pdf
from matplotlib import pyplot # pyplot as command

def cartesianX(r,phi,theta):
    'Calculate cartesian coordinates from sperical coordinates. Returns x.'
    x = r*numpy.sin(theta)*numpy.cos(phi)
    return x

def cartesianY(r,phi,theta):
    'Calculate cartesian coordinates from sperical coordinates. Returns y.'
    y = r*numpy.cos(theta)*numpy.sin(phi)
    return y

def cartesianZ(r,phi,theta):
    'Calculate cartesian coordinates from sperical coordinates. Returns z.'
    z = r*numpy.cos(theta)
    return z

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
    X = numpy.linspace(0,earthRadius,100)
    X, Y = numpy.meshgrid(X, X)
    Y = numpy.linspace(0,earthRadius,100)
    Z = array([],[])
    earthX = numpy.vectorize(cartesianX)
    earthY = numpy.vectorize(cartesianY)
    earthZ = numpy.vectorize(cartesianZ)
    x = earthX(earthRadius, phi, theta)
    y = earthY(earthRadius, phi, theta)
    z = earthZ(earthRadius, phi, theta)
    pyplot.contour(x, y, z)
    pyplot.savefig()

if __name__ == '__main__':
    main()
else:
    print "I was imported as a module!"
