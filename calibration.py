#!/usr/bin/env python2

import numpy as np
from math import *
import arm_model

# note: this completely ignores the rotational servo in the base

cmd1 = np.array([110, 100])
Y1 = np.array([-.108, 0])

cmd2 = np.array([110, 180])
Y2 = np.array([-.185, .08])

# each X is an array of two theta values
state1 = arm_model.inverse_2d(Y1)
state2 = arm_model.inverse_2d(Y2)

# state2cmd = 

# servo1 of 110 corresponds to theta1 of state1[0]
# servo2 of 100 corresponds to theta2 of state1[1]


# calculate servo values from angle values
def calc_arm_servos(thetas):
    m = (cmd1 - state1) / (cmd2 - state2)

    cmd = cmd1 + m * (thetas - state1)
    return cmd
