struct MotorConn {
    int stepPin;
    int dirPin;
};

MotorConn conns[] = {
    {7, 6}, // base
    {5, 4}, // up/down
    {3, 2}, //forward/back
};

const int kBaseIdx = 0;
const int kVertIdx = 1;
const int kForwardbackIdx = 2;

void setup() {
    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);

    for (MotorConn& c : conns) {
        pinMode(c.dirPin, OUTPUT);
        pinMode(c.stepPin, OUTPUT);
    }
}

const int delayUs = 500;
const int stepIncrement = 20; // # of steps per instruction

void step(int pin) {
    for (int i = 0; i < stepIncrement; i++) {
        digitalWrite(pin, HIGH);
        delayMicroseconds(delayUs);
        digitalWrite(pin, LOW);
        delayMicroseconds(delayUs);
    }
}

void setDir(int pin, bool forward) {
    digitalWrite(pin, forward ? HIGH : LOW);
    delayMicroseconds(delayUs);
}

void loop() {
    static bool ledOn = false;
    static bool forward = true;

    // read values from serial into the servoValues buffer
    if (Serial.available() > 0) {
        ledOn = !ledOn;
        uint8_t cmd = Serial.read();
        if (cmd == 'j') {
            MotorConn& c = conns[kVertIdx];
            setDir(c.dirPin, true); // down
            step(c.stepPin);
            Serial.write('j');
        } else if (cmd == 'k') {
            MotorConn& c = conns[kVertIdx];
            setDir(c.dirPin, false); // up
            step(c.stepPin);
            Serial.write('k');
        } else if (cmd == 'h') {
            MotorConn& c = conns[kBaseIdx];
            setDir(c.dirPin, true); // left?
            step(c.stepPin);
        } else if (cmd == 'l') {
            MotorConn& c = conns[kBaseIdx];
            setDir(c.dirPin, false); // right?
            step(c.stepPin);
        } else if (cmd == 'g') {
            MotorConn& c = conns[kForwardbackIdx];
            setDir(c.dirPin, true); // out?
            step(c.stepPin);
        } else if (cmd == 'G') {
            MotorConn& c = conns[kForwardbackIdx];
            setDir(c.dirPin, false); // in?
            step(c.stepPin);
        }
    }

    digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
}
