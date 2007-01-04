"""Utility functions and classes for PyFeyn"""
import pyx


defunit = pyx.unit.cm
todefunit = pyx.unit.tocm


def sign(x):
    """Get the sign of a numeric type"""
    if x < 0: return -1
    if x > 0: return 1
    if x == 0: return 0


class Visible:
    def isVisible(self):
        return True

    def getPath(self):
        return None

    def getVisiblePath(self):
        return self.getPath()
