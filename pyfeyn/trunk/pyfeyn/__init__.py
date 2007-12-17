"""
PyFeyn - a simple Python interface for making Feynman diagrams.
"""

__author__ = "Andy Buckley & Georg von Hippel (pyfeyn@projects.hepforge.org)"
__version__ = "0.3.1"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2007 Andy Buckley"
__license__ = "GPL"


## Import PyX and set up some things
try:
    import pyx

    ## Check the version
    from distutils.version import StrictVersion as Version
    if Version(pyx.version.version) < Version("0.9.0"):
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

    ## Set __all__ (for "from pyfeyn import *")
    __all__ = ["diagrams", "points", "blobs", "lines", "deco", "utils", "config"]
except:
    print "You don't have PyX - that's a problem unless you're just running the setup script."
