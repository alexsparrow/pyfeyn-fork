"""Utility functions and classes for PyFeyn"""

import pyx
from pyfeyn.diagrams import FeynDiagram
from pyfeyn import config


## Default units
defunit = pyx.unit.cm
todefunit = pyx.unit.tocm


def sign(x):
    """Get the sign of a numeric type"""
    if x < 0:
        return -1
    if x > 0:
        return 1
    if x == 0:
        return 0


class Visible:
    def isVisible(self):
        return True

    def getPath(self):
        return None

    def getVisiblePath(self):
        return self.getPath()

    def setDepth(self, depth):
        self.depth = depth
        return self

    def getDepth(self):
        if self.__dict__.has_key("depth"):
            return self.depth
        else:
            return None
        
    def __cmp__(self, other):
        """Compare with another visible class, just using layers."""
        if other is None:
            return -1

        if config.getOptions().DEBUG:
            print "Comparing visible classes: ", \
                  self.__class__, "->", self.getDepth(), "vs.", \
                  other.__class__, "->", other.getDepth()
        else:
            return cmp(self.getDepth(), other.getDepth())
