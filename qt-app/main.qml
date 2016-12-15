import QtQuick 2.7
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.2

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

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: column.spacing


        GroupBox {
            title: "Drawing"

            Layout.fillWidth: true

            RobotView {
                id: robotDrawing
                objectName: "robotDrawing"
                // anchors.fill: parent
                // anchors.centerIn: parent
                width: 200
                height: 200
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

                RowLayout {

                    Slider {
                        id: servo0
                        objectName: "servo0"
                        // label: "Base"

                        minimumValue: -3.14/2;
                        maximumValue: 3.14/2
                        value: 0.2
                    }

                    Text {
                        text: Math.round(servo0.value * 100) / 100
                    }
                }

                Slider {
                    id: servo1
                    objectName: "servo1"

                    minimumValue: 0
                    maximumValue: 3.14
                    value: 1.8
                }

                Slider {
                    id: servo2
                    objectName: "servo2"

                    minimumValue: 0
                    maximumValue: 3.14
                    value: 0.2
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
        value: servo0.value
    }
    Binding {
        target: arm
        property: "servo1"
        value: servo1.value
    }
    Binding {
        target: arm
        property: "servo2"
        value: servo2.value
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