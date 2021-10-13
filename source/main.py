"""Main module."""
import sys

from serial.tools.list_ports import comports
from cli_options import PARSER, VERSION
from elm import Device
from ecu import Database
from vehicles import Vehicle, DATA

COPYRIGHTS = '(C) by Vitaly Bogomolov 2021'
OPTS = None


def find_elm(_options):
    """Search for ELM device at the serial ports."""
    device = None
    print("Searching for ELM device...")
    for port, desc, _hwid in comports():
        print("Try {} {}...".format(port, desc))
        device = Device.at_port(port, 38400)
        if device:
            break

    return device


def main(_argv, options):
    """Entry point."""
    print("Vehicle settings viewer version {}. {}.".format(VERSION, COPYRIGHTS))
    # PARSER.print_usage()

    print("Using ECU DB", options.ecus_file)
    ecu_db = Database(options.ecus_file, DATA)
    print("ECU items loaded:", ecu_db.count)

    device = None
    if not options.noelm:
        device = find_elm(options)

    if device:
        print("Using {}".format(device))
    else:
        print("No ELM device set.", "Database view mode.")

    if not options.vehicle_code:
        print("Vehicle code not set.", "Use --vehicle option to set.")
        return 1

    vehicle = Vehicle(options.vehicle_code, ecu_db.vehicles[options.vehicle_code])
    print(str(vehicle))
    for group in sorted(vehicle.groups.keys()):
        print("\n# {}: {}".format(group, len(vehicle.groups[group])))
        print(vehicle.dump_group(group))

    return 0


if __name__ == '__main__':  # pragma: no cover
    OPTS, ARGS = PARSER.parse_args()
    sys.exit(main(ARGS, OPTS))
