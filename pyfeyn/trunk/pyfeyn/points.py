"""Various types of points for vertices etc."""

from pyx import *
from copy import *
import math

from pyfeyn.diagrams import FeynDiagram
from pyfeyn.utils import Visible
from pyfeyn.deco import PointLabel


## Point base class
class Point:
    """Base class for all pointlike objects in Feynman diagrams."""
    def __init__(self, x, y, blob = None):
        self.setXY(x, y)
        self.setBlob(blob)
        self.labels = []

#     def __plus__(self, point = None):
#         if point:
#             addx, addy = point.getX(), point.getY()
#             self.setX(self.getX() + addx)
#             self.setY(self.getY() + addy)
#         else:
#             raise Exception("Tried to add a null x or y component")

#     def __minus__(self, point = None):
#         if point:
#             addx, addy = point.getX(), point.getY()
#             self.setX(self.getX() - addx)
#             self.setY(self.getY() - addy)
#         else:
#             raise Exception("Tried to subtract a null x or y component")

    def addLabel(self, text, displace=0.3, angle = 0):
        """Add a LaTeX label to this point, either via parameters or actually as
        a PointLable object."""
        if FeynDiagram.options.DEBUG:
            print "Adding label: " + text
        self.labels.append(PointLabel(text=text, point=self, displace=displace, angle=angle))
        if FeynDiagram.options.DEBUG:
            print "Labels = " + str(self.labels)
        return self

            
    def removeLabels(self):
        self.labels = []
        return self


    def draw(self, canvas):
        "Do nothing (abstract base class)."
        pass

    def getPath(self):
        "Return the path of the attached blob path, if there is one, otherwise None."
        if self.getBlob() and hasattr(self.getBlob(), "getPath"):
            return self.getBlob().getPath()
        else:
            return None

    def midpoint(self, otherpoint):
        "Return the point midway between this point and the argument."
        return Point( (self.getX() + otherpoint.getX()) / 2.0,
                      (self.getY() + otherpoint.getY()) / 2.0 )

    def distance(self, otherpoint):
        "Calculate the distance between this point and the argument."
        return math.hypot(self.x()-otherpoint.x(), self.y()-otherpoint.y()) 

    def intercept(self, otherpoint):
        "Return the y-intercept of the straight line defined by this point and the argument."
        return self.y() - self.tangent(otherpoint) * self.x()


    def tangent(self,otherpoint):
        "Return the tangent of the straight line defined by this point and the argument."
        if otherpoint.x() != self.x():
           return (otherpoint.y() - self.y()) / (otherpoint.x() - self.x())
        else:
           return float(10000) ## An arbitrary large number to replace infinity


    def arg(self, otherpoint):
        """Return the angle between the x-axis and the straight line defined
        by this point and the argument (cf. complex numbers)."""
        arg = None
        if otherpoint.x() == self.x():
            if otherpoint.y() > self.y():
                arg = math.pi / 2.0
            elif otherpoint.y() < self.y():
                arg = 3 * math.pi / 2.0  # this will be reset to 0 if the points are the same

        if otherpoint.y() == self.y():
            if otherpoint.x() < self.x():
                arg = math.pi
            else:
                arg = 0.0

        if otherpoint.x() != self.x() and otherpoint.y() != self.y():
            arg = math.atan( (otherpoint.y() - self.y()) / (otherpoint.x() - self.x()) )
            if otherpoint.x() < self.x():
                arg += math.pi
            elif otherpoint.y() < self.y():
                arg += 2 * math.pi 

        ## Convert to degrees
        argindegs = math.degrees(arg)
        return argindegs


    def getBlob(self):
        "Get the attached blob."
        return self.blob


    def setBlob(self, blob):
        "Set the attached blob."
        self.blob = blob
        return self

 
    def getX(self):
        "Return the x-coordinate of this point."
        return self.xpos

    def setX(self, x):
        "Set the x-coordinate of this point."
        self.xpos = x
        return self

    def getY(self):
        "Return the y-coordinate of this point."
        return self.ypos

    def setY(self, y):
        "Set the y-coordinate of this point."
        self.ypos = y
        return self

    def getXY(self):
        "Return the x and y coordinates of this point as a 2-tuple."
        return self.getX(), self.getY()

    def setXY(self, xpos, ypos):
        "Set the x and y coordinates of this point."
        self.setX(float(xpos))
        self.setY(float(ypos))
        return self

    def x(self):
        "Alias for getX()."
        return self.getX()

    def y(self):
        "Alias for getY()."
        return self.getY()

    def xy(self):
        "Alias for getXY()."
        return self.getXY()


## Decorated point class
class DecoratedPoint(Point, Visible):
    "Class for a point drawn with a marker"
    def __init__(self, xpos, ypos,
                 mark = None,
                 size = 0.1,
                 fill = [color.rgb.black],
                 stroke = [color.rgb.black],
                 blob = None):
        self.setXY(xpos, ypos)
        self.labels = []
        
        if mark != None:
           self.marker = NamedMark[mark]
           self.radius = size
        else:
           self.marker = None
           self.radius = 0 

        self.blob = blob
        self.fillstyles = copy( fill ) # lists are mutable --
        self.strokestyles = copy( stroke ) # hence make a copy!
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)

    def getPath(self):
        if self.blob:
            return self.blob.getPath()
        elif self.marker:
            return self.marker(self.xpos, self.ypos, self.radius).path()
        else:
            return None

    def mark(self, mark, size=None):
        self.marker = mark
        if size is not None:
           self.radius = size
        if size is None and self.radius == 0: # change shape of a true point?
           self.radius = 4*unit.t_pt # probably want to use default size
        return self

    def size(self, size):
        self.radius = size
        return self

    def getFillstyles(self):
        return self.fillstyles

    def setFillstyles(self, styles):
        self.fillstyles = styles
        return self

    def addFillstyles(self, styles):
        self.fillstyles.add(styles)
        return self

    def addFillstyle(self, style):
        self.fillstyles.append(style)
        return self

    def getStrokestyles(self):
        return self.strokestyles

    def setStrokestyles(self, styles):
        self.strokestyles = styles
        return self

    def addStrokestyles(self, styles):
        self.strokestyles.add(styles)
        return self

    def addStrokestyle(self, style):
        self.strokestyles.append(style)
        return self
    
    def draw(self, canvas):
        if self.getPath():
            canvas.fill(self.getPath(), self.fillstyles)
            canvas.stroke(self.getPath(), self.strokestyles)
        for l in self.labels:
            l.draw(canvas)


class Vertex(DecoratedPoint):
    """Vertex is an alias for DecoratedPoint"""
    pass




# A square marker
_square = lambda x, y, r : box.rect(x-r, y-r, 2*r, 2*r)

# A dictionary mapping feynML "mark" choices to marker classes
NamedMark = {"square": _square, "circle": path.circle}
MarkedName = {_square: "square", path.circle : "circle"}
