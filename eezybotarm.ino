#include <Servo.h>

struct ServoRange {
    int Min, Max;
    ServoRange(int min, int max) : Min(min), Max(max) {}
};

struct ArmState {
    ArmState(size_t i = 0, size_t j = 0, size_t k = 0) {
        joints[0] = i;
        joints[1] = j;
        joints[2] = k;
    }

    size_t joints[3];
};

void Print(const ArmState& armState) {
    // Serial.print("<%u, %u, %u>", armState.joints[0], armState.joints[1], armState.joints[2]);
}

class Arm {
public:
    Arm() {}

    void Init(const size_t pins[3]) {
        for (int i = 0; i < 3; i++) {
            _servos[i].attach(pins[i]);
        }
        _initialized = true;
    }

    void setState(ArmState state) {
        _state = state;
        for (int i = 0; i < 3; i++) {
            _servos[i].write(_state.joints[i]);
        }
    }

    void printState() {
        Serial.print("Arm: ");
        Print(_state);
    }

private:
    ArmState _state;
    Servo _servos[3];
    bool _initialized = false;
};

//==============================================================================

const size_t SERVO_PINS[3] = {
    9,
    10,
    11,
};

// global arm object
Arm arm;

void setup() {
    arm.Init(SERVO_PINS);

    // something reasonable
    arm.setState({100, 100, 100});

    arm.printState();

    Serial.begin(9600);
}

//==============================================================================


// a number not in the range of servo values that indicates the start of a message
const uint8_t MAGIC = 200;
// Format: '<1><2><3>' where 1, 2, 3 are joint deltas as 8 bit numbers
uint8_t serialMsg[3];
size_t msgIndex = 0;
bool haveMessage = false;

void loop() {
    while (Serial.available() > 0) {
        uint8_t c = Serial.read() - 'a';
        if (c == MAGIC) {
            msgIndex = 0;
        } else if (msgIndex >= 2) {
            // invalid
            haveMessage = false;
        } else {
            serialMsg[msgIndex++] = c;
            if (msgIndex == 3) {
                haveMessage = true;
                // Serial.println("Got message: %u:%u:%u", serialMsg[0], serialMsg[1], serialMsg[2]);
                Serial.println("got message!");
                Serial.println(0);
            }
        }
        // Serial.println(c);
        Serial.println(c);
    }


    // arm.setState({100, 100, 100});
//  for (pos = min; pos <= max; pos += 1) { // goes from 0 degrees to 180 degrees
//    // in steps of 1 degree
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(d);                       // waits 15ms for the servo to reach the position
//  }
//  for (pos = max; pos >= min; pos -= 1) { // goes from 180 degrees to 0 degrees
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(d);                       // waits 15ms for the servo to reach the position
//  }
}

