"""Elm327 device interface."""
import serial


class Device:
    """Elm327 device."""

    timeout = 2

    @classmethod
    def at_port(cls, port_name, boud):
        """Return device instance at the given port or None if not found."""
        try:
            port = serial.Serial(port_name, baudrate=boud, timeout=cls.timeout)
        except serial.serialutil.SerialException:
            return None
        except ValueError:
            return None

        port.write(bytearray("ATZ\r", 'utf-8'))
        print("# read with timeout: {}".format(cls.timeout))
        response = port.read(100).decode("utf-8")
        print("# {} response: '{}'".format(port_name, response))

        if 'ELM' in response:
            return cls(port, response)

        return None

    def __init__(self, port, response):
        """Elm device at given port."""
        self.port = port
        self.name = response

    def __str__(self):
        """String representation for Elm device."""
        return self.name
