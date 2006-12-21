
## Units
pyx.unit.set(uscale = 4, vscale = 4, wscale = 4, xscale = 4)
#pyx.unit.set(defaultunit = "inch")
defunit = pyx.unit.cm
todefunit = pyx.unit.tocm

## Imports
from diagrams import *
from utils import *
from points import *
from blobs import *
from lines import *
from deco import *


## Option parsing
from optparse import OptionParser 
parser = OptionParser()
parser.add_option("-V", "--visual-debug", dest="VDEBUG", action = "store_true", default = False,
                  help="produce visual debug output")
parser.add_option("-D", "--debug", dest="DEBUG", action = "store_true", default = False,
                  help="produce debug output")
(FeynDiagram.options, args) = parser.parse_args()
