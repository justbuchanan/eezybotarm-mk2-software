#!/usr/bin/env python2
import sys
from PyQt5.QtCore import QObject, QUrl, Qt, QRectF, pyqtProperty, QPointF, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtGui import QColor, QPen, QPainter
from robot_view import *
from math import *
import numpy as np

from arm import *

from arm_driver import *
from calibration import *

import arm_model



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

    engine.addImportPath('./')

    engine.load('main.qml')

    win = engine.rootObjects()[0]

    # def myHandler():
    #     print('handler called')
    # button = win.findChild(QObject, "myButton")
    # button.clicked.connect(myHandler)

    win.show()
    sys.exit(app.exec_())
