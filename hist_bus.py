from matplotlib import pyplot as pl
import numpy as np
from numpy import min, max, pi

bus_ns = ['3113']
plot_stops = False
Rearth = 6400e3  # meters
bin_dist = 10  # meters
bin_width = bin_dist / Rearth * 180 / pi  # degrees

dt = [('bus_n', '5a'), ('time', 'u8'), ('lat', 'f'), ('lon', 'f')]
d = np.genfromtxt('h', dtype=dt)
if bus_ns:
        mask = np.zeros_like(d['time'])
        for b in bus_ns:
                mask = np.logical_or(mask, d['bus_n'] == b)
        d = d[mask]

bins = ((max(d['lat'])-min(d['lat'])) / bin_width,
        (max(d['lon'])-min(d['lon'])) / bin_width)
H,xedges,yedges = np.histogram2d(d['lat'], d['lon'], bins=bins)

extent = (yedges[0], yedges[-1], xedges[-1], xedges[0])
H = np.log1p(H) # Log makes data much clearer

pl.imshow(H, extent=extent, interpolation='nearest')
pl.colorbar()
if plot_stops:
        import json
        stops = json.load(open('stops'))
        for name,lat,lon in stops.values():
                #pl.annotate(name, (lon,lat), color='white')
                pl.plot([lon], [lat], 'o', color='white', alpha=0.5)

pl.show()

