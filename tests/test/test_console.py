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

    def test_duster2021(self):
        """Call app with --noelm option and DusterII vehicle code."""
        from source import main

        self.options.noelm = True
        self.options.ecus_file = self.fixture('ecu_2019.zip')
        self.options.vehicle_code = "xJD"
        assert main.main([], self.options) == 0

    def test_noelm_cli(self):
        """Call app with --noelm option."""
        from source import main

        self.options.noelm = True
        self.options.ecus_file = self.fixture('ecu_2018.zip')
        assert main.main([], self.options) == 1

    def test_no_elm(self):
        """Call app without ELM device."""
        from source import main

        self.options.ecus_file = self.fixture('ecu_2018.zip')

        saved = main.comports
        main.comports = stub_com1_bluetooth
        assert main.main([], self.options) == 1
        main.comports = saved

    def test_elm(self):
        """Call app with ELM device."""
        from source import main
        from source.elm import serial as mockserial
        from tests.mock.serial import MockElm

        self.options.ecus_file = self.fixture('ecu_2018.zip')
        saved = mockserial.Serial
        mockserial.Serial = MockElm

        assert main.main([], self.options) == 1
        mockserial.Serial = saved
