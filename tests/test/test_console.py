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
