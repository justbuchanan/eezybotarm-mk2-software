#!/usr/bin/env python2

import numpy as np
from sympy.solvers import solve
from sympy import Symbol

def circ2_intersect(p0, r0, p1, r1):
    x, y = Symbol('x'), Symbol('y')
    # give the equations of both circles and solve for x and y, giving the two
    # intersection points as (x,y) pairs
    s1, s2 = solve([
        (x - p0[0])**2 + (y-p0[1])**2 - r0**2,
        (x - p1[0])**2 + (y - p1[1])**2 - r1**2],
        x, y)
    return [s1, s2]


if __name__ == '__main__':
    s = circ2_intersect(np.array([0, 0]), 4, np.array([3, 3]), 2)
    s2 = []
    for x in s:
        x = [float(i) for i in x]
        s2.append(x)
    s = s2

    print(s)
