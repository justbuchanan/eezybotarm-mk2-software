#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt




import matplotlib.pyplot as plt
import time
import threading
import random

data = []

# This just simulates reading from a socket.
def data_listener():
    while True:
        time.sleep(1)
        data.append(random.random())

if __name__ == '__main__':
    thread = threading.Thread(target=data_listener)
    thread.daemon = True
    thread.start()
    #
    # initialize figure
    plt.figure() 
    ln, = plt.plot([])
    plt.ion()
    plt.show()
    while True:
        plt.pause(1)
        ln.set_xdata(range(len(data)))
        ln.set_ydata(data)
        plt.draw()
    exit()







plt.axis([0, 10, 0, 1])
plt.ion()

# for i in range(10):
# y = np.random.random()
# plt.scatter(i, y)
# plt.pause(0.05)
# plt.Line2D
line = plt.Line2D((0, 0), (0, 0), lw=2)
plt.gca().add_line(line)
# plt.add_line(line)

while True:
    y = np.random.random()
    plt.scatter(y, 1/y)
    plt.pause(0.05)
