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
