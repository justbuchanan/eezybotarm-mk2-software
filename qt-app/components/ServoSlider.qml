import QtQuick 2.7
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.2

RowLayout {
    property alias slider: slider;

    Slider {
        id: slider

        minimumValue: -3.14/2
        maximumValue: 3.14/2
        value: 0.2
    }

    Text {
        text: Math.round(slider.value * 100) / 100
    }
}
