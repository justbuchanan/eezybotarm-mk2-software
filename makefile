ARDUINO_DIR=/usr/share/arduino
ARDMK_DIR=./Arduino-Makefile
AVR_TOOLS_DIR=/usr
MONITOR_PORT=/dev/ttyACM*

AVRDUDE=/usr/bin/avrdude
AVRDUDE_CONF=/etc/avrdude.conf

ISP_PORT=/dev/ttyACM*


BOARD_TAG=uno

ARDUINO_LIBRARIES=Wire Servo

CXXFLAGS_STD = -std=gnu++0x

include $(ARDMK_DIR)/Arduino.mk


