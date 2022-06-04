"""
SERVO Command: Orders a servo to move to given position.

code: CommandCode::SERVO
"""

from hermes.core.command import AbstractCommand, CommandCode


class ServoCommand(AbstractCommand):
    """ Sends a Servo command """

    def __init__(self):
        super().__init__(CommandCode.SERVO, 'SERVO')
