#!/usr/bin/python2.7

import xml.etree.ElementTree as ET
from urllib2 import urlopen
import datetime
from time import time
import os.path

data_path = os.path.expanduser('~/bus/data')
uts_url = 'http://uts.pvta.com:81/InfoPoint/map/GetVehicleXml.ashx?RouteId=%s'
ntf_url = 'http://ntf.pvta.com:81/InfoPoint/map/GetVehicleXml.ashx?RouteId=%s'
routes = {}
routes.update({ r: uts_url%r for r in ['30', '31', '38', '39', '45', '46'] })
routes.update({ r: ntf_url%r for r in ['B43', 'R41', 'M40'] })

def fetch_route_vehicles(url):
        f = urlopen(url)
        d = ET.fromstring(f.read())

        vehicles = []
        for b in d:
                lat, lon = float(b.attrib['lat']), float(b.attrib['lng'])
                bus_n = b.attrib['name']
                vehicles.append((bus_n, (lat,lon)))

        return vehicles

for route,url in routes.items():
        vehicles = fetch_route_vehicles(url)
        t = time()

        p = os.path.join(data_path, 'route%s' % route)
        if not os.path.isdir(p):
                os.makedirs(p)

        f = open(os.path.join(p, datetime.date.today().strftime('%Y%m%d')), 'a')
        for (bus_n, (lat,lon)) in vehicles:
                f.write('%5s\t%5s\t%20d\t%2.10f\t%2.10f\n' % (bus_n, route, t, lat, lon))

