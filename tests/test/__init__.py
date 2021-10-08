"""Root class for testing."""
import os
from unittest import TestCase

import serial


class TestBase(TestCase):
    """Base class for tests."""

    def setUp(self):
        """Set up tests."""
        super().setUp()

        from cli_options import PARSER
        self.options, _args = PARSER.parse_args(args=[])

        from ..mock import serial as MockSerial

        self.saved_serial = serial.Serial
        serial.Serial = MockSerial.Port
        self.port = serial.Serial()

    def tearDown(self):
        """Clear tests."""
        serial.Serial = self.saved_serial
        super().tearDown()

    @staticmethod
    def fixture(file_name):
        """Return path to fixture file."""
        return os.path.join('tests', 'fixture', file_name)
