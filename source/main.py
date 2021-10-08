"""Main module."""
import sys

import serial
from cli_options import PARSER

COPYRIGHTS = '(C) by Vitaly Bogomolov 2021'
OPTS = None


def main(_argv, _options):
    """Entry point."""
    print("ELM scanner. {}".format(COPYRIGHTS))
    # PARSER.print_usage()

    print("Scanning for serial ports...")
    ports = []
    for i in range(15):
        port_name = "COM{}".format(i + 1)
        # https://pythonhosted.org/pyserial/
        try:
            ports.append(serial.Serial(port=port_name).port)
        except serial.SerialException as exc:
            pass
        except (ValueError, KeyError) as exc:
            print("Wrong port settings:", port_name, str(exc))

    print("Found:", ports)
    return 0


if __name__ == '__main__':  # pragma: no cover
    OPTS, ARGS = PARSER.parse_args()
    sys.exit(main(ARGS, OPTS))
