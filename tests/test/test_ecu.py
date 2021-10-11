"""Module ecu.py tests.

make test T=test_ecu.py
"""
from . import TestBase


class TestEcu(TestBase):
    """Tests Ecu database."""

    def test_database(self):
        """Database class."""
        from source.ecu import Database
        from source.vehicles import DATA

        assert len(DATA) == 80
        # ecu_db = Database(self.fixture('ecu_2018.zip'))
        # assert ecu_db.numecu == 1835
        ecu_db = Database(self.fixture('ecu_2019.zip'), DATA)
        assert ecu_db.numecu == 3478
        assert len(ecu_db.unknown_vehicles) == 77
        assert len(ecu_db.vehiclemap) == len(DATA)

        # print("## Unknown:")
        # for i, j in ecu_db.unknown_vehicles.items():
        #     print("#", i, '->', j)
