#!/usr/bin/env python2

import numpy as np
from arm_model import *
from math import *
import time
import sys
from calibration import *
from arm_driver import *
import matplotlib.pyplot as plt


# waypoints is an array of (base, grip_x, grip_y) tuples
def path_from_waypoints(waypoints, steps_per_m=5000):
    path = []

    for i in range(len(waypoints) - 1):
        a = waypoints[i]
        b = waypoints[i+1]
        # print('segment\n-----------------------------')
        # print('%s -> %s' % (str(a), str(b)))

        delta = b - a
        dist = norm(delta)
        if dist == 0:
            # print('zero len')
            continue
        direc = delta / dist

        stepcount = np.matmul(abs(delta), np.array([0.1, 1.0, 1.5]) * steps_per_m)
        # print('stepcount: %d' % stepcount)
        dist_vals = np.linspace(0, dist, num=stepcount)

        segment = [a + direc * d for d in dist_vals]
        path += segment

    return path




def plot_path(path):
    ii = list(range(len(path)))
    xx = [p[1] for p in path]
    yy = [p[2] for p in path]

    plt.subplot(3, 1, 1)
    plt.title('Gripper path')
    plt.xlabel('step')
    plt.ylabel('position (m)')
    plt.plot(ii, xx, color='b', label='x')
    plt.plot(ii, yy, color='g', label='y')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.title('Servo angles')
    plt.ylabel('Radians')
    plt.xlabel('step')
    thetas = [arm_model.inverse_2d(path[i][1:3]) for i in range(len(path))]
    plt.plot(ii, [tt[0] for tt in thetas], color='r', label='theta0')
    plt.plot(ii, [tt[1] for tt in thetas], color='r', label='theta1')

    plt.subplot(3, 1, 3)
    servos = [endpoint_state_to_servos(p) for p in path]
    def plot_servos(servos):
        plt.title('Servo values')
        ii = list(range(len(servos)))
        plt.plot(ii, [s[1] for s in servos], color='b', label='s1')
        plt.plot(ii, [s[2] for s in servos], color='g', label='s2')
        plt.legend()

    plot_servos(servos)

    plt.show()



# @param p (base_angle, grip_x, grip_y)
def endpoint_state_to_servos(p):
    grip_pos = p[1:3]

    # calculate servo angles needed to put the gripper at @grip_pos
    thetas = arm_model.inverse_2d(grip_pos)

    # calulate the servo values to put the servos at the desired angles
    arm_servos = calc_arm_servos(thetas)
    base = calc_base_servo_cmd(p[0])
    servos = [base, arm_servos[0], arm_servos[1]]

    servos = clip_servos(servos)
    servos = [int(s) for s in servos]

    return servos


def run_waypoints(arm, waypoints, speed):
    # dt = 1.0 / 60
    dt = 1.0 / 10
    steps_per_m = 1 / (speed * dt)
    path = path_from_waypoints(waypoints, steps_per_m)

    plot_path(path + list(reversed(path)))
    sys.exit()
    # return

    while True:
        for p in path:
            state = endpoint_state_to_servos(p)
            arm.set_servo_values(state)
            # print(state)

            time.sleep(dt)



if __name__ == '__main__':
    waypoints = [
        # np.array([pi/4, -0.15, -0.02]),
        np.array([pi/4, -0.12, 0.0]),
        np.array([-pi/4, -0.12, 0.0]),
        # np.array([-pi/4, -0.12, 0.0]),
        np.array([0, -0.12, 0.0]),
        np.array([0, -0.15, 0.01]),
        np.array([0, -0.15, -0.02]),
        # np.array([0, -0.06, 0.1]),
    ]

    arm = Arm()
    speed = 0.04
    # speed = 0.1

    # plot_path(path_from_waypoints())

    # while True:
    run_waypoints(arm, waypoints, speed)
    run_waypoints(arm, list(reversed(waypoints)), speed)
