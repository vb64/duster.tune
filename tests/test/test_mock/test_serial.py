"""Mock serial tests.

make test T=test_mock/test_serial.py
"""
import pytest
import serial
from . import TestMock


class TestSerial(TestMock):
    """Tests mock serial module."""

    @staticmethod
    def test_wrong_name():
        """Wrong port name."""
        from tests.mock import serial as MockSerial

        with pytest.raises(serial.SerialException) as err:
            MockSerial.Port(port='XXX')
        assert 'Wrong port' in str(err.value)

    @staticmethod
    def test_bytesize():
        """Wrong bytesize."""
        from tests.mock import serial as MockSerial

        with pytest.raises(ValueError) as err:
            MockSerial.Port(bytesize=666)
        assert 'Wrong bytesize' in str(err.value)

    def test_close(self):
        """Method close."""
        self.port.close()
        assert not self.port.is_opened  # pylint: disable=no-member

    def test_read(self):
        """Method read."""
        self.port.set_out(bytearray('XXX', 'utf-8'))
        assert self.port.read(3) == bytearray('XXX', 'utf-8')

        self.port.set_out(bytearray('XXX', 'utf-8'), is_constantly=True)  # pylint: disable=no-member
        assert self.port.read(3) == bytearray('XXX', 'utf-8')
        assert self.port.read(3) == bytearray('XXX', 'utf-8')

        with pytest.raises(ValueError) as err:
            self.port.set_out([100, 500])  # pylint: disable=no-member
        assert 'bytes: [100, 500]' in str(err.value)
