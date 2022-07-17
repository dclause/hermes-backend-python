"""
BLINK Command: blinks a LED.

code: CommandCode::BLINK
"""
from enum import Enum

from hermes.core.commands import AbstractCommand, CommandCode


class BlinkCommand(AbstractCommand):
    """ Blinks a led. """

    @property
    def __type__(self) -> Enum:
        # @todo here the type is a code: rethink this.
        return CommandCode.BLINK

    def __init__(self):
        super().__init__(CommandCode.BLINK, 'BLINK')
