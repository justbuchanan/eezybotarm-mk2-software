#!/usr/bin/env python2

import numpy as np
from math import *
import arm_model

# note: this completely ignores the rotational servo in the base

cmd1 = np.array([110.0, 100.0])
Y0 = np.array([-.108, 0])

cmd2 = np.array([150.0, 180.0])
Y1 = np.array([-.21, -0.01])

# each X is an array of two theta values
state0 = arm_model.inverse_2d(Y0)
state1 = arm_model.inverse_2d(Y1)


# TODO: unify this with the arm servo calibration
def calc_base_servo_cmd(theta):
    # 60 -> 0
    # 155 -> pi/4

    m = (155 - 60) / (pi/4 - 0)
    return 60 + m * (theta - 0)

# servo1 of 110 corresponds to theta1 of state0[0]
# servo2 of 100 corresponds to theta2 of state0[1]

# calculate servo values from angle values
def calc_arm_servos(thetas):
    m = (cmd2 - cmd1) / (state1 - state0)
    print(m)

    cmd = cmd1 + m * (thetas - state0)
    return cmd


def draw_calibration_curve():
    import matplotlib.pyplot as plt
    plt.ylabel('Servo cmd')
    plt.xlabel('Angle')
    t0 = np.linspace(0, 2*pi, num=20)
    t1 = np.linspace(0, 2*pi, num=20)
    plt.plot(t0, [calc_arm_servos([t, 0])[0] for t in t0], color='b', label='Servo 1')
    plt.plot(t1, [calc_arm_servos([0, t])[1] for t in t1], color='g', label='Servo 2')
    plt.legend()
    plt.title('Arm angle -> servo mapping')
    # plt.plot(t1)
    plt.show()

if __name__ == '__main__':
    print('state0: %s' % str(state0))
    print('state1: %s' % str(state1))
    draw_calibration_curve()
