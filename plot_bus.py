#!/usr/bin/python

from matplotlib import pyplot as pl
import numpy as np
from numpy import min, max, pi
import sys
from bus_utils import Rearth, read_bus_data

plot_stops = False
bin_dist = 10  # meters
bin_width = bin_dist / Rearth * 180 / pi  # degrees

d = read_bus_data()

pl.gray()
pl.scatter(d['lat'], d['lon'], c=np.arange(len(d)))
pl.savefig('bus.png')

