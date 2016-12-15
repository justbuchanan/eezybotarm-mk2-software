#include <Servo.h>

const uint8_t NUM_SERVOS = 4;

// pin mapping
const uint8_t SERVO_PINS[NUM_SERVOS] = {
    9,
    10,
    11,
    6,
};

Servo servos[NUM_SERVOS];

void setup() {
    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);
}


// timeout after 1/2 second
const unsigned long CMD_TIMEOUT = 1000 / 2;

// a number not in the range of servo values that indicates the start of a message
const uint8_t MSG_DELIMITER = 200;

void loop() {
    static bool ledOn = false;
    static uint8_t servoIndex = 0;
    static unsigned long lastMsgTime = 0;

    // read values from serial into the servoValues buffer
    if (Serial.available() > 0) {
        uint8_t c = Serial.read();
        if (c == MSG_DELIMITER) {
            ledOn = !ledOn; // toggle led
            lastMsgTime = millis();
            servoIndex = 0;
        } else if (servoIndex < NUM_SERVOS) {
            servos[servoIndex].attach(SERVO_PINS[servoIndex]);
            servos[servoIndex].write(c);
            servoIndex += 1;
        }
    }

    // disable servos if we haven't received a command in a while
    if (millis() - lastMsgTime > CMD_TIMEOUT) {
        for (Servo& s : servos) {
            s.detach();
        }

        ledOn = false;
    }

    digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
}
