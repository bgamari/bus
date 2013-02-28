#!/usr/bin/python

import xml.etree.ElementTree as ET
from urllib2 import urlopen
import datetime
from time import time
import os.path

data_path = os.path.expanduser('~/bus/data')
url = 'http://uts.pvta.com:81/InfoPoint/map/GetVehicleXml.ashx?RouteId=%s'
routes = ['30', '31', '38', '39', '45', '46']

def fetch_route_vehicles(route):
        f = urlopen(url % route)
        d = ET.fromstring(f.read())

        vehicles = []
        for b in d:
                lat, lon = float(b.attrib['lat']), float(b.attrib['lng'])
                bus_n = b.attrib['name']
                vehicles.append((bus_n, (lat,lon)))

        return vehicles

for route in routes:
        vehicles = fetch_route_vehicles(route)
        t = time()

        p = os.path.join(data_path, 'route%s' % route)
        if not os.path.isdir(p):
                os.makedirs(p)

        f = open(os.path.join(p, datetime.date.today().strftime('%Y%m%d')), 'a')
        for (bus_n, (lat,lon)) in vehicles:
                f.write('%5s\t%5s\t%20d\t%2.10f\t%2.10f\n' % (bus_n, route, t, lat, lon))

