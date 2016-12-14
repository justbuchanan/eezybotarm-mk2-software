#!/usr/bin/env python2

# Program for using the SpaceNavigator 3d mouse with the EEZYbotARM.
# Note: make sure spacenavd is running before starting this

from __future__ import print_function
from spnav import *
import signal
import sys
import serial
import time
import arm_model
import numpy as np
from calibration import *
from arm_driver import *

import argparse
parser = argparse.ArgumentParser('Control eezybotarm mk2 with a spacenav mouse')
parser.add_argument('--dumb', action='store_true', help='dumb controls')
parser.add_argument('device_path', type=str, default='/dev/arduino')
args = parser.parse_args()



# exit gracefully
def on_signal(signum, frame):
    print('Ctrl+C received, exiting...')
    spnav_close()
    sys.exit(0)
signal.signal(signal.SIGINT, on_signal)


def latest_event():
    event = None
    while True:
        event2 = spnav_poll_event()
        if event2:
            event = event2
        else:
            break
    return event

arm = Arm(args.device_path, 9600)

lastCmdTime = time.time()
CMD_FREQ = 20 # Hz

spnav_open()


closed = False
state = [80, 110, 100, 180]
grip_pos = np.array([-0.1, 0.05])

while True:
    event = latest_event()
    # if event:
        # print('event: %s' % str(event))
    if event and event.ev_type == SPNAV_EVENT_MOTION:
        # print('event')
        t, r = event.translation, event.rotation
        state[0] = calc_base_servo_cmd(-r[1] / 350.0 * pi/4)
        state[1] = 110 - t[2] / 350.0 * 90
        state[2] = 100 + t[1] / 350.0 * 90
        # print('state: %s' % str(state))

        grip_pos = np.array([-0.1, 0.05]) + np.array([-t[2] / 350.0 * .1, t[1] / 350.0 * .1])

    if event and event.ev_type == SPNAV_EVENT_BUTTON:
        closed = event.bnum == 0 and event.press


    # send commands at CMD_FREQ Hz
    now = time.time()
    dt = now - lastCmdTime
    if dt > 1.0 / CMD_FREQ:
        state[3] = 100 if closed else 180

        print("gripper: %s" % str(grip_pos))

        if not args.dumb:
            thetas = arm_model.inverse_2d(grip_pos)
            if thetas != None:
                arm_cmds = calc_arm_servos(thetas)
                state[1:3] = arm_cmds

        state = clip_servos(state)
        state = [int(s) for s in state]
        # state[3] = 180 # safety override. TODO remove
        arm.set_servo_values(state)

        lastCmdTime = now
        print("cmd: ", end='')
        print(state)
