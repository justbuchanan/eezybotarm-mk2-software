#!/usr/bin/env python2

# TODO: /dev/ttyACM0 should be accessible without sudo

from __future__ import print_function
from spnav import *
import signal
import sys
import serial
import time
import arm_model
import numpy as np
from calibration import *


# exit gracefully
def on_signal(signum, frame):
    print('Ctrl+C received, exiting...')
    spnav_close()
    sys.exit(0)
signal.signal(signal.SIGINT, on_signal)


port = sys.argv[1]

arduino = serial.Serial(port, 9600, timeout=1)
time.sleep(1)

MAGIC = 200
msg = [MAGIC, 80, 110, 100]

lastCmdTime = time.time()
CMD_FREQ = 20 # Hz

def clip(x, minval, maxval):
    if x > maxval:
        return maxval
    elif x < minval:
        return minval
    else:
        return x


spnav_open()


def latest_event():
    event = None
    while True:
        event2 = spnav_poll_event()
        if event2:
            event = event2
        else:
            break
    return event


t, r = None, None
while True:
    event = latest_event()
    if event and isinstance(event, SpnavMotionEvent):
        t, r = event.translation, event.rotation

        # for i in range(3):
        #     if abs(r[i]) < DEADZONE[i]:
        #         r[i] = 0
        #     else:
        #         r[i] = 

    state = [80, 110, 100]


    now = time.time()
    dt = now - lastCmdTime
    # send commands at CMD_FREQ Hz
    if dt > 1.0 / CMD_FREQ:
        grip_pos = np.array([-0.1, 0.05])

        if t and r:
            state[0] = int((-r[1] / 350.0 * 90) + 55)
            state[1] = int((t[2] / 350.0 * 90) + 110)
            state[2] = int((t[1] / 350.0 * 90) + 100)

            grip_pos[0] -= t[2] / 350.0 * .1
            grip_pos[1] += t[1] / 350.0 * .1

            print("gripper: %s" % str(grip_pos))

        # angle_ranges = [(-pi/2, pi/2), ]

        thetas = arm_model.inverse_2d(grip_pos)
        print('thetas: %s' % str(thetas))
        arm_cmds = calc_arm_servos(thetas)
        print('cmds: %s' % str(arm_cmds))

        state[1] = arm_cmds[0]
        state[2] = arm_cmds[1]
        # state1[1] = arm_cmds

        # state = [80, 150, 180]

        state = [clip(s, 0, 180) for s in state]
        state = [int(s) for s in state]

        encoded_msg = [chr(c) for c in [MAGIC] + state]
        arduino.write(encoded_msg)

        lastCmdTime = now
        print("cmd: ", end='')
        print(state)
