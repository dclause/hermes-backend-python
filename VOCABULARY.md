### Board

A _Board_ is a physical electronic circuit with input / output pins on which devices are connected. A single board
can have multiple devices affected to it.
_Examples: Arduino board, nodeMCU, RaspberryPI, etc..._

### Device

A device is an electronic component that is connected a board and use to provide actions or inputs to it.  
_Examples: LED, PIR sensor, Servo, etc..._

In the context of this application, a device is a logical group of actions and inputs (commands). In that, it can
represent a logical _Group_ rather than an individual physical component.  
_Example: a robot hand can be a declared as a device and gather multiple actions commands, each for each finger servos._

### Command

A command is a message transmitted between the backend and board to require something from it. It is represented by
an 8bit _CommandCode_ which is the common vocabulary between the application layers (board, backend, frontend) to
transfer commands data. Multiple commands can be affected to a single device. _Commands_ can be of three kinds :

#### Generic command

A generic command will not be linked to a device on any sort but serve a generic purpose of communication between a
board and the backend. For instance HANDSHAKE, HEARTBEAT, ACK, PATCH, DEBUG, etc...

#### Action command

An action is a command that will modify the state of a device (led, servo, etc...)

#### Input command

An input is a command that will retrieve information about the state of a device (PIR sensor, distance sensor, etc...)

#### Runnable

A _Runnable_ is a command that cannot be run instantly, hence must executed on the go. That could be an action (for instance turning a servo takes time) or an input (for instance polling the distance sensor every seconds).