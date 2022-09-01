[![GitHub release](https://img.shields.io/github/release/dclause/hermes?include_prereleases=&sort=semver&color=blue)](https://github.com/dclause/hermes/releases/)
[![License](https://img.shields.io/github/license/dclause/hermes)](https://github.com/dclause/hermes/blob/main/LICENSE)
[![Backend tests](https://img.shields.io/github/workflow/status/dclause/hermes/backend_tests.yml)](https://github.com/dclause/hermes/actions/workflows/backend_tests.yml")
[![Frontend tests](https://img.shields.io/github/workflow/status/dclause/hermes/frontend_tests.yml)](https://github.com/dclause/hermes/actions/workflows/frontend_tests.yml")

[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](https://github.com/dclause/hermes#readme "Go to project documentation")

# HERMES - a Robot Management System (RMS)

Hermes - _a Robot Management System (RMS)_ - is a set of tools to remotely pilot a robot.

It is designated for robots with a single embedded master system (computer, raspberry, etc..) sending orders to a 
set of slave sub-systems (itself or arduino(s)) connected via serial (extendable to other protocols).
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

Inspired by [MyRobotLab](http://myrobotlab.org/), it _<ins>tries</ins>_ to be lighter (to be used on a raspberry), easier and 
  more user-friendly.

***

**The HERMES project is done on my spare time, it does not intend to compete with any other solutions you might want to 
try.** 
