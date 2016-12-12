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
from arm_driver import *


# exit gracefully
def on_signal(signum, frame):
    print('Ctrl+C received, exiting...')
    spnav_close()
    sys.exit(0)
signal.signal(signal.SIGINT, on_signal)


port = sys.argv[1]

arduino = serial.Serial(port, 9600, timeout=1)
time.sleep(1)


lastCmdTime = time.time()
CMD_FREQ = 20 # Hz


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
    grip_pos = np.array([-0.1, 0.05])


    # send commands at CMD_FREQ Hz
    now = time.time()
    dt = now - lastCmdTime
    if dt > 1.0 / CMD_FREQ:

        if t and r:
            state[0] = calc_base_servo_cmd(-r[1] / 350.0 * pi/4)

            grip_pos[0] -= t[2] / 350.0 * .1
            grip_pos[1] += t[1] / 350.0 * .1

        print("gripper: %s" % str(grip_pos))

        thetas = arm_model.inverse_2d(grip_pos)
        arm_cmds = calc_arm_servos(thetas)
        state[1:3] = arm_cmds

        state = clip_servos(state)
        state = [int(s) for s in state]

        encoded_msg = [chr(c) for c in [MAGIC] + state]
        arduino.write(encoded_msg)

        lastCmdTime = now
        print("cmd: ", end='')
        print(state)
