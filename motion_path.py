#!/usr/bin/env python2

import numpy as np
from arm_model import *
from math import *
import time
import sys
from calibration import *
from arm_driver import *


# waypoints is an array of (base, grip_x, grip_y) tuples
def path_from_waypoints(waypoints, steps_per_m=10000):
    path = []

    for i in range(len(waypoints) - 1):
        a = waypoints[i]
        b = waypoints[i+1]
        print('%s -> %s' % (str(a), str(b)))

        delta = b - a
        dist = norm(delta)
        if dist == 0:
            continue
        direc = delta / dist

        dist_vals = np.linspace(0, dist, num=int(steps_per_m * dist))

        path += [a + direc * d for d in dist_vals]

    return path


def plot_path(path):
    import matplotlib.pyplot as plt
    plt.title('Gripper path')
    plt.xlabel('x')
    plt.ylabel('y')
    xx = [p[1] for p in path]
    yy = [p[2] for p in path]
    plt.plot(xx, yy, color='b', label='path')
    plt.legend()
    plt.show()




if __name__ == '__main__':
    waypoints = [
        # np.array([pi/4, -0.15, -0.02]),
        np.array([0, -0.15, -0.02]),
        np.array([0, -0.13, 0]),
        np.array([0, -0.15, 0.04]),
    ]
    path = path_from_waypoints(waypoints)

    # print(path)
    # plot_path(path)
    # exit() 

    arm = Arm()

    state = [0,0,0]
    while True:
        for p in path:
            state[0] = calc_base_servo_cmd(p[0])

            grip_pos = p[1:3]

            print("gripper: %s" % str(grip_pos))

            thetas = arm_model.inverse_2d(grip_pos)
            arm_cmds = calc_arm_servos(thetas)
            state[1:3] = arm_cmds

            state = clip_servos(state)
            state = [int(s) for s in state]

            arm.set_servo_values(state)
            time.sleep(0.001)

        path.reverse()
