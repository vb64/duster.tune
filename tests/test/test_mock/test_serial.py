"""Mock serial tests.

make test T=test_mock/test_serial.py
"""
from . import TestMock


class TestSerial(TestMock):
    """Tests mock serial module."""

    def test_close(self):
        """Method close."""
        self.port.close()
        assert not self.port.is_opened  # pylint: disable=no-member
