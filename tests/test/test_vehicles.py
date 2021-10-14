"""Module vehicles.py tests.

make test T=test_vehicles.py
"""
from . import TestBase


class TestVehicle(TestBase):
    """Tests Vehicle class."""

    def test_display(self):
        """Display section."""
        from source.ecu import Database
        from source.vehicles import Vehicle, DATA

        ecu_db = Database(self.fixture('ecu_2019.zip'), DATA)
        assert ecu_db.count == 3478

        duster2021 = Vehicle("xJD", ecu_db)
        ecu = duster2021.get_ecu("Tableau de bord", "Cluster_L1_L2_v6.09_20190201T164850.json")
        assert ecu.data_layout
        assert ecu.data_json

        # use cached, no real load
        ecu = duster2021.get_ecu("Tableau de bord", "Cluster_L1_L2_v6.09_20190201T164850.json")
