import sys
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
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
        self._command = ArmCommand(None, [100, 100, 100, 100])
        self._port = '/dev/arduino'
        self._arm = None
        self._connected = False

    connected_changed = pyqtSignal(bool)

    @pyqtProperty(bool, notify=connected_changed)
    def connected(self):
        return self._connected
    @connected.setter
    def connected(self, value):
        if value != self._connected:
            if value:
                try:
                    self._arm = Arm(port=self.port)
                    self._connected = self._arm != None
                except ConnectionError as e:
                    print("failed to connect to arduino")
            else:
                del self._arm
                self._arm = None
                self._connected = False

            self.connected_changed.emit(value)
            self._connected = value
            self.send_command()

    @pyqtProperty(ArmCommand)
    def command(self):
        return self._command
    @command.setter
    def command(self, value):
        self._command = value
        self.send_command()

    def send_command(self):
        if self._command and self._arm:
            # print('sent cmd: %s' % self._command)
            self._arm.set_servo_values(self._command.servos)

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
        self._gripper_closed = False

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
        # TODO: move gripper values elsewhere
        servos.append(50 if self.gripper_closed else 180) # gripper servo
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

    @pyqtProperty(bool)
    def gripper_closed(self):
        return self._gripper_closed
    @gripper_closed.setter
    def gripper_closed(self, value):
        self._gripper_closed = value
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


