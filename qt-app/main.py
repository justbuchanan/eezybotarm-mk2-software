#!/usr/bin/env python2
import sys
from PyQt5.QtCore import QObject, QUrl, Qt, QRectF, pyqtProperty, QPointF, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtGui import QColor, QPen, QPainter
from math import *
import numpy as np

from arm_driver import *
from calibration import *

import arm_model

class ArmConfig(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._points = []

    @pyqtProperty(list)
    def points(self):
        return self._points
    @points.setter
    def points(self, value):
        self._points = value


class ArmCommand(QObject):
    def __init__(self, parent=None, values=[]):
        QObject.__init__(self, parent)
        self._servos = values

    @pyqtProperty(list)
    def servos(self):
        return self._servos
    @servos.setter
    def servos(self, value):
        self._servos = value


class ArmDriver(QObject):
    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._command = ArmCommand(None, [100, 100, 100])
        self._port = '/dev/arduino'
        self._arm = None
        self._connected = False

    def connect(self):
        try:
            self._arm = Arm(port=self.port)
        except ConnectionError as e:
            print("failed to connect to arduino")

        self.connected = self._arm != None

    connected_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=connected_changed)
    def connected(self):
        return self._connected

    @pyqtProperty(ArmCommand)
    def command(self):
        return self._command
    @command.setter
    def command(self, value):
        self._command = value
        if value and self._arm:
            # print('sent cmd: %s' % value)
            self._arm.set_servo_values(value.servos)

    @pyqtProperty(str)
    def port(self):
        return self._port


class ArmModel(QObject):

    config_changed = pyqtSignal(ArmConfig)

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._servo0 = 0
        self._servo1 = pi/2
        self._servo2 = pi/4
        self._config = None
        self._command = None

    # update model points based on servo values
    def recalculate(self):
        X = np.array([self.servo1, self.servo2])
        cfg = ArmConfig()
        cfg.points = arm_model.forward(X)
        # TODO: show that it's out of bounds?
        if cfg.points:
            self.config = cfg

        arm_servos = calc_arm_servos(X)
        base = calc_base_servo_cmd(self.servo0)
        servos = [base, arm_servos[0], arm_servos[1]]
        # TODO: share this code with motion_path.py
        servos = clip_servos(servos)
        servos = [int(s) for s in servos]
        cmd = ArmCommand(None, servos)
        self.command = cmd

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

    @pyqtProperty(float)
    def servo2(self):
        return self._servo2
    @servo2.setter
    def servo2(self, value):
        self._servo2 = value
        self.recalculate()

    @pyqtProperty(ArmConfig, notify=config_changed)
    def config(self):
        return self._config
    @config.setter
    def config(self, value):
        self._config = value

        self.config_changed.emit(value)


    command_changed = pyqtSignal(ArmCommand)

    @pyqtProperty(ArmCommand, notify=command_changed)
    def command(self):
        return self._command
    @command.setter
    def command(self, value):
        self._command = value
        self.command_changed.emit(value)


class RobotView(QQuickPaintedItem):
    def __init__(self, parent):
        QObject.__init__(self, parent)
        # self._points = []
        self._config = None

    # # list of QPointF values
    @pyqtProperty(ArmConfig)
    def config(self):
        return self._config
    @config.setter
    def config(self, value):
        self._config = value
        self.update()

    def paint(self, painter):

        painter.setRenderHints(QPainter.Antialiasing)

        if not self.config or len(self.config.points) != 5:
            print("invalid points array, wrong length")
            return

        # transform into the model's coordinate system
        # scale so:
        #   x ranges from [-0.5, 0.2]
        #   y ranges from [-0.2, 0.5]
        # rotate (with a negative y scale) so that +y is up
        painter.scale(self.width() / 0.7, -self.height() / 0.7)
        painter.translate(QPointF(0.4, -0.4))

        painter.save()
        painter.setPen(QPen(QColor('blue'), 0.01))

        pts = [QPointF(p[0], p[1]) for p in self.config.points]

        for m in arm_model.LINE_MAPPING:
            p0 = pts[m[0]]
            p1 = pts[m[1]]
            painter.drawLine(p0, p1)
        painter.restore()

        painter.setPen(QPen(QColor('blue'), 0))
        painter.setBrush(QColor('orange'))
        for p in pts:
            rad = 0.01
            painter.drawEllipse(p, rad, rad)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    qmlRegisterType(RobotView, 'RobotView', 1, 0, 'RobotView')
    qmlRegisterType(ArmDriver, 'ArmDriver', 1, 0, 'ArmDriver')
    qmlRegisterType(ArmModel, 'ArmModel', 1, 0, 'ArmModel')
    qmlRegisterType(ArmConfig, 'ArmConfig', 1, 0, 'ArmConfig')
    qmlRegisterType(ArmCommand, 'ArmCommand', 1, 0, 'ArmCommand')

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)

    engine.load('main.qml')

    win = engine.rootObjects()[0]

    # def myHandler():
    #     print('handler called')
    # button = win.findChild(QObject, "myButton")
    # button.clicked.connect(myHandler)

    win.show()
    sys.exit(app.exec_())
