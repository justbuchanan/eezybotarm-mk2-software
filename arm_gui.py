#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import arm_model
from math import *


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
plt.axis([-0.2, 0.2, 0, 0.4])

# calculate the points given the angles
X = np.array([1.88, pi/4])
pts = arm_model.forward(X)

# circles for each of the points on the arm
circles = [plt.Circle(p, radius=0.005) for p in pts]
for c in circles:
    plt.gca().add_patch(c)

# draw a line for each entry in @LINE_MAPPING
lines = [plt.Line2D((0, 0), (0, 0), lw=2) for i in range(len(LINE_MAPPING))]
for line in lines:
    plt.gca().add_line(line)

# update lines from the data in @pts
def update_lines():
    for i in range(len(LINE_MAPPING)):
        src, dst = LINE_MAPPING[i]
        p0 = pts[src]
        p1 = pts[dst]
        lines[i].set_xdata([p0[0], p1[0]])
        lines[i].set_ydata([p0[1], p1[1]])

update_lines()

# sliders for the two servos
axcolor = 'lightgoldenrodyellow'
ax_servo0 = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
ax_servo1 = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
s_theta0 = Slider(ax_servo0, 'Servo0', pi/4, pi, valinit=X[0])
s_theta1 = Slider(ax_servo1, 'Servo1', 0, pi/2, valinit=X[1])

def update(val):
    global X
    global pts
    global circles
    X = np.array([s_theta0.val, s_theta1.val])
    pts = arm_model.forward(X)
    update_lines()

    for i in range(len(circles)):
        circles[i].center = pts[i]
    fig.canvas.draw_idle()
s_theta0.on_changed(update)
s_theta1.on_changed(update)

plt.show()
