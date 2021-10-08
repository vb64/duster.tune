"""Module main.py tests.

make test T=test_console.py
"""
from . import TestBase


class TestConsole(TestBase):
    """Tests console client."""

    def test_no_elm(self):
        """Call app without ELM device."""
        from source.main import main

        assert main([], self.options) == 1

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
