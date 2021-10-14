"""Module vehicles.py tests.

make test T=test_vehicles.py
"""
from . import TestBase


def to866(text):
    """Text for console redirection."""
    return str(text).encode("cp866", errors='replace').decode("cp866")


def dump_data(data, desc):
    """Dump ecu Controls data."""
    if data:
        print("----", desc)
        for i in data:
            print(to866(str(i)))


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

        print("###")
        for i in sorted(ecu.categories):
            print()
            print("# ", to866(i))
            for j in sorted(ecu.category(i)):
                screen = ecu.screen(j)

                print("\n## ", to866(j), "PRE:", len(screen.presend))
                for data, desc in [
                  # (screen.presend, "Presend:"),
                  (screen.labels, "Labels:"),
                  (screen.displays, "Displays:"),
                  (screen.inputs, "Inputs:"),
                  (screen.buttons, "Buttons:"),
                ]:
                    dump_data(data, desc)
