#!/usr/bin/env python2

from sympy import *
import numpy as np
# from math import *
from circ2_intersect import *

"""
# rough diagram:

      L4  L3
  p4     p2 p3
  _*-----*--*
    L1  /  / L2
       /  / 
   p0 *--* p1
       L5
theta0    theta1


# Coordinate system:

y axis
^
|
|
|--------> x axis (and theta == 0)
"""


# returns a unit vector in the direction of the given angle
def vec_dir(theta):
    v = np.array([cos(theta), sin(theta)])
    nrm = sqrt(v[0]**2 + v[1]**2)
    # nrm = np.linalg.norm(v)
    return v / nrm

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

# calculate the end-effector position (p4) from the angles of the two arm servos
def forward(theta0, theta1):
    p0 = np.array([0, 0])
    p1 = p0 + vec_dir(theta1) * L5
    p2 = p0 + L1 * vec_dir(theta0)
    i = circ2_intersect(p1, L2, p2, L3)
    p3 = max(i, key=lambda p: p[0]) # right-most circle-circle intersection
    p3 = np.array(p3)
    d = p2 - p3
    p4 = d * L4 + p2
    return p4


# given the position of the end-effector, return the angles of the two arm servos
# note: ignores the rotation of the base
def inverse_2d(p4):
    p0 = np.array([0, 0])

    p2 = max(circ2_intersect(p4, L4, p0, L1), key=lambda p: p[1]) # top-most intersection point

    theta0 = atan2(p2[1] - p0[1], p2[0] - p0[0])

    d = p2 - p4
    d = np.array([float(d[0]), float(d[1])])
    p3 =  d / np.linalg.norm(d) * L3 + p2
    p1 = max(circ2_intersect(p3, L2, p0, L5), key=lambda p: p[0])
    theta1 = atan2(p1[1] - p0[1], p1[0] - p0[0])

    return float(theta0), float(theta1)


if __name__ == '__main__':
    x = inverse_2d(p4 = np.array([-0.15, 0.03]))
    print(x)
