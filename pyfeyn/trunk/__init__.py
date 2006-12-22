import pyx

## Version check
import re
majorversionstr = re.sub(r"(\d+\.\d+).*", r"\1", pyx.version.version)
if float(majorversionstr) < 0.9:
    print "Warning: PyFeyn may not work with PyX versions older than 0.9!"

## Units
pyx.unit.set(uscale = 4, vscale = 4, wscale = 4, xscale = 4)
#pyx.unit.set(defaultunit = "inch")
defunit = pyx.unit.cm
todefunit = pyx.unit.tocm

## TeX stuff
pyx.text.defaulttexrunner.set(mode="latex")
if pyx.pykpathsea.find_file("hepnicenames.sty", pyx.pykpathsea.kpse_tex_format):
   pyx.text.defaulttexrunner.preamble(r"\usepackage{hepnicenames}")
else:
   print "Warning: hepnames LaTeX package not found!"


## Imports
from diagrams import *
from utils import *
from points import *
from blobs import *
from lines import *
from deco import *


## Set __all__ (for "import * from pyfeyn")
__all__ = ["FeynDiagram", "Point", "Vertex", "DecoratedPoint",
           "Blob", "Circle", "Ellipse",
           "Line", "DecoratedLine", "Photon", "Gluon", "Fermion", "NamedLine",
           "Arrow", "Label"]




## Option parsing
from optparse import OptionParser 
parser = OptionParser()
parser.add_option("-V", "--visual-debug", dest="VDEBUG", action = "store_true", default = False,
                  help="produce visual debug output")
parser.add_option("-D", "--debug", dest="DEBUG", action = "store_true", default = False,
                  help="produce debug output")
(FeynDiagram.options, args) = parser.parse_args()
