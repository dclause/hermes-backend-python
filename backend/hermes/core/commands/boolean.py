"""
DigitalWrite Command: simple command attached to digitalPin.

code: CommandCode::DIGITAL_WRITE
"""

from hermes.core.commands import AbstractCommand, CommandCode


class BooleanAction(AbstractCommand):
    """ BooleanAction command: turns a pin full on / off. """

    @property
    def code(self) -> CommandCode:
        return CommandCode.BOOLEAN_ACTION

    def __init__(self):
        super().__init__()
        self.pin: int = 0

    def encode(self, value: any) -> bytearray:
        return bytearray([self.pin, value])


class BooleanInput(AbstractCommand):
    """ BooleanAction command: turns a pin full on / off. """

    @property
    def code(self) -> CommandCode:
        return CommandCode.BOOLEAN_INPUT
