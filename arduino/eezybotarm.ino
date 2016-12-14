#include <Servo.h>


const uint8_t SERVO_PINS[4] = {
    9,
    10,
    11,
    6,
};

Servo _servos[4];

void setState(const uint8_t servos[4]) {
    for (int i = 0; i < 4; i++) {
        _servos[i].write(servos[i]);
    }
}

// servo values as 8 bit numbers - initialized to something reasonable
uint8_t servoValues[4] = {100, 100, 100, 180};

void setup() {
    for (int i = 0; i < 4; i++) {
        _servos[i].attach(SERVO_PINS[i]);
    }

    setState(servoValues);

    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);
}

// a number not in the range of servo values that indicates the start of a message
const uint8_t MSG_DELIMITER = 200;
uint8_t msgIndex = 0;
bool haveMessage = false;

void loop() {
    // read values from serial into the servoValues buffer
    if (Serial.available() > 0) {
        uint8_t c = Serial.read();
        if (c == MSG_DELIMITER) {
            msgIndex = 0;
        } else if (msgIndex >= 4) {
            // invalid
            haveMessage = false;
        } else {
            servoValues[msgIndex++] = c;
            if (msgIndex == 4) {
                haveMessage = true;
                // Serial.println("got message!");

                setState(servoValues);
            }
        }
    }

    digitalWrite(LED_BUILTIN, haveMessage ? HIGH : LOW);
}

