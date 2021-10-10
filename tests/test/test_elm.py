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
