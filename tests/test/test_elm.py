"""Module elm.py tests.

make test T=test_elm.py
"""
from . import TestBase


class TestElm(TestBase):
    """Tests ELM module."""

    def test_init(self):
        """Method init and str."""
        from source.elm import Device

        device = Device(self.port, 'Elm device')
        assert str(device) == 'Elm device'

    @staticmethod
    def test_at_port_none():
        """Method at_port with wrong params."""
        from source.elm import Device, serial
        from tests.mock import serial as MockSerial

        saved = serial.Serial
        serial.Serial = MockSerial.Port

        assert Device.at_port('XXX', 666) is None
        assert Device.at_port('COM1', 666) is None
        serial.Serial = saved
