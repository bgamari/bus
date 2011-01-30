#!/usr/bin/python

import json
import numpy
from math import pi
import sys
from datetime import datetime

thresh = 50   # meters

stops = json.load(open('stops'))

dt = [('bus_n', '5a'), ('route', '5a'), ('time', 'u8'), ('lat', 'f'), ('lon', 'f')]
data = numpy.genfromtxt(sys.stdin, dtype=dt)

data['lat'] *= pi/180
data['lon'] *= pi/180

def distance(lat1, lon1, lat2, lon2):
        """ Compute distance between two points with haversine formula.
            Angles are of course in radians, distance in kilometers """
        from numpy import sin, cos, arctan2, sqrt
        R = 6371   # kilometers
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2*arctan2(sqrt(a), sqrt(1-a))
        return R*c

for name,lat,lon in stops.values():
        lat *= pi/180; lon *= pi/180
        dist = distance(data['lat'], data['lon'], lat, lon)
        arrivals = dist < thresh*1e-3
        if any(arrivals):
                # times are in milliseconds past epoch; go figure
                times = map(datetime.fromtimestamp, data['time'][arrivals]/1e3)
                bus_ns = data['bus_n'][arrivals]

                print name
                print '\n'.join(('%s\t%s' % (n,t.isoformat(' ')) for n,t in zip(bus_ns,times)))
                print

