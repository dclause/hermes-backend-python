"""
DigitalWrite Command: simple command attached to digitalPin.

code: CommandCode::DIGITAL_WRITE
"""
from hermes.core.commands import AbstractCommand, CommandCode


class DigitalWriteCommand(AbstractCommand):
    """ DigitalWrite command: turns a pin full on / off. """

    def __init__(self):
        super().__init__(CommandCode.DIGITAL_WRITE, 'DIGITAL_WRITE')
