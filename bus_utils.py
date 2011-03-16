import sys
import numpy as np
from numpy.linalg import norm
from numpy import pi, array, dot, sqrt, transpose, cos, arccos

# Maximum distance between point and path for point to be consider to be on path
on_path_thresh = 5  # meters

# Radius of Earth
Rearth = 6371e3  # meters

def read_bus_data(f=sys.stdin):
        dt = [('bus_n', '5a'), ('route', '5a'), ('time', 'u8'), ('lat', 'f'), ('lon', 'f')]
        data = np.genfromtxt(f, dtype=dt)
        return sanitize_data(data)

def sanitize_data(data):
        lat,lon = data['lat'], data['lon']
        return data[np.logical_and(np.logical_and(lon > 72.35, lon < 72.55),
                                   np.logical_and(lat > 42.30, lat < 42.45))]

def latlon_to_3vec(v):
        """ Convert a record array of lat/lons in degrees into an array of
            3-vectors in spherical coordinates """
        R = [Rearth]*len(v)
        lat = v['lat']*pi/180
        lon = v['lon']*pi/180
        return transpose(np.vstack([R,lat,lon]))

def great_circle_dist(a, b):
        """ Compute distance between two points on sphere.
            Points a and b given as 3-vectors, distance in meters """
        a = array(a); b = array(b)
        # Normalize
        a = [ v/norm(v) for v in a ]
        b = [ v/norm(v) for v in b ]
        print a
        alpha = arccos(np.sum(a*b, axis=0))
        print alpha
        return alpha*Rearth

def great_circle_normal(a, b):
        """ Find unit normal to great circle defined by a and b, given as
            3-vectors. This returns a normalized three-vector. """
        n = np.cross(array(a), array(b))
        return n/norm(n)

def point_path_dist(a, b, p):
        """ Find the shortest distance between the great circle connecting a
            and b and the point p, all given as 3-vectors. Distance given in
            meters """
        n = great_circle_normal(a, b)
        alpha = np.arccos(dot(n, p/norm(p)))
        return Rearth*(pi/2-alpha)

def point_path_arclen(a, b, p):
        """ Compute the arc length from point a to the projection of point p onto
            the great circle defined by points a and b """
        n = great_circle_normal(a, b)
        v = proj_point_on_plane(n, p)
        alpha = np.arccos(dot(a, v))
        return Rearth*alpha

def proj_point_on_plane(n, v):
        """ Project a vector v into the plane defined by unit normal n """
        return v - dot(n, v)*n

def point_to_arclen(path, p):
        """ Map a point p to a distance along path """
        dists = [ point_path_dist(a, b, p) for a,b in zip(path[:-1], path[1:]) ]
        idx = np.argmin(dists)
        if dists[idx] > on_path_thresh:
                return None

        dist = 0
        for i in range(0,idx-1):
                dist += great_circle_dist(path[i], path[i+1])

        dist += point_path_arclen(path[idx], path[idx+1], p)
        return dist

