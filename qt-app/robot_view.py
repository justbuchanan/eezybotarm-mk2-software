from PyQt5.QtCore import QObject, Qt, QRectF, pyqtProperty, QPointF
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtGui import QColor, QPen, QPainter
from arm import ArmConfig
import arm_model
import numpy as np
from math import *

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

        #TODO: remove
        painter.drawRect(QRectF(0, 0, self.width(), self.height()))

        # transform into the model's coordinate system
        # scale so:
        #   x ranges from [-0.5, 0.2]
        #   y ranges from [-0.2, 0.5]
        # rotate (with a negative y scale) so that +y is up

        scale_factor = min(self.width(), self.height()) / 0.7

        painter.scale(scale_factor, -scale_factor)
        painter.translate(QPointF(0.4, -0.4))

        # draw sampled points on the workspace - show the robots usable area
        ws_color = QColor('black')
        ws_color.setAlphaF(0.2)
        painter.setPen(QPen(ws_color, 0))
        painter.setBrush(ws_color)

        for s1 in np.linspace(1.6, 2.8, 50):
            for s2 in np.linspace(pi * 0.1, 1.1, 50):
                angles = np.array([s1, s2])
                pts = arm_model.forward(angles)
                if pts:
                    g = pts[4]
                    r = 0.002
                    painter.drawEllipse(QPointF(g[0], g[1]), r,r)



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


