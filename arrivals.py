#!/usr/bin/python

import json
import numpy as np
from math import pi
import sys
from datetime import datetime
from bus_utils import read_bus_data, great_circle_dist, Rearth, latlon_to_3vec

thresh = 50   # meters

stops = json.load(open('stops'))
data = read_bus_data()

#for d in latlon_to_3vec(data): print d/np.linalg.norm(d)

for name,lat,lon in stops.values():
        dist = great_circle_dist(latlon_to_3vec(data), [(Rearth, lat*pi/180, lon*pi/180)]*len(data))
        arrivals = dist < thresh
        if np.any(arrivals):
                # times are in milliseconds past epoch; go figure
                times = map(datetime.fromtimestamp, data['time'][arrivals]/1e3)
                bus_ns = data['bus_n'][arrivals]

                print name
                print '\n'.join(('%s\t%s' % (n,t.isoformat(' ')) for n,t in zip(bus_ns,times)))
                print

