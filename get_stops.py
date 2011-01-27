#!/usr/bin/python

from urllib2 import urlopen
import re
import json

url = 'http://dieselnet.cs.umass.edu/stops/get_stops'

stops = {}
lat = None
lon = None
name = None
for l in urlopen(url).readlines():
        m = re.match("\s*lat\s*=\s*parseFloat\((\d+\.\d+)\);", l)
        if m: lat = float(m.group(1))

        m = re.match("\s*lon\s*=\s*-parseFloat\((\d+\.\d+)\);", l)
        if m: lon = float(m.group(1))
        
        m = re.match("\s*name\s*=\s*'([\w\s\(\)]+)';", l)
        if m: name = m.group(1)

        m = re.match("\s*loc\s*=\s*", l)
        if m:
                m = re.search('(\d+)', l)
                id = m.group(1)
                stops[id] = (name,lat,lon)

json.dump(stops, open('stops','w'), indent=2)
