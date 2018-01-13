#!/usr/bin/env python2

from __future__ import print_function
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
from sympy.geometry import *
from math import *


# borrowed from: https://gist.github.com/xaedes/974535e71009fa8f090e
def circ2_intersect_github(p0, r0, p1, r1):
    '''
    @summary: calculates intersection points of two circles
    @param circle1: tuple(x,y,radius)
    @param circle2: tuple(x,y,radius)
    @result: tuple of intersection points (which are (x,y) tuple)
    '''
    # http://stackoverflow.com/a/3349134/798588
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = sqrt(dx * dx + dy * dy)
    if d > r0 + r1:
        # print "#1"
        return None  # no solutions, the circles are separate
    if d < abs(r0 - r1):
        # print "#2"
        return None  # no solutions because one circle is contained within the other
    if d == 0 and r0 == r1:
        # print "#3"
        return [
        ]  # circles are coincident and there are an infinite number of solutions

    a = (r0 * r0 - r1 * r1 + d * d) / (2 * d)
    h = sqrt(r0 * r0 - a * a)
    xm = p0[0] + a * dx / d
    ym = p0[1] + a * dy / d
    xs1 = xm + h * dy / d
    xs2 = xm - h * dy / d
    ys1 = ym - h * dx / d
    ys2 = ym + h * dx / d

    return np.array([xs1, ys1]), np.array([xs2, ys2])


# get the intersection points of two circles
# tiny wrapper over sympy geometry
def circ2_intersect(p0, r0, p1, r1):
    return circ2_intersect_github(p0, r0, p1, r1)


def circ2_intersect_sympy(p0, r0, p1, r1):
    c1 = Circle(Point(p0[0], p0[1], evaluate=False), r0)
    c2 = Circle(Point(p1[0], p1[1], evaluate=False), r1)
    ss = intersection(c1, c2)
    ss = [np.array([float(s[0]), float(s[1])]) for s in ss]
    return ss


if __name__ == '__main__':
    for i in range(120):
        ss = circ2_intersect(np.array([0, 0]), 2, np.array([0, 3]), 2)
        ss = [np.array(s) for s in ss]
        print(ss)
