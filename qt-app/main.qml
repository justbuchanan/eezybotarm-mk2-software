import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1
import RobotView 1.0

ApplicationWindow {
    title: qsTr("Test Invoke")

    width: 200
    height: 200

    RobotView {
        id: robot
        x: 10
        y: 20
        objectName: "robot"
        width: 200
        height: 200
        anchors.centerIn: parent
    }

    // Button{
    //     objectName: "myButton"
    //     text : "About"
    //     y : 70
    // }

    Slider {
        id: servo0
        objectName: "servo0"

        y: 100

        minimumValue: 0
        maximumValue: 3.14
        value: 1.8
    }
    Slider {
        id: servo1
        objectName: "servo0"

        y: 150

        minimumValue: 0
        maximumValue: 3.14
        value: 0.2
    }

    Binding {
        target: robot
        property: "servo0"
        value: servo0.value
    }
    Binding {
        target: robot
        property: "servo1"
        value: servo1.value
    }
}