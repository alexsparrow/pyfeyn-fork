"""
PyFeyn - a simple Python interface for making Feynman diagrams.
"""

__author__ = "Andy Buckley (andy@insectnation.org)"
__version__ = "0.3.0"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2007 Andy Buckley"
__license__ = "GPL"


## Import PyX and check the version
import pyx, re
_majorversionstr = re.sub(r"(\d+\.\d+).*", r"\1", pyx.version.version)
if float(_majorversionstr) < 0.9:
    print "Warning: PyFeyn may not work with PyX versions older than 0.9!"


## Units
pyx.unit.set(uscale = 4, vscale = 4, wscale = 4, xscale = 4)
pyx.unit.set(defaultunit = "cm")


## TeX stuff
pyx.text.defaulttexrunner.set(mode="latex")
if pyx.pykpathsea.find_file("hepnicenames.sty", pyx.pykpathsea.kpse_tex_format):
    pyx.text.defaulttexrunner.preamble(r"\usepackage{hepnicenames}")
else:
    print "Warning: hepnames LaTeX package not found!"


## Set __all__ (for "import * from pyfeyn")
__all__ = ["diagrams", "points", "blobs", "lines", "deco", "utils", "config"]
