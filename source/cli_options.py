"""CLI options."""
from optparse import OptionParser

VERSION = '1.0'
USAGE = '\n'.join([
  "%prog [OPTIONS]\nor",
  "%prog --help"
])


PARSER = OptionParser(
  usage=USAGE,
  version="%prog version {}".format(VERSION)
)
PARSER.add_option(
  "--com",
  dest="portname",
  default="COM1",
  help="Set target COM port name. Default is COM1"
)
