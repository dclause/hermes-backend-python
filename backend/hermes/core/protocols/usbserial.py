"""
Serial communication handling.
Used by boards in serial mode (only supported mode as of today).

--
TLDR: To send a command, ClearableQueue it. That ClearableQueue is consumed by a dedicated thread of each board
(CommandSenderThread) which actually sends the command. The number of commands sent is limited until ACK are received to
prevent growing the serial buffer (CommandListenerThread).
--

This package introduces multithreading to handle communication over the serial port.

Commands that need to be sent over `serial` should be queues using a :class:CommandQueue.

- The class :class:CommandThread defines a separated thread which role is to consume that ClearableQueue and actually
send the commands. It can only send a given amount of commands, hence the CommandQueue acting as a waiting
ClearableQueue.
The number of commands sent is tracked via a semaphore and only frees the way when the corresponding ACK is received.

- The class :class:ListenerThread defines a separated which role is to receive data from the serial communication and
execute the corresponding command. It is also frees the semaphore when receiving ACK to let the :class:CommandThread
continue its work on sending queued commands.
"""

import glob
import sys
import threading

from serial import Serial, SerialException

from hermes.core import logger
from hermes.core.commands import CommandCode, CommandFactory
from hermes.core.protocols import AbstractProtocol, ProtocolException


class SerialProtocol(AbstractProtocol):
    """ Implements an :class:AbstractProtocol class using the serial port. """

    def __init__(self, serial_port, baudrate=115200, timeout=0, write_timeout=0):
        self._serial_port: bool = serial_port
        self._baudrate: int = baudrate
        self._timeout: int = timeout
        self._write_timeout: int = write_timeout
        self._serial: Serial = Serial()

    def open(self) -> None:
        try:
            self._serial = Serial(
                port=self._serial_port,
                baudrate=self._baudrate,
                timeout=self._timeout,
                writeTimeout=self._write_timeout
            )
        except SerialException as error:
            logger.error(
                'Serial connexion: Port %s could not be opened. Available ports are %s.',
                self._serial_port,
                self.get_serial_ports()
            )
            raise ProtocolException(
                f'Port {self._serial_port} could not be opened. Available ports are {self.get_serial_ports()}'
            ) from error

    def close(self) -> None:
        self._serial.close()

    def is_open(self) -> bool:
        return self._serial.isOpen()

    def read_command(self) -> CommandCode:
        bytes_array = None
        while not bytes_array:
            bytes_array = bytearray(self._serial.read(1))
        logger.debug('Serial protocol: Received command code %s', str(bytes_array[0]))
        return CommandCode(bytes_array[0])

    def send_command(self, command_code: CommandCode, *args, **kwargs) -> None:
        data = bytearray([command_code, *args])  # SERVO, device 1, position 180
        logger.error('Serial protocol: Send command %s', data)
        self._serial.write(data)

    def read_line(self) -> str:
        response = ""
        while True:
            bytes_array = bytearray(self._serial.read(1))
            if bytes_array:
                response += chr(bytes_array[0])
            if "\r\n" in response:
                break
        return response.rstrip()

    @staticmethod
    def get_serial_ports() -> list[str]:
        """
        Lists serial ports.

        Returns:
            list[str]: A list of available serial ports.

        Raises:
            EnvironmentError: The code is running on an unknown platform.
        """
        if sys.platform.startswith('win'):
            ports = [f'COM{(i + 1)}' for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # Exclude your current terminal "/dev/tty".
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        results = []
        for port in ports:
            try:
                connexion = Serial(port)
                connexion.close()
                results.append(port)
            except (OSError, SerialException):
                pass
        return results


# class SerialSenderThread(threading.Thread):
#     """
#     Thread that send orders to the arduino
#     it blocks if there is no more send_token left (here it is the n_received_semaphore).
#     :param serial_file: (Serial object)
#     :param command_queue: (Queue)
#     :param exit_event: (Threading.Event object)
#     :param n_received_semaphore: (threading.Semaphore)
#     :param serial_lock: (threading.Lock)
#     """
#
#     def __init__(self, serial_file, command_queue, exit_event, n_received_semaphore, serial_lock):
#         threading.Thread.__init__(self)
#         self.deamon = True
#         self.serial_file = serial_file
#         self.command_queue = command_queue
#         self.exit_event = exit_event
#         self.n_received_semaphore = n_received_semaphore
#         self.serial_lock = serial_lock
#
#     def run(self):
#         while not self.exit_event.is_set():
#             self.n_received_semaphore.acquire()
#             if self.exit_event.is_set():
#                 break
#             try:
#                 order, param = self.command_queue.get_nowait()
#             except ClearableQueue.Empty:
#                 time.sleep(rate)
#                 self.n_received_semaphore.release()
#                 continue
#
#             with self.serial_lock:
#                 write_order(self.serial_file, order)
#                 # print("Sent {}".format(order))
#                 if order == Order.MOTOR:
#                     write_i8(self.serial_file, param)
#                 elif order == Order.SERVO:
#                     write_i16(self.serial_file, param)
#             time.sleep(rate)
#         print("Command Thread Exited")


class CommandListenerThread(threading.Thread):
    """
    Thread that listens to communication protocol for commands and executes it.

    The thread reads a commandCode from the communication protocol, turns it to an actual command and processes it.
    If the commandCode is an ACK, the thread releases one lock to the n_received_semaphore semaphore to clear the way
    for the CommandSenderThread.

    Args:
        connexion (AbstractProtocol)
        exit_event (threading.Event object)
        n_received_semaphore (threading.Semaphore)
        serial_lock (threading.Lock)
    """

    def __init__(
            self,
            connexion: AbstractProtocol,
            exit_event: threading.Event,
            n_received_semaphore: threading.Semaphore,
            serial_lock: threading.Lock
    ):
        threading.Thread.__init__(self)
        self.deamon = True
        self._connexion = connexion
        self.exit_event = exit_event
        self.n_received_semaphore = n_received_semaphore
        self.serial_lock = serial_lock

    def run(self):
        logger.info("CommandListenerThread: thread started.")

        while not self.exit_event.is_set():

            command_code = self._connexion.read_command()
            logger.debug(f'CommandListenerThread: receive command code {command_code}')

            with self.serial_lock:
                command = CommandFactory().get_by_code(command_code)
                logger.debug(command)
                command.receive(self._connexion)
                command.process()

                if command_code == CommandCode.ACK:
                    self.n_received_semaphore.release()

        logger.info("CommandListenerThread: thread stops.")
