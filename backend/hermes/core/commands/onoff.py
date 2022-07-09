"""
OnOff Command: simple OnOff command attached to digitalPin.

code: CommandCode::ON_OFF
"""
from hermes.core.commands import AbstractCommand, CommandCode


class OnOffCommand(AbstractCommand):
    """ On/Off command: turns a pin full on / off. """

    def __init__(self):
        super().__init__(CommandCode.ON_OFF, 'ON_OFF')
