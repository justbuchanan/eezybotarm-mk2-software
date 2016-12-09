#include <Servo.h>

const size_t SERVO_PINS[3] = {
    9,
    10,
    11,
};


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

class Arm {
public:
    Arm() {}

    void Init(size_t pins[3]) {
        for (int i = 0; i < 3; i++) {
            _servos[i].attach(pins[i]);
        }
    }

    void setState(ArmState state) {
        _state = state;
        for (int i = 0; i < 3; i++) {
            _servos[i].write(_state.joints[i]);
        }
    }

private:
    ArmState _state;
    Servo _servos[3];
};

// global arm object
Arm arm;

void setup() {
    arm.Init(SERVO_PINS);
}

void loop() {
    arm.setState({100, 100, 100});
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

