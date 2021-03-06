import serial
import time
from PyQt5.QtCore import QTimer
import arm_model

# command delimiter for the serial communication to arduino
SERIAL_MSG_DELIMITER = 200


class ConnectionError(RuntimeError):
    pass


class Arm:
    def __init__(self, port='/dev/arduino', baud=9600, update_freq=30):
        try:
            self._arduino = serial.Serial(port, baud, timeout=1)
        except serial.SerialException as e:
            raise ConnectionError(e)

        time.sleep(0.01)  # TODO: is this needed?

        self._encoded_msg = None
        self._update_freq = update_freq

        # update at a set frequency
        t = QTimer()
        t.setInterval(1000 / self._update_freq)
        t.timeout.connect(self.send_message)
        self._timer = t
        t.start()

    # @param servos list of three int values between 0 and 180
    def set_servo_values(self, servos):
        if len(servos) != arm_model.NUM_SERVOS:
            raise RuntimeError("Invalid number of servos")
        self._encoded_msg = [SERIAL_MSG_DELIMITER] + list(
            [chr(c) for c in servos])

    def send_message(self):
        if self._encoded_msg:
            self._arduino.write(self._encoded_msg)
