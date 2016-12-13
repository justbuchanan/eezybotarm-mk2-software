#!/usr/bin/env python2
import sys
from PyQt5.QtCore import QObject, QUrl, Qt, QRectF, pyqtProperty, QPointF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtGui import QColor, QPen
from math import *
import numpy as np

import arm_model



class RobotView(QQuickPaintedItem):
    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._points = []
        self._servo0 = pi/2
        self._servo1 = pi/4

    # update model points based on servo values
    def recalculate(self):
        X = np.array([self.servo0, self.servo1])
        self.points = arm_model.forward(X)
        self.update()


    @pyqtProperty(float)
    def servo0(self):
        return self._servo0
    @servo0.setter
    def servo0(self, value):
        self._servo0 = value
        self.recalculate()

    @pyqtProperty(float)
    def servo1(self):
        return self._servo1
    @servo1.setter
    def servo1(self, value):
        self._servo1 = value
        self.recalculate()

    @pyqtProperty(list)
    def points(self):
        return self._points
    @points.setter
    def points(self, value):
        self._points = value
        self.update()

    def paint(self, painter):

        if not self.points or len(self.points) != 5:
            print("invalid points array, wrong length")
            return

        # transform into the model's coordinate system
        # scale so:
        #   x ranges from [-0.4, 0.1]
        #   y ranges from [0, 0.5]
        # rotate (with a negative y scale) so that +y is up
        painter.scale(self.width() / 0.5, -self.height() / 0.5)
        painter.translate(QPointF(0.4, -0.5))

        painter.save()
        painter.setPen(QPen(QColor('blue'), 0.01))

        for m in arm_model.LINE_MAPPING:
            p0 = self.points[m[0]]
            p1 = self.points[m[1]]
            painter.drawLine(QPointF(p0[0], p0[1]), QPointF(p1[0], p1[1]))
        painter.restore()

        painter.setPen(QPen(QColor('blue'), 0))
        painter.setBrush(QColor('orange'))
        for p in self.points:
            rad = 0.01
            painter.drawEllipse(QPointF(p[0], p[1]), rad, rad)





if __name__ == "__main__":
    app = QApplication(sys.argv)

    qmlRegisterType(RobotView, 'RobotView', 1, 0, 'RobotView')

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)


    engine.load('main.qml')
    def myHandler():
        print('handler called')

    win = engine.rootObjects()[0]

    button = win.findChild(QObject, "myButton")
    button.clicked.connect(myHandler)

    win.show()


    rview = win.findChild(RobotView, "robot")

    servo0slider = win.findChild(QObject, "servo0")
    servo1slider = win.findChild(QObject, "servo1")

    def recalculate():
        # X = np.array([pi/2, pi/4])
        X = np.array([servo0slider.value, servo1slider.value])
        rview.points = arm_model.forward(X)

    # rview.servo0.valueChanged.connect(lambda: recalculate())


    # servo0slider.onPositionChanged.connect(lambda: recalculate())
    # servo1slider.onValueChanged.connect(lambda: recalculate())

    # servo1slider.value = 0.2


    sys.exit(app.exec_())
