"""
SERVO Command: Orders a servo to move to given position.

code: CommandCode::SERVO
"""
from enum import Enum

from hermes.core.commands import AbstractCommand, CommandCode


class ServoCommand(AbstractCommand):
    """ Sends a Servo command """

    @property
    def __type__(self) -> Enum:
        # @todo here the type is a code: rethink this.
        return CommandCode.SERVO

    def __init__(self):
        super().__init__(CommandCode.SERVO, 'SERVO')

    def send(self, device_id, command_id: any, value: any):
        """ Sends the command. """

    def receive(self, connexion):
        """ Reads the additional parameters sent with the command. """

    # @logthis
    def process(self):
        """ Processes the command """
