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
