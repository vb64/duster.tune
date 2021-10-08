"""Module main.py tests.

make test T=test_console.py
"""
from . import TestBase


class TestConsole(TestBase):
    """Tests console client."""

    def test_empty_cli(self):
        """Call app with empty CLI."""
        from source.main import main

        assert main([], self.options) == 0
