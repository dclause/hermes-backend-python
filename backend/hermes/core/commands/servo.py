"""
SERVO Command: Orders a servo to move to given position.

code: CommandCode::SERVO
"""

from hermes.core.commands import AbstractCommand, CommandCode
from hermes.core.devices import AbstractDevice


class ServoCommand(AbstractCommand):
    """ Sends a Servo command """

    def __init__(self):
        super().__init__(CommandCode.SERVO, 'SERVO')

    def send(self, device: AbstractDevice, value: any):
        """ Sends the command. """

    def receive(self, connexion):
        """ Reads the additional parameters sent with the command. """

    # @logthis
    def process(self):
        """ Processes the command """
