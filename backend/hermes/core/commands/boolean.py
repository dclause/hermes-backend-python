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


class BooleanInput(AbstractCommand):
    """ BooleanAction command: turns a pin full on / off. """

    @property
    def code(self) -> CommandCode:
        return CommandCode.BOOLEAN_INPUT
