"""Serial port for testing."""
import serial


class Port:
    """Mocked serial port."""

    valid_names = ["COM1"]

    allowed_bytesize = [
      serial.FIVEBITS,
      serial.SIXBITS,
      serial.SEVENBITS,
      serial.EIGHTBITS,
    ]

    def __init__(
      self,
      port="COM1",
      baudrate=9600,
      bytesize=serial.EIGHTBITS,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      timeout=None
    ):
        """Open serial port."""
        if port not in self.valid_names:
            raise serial.SerialException("Wrong port")

        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout

        if self.bytesize not in self.allowed_bytesize:
            raise ValueError("Wrong bytesize")

        self.is_opened = True
        self.in_buffer = []
        self.out_buffer = []
        self.is_constantly = False

    def close(self):
        """Close serial port."""
        self.is_opened = False

    def write(self, bytes_array):
        """Write bytes to serial port."""
        self.in_buffer.append(bytes_array)
        return len(bytes_array)

    def read(self, _bytes_num):
        """Read given bytes number from serial port."""
        if self.is_constantly:
            return self.out_buffer[0]

        if self.out_buffer:
            return self.out_buffer.pop(0)
        return bytearray()

    def set_out(self, byte_list, is_constantly=False):
        """Set content for out_buffer."""
        try:
            data = bytearray(byte_list)
        except ValueError as wrong_bytes:
            raise ValueError("bytes: {}".format(byte_list)) from wrong_bytes

        if is_constantly:
            self.out_buffer = [data]
        else:
            self.out_buffer.append(data)

        self.is_constantly = is_constantly
