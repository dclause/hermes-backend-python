"""
OnOff Command: simple OnOff command attached to digitalPin.

code: CommandCode::ON_OFF
"""
from enum import Enum

from hermes.core.commands import AbstractCommand, CommandCode


class OnOffCommand(AbstractCommand):
    """ On/Off command: turns a pin full on / off. """

    @property
    def __type__(self) -> Enum:
        # @todo here the type is a code: rethink this.
        return CommandCode.ON_OFF

    def __init__(self):
        super().__init__(CommandCode.ON_OFF, 'ON_OFF')
