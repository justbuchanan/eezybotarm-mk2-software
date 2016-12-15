#!/usr/bin/env python2

import numpy as np
from math import *
import arm_model
import os
import yaml
import logging

def clip(x, minval, maxval):
    if x > maxval:
        return maxval
    elif x < minval:
        return minval
    else:
        return x

CALIBRATION_FILE = 'calibration.yml'
if os.path.exists(CALIBRATION_FILE):
    SERVO_LIMITS = yaml.load(open(CALIBRATION_FILE, 'r'))['limits']
    logging.info("Loaded servo limits from '%s'" % CALIBRATION_FILE)
else:
    logging.warning("No calibration file found at '%s', using (0, 180) for all" % CALIBRATION_FILE)
    SERVO_LIMITS = [{'min': 0, 'max': 180}] * arm_model.NUM_SERVOS

def limit_servos(servos):
    for i in range(arm_model.NUM_SERVOS):
        l = SERVO_LIMITS[i]
        servos[i] = clip(servos[i], l['min'], l['max'])
    return servos



# note: this completely ignores the rotational servo in the base

cmd1 = np.array([110.0, 100.0])
Y0 = np.array([-.108, 0])

cmd2 = np.array([150.0, 180.0])
Y1 = np.array([-.21, -0.01])


# hack in a differnt point2
cmd3 = np.array([105, 170])
Y2 = np.array([-0.16, 0.09])
cmd2, Y1 = cmd3, Y2

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
    # print(m)

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
