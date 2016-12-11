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
MAGIC = 200

while True:
    # msg = 'h'
    msg = bytes([MAGIC, 100, 100, 100])
    print(msg)
    # arduino.write(msg)
    for b in msg:
        arduino.write(b)
    time.sleep(0.01)
    reply = arduino.readline()
    if len(reply):
        print(reply)
    time.sleep(2)





spnav_open()

while True:
    event = spnav_poll_event()
    if event and isinstance(event, SpnavMotionEvent):
        # print(event.translation[2]) # forward
        event.translation[1] # down
        vals = [
            event.rotation[1],
            event.translation[0],
        ]

        print(vals)
