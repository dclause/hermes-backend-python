"""
DigitalWrite Command: simple command attached to digitalPin.

code: CommandCode::DIGITAL_WRITE
"""
from enum import Enum

from hermes.core.commands import AbstractCommand, CommandCode


class BooleanAction(AbstractCommand):
    """ DigitalWrite command: turns a pin full on / off. """

    @property
    def __type__(self) -> Enum:
        # @todo here the type is a code: rethink this.
        return CommandCode.BOOLEAN_ACTION

    def __init__(self):
        super().__init__(CommandCode.BOOLEAN_ACTION, 'DIGITAL_WRITE')
