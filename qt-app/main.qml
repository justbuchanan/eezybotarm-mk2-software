import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1
import RobotView 1.0
import QtQuick.Layouts 1.2

ApplicationWindow {
    title: qsTr("Test Invoke")

    width: 200
    height: 200

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
                id: robot
                // x: 0
                // y: 0
                // anchors.fill: parent
                objectName: "robot"
                // width: parent.parent.width
                width: 500
                height: 500
                // anchors.fill: parent
                anchors.centerIn: parent
            }
        }

        // Button{
        //     objectName: "myButton"
        //     text : "About"
        //     y : 70
        // }
        GroupBox {
            title: "Servo 0"


            Slider {
                id: servo0
                objectName: "servo0"

                // y: 100

                minimumValue: 0
                maximumValue: 3.14
                value: 1.8
                // height: 50
            }
        }

        GroupBox {
            title: "Servo 1"
            Slider {
                id: servo1
                objectName: "servo0"

                // y: 150

                minimumValue: 0
                maximumValue: 3.14
                value: 0.2
                // height: 50
            }
        }

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