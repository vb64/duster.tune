"""Main module."""
import sys

from serial.tools.list_ports import comports
from cli_options import PARSER
from elm import Device

COPYRIGHTS = '(C) by Vitaly Bogomolov 2021'
OPTS = None


def main(_argv, _options):
    """Entry point."""
    print("ELM scanner. {}".format(COPYRIGHTS))
    # PARSER.print_usage()

    print("Searching for ELM device...")
    device = None
    for port, desc, _hwid in comports():
        print("Try {} {}...".format(port, desc))
        device = Device.at_port(port, 38400)
        if device:
            break

    if not device:
        print("No ELM device found.")
        return 1

    print("Using {}".format(device))
    return 0


if __name__ == '__main__':  # pragma: no cover
    OPTS, ARGS = PARSER.parse_args()
    sys.exit(main(ARGS, OPTS))
