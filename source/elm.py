"""Elm327 device interface."""
import serial

ELM_SIGN = 'ELM327'


def name_from_response(response_bytes):
    """Construct Elm327 device name from port response."""
    # b'ATZ\r\r\rELM327 v1.5\r\r'
    text = response_bytes.replace(b'\r', b'\n').decode('ascii')
    if ELM_SIGN not in text:
        return ""

    return text[text.index(ELM_SIGN):].split('\n')[0]


class Device:
    """Elm327 device."""

    r_timeout = 2
    w_timeout = 2

    @classmethod
    def at_port(cls, port_name, boud):
        """Return device instance at the given port or None if not found."""
        port = serial.Serial(
          port_name, baudrate=boud,
          timeout=cls.r_timeout, write_timeout=cls.w_timeout
        )
        try:
            port.write(bytearray("ATZ\r", 'utf-8'))
        except serial.serialutil.SerialTimeoutException:
            return None

        response = port.read(100)
        print("# {} response: '{}'".format(port_name, response))
        name = name_from_response(response)
        if name:
            return cls(port, name)

        return None

    def __init__(self, port, response):
        """Elm device at given port."""
        self.port = port
        self.name = response

    def __str__(self):
        """String representation for Elm device."""
        return self.name
