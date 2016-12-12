#!/usr/bin/env python2

import numpy as np
from arm_model import *


def path_from_waypoints(waypoints, steps_per_m=1000):
    path = []

    for i in range(len(waypoints) - 1):
        a = waypoints[i]
        b = waypoints[i+1]

        delta = b - a
        dist = norm(delta)
        direc = delta / dist

        dist_vals = np.linspace(0, dist, num=int(steps_per_m * dist))

        path += [a + direc * d for d in dist_vals]

    return path



if __name__ == '__main__':
    waypoints = [
        np.array([-0.15, -0.2]),
        np.array([-0.1, 0]),
        np.array([-0.5, 4]),
    ]
    path = path_from_waypoints(waypoints)

    print(path)

