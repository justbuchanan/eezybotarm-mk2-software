#include <Servo.h>

struct ServoRange {
    int Min, Max;
    ServoRange(int min, int max) : Min(min), Max(max) {}
};

struct ArmState {
    ArmState(size_t i = 0, size_t j = 0, size_t k = 0, size_t grip = 0) {
        joints[0] = i;
        joints[1] = j;
        joints[2] = k;
        joints[3] = grip;
    }

    size_t joints[4];
};

void Print(const ArmState& armState) {
    // Serial.print("<%u, %u, %u>", armState.joints[0], armState.joints[1], armState.joints[2]);
}

class Arm {
public:
    Arm() {}

    void Init(const size_t pins[4]) {
        for (int i = 0; i < 4; i++) {
            _servos[i].attach(pins[i]);
        }
        _initialized = true;
    }

    void setState(ArmState state) {
        _state = state;
        for (int i = 0; i < 4; i++) {
            _servos[i].write(_state.joints[i]);
        }
    }

    void printState() {
        Serial.print("Arm: ");
        Print(_state);
    }

private:
    ArmState _state;
    Servo _servos[4];
    bool _initialized = false;
};

//==============================================================================

const size_t SERVO_PINS[4] = {
    9,
    10,
    11,
    6,
};

// global arm object
Arm arm;

void setup() {
    arm.Init(SERVO_PINS);

    // something reasonable
    arm.setState({100, 100, 100, 180});

    arm.printState();

    Serial.begin(9600);

    pinMode(LED_BUILTIN, OUTPUT);
}

//==============================================================================


// a number not in the range of servo values that indicates the start of a message
const uint8_t MAGIC = 200;
// Format: '<1><2><3>' where 1, 2, 3 are joint servo values as 8 bit numbers
uint8_t serialMsg[4];
size_t msgIndex = 0;
bool haveMessage = false;

void loop() {
    if (Serial.available() > 0) {
        uint8_t c = Serial.read();
        if (c == MAGIC) {
            msgIndex = 0;
        } else if (msgIndex >= 4) {
            // invalid
            haveMessage = false;
        } else {
            serialMsg[msgIndex++] = c;
            if (msgIndex == 4) {
                haveMessage = true;
                // Serial.println("got message!");
                // Serial.println(0);

                arm.setState({serialMsg[0], serialMsg[1], serialMsg[2], serialMsg[3]});
            }
        }
        // Serial.print("msgIndex: ");
        // Serial.println(msgIndex);
        // Serial.println(c);
    }

    digitalWrite(LED_BUILTIN, haveMessage ? HIGH : LOW);
}

