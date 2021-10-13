"""CLI options."""
from optparse import OptionParser
import vehicles

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
  help="Set COM port name for ELM327 device. Default is COM1."
)
PARSER.add_option(
  "--vehicle",
  dest="vehicle_code",
  choices=list(vehicles.DATA.keys()) + [''],
  default='',
  help="Set target vehicle for explore. Default is empty (not selected)."
)
PARSER.add_option(
  "--noelm",
  action="store_true",
  dest="noelm",
  default=False,
  help="Don't search for ELM327 device, just view ecus."
)
PARSER.add_option(
  "--ecuzip",
  dest="ecus_file",
  default="ecu.zip",
  help="Path to zipped ecu database file. Default is ecu.zip in current dir."
)
