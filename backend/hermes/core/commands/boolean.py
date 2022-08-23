"""
DigitalWrite Command: simple command attached to digitalPin.

code: CommandCode::DIGITAL_WRITE
"""

from hermes.core.commands import AbstractCommand, CommandCode


class BooleanAction(AbstractCommand):
    """ BooleanAction command: turns a pin full on / off. """

    def __init__(self):
        super().__init__()
        self.pin: int = 0

    @property
    def code(self) -> CommandCode:
        return CommandCode.BOOLEAN_ACTION

    @property
    def _is_runnable(self) -> bool:
        return False

    def _get_settings(self) -> bytearray:
        return bytearray([self.pin, self.default])

    def _get_mutation(self, value: any) -> bytearray:
        return bytearray([self.pin, value])


class BooleanInput(AbstractCommand):
    """ BooleanAction command: turns a pin full on / off. """

    @property
    def _is_runnable(self) -> bool:
        return True

    @property
    def code(self) -> CommandCode:
        return CommandCode.BOOLEAN_INPUT

    def _get_settings(self) -> bytearray:
        return bytearray()

    def _get_mutation(self, value: any) -> bytearray:
        return bytearray()
