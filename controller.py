#!/usr/bin/env python2

from spnav import *
import signal
import sys
import serial
import time

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


spnav_open()

t, r = None, None

while True:
    event = spnav_poll_event()
    if event and isinstance(event, SpnavMotionEvent):
        t, r = event.translation, event.rotation

    now = time.time()
    dt = now - lastCmdTime
    if dt > 1.0 / CMD_FREQ and t and r:
        state = [80, 110, 100]

        state[0] = int((-r[1] / 350.0 * 90) + 90)

        state[1] = int((t[2] / 350.0 * 90) + 110)

        state[2] = int((t[1] / 350.0 * 90) + 100)

        encoded_msg = [chr(c) for c in [MAGIC] + state]
        arduino.write(encoded_msg)

        lastCmdTime = now
        print(state)

