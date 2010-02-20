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
        """Constructor."""
        self.setXY(x, y)
        self.setBlob(blob)
        self.labels = []


    def addLabel(self, text, displace=0.3, angle = 0, size=pyx.text.size.normalsize):
        """Add a LaTeX label to this point, either via parameters or actually as
        a PointLable object."""
        if config.getOptions().DEBUG:
            print "Adding label: " + text
        self.labels.append(PointLabel(text=text, point=self, displace=displace, angle=angle, size=size))
        if config.getOptions().DEBUG:
            print "Labels = " + str(self.labels)
        return self

            
    def removeLabels(self):
        """Remove all labels from this point."""
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
        """Constructor."""
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
        """Return the path belonging to the blob or marker attached to this point, if any."""
        if self.blob:
            return self.getBlob().getPath()
        elif self.marker:
            return self.getMark().getPath()
        else:
            return None

    def getMark(self):
        """Return the marker attached to this point."""
        return self.marker

    def setMark(self, mark):
        """Set the marker attached to this point."""
        self.marker = mark
        if self.marker is not None:
            self.marker.setPoint(self)
        # if size is None and self.radius == 0: # change shape of a true point?
        #     self.radius = 4*unit.t_pt # probably want to use default size
        return self

    def getBlob(self):
        """Return the blob attached to this point."""
        return self.blob

    def setBlob(self, blob):
        """Set the blob attached to this point."""
        self.blob = blob
        if self.blob is not None:
            self.blob.setPoints([self])
        return self

    def getFillstyles(self):
        """Return the fillstyles for the marker or blob attached to this point."""
        return self.fillstyles

    def setFillstyles(self, styles):
        """Set the fillstyles for the marker or blob attached to this point."""
        self.fillstyles = styles
        return self

    def addFillstyles(self, styles):
        """Add fillstyles to the marker or blob attached to this point."""
        self.fillstyles.add(styles)
        return self

    def addFillstyle(self, style):
        """Add a fillstyle to the marker or blob attached to this point."""
        self.fillstyles.append(style)
        return self

    def getStrokestyles(self):
        """Return the stroke styles for the marker or blob attached to this point."""
        return self.strokestyles

    def setStrokestyles(self, styles):
        """Set the stroke styles for the marker or blob attached to this point."""
        self.strokestyles = styles
        return self

    def addStrokestyles(self, styles):
        """Add stroke styles to the marker or blob attached to this point."""
        self.strokestyles.add(styles)
        return self

    def addStrokestyle(self, style):
        """Add a stroke style to the marker or blob attached to this point."""
        self.strokestyles.append(style)
        return self
    
    def draw(self, canvas):
        """Draw the marker or blob attached to this point."""
        if self.getPath():
            canvas.fill(self.getPath(), self.fillstyles)
            canvas.stroke(self.getPath(), self.strokestyles)
        for l in self.labels:
            l.draw(canvas)


## Vertex is an alias for DecoratedPoint
Vertex = DecoratedPoint
    

class Mark:
    def getPoint(self):
        """Return the point to which this marker is attached."""
        return self.point

    def setPoint(self, point):
        """Attach this marker to a new point."""
        self.point = point
        return self


class SquareMark(Mark):
    def __init__(self,
                 size = 0.075):
        """A square mark."""
        self.size = size
        self.point = None
        
    def getPath(self):
        """Return the path for this marker."""
        if self.getPoint() is not None:
            x, y = self.point.getXY()
            return pyx.box.rect(x-self.size, y-self.size, 2*self.size, 2*self.size).path()
        return None    


class CircleMark(Mark):
    def __init__(self,
                 size = 0.075):
        """A circular mark."""
        self.radius = size
        self.point = None
        
    def getPath(self):
        """Return the path for this marker."""
        if self.point is not None:
            x, y = self.point.getXY()
            return pyx.path.circle(x, y, self.radius).path()
        return None

class PolygonalMark(Mark):
    def __init__(self,
                 size = 0.075, corners = 3):
        """A polygonal mark."""
        self.radius = size
        self.n = corners
        self.point = None

    def getPath(self):
        """Return the path for this marker."""
        if self.point is not None:
            x, y = self.point.getXY()
            return pyx.box.polygon([(x-self.radius*math.sin(i*2*math.pi/self.n),
                                     y+self.radius*math.cos(i*2*math.pi/self.n))
                      for i in range(self.n)]).path()
        return None

class StarshapeMark(Mark):
    def __init__(self,
                 size = 0.075, raysize = 0.05, rays = 3):
        """A star-shaped mark."""
        self.radius = size
        self.wiggle = raysize
        self.n = rays
        self.point = None

    def getPath(self):
        """Return the path for this marker."""
        if self.point is not None:
            x, y = self.point.getXY()
            return pyx.box.polygon([(x-(self.radius-self.wiggle*(i%2))*math.sin(i*math.pi/self.n),
                                     y+(self.radius-self.wiggle*(i%2))*math.cos(i*math.pi/self.n))
                      for i in range(2*self.n)]).path()
        return None



## Convenience constants
CIRCLE = CircleMark()
SQUARE = SquareMark()

TRIANGLE = PolygonalMark(corners=3)
DIAMOND = PolygonalMark(corners=4)
PENTAGON = PolygonalMark(corners=5)
HEXAGON = PolygonalMark(corners=6)
HEPTAGON = PolygonalMark(corners=7)
OCTAGON = PolygonalMark(corners=8)

TETRASTAR = StarshapeMark(rays=4)
STAR = StarshapeMark(rays=5)
HEXASTAR = StarshapeMark(rays=6)
OCTOSTAR = StarshapeMark(rays=8)


