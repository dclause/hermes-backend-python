"""
SERVO Command: Orders a servo to move to given position.

code: CommandCode::SERVO
"""

from hermes.core.commands import AbstractCommand, CommandCode


class ServoCommand(AbstractCommand):
    """ Sends a Servo command """

    @property
    def code(self) -> CommandCode:
        return CommandCode.SERVO

    def send(self, device_id, command_id: any, value: any):
        """ Sends the command. """

    def receive(self, connexion):
        """ Reads the additional parameters sent with the command. """

    def process(self):
        """ Processes the command """
