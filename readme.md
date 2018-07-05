# EEZYbotARM MK2 Software [![CircleCI](https://circleci.com/gh/justbuchanan/eezybotarm-mk2-software.svg?style=svg)](https://circleci.com/gh/justbuchanan/eezybotarm-mk2-software)

Collection of software for the [EEZYbotARM MK2](http://www.thingiverse.com/thing:1454048).

This project contains two main programs:
* An arduino program that listens for commands over the serial connection and moves the servos. See the code in the arduino/ directory and instructions in the makefile. You will need to compile this program and flash it to your eezybotarm's arduino.
* A qt-based gui application that sends commands to the arm over a serial (usb) connection.

## Install dependencies

Download this repo, then install the required python packages:

```
pip -r requirements.txt
```

You'll also need [arduino-mk](https://github.com/sudar/Arduino-Makefile) in order to build the firmware

## Build and upload arduino firmware

```
cd arduino
make
make upload
```

## Run control app

```
cd qt-app
PYTHONPATH=../ python main.py
```

![Screenshot](doc/screenshot.png)
