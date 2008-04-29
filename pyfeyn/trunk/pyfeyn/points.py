"""Various types of points for vertices etc."""

import pyx
from copy import copy
import math

from pyfeyn.diagrams import FeynDiagram
from pyfeyn.utils import Visible
from pyfeyn.deco import PointLabel
from pyfeyn import config


def midpoint(point1, point2):
    "Return the point midway between this point and the argument."
    return Point( (point1.getX() + point2.getX()) / 2.0,
                  (point1.getY() + point2.getY()) / 2.0 )

def distance(point1, point2):
    "Calculate the distance between this point and the argument."
    return math.hypot(point1.x()-point2.x(), point1.y()-point2.y())


## Point base class
class Point:
    """Base class for all pointlike objects in Feynman diagrams."""

    def __init__(self, x, y, blob = None):
        self.setXY(x, y)
        self.setBlob(blob)
        self.labels = []


    def addLabel(self, text, displace=0.3, angle = 0):
        """Add a LaTeX label to this point, either via parameters or actually as
        a PointLable object."""
        if config.getOptions().DEBUG:
            print "Adding label: " + text
        self.labels.append(PointLabel(text=text, point=self, displace=displace, angle=angle))
        if config.getOptions().DEBUG:
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
        return midpoint(self, otherpoint)

    def distance(self, otherpoint):
        "Calculate the distance between this point and the argument."
        return distance(self, otherpoint)

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
                 blob = None,
                 fill = [pyx.color.rgb.black],
                 stroke = [pyx.color.rgb.black]):
        self.setXY(xpos, ypos)
        self.labels = []
        self.setMark(copy(mark))
        self.setBlob(blob)
        self.layeroffset = 1000
        self.fillstyles = copy(fill) # lists are mutable --
        self.strokestyles = copy(stroke) # hence make a copy!
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)

    def getPath(self):
        if self.blob:
            return self.getBlob().getPath()
        elif self.marker:
            return self.getMark().getPath()
        else:
            return None

    def getMark(self):
        return self.marker

    def setMark(self, mark):
        self.marker = mark
        if self.marker is not None:
            self.marker.setPoint(self)
        # if size is None and self.radius == 0: # change shape of a true point?
        #     self.radius = 4*unit.t_pt # probably want to use default size
        return self

    def getBlob(self):
        return self.blob

    def setBlob(self, blob):
        self.blob = blob
        if self.blob is not None:
            self.blob.setPoints([self])
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


## Vertex is an alias for DecoratedPoint
Vertex = DecoratedPoint
    

class Mark:
    def getPoint(self):
        return self.point

    def setPoint(self, point):
        self.point = point
        return self


class SquareMark(Mark):
    def __init__(self,
                 size = 0.075):
        self.size = size
        self.point = None
        
    def getPath(self):
        if self.getPoint() is not None:
            x, y = self.point.getXY()
            return pyx.box.rect(x-self.size, y-self.size, 2*self.size, 2*self.size).path()
        return None    


class CircleMark(Mark):
    def __init__(self,
                 size = 0.075):
        self.radius = size
        self.point = None
        
    def getPath(self):
        if self.point is not None:
            x, y = self.point.getXY()
            return pyx.path.circle(x, y, self.radius).path()
        return None

## Convenience constants
CIRCLE = CircleMark()
SQUARE = SquareMark()
