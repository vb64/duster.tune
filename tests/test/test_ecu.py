"""Module ecu.py tests.

make test T=test_ecu.py
"""
from . import TestBase


class TestEcu(TestBase):
    """Tests Ecu database."""

    def test_database_2018(self):
        """Database class from ecu_2018.zip."""
        from source.ecu import Database
        from source.vehicles import DATA

        ecu_db = Database(self.fixture('ecu_2018.zip'), DATA)
        assert ecu_db.count == 1835
        assert len(ecu_db.unknown_vehicles) == 60
        assert len(ecu_db.vehicles) == 77
        assert len(ecu_db.protocol_kwp) == 28
        assert len(ecu_db.protocol_can) == 103
        assert len(ecu_db.protocol_unknown) == 1

    def test_database_2019(self):
        """Database class from ecu_2019.zip."""
        from source.ecu import Database
        from source.vehicles import DATA

        assert len(DATA) == 80
        ecu_db = Database(self.fixture('ecu_2019.zip'), DATA)
        assert ecu_db.count == 3478
        assert len(ecu_db.unknown_vehicles) == 77
        assert len(ecu_db.vehicles) == len(DATA)
        assert len(ecu_db.protocol_kwp) == 28
        assert len(ecu_db.protocol_can) == 133
        assert len(ecu_db.protocol_unknown) == 2

        duster2021 = ecu_db.vehicles["xJD"]
        assert len(duster2021) == 414
        # print("## Unknown vehicles:")
        # for i, j in ecu_db.unknown_vehicles.items():
        #     print("#", i, '->', j)
