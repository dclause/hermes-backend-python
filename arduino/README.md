# HERMES Arduino

The arduino code for HERMES implements the hermes communication protocol between the HERMES backend and an arduino
slave connected via the serial port.

## Installation

* Open the `arduino.ino` file in [Arduino IDE](https://www.arduino.cc/en/software)
* Upload to the board as usual

**_Don't worry about Arduino IDE
not capable of showing related files in inner folder, it will be compiled and uploaded appropriately._**

## Compatibility

The code is written to be compatible with all Arduino boards. **It has only been tested on _Arduino NANO_ and _Arduino
MEGA_**.

## Usage

The code implements the HERMES protocol and is meant to be used in conjunction with HERMES backend. Any other
third-party system is not tested and supported.

**It does not do anything on its own. Control is done by backend master code.**

## Developers

The project is handled via CLion IDE but any IDE of your own convenience is good. Code style and formatting is
handled by the .clang-tidy and .clang-format added. Feel free to submit PR for more enforcements.

### /!\ Information about code structure

The code is written within .h files, which is uncommon for C++ code. The reason is the Arduino IDE is not
capable to handle inclusion of cpp outside the main folder and/or residing in specific lib structure. I wanted to
keep compatibility with the Arduino IDE to handle code compiling and upload made easy.
