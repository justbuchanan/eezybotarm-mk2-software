import serial
import time


# command delimeter for the serial communication to arduino
MAGIC = 200

def clip(x, minval, maxval):
    if x > maxval:
        return maxval
    elif x < minval:
        return minval
    else:
        return x

def clip_servos(servos):
    return [clip(s, 0, 180) for s in servos]

class ConnectionError(RuntimeError): pass


class Arm:
    def __init__(self, port='/dev/arduino', baud=9600):
        try:
            self._arduino = serial.Serial(port, baud, timeout=1)
        except serial.SerialException as e:
            raise ConnectionError(e)

        time.sleep(0.01) # TODO: is this needed?

    # @param servos list of three int values between 0 and 180
    def set_servo_values(self, servos):
        encoded_msg = [chr(c) for c in [MAGIC] + servos]
        self._arduino.write(encoded_msg)
