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
    def test_name_from_response():
        """Function name_from_response."""
        from source.elm import name_from_response

        assert not name_from_response(b'')
        assert not name_from_response(b'xxx')
        assert name_from_response(b'ATZ\r\r\rELM327 v1.5\r\r') == "ELM327 v1.5"

    @staticmethod
    def test_at_port_wrong():
        """Class method at_port."""
        from source.elm import Device, serial as mockserial
        from tests.mock.serial import MockNotWriteble, MockElm

        saved = mockserial.Serial
        mockserial.Serial = MockNotWriteble

        assert Device.at_port('COM1', 38400) is None

        mockserial.Serial = MockElm
        assert Device.at_port('COM1', 38400).name == 'ELM327 v1.5'

        mockserial.Serial = saved
