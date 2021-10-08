"""Mock serial tests.

make test T=test_mock/test_serial.py
"""
import pytest
from . import TestMock


class TestSerial(TestMock):
    """Tests mock serial module."""

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
