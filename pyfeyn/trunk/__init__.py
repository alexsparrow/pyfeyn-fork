import pyx

## Version check
import re
majorversionstr = re.sub(r"(\d+\.\d+).*", r"\1", pyx.version.version)
if float(majorversionstr) < 0.9:
    print "Warning: PyFeyn may not work with PyX versions older than 0.9!"


## TeX stuff
pyx.text.defaulttexrunner.set(mode="latex")
if pyx.pykpathsea.find_file("hepnicenames.sty", pyx.pykpathsea.kpse_tex_format):
   pyx.text.defaulttexrunner.preamble(r"\usepackage{hepnicenames}")
else:
   print "Warning: hepnames LaTeX package not found!"


## Set __all__ (for "import * from pyfeyn")
__all__ = ["diagrams", "utils", "points", "blobs", "lines", "deco"]
