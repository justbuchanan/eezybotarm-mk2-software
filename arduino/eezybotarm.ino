#include <Servo.h>

const uint8_t NUM_SERVOS = 4;

// pin mapping
const uint8_t SERVO_PINS[NUM_SERVOS] = {
    9,
    10,
    11,
    6,
};

Servo _servos[NUM_SERVOS];

void setState(const uint8_t servos[NUM_SERVOS]) {
    for (int i = 0; i < NUM_SERVOS; i++) {
        _servos[i].write(servos[i]);
    }
}

// servo values as 8 bit numbers - initialized to something reasonable
uint8_t servoValues[NUM_SERVOS] = {100, 100, 100, 180};


// if @attach is true, enables servos and assigns pin numbers. Otherwise
// disables the servos.
bool servos_attached = false;
void servos_attach(bool attach) {
    if (attach == servos_attached) return;

    for (size_t i = 0; i < NUM_SERVOS; i++) {
        Servo& s = _servos[i];
        if (attach) {
            s.attach(SERVO_PINS[i]);
        } else {
            s.detach();
        }
    }

    servos_attached = attach;
}

void setup() {
    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);
}



// timeout after one second
const unsigned long CMD_TIMEOUT = 1 * 1000;

// a number not in the range of servo values that indicates the start of a message
const uint8_t MSG_DELIMITER = 200;

void loop() {
    static uint8_t msgIndex = 0;
    static bool haveMessage = false;
    static unsigned long lastMsgTime = 0;

    // read values from serial into the servoValues buffer
    if (Serial.available() > 0) {
        uint8_t c = Serial.read();
        if (c == MSG_DELIMITER) {
            msgIndex = 0;
        } else if (msgIndex >= NUM_SERVOS) {
            // invalid message - too long
            haveMessage = false;
        } else {
            servoValues[msgIndex++] = c;
            if (msgIndex == NUM_SERVOS) {
                lastMsgTime = millis();
                haveMessage = true;
                // Serial.println("got message!");
                servos_attach(true);
                setState(servoValues);
            }
        }
    }

    // disable servos if we haven't received a command in a while
    if (millis() - lastMsgTime > CMD_TIMEOUT) {
        servos_attach(false);
    }

    digitalWrite(LED_BUILTIN, haveMessage ? HIGH : LOW);
}
