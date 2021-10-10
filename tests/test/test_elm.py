"""Module elm.py tests.

make test T=test_elm.py
"""
import serial
from tests.mock.serial import Port
from . import TestBase


class MockNotWriteble(Port):
    """Mocked not writeble serial port."""

    def write(self, _bytes_array):
        """No write."""
        raise serial.serialutil.SerialTimeoutException(self.port)


class MockElm(Port):
    """Mocked serial port with ELM device."""

    def read(self, _bytes_num):
        """Read given bytes number from serial port."""
        return b'ATZ\r\r\rELM327 v1.5\r\r'


class TestElm(TestBase):
    """Tests ELM module."""

    def test_init(self):
        """Method init and str."""
        from source.elm import Device

        device = Device(self.port, 'Elm device')
        assert str(device) == 'Elm device'

    @staticmethod
    def test_name_from_response():
        """Function name_from_response."""
        from source.elm import name_from_response

        assert not name_from_response(b'')
        assert not name_from_response(b'xxx')
        assert name_from_response(b'ATZ\r\r\rELM327 v1.5\r\r') == "ELM327 v1.5"

    @staticmethod
    def test_at_port_wrong():
        """Class method at_port."""
        from source.elm import Device, serial as mockserial

        saved = mockserial.Serial
        mockserial.Serial = MockNotWriteble

        assert Device.at_port('COM1', 38400) is None

        mockserial.Serial = MockElm
        assert Device.at_port('COM1', 38400).name == 'ELM327 v1.5'

        mockserial.Serial = saved
