#!/usr/bin/python

import json
from urllib2 import urlopen
import datetime
import os.path

data_path = os.path.expanduser('~/bus/data')
url = 'http://dieselnet.cs.umass.edu/bus_plotter'
#routes = ['31', '45']
routes = None # All routes


f = urlopen(url)
d = json.loads(f.read())
#print json.dumps(d, sort_keys=True, indent=4)

for b in d['unitList']:
        lat, lon = b['gps']['latitude'], b['gps']['longitude']
        route = b['schedule']['route_id']
        time = b['gps']['check_in_time']
        bus_n = b['vehicle']['bus_number']

        if time is None: continue
        if routes is not None and route not in routes: continue

        p = os.path.join(data_path, 'route%s' % route)
        if not os.path.isdir(p):
                os.makedirs(p)

        f = open(os.path.join(p, datetime.date.today().strftime('%Y%m%d')), 'a')
        f.write('%5s\t%5s\t%20d\t%2.10f\t%2.10f\n' % (bus_n, route, time, lat, lon))

