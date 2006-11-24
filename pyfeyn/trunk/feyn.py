import pyx
import math, re
from optparse import OptionParser 

## Version check
majorversionstr = re.sub(r"(\d+\.\d+).*", r"\1", pyx.version.version)
if float(majorversionstr) < 0.9:
    print "Warning: PyFeyn may not work with PyX versions older than 0.9!"

## TeX stuff
pyx.text.defaulttexrunner.set(mode="latex")
if pyx.pykpathsea.find_file("hepnicenames.sty", pyx.pykpathsea.kpse_tex_format):
   pyx.text.defaulttexrunner.preamble(r"\usepackage{hepnicenames}")
else:
   print "Warning: hepnames LaTeX package not found!"

from diagrams import FeynDiagram

## Option parsing
parser = OptionParser()
parser.add_option("-V", "--visual-debug", dest="VDEBUG", action = "store_true", default = False,
                  help="produce visual debug output")
parser.add_option("-D", "--debug", dest="DEBUG", action = "store_true", default = False,
                  help="produce debug output")
(FeynDiagram.options, args) = parser.parse_args()

## Imports
from utils import *
from points import *
from blobs import *
from lines import *
from deco import *
