'''
Adapted from Charles Leifer's website.
http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/
Which is presumably public domain.

Imagine RGB values are points in 3d space. This algorithm tries to find the
heaviest cluster by starting at a random point and iterating.

'''
from __future__ import division
from collections import namedtuple
from math import sqrt
import random
from PIL import Image
from colorsys import hsv_to_rgb
from zlib import adler32
from numpy import std

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points


def colorz(img, n=1):
    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return rgbs

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
        ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters

def deterministic_colour(*args):
    '''Produces a weighted deterministic colour'''
    seed = unicode(args)

    # faster than crc32
    hue = adler32(seed) % 256
    sat = 128
    val = 200

    rgb = hsv_to_rgb(hue/255,sat/255,val/255)

    return map(lambda v: int(v*255),rgb)


def get_significant_colour(img):
    'the most distinctive out of the primary and secondary colours'
    rgbs = colorz(img,2)
    rgbs.sort(key=std)
    return rgbs[-1]
