// #include <Servo.h>

void setup() {
    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    static bool ledOn = false;

    // read values from serial into the servoValues buffer
    if (Serial.available() > 0) {
        uint8_t c = Serial.read();
        if (c == 'j') {
            ledOn = !ledOn;

            // TODO: step forward
        } else if (c == 'k') {
            ledOn = !ledOn;

            // TODO: step backward
        }
    }

    digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
}

// void loop() {
//     static bool ledOn = false;
//     static uint8_t servoIndex = 0;
//     static unsigned long lastMsgTime = 0;

//     // read values from serial into the servoValues buffer
//     if (Serial.available() > 0) {
//         uint8_t c = Serial.read();
//         if (c == MSG_DELIMITER) {
//             ledOn = !ledOn; // toggle led
//             lastMsgTime = millis();
//             servoIndex = 0;
//         } else if (servoIndex < NUM_SERVOS) {
//             servos[servoIndex].attach(SERVO_PINS[servoIndex]);
//             servos[servoIndex].write(c);
//             servoIndex += 1;
//         }
//     }

//     // disable servos if we haven't received a command in a while
//     if (millis() - lastMsgTime > CMD_TIMEOUT) {
//         for (Servo& s : servos) {
//             s.detach();
//         }

//         ledOn = false;
//     }

//     digitalWrite(LED_BUILTIN, ledOn ? HIGH : LOW);
// }
