#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import arm_model
from math import *


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
# t = np.arange(0.0, 1.0, 0.001)
# a0 = 5
# f0 = 3
# s = a0*np.sin(2*np.pi*f0*t)
# l, = plt.plot(t, s, lw=2, color='red')
plt.axis([-0.2, 0.2, 0, 0.4])

# calculate the points given the angles
X = np.array([3*pi/4, pi/4])
pts = arm_model.forward(X)

# circles for each of the points
circles = [plt.Circle(p, radius=0.01) for p in pts]
for c in circles:
    print(c)
    plt.gca().add_patch(c)

# plt.gca().add_patch(plt.Circle((0, 0.01), radius=0.1))

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)


s_theta0 = Slider(axfreq, 'Theta0', pi/4, pi, valinit=X[0])
s_theta1 = Slider(axamp, 'Amp', 0, pi/2, valinit=X[1])

def update(val):
    X = np.array([s_theta0.val, s_theta1.val])
    pts = arm_model.forward(X)

    for i in range(len(circles)):
        circles[i].center = pts[i]
    # amp = s_theta1.val
    # rad = s_theta0.val
    # c.set_radius(rad)
    # l.set_ydata(amp*np.sin(2*np.pi*freq*t))
    fig.canvas.draw_idle()
s_theta0.on_changed(update)
s_theta1.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    s_theta0.reset()
    s_theta1.reset()
button.on_clicked(reset)

rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

plt.show()

# fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.25, bottom=0.25)
# l = plt.plot(lw=2, color='red')
# plt.axis([-0.5, 0.5, 0, 1])

# axcolor = 'lightgoldenrodyellow'
# axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
# axamp = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

# # ll = plt.Line2D((0.1, -6), (5, 6), lw=2)
# # plt.gca().add_line(ll)



# s_theta0 = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=pi/2)
# s_theta1 = Slider(axamp, 'Amp', 0.1, 10.0, valinit=pi/2)
