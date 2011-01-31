#!/usr/bin/python

from matplotlib import pyplot as pl
import numpy as np
from numpy import min, max, pi
import sys

plot_stops = False
Rearth = 6400e3  # meters
bin_dist = 10  # meters
bin_width = bin_dist / Rearth * 180 / pi  # degrees

dt = [('bus_n', '5a'), ('route', '5a'), ('time', 'u8'), ('lat', 'f'), ('lon', 'f')]
d = np.genfromtxt(sys.stdin, dtype=dt)

pl.gray()
pl.scatter(d['lat'], d['lon'], c=np.arange(len(d)))
pl.show()

