"""Main module."""
import sys

import serial
from cli_options import PARSER
from elm import Device

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
        try:
            # https://pythonhosted.org/pyserial/
            ports.append(serial.Serial(port=port_name).port)
        except serial.SerialException:
            pass
        except (ValueError, KeyError) as exc:
            print("Wrong port settings:", port_name, str(exc))

    if not ports:
        print("Com port not found.")
        return 1

    print("Found:", ports)
    device = None
    for port in ports:
        print("Try {}...".format(port))
        device = Device.at_port(port, 38400)
        if device:
            break

    if not device:
        print("No ELM divice found.")
        return 1

    print("Using {}".format(device))
    return 0


if __name__ == '__main__':  # pragma: no cover
    OPTS, ARGS = PARSER.parse_args()
    sys.exit(main(ARGS, OPTS))
