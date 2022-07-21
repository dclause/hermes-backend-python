# HERMES backend

The backend code for HERMES is written in python 3.x. It acts as a master program to give orders to slave boards
(arduino, etc..) to transmit commands to devices (servos, LEDs, ...).

It operates in coordination with the arduino code defined in the `arduino` folder.

## Developers

1. Create and setup a virtual environment:

```
python3 -m venv .venv
source ./.venv/Scripts/activate # can vary depending on your system
pip install -r requirements.txt && pip install -r dev_requirements.txt
```

2. Start the program: `python3 -m hermes`

3. For your convenience, you can use `make` commands in the project:

```
$ make
Available commands:
clean                     Cleanup
deps-install              Install the dependencies
deps-update               Update the dependencies
dev-deps-install          Install the dependencies
dev-deps-update           Update the dependencies
feedback                  Provide feedback
help                      Print help for each target
lint                      Lint the code
run                       Run the code
debug                     Debug the code
test                      Test the code
```
