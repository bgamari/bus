#!/usr/bin/python

from matplotlib import pyplot as pl
from matplotlib.widgets import Cursor
import numpy as np
from numpy import min, max, pi
import sys
from time import time
from bus_utils import Rearth, read_bus_data

bin_dist = 10  # meters
bin_width = bin_dist / Rearth * 180 / pi  # degrees

d = read_bus_data()

bins = ((max(d['lat'])-min(d['lat'])) / bin_width,
        (max(d['lon'])-min(d['lon'])) / bin_width)
H,xedges,yedges = np.histogram2d(d['lat'], d['lon'], bins=bins)

extent = (yedges[0], yedges[-1], xedges[-1], xedges[0])
H = np.log1p(H) # Log makes data much clearer

class LineBuilder(object):
        def __init__(self, axes):
                self.axes = axes
                self.line = None
                self.xs = []
                self.ys = []
                axes.figure.canvas.mpl_connect('button_press_event', self.press)
                axes.figure.canvas.mpl_connect('button_release_event', self.release)

        def press(self, event):
                self.press_time = time()

        def release(self, event):
                if time() - self.press_time > 0.2: return
                if event.inaxes != self.axes: return

                if event.button == 1:
                        self.xs.append(event.xdata)
                        self.ys.append(event.ydata)
                elif event.button == 3:
                        if len(self.xs) == 0: return
                        self.xs.pop()
                        self.ys.pop()

                if self.line is not None and len(self.xs) == 0:
                        self.line.remove()
                        self.line = None
                elif self.line is None:
                        self.line, = self.axes.plot(self.xs, self.ys, 'r-o')
                elif self.line is not None and len(self.xs) > 0:
                        self.line.set_data(self.xs, self.ys)

                self.axes.figure.canvas.draw()

fig = pl.figure()
ax = fig.add_subplot(111)
ax.imshow(H, extent=extent, interpolation='nearest')
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
linebuilder = LineBuilder(ax)
if len(sys.argv) > 1:
        d = np.genfromtxt(open(sys.argv[1]), names='x,y')
        self.xs.extend(d['x'])
        self.ys.extend(d['y'])

pl.show()

for x,y in zip(linebuilder.xs, linebuilder.ys):
        print '%1.8f\t%1.8f' % (x, y)

