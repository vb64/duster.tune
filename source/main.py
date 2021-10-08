"""Main module."""
import sys
from cli_options import PARSER

COPYRIGHTS = '(C) by Vitaly Bogomolov 2021'
OPTS = None


def main(_argv, _options):
    """Entry point."""
    print("ELM scanner. {}".format(COPYRIGHTS))

    PARSER.print_usage()
    return 0


if __name__ == '__main__':  # pragma: no cover
    OPTS, ARGS = PARSER.parse_args()
    sys.exit(main(ARGS, OPTS))
