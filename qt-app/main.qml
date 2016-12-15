import QtQuick 2.7
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.2

import components 1.0

import RobotView 1.0
import ArmDriver 1.0
import ArmCommand 1.0
import ArmModel 1.0

ApplicationWindow {
    title: "Arm Control"

    width: 200
    height: 200

    ArmModel {
        id: arm
        objectName: "arm"
    }

    ArmDriver {
        id: armDriver
        objectName: "armDriver"
    }

    Binding {
        target: armDriver
        property: "command"
        value: arm.command
    }

    ColumnLayout {
        id: column
        spacing: 10

        // anchors.top: parent.top
        // anchors.left: parent.left
        // anchors.right: parent.right
        anchors.fill: parent
        anchors.centerIn: parent
        anchors.margins: column.spacing


        GroupBox {
            title: "Drawing"

            // Layout.fillWidth: true
            // Layout.fillHeight: true
            // anchors.fill: parent
            // anchors.centerIn: parent
            height: parent.height / 2
            width: parent.width

            RobotView {
                id: robotDrawing
                objectName: "robotDrawing"
                anchors.fill: parent
                anchors.centerIn: parent
                // width: 200

                height: parent.height / 2
                //  Component.onCompleted: {
                //     robotDrawing.implicitWidth = contentView.implicitWidth
                //     robotDrawing.implicitHeight = contentView.implicitHeight
                // }
            }
        }

        GroupBox {
            title: "Arduino"

            ColumnLayout {
                anchors.fill: parent
                Text {
                    objectName: "portLabel"
                    text: "Port: " + armDriver.port
                }
                CheckBox {
                    text: "connected"
                    checked: armDriver.connected
                    id: arduino_connected

                    Shortcut { sequence: 'c'; onActivated: arduino_connected.checked = !arduino_connected.checked }
                }
            }
        }
        // Button{
        //     objectName: "myButton"
        //     text : "About"
        //     y : 70
        // }
        GroupBox {
            title: "Servos"

            ColumnLayout {
                anchors.fill: parent

                ServoSlider {

                    id: servo0
                    objectName: "servo0"
                    slider.value: 0.2
                }

                ServoSlider {
                    id: servo1
                    objectName: "servo1"

                    slider {
                        value: 1.8
                        minimumValue: 0
                        maximumValue: 3.14
                    }

                    Shortcut { sequence: 'h'; onActivated: servo1.slider.value += 0.05 }
                    Shortcut { sequence: 'l'; onActivated: servo1.slider.value -= 0.05 }
                }

                ServoSlider {
                    id: servo2
                    objectName: "servo2"

                    slider {
                        value: 0.2
                        minimumValue: 0
                        maximumValue: 3.14
                    }

                    Shortcut { sequence: 'j'; onActivated: servo2.slider.value += 0.05 }
                    Shortcut { sequence: 'k'; onActivated: servo2.slider.value -= 0.05 }
                }
                CheckBox {
                    text: "Gripper"
                    checked: armDriver.gripper_closed
                    id: gripper

                    Shortcut {
                        sequence: 'g'
                        onActivated: gripper.checked = !gripper.checked
                    }
                }
            }
        }

    }

    Binding {
        target: arm
        property: "servo0"
        value: servo0.slider.value
    }
    Binding {
        target: arm
        property: "servo1"
        value: servo1.slider.value
    }
    Binding {
        target: arm
        property: "servo2"
        value: servo2.slider.value
    }
    Binding {
        target: arm
        property: "gripper_closed"
        value: gripper.checked
    }
    Binding {
        target: robotDrawing
        property: "config"
        value: arm.config
    }
    Binding {
        target: armDriver
        property: "connected"
        value: arduino_connected.checked
    }
}