"""PyFeyn - a simple Python interface for making Feynman diagrams."""

__author__ = "Andy Buckley (andy@insectnation.org)"
__version__ = "0.2.0b1"
__date__ = "$Date: 2006/08/05 00:14:20 $"
__copyright__ = "Copyright (c) 2007 Andy Buckley"
__license__ = "GPL"

import pyx

## Version check
import re
majorversionstr = re.sub(r"(\d+\.\d+).*", r"\1", pyx.version.version)
if float(majorversionstr) < 0.9:
    print "Warning: PyFeyn may not work with PyX versions older than 0.9!"


## Units
pyx.unit.set(uscale = 4, vscale = 4, wscale = 4, xscale = 4)
#pyx.unit.set(defaultunit = "inch")


## TeX stuff
pyx.text.defaulttexrunner.set(mode="latex")
if pyx.pykpathsea.find_file("hepnicenames.sty", pyx.pykpathsea.kpse_tex_format):
   pyx.text.defaulttexrunner.preamble(r"\usepackage{hepnicenames}")
else:
   print "Warning: hepnames LaTeX package not found!"


## Set __all__ (for "import * from pyfeyn")
__all__ = ["diagrams", "points", "blobs", "lines", "deco", "utils"]

#__all__ = ["FeynDiagram",
#           "Point", "Vertex", "DecoratedPoint",
#           "Blob", "Circle", "Ellipse",
#           "Line", "DecoratedLine", "Photon", "Gluon", "Fermion", "NamedLine",
#           "Arrow", "Label"]


## Option parsing
from optparse import OptionParser 
_parser = OptionParser()
_parser.add_option("-V", "--visual-debug", dest="VDEBUG", action = "store_true", default = False,
                   help="produce visual debug output")
_parser.add_option("-D", "--debug", dest="DEBUG", action = "store_true", default = False,
                   help="produce debug output")
from diagrams import FeynDiagram
(FeynDiagram.options, args) = _parser.parse_args()
