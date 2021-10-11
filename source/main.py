"""Main module."""
import sys

from serial.tools.list_ports import comports
from cli_options import PARSER
from elm import Device

COPYRIGHTS = '(C) by Vitaly Bogomolov 2021'
OPTS = None


def main(_argv, options):
    """Entry point."""
    print("Vehicle settings viewer. {}".format(COPYRIGHTS))
    # PARSER.print_usage()

    device = None
    if not options.noelm:

        print("Searching for ELM device...")
        for port, desc, _hwid in comports():
            print("Try {} {}...".format(port, desc))
            device = Device.at_port(port, 38400)
            if device:
                break

    if device:
        print("Using {}".format(device))
    else:
        print("No ELM device set.")

    return 0


if __name__ == '__main__':  # pragma: no cover
    OPTS, ARGS = PARSER.parse_args()
    sys.exit(main(ARGS, OPTS))
