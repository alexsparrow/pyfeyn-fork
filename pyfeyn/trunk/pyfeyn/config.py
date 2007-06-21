"""Handle runtime options and command line option parsing."""

from optparse import OptionParser 


def addPyfeynOptions(parser):
    parser.add_option("-V", "--visual-debug", dest="VDEBUG", action = "store_true",
                      default = False, help="produce visual debug output")
    parser.add_option("-D", "--debug", dest="DEBUG", action = "store_true",
                      default = False, help="produce debug output")
    parser.add_option("-d", "--draft", dest="DRAFT", action = "store_true",
                      default = False, help="produce draft output, skipping time-consuming calculations")
    return parser


def processOptions(parser=None):
    global _opts
    if parser is None:
        parser = OptionParser()
        addPyfeynOptions(parser)
    (_options, _args) = parser.parse_args()
    _opts = _options
    return _options, _args


class OptionSet:
    """A container for options."""
    def __init__(self):
        self.DEBUG = False
        self.VDEBUG = False
        self.DRAFT = False


_opts = OptionSet()


def getOptions():
    return _opts
