import pyx
import math

##### Version check #####

if float(pyx.version.version)<0.9:
    print "Warning: PyFeyn may not work with PyX versions older than 0.9 !"

pyx.text.defaulttexrunner.set(mode="latex")
if pyx.pykpathsea.find_file("hepnicenames.sty",None):
   pyx.text.defaulttexrunner.preamble(r"\usepackage{hepnicenames}")
else:
   print "Warning: hepnames LaTeX package not found!"

from utils import sign

from diagrams import FeynDiagram

from points import Point
from points import DecoratedPoint
from points import NamedMark

from blobs import Blob
from blobs import Circle
from blobs import Ellipse
from blobs import NamedBlob

from lines import Line
from lines import DecoratedLine
from lines import Gluon
from lines import Photon
from lines import NamedLine

from deco import Arrow
from deco import TeXLabel
from deco import FreeTeXLabel
from deco import Coil

