"""
BLINK Command: blinks a LED.

code: CommandCode::BLINK
"""

from hermes.core.commands import AbstractCommand, CommandCode


class BlinkCommand(AbstractCommand):
    """ Blinks a led. """

    def __init__(self):
        super().__init__(CommandCode.BLINK, 'BLINK')
