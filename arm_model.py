#!/usr/bin/env python2

import numpy as np
from math import *
from circ2_intersect import *

"""
rough diagram:

      L4  L3
  p4     p2 p3
  _*-----*--*
    L1  /  / L2
       /  / 
   p0 *--* p1
       L5
theta0    theta1


-----> angle of 0
"""


def vec_dir(theta):
    v = np.array([cos(theta), sin(theta)])
    return v / np.linalg.norm(v)

# units are in m
m = 1.0
mm = m / 1000

# model params
# TODO: pull these from cad, not half-assed measurements
L1 = 135 * mm
L2 = 135 * mm
L3 = 56 * mm
L4 = 147 * mm
L5 = 62 * mm

# state
theta0 = 3*pi / 4
theta1 = pi / 4

p0 = np.array([0, 0])
p1 = p0 + vec_dir(theta1) * L5
p2 = p0 + L1 * vec_dir(theta0)
i = circ2_intersect(p1, L2, p2, L3)
p3 = max(i, key=lambda p: p[0]) # right-most circle-circle intersection
p3 = np.array(p3)
print(i)
print('p0: %s' % str(p0))
print('p1: %s' % str(p1))
print('p2: %s' % str(p2))
print('p3: %s' % str(p3))
d = p2 - p3
d = np.array([float(d[0]), float(d[1])])
p4 = d * L4 + p2
# d = np.transpose(d)
# print('d: %s' % str(d))
# p4 = np.linalg.norm(np.array([float(d[0]), float(d[1])]))
# p4 = np.array([-0.5, -0.2]) * L4 + p2
print('p4: %s' % str(p4))
