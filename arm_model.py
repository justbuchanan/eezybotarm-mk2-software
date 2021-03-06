#!/usr/bin/env python2

# from sympy import *
import numpy as np
from math import *
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

note: end effector x value is usually (always?) negative
"""

NUM_SERVOS = 4

# mapping of which points to draw lines between
LINE_MAPPING = [
    (0, 2),  # line between p0 and p2
    (0, 1),
    (1, 3),
    (3, 4),
]


def norm(v):
    return np.linalg.norm(v)
    # return sqrt(v[0]**2 + v[1]**2)


# returns a unit vector in the direction of the given angle
def vec_dir(theta):
    v = np.array([cos(theta), sin(theta)])
    nrm = norm(v)
    return v / nrm


# units are in m
m = 1.0
mm = m / 1000

# model params
# TODO: pull these from cad, not half-assed measurements
L1 = 135 * mm
L2 = 135 * mm
L3 = 58 * mm
L4 = 147 * mm
L5 = 62 * mm

SERVO_LIMITS = [
    (0, 180),
    (80, 180),
    (100, 180),
]


# calculate the end-effector position (p4) from the angles of the two arm servos
def forward(thetas):
    try:
        p0 = np.array([0, 0])
        p1 = p0 + vec_dir(thetas[1]) * L5
        p2 = p0 + L1 * vec_dir(thetas[0])
        i = circ2_intersect(p1, L2, p2, L3)
        p3 = max(
            i, key=lambda p: p[0])  # right-most circle-circle intersection
        # if p3 is below p2, we've found an invalid solution and this configuration isn't possible
        if p3[1] < p2[1]: return None
        p3 = np.array(p3)
        d = p2 - p3
        p4 = d / norm(d) * (L4) + p2
        return [p0, p1, p2, p3, p4]
    except TypeError as e:
        return None


# given the position of the end-effector, return the angles of the two arm servos
# note: ignores the rotation of the base
def inverse_2d(p4):
    try:
        p0 = np.array([0, 0])

        p2 = max(
            circ2_intersect(p4, L4, p0, L1),
            key=lambda p: p[1])  # top-most intersection point

        theta0 = atan2(p2[1] - p0[1], p2[0] - p0[0])

        d = p2 - p4
        d = np.array([float(d[0]), float(d[1])])
        p3 = d / np.linalg.norm(d) * L3 + p2
        p1 = max(circ2_intersect(p3, L2, p0, L5), key=lambda p: p[0])
        theta1 = atan2(p1[1] - p0[1], p1[0] - p0[0])

        return np.array([theta0, theta1])
    except TypeError as e:
        return None


if __name__ == '__main__':
    for i in range(60):
        x = inverse_2d(p4=np.array([-0.15, 0.03]))
        print(x)
