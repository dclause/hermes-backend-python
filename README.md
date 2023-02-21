[![GitHub release](https://img.shields.io/github/release/dclause/hermes?include_prereleases=&sort=semver&color=blue)](https://github.com/dclause/hermes/releases/)
[![License](https://img.shields.io/github/license/dclause/hermes)](https://github.com/dclause/hermes/blob/main/LICENSE)
[![Backend tests](https://img.shields.io/github/workflow/status/dclause/hermes/backend_tests.yml)](https://github.com/dclause/hermes/actions/workflows/backend_tests.yml")
[![Frontend tests](https://img.shields.io/github/workflow/status/dclause/hermes/frontend_tests.yml)](https://github.com/dclause/hermes/actions/workflows/frontend_tests.yml")

[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](https://github.com/dclause/hermes#readme "Go to project documentation")

# HERMES - a Robot Management System (RMS)

Hermes - _a Robot Management System (RMS)_ - is a set of tools to remotely pilot a robot, or at least a set of
electronic devices build on one of supported boards.

It's primary focus is robots or systems with a single (embedded or not) master _head_ (computer, raspberry,
etc..) sending orders to a set of _slaves_ - sub-systems - (arduino for instance) connected via a supported protocol 
(serial at the moment).
It is composed of three main parts:

- `arduino`: an arduino "slave" client - _designed to receive and execute orders from the control script to actuators
  (servos, sensors, etc...)._
- `backend`: a python control script - _designed to pilot de robot by sending appropriate orders to the appropriate
  slave._
- `frontend`: a web interface - _designed to give a comprehensive interface to pilot the robot via the python script._

# Try it!

**The project needs python 3.10 or later.**

For raspberryPI, you can use:

```
wget -qO - https://raw.githubusercontent.com/tvdsluijs/sh-python-installer/main/python.sh | sudo bash -s 3.10.6
```

**Current develops happen on the `main` branch**:

```
git clone --branch main https://github.com/dclause/hermes.git HERMES
```

# Motivation

HERMES is an experimentation of my own to unify the control of some of my personal robots :

- a custom 3D-printed [ZeroBot](https://www.thingiverse.com/thing:2800717) - _an open-source project by Max Kern._
- a modified [Watney](https://github.com/nikivanov/watney) like robot - _an open-source by Nik Ivanov._
- my own designed rover robot
- a modified/motorized 3D printed [GladOS replica](https://ytec3d.com/glados-lamp) - _an open-source project by Yvo de
  Haas._
- a full [InMoov robot](https://inmoov.fr) - _an open-source project by Gaël Langevin._

It is also biased by my experience as an escape room creator since a room can be seen in the context of this 
software as a robot where game master PC is the _head_ and the various puzzles are _slaves_.

Inspired by [MyRobotLab](http://myrobotlab.org/), it _<ins>tries</ins>_ to be lighter (to be used on a raspberry),
easier and more user-friendly, but do not attempt to replace it.

***

**The HERMES project is done on my spare time, it does not intend to compete with any other solutions you might want to
try.**

# Installation

The code for HERMES is written in python 3.x. It acts as a master program to give orders to slave boards
(arduino, etc..) to transmit commands to devices (servos, LEDs, ...).

It operates in coordination with the arduino code defined in the `arduino` folder.

## Developers

1. Clone the repository:
```
git clone https://github.com/dclause/hermes.git
cd hermes
```

2. Create and setup a virtual environment:

```
python3 -m venv .venv
source ./.venv/Scripts/activate # can vary depending on your system
pip install -r requirements.txt && pip install -r dev_requirements.txt
```

2. Start the program:

```
python3 -m hermes
```

* Open UI: `python3 -m hermes --open`
* Run in debug mode: `python3 -m hermes --debug`
* Help: `python3 -m hermes --help`

3. For your convenience, you can use `make` commands in the project:

```
$ make
Available commands:
help                      Print help for each target
documentation             Open documentation
install                   Install everything
run                       Run the code
env                       Source the virtual environment
debug                     Debug the code
clean                     Cleanup
test                      Run all tests
lint                      Lint the code
deps-install              Install the dependencies
dev-deps-install          Install the dev dependencies
deps-update               Update the dependencies
dev-deps-update           Update the dependencies
feedback                  Provide feedback
```
