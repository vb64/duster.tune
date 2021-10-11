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
        assert ecu_db.count == 3478
        assert len(ecu_db.unknown_vehicles) == 77
        assert len(ecu_db.vehiclemap) == len(DATA)
        assert len(ecu_db.protocol_kwp) == 28
        assert len(ecu_db.protocol_can) == 133
        assert len(ecu_db.protocol_unknown) == 2

        assert len(ecu_db.targets_by_href) == 3478
        count = 0
        for _i, lst in ecu_db.targets_by_href.items():
            count += len(lst)
        assert count == 28285
        assert not ecu_db.get_targets_by_name('XXX')

        assert len(ecu_db.targets_by_name) == 3422
        count = 0
        for _i, lst in ecu_db.targets_by_name.items():
            count += len(lst)
        assert count == 28285
        assert not ecu_db.get_targets_by_href('XXX')

        # print("## Unknown vehicles:")
        # for i, j in ecu_db.unknown_vehicles.items():
        #     print("#", i, '->', j)
