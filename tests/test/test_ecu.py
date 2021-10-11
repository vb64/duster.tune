"""Module ecu.py tests.

make test T=test_ecu.py
"""
from . import TestBase


class TestEcu(TestBase):
    """Tests Ecu database."""

    def test_database(self):
        """Database class."""
        from source.ecu import Database

        # ecu_db = Database(self.fixture('ecu_2018.zip'))
        # assert ecu_db.numecu == 1835
        ecu_db = Database(self.fixture('ecu_2019.zip'))
        assert ecu_db.numecu == 3478
