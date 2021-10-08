"""Module main.py tests.

make test T=test_console.py
"""
from . import TestBase


def stub_com1_bluetooth():
    """Return one comport."""
    return [('COM1', 'Bluetooth port COM1', 1)]


def stub_com45_bluetooth():
    """Return two comports."""
    return [
      ('COM4', 'Bluetooth port COM4', 1),
      ('COM5', 'Bluetooth port COM5', 2),
    ]


class TestConsole(TestBase):
    """Tests console client."""

    def test_no_elm(self):
        """Call app without ELM device."""
        from source import main
        saved = main.comports

        main.comports = stub_com1_bluetooth
        assert main.main([], self.options) == 1
        main.comports = saved

    def test_no_ports(self):
        """Call app without COM ports."""
        from source.main import main
        from ..mock.serial import Port

        saved = Port.valid_names
        Port.valid_names = []
        assert main([], self.options) == 1
        Port.valid_names = saved

    def test_wrong_port_params(self):
        """Wrong COM port parameters."""
        from source.main import main
        from ..mock.serial import Port

        saved = Port.allowed_bytesize
        Port.allowed_bytesize = []
        assert main([], self.options) == 1
        Port.allowed_bytesize = saved
