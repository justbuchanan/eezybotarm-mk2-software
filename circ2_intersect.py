#!/usr/bin/env python2

from __future__ import print_function
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
from sympy.geometry import *

# get the intersection points of two circles
# tiny wrapper over sympy geometry
def circ2_intersect(p0, r0, p1, r1):
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
