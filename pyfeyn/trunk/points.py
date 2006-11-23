import pyx
import math
from diagrams import *


## Point base class
class Point:
    "Base class for all pointlike objects in Feynman diagrams"
    def __init__(self, xpos, ypos, blob = None):
        self.setpos(xpos, ypos)
        self.blob = blob
        ## Add this to the current diagram automatically
        #print "foo" + str(self) + str(xpos) + " " + str(ypos)
        FeynDiagram.currentDiagram.add(self)

    def draw(self, canvas):
        pass

    def path(self):
        if self.blob:
            return self.blob.path()
        else:
            return None

    def midpoint(self, otherpoint):
        return Point( (self.x() + otherpoint.x()) / 2.0,
                      (self.y() + otherpoint.y()) / 2.0 )

    def distance(self, otherpoint):
        return math.hypot(self.x()-otherpoint.x(), self.y()-otherpoint.y()) 

    def intercept(self,otherpoint):
        return self.y() - self.tangent(otherpoint) * self.x()

    def tangent(self,otherpoint):
        if otherpoint.x() != self.x():
           return (otherpoint.y() - self.y()) / (otherpoint.x() - self.x())
        else:
           return 9999. ## An arbitrary large number to replace infinity

    def arg(self, otherpoint):
        if otherpoint.x() != self.x():
           arg = math.atan( (otherpoint.y() - self.y()) /
                            (otherpoint.x() - self.x()) )
        else:
            arg = math.pi/2.
        ## Handle tangent sign ambiguity
        if otherpoint.x() < self.x():
            arg = arg + math.pi
        ## Convert to degrees
        return math.degrees(arg)
 
    def x(self):
        return self.xpos

    def y(self):
        return self.ypos

    def pos(self):
        return self.xpos, self.ypos

    def setpos(self, xpos, ypos):
        self.xpos = float(xpos)
        self.ypos = float(ypos)



## Decorated point class
class DecoratedPoint(Point):
    "Class for a point drawn with a marker"
    def __init__(self, xpos, ypos, mark=None, blob = None,
                 size=4*pyx.unit.t_pt,
                 fillstyles=[pyx.color.rgb.black],
                 strokestyles=[pyx.color.rgb.black]):
        self.setpos(xpos, ypos)
        if mark is not None:
           self.marker = mark
           self.radius = size
        else:
           self.marker = NamedMark["square"]
           self.radius = 0 
        self.blob = blob
        self.fillstyles = [x for x in fillstyles] # lists are mutable --
        self.strokestyles = [x for x in strokestyles] # hence make a copy!

    def path(self):
        if self.blob:
            return self.blob.path()
        else:
            return self.marker(self.xpos, self.ypos, self.radius).path()

    def mark(self, mark, size=None):
        self.marker = mark
        if size is not None:
           self.radius = size
        if size is None and self.radius == 0: # change shape of a true point?
           self.radius = 4*pyx.unit.t_pt # probably want to use default size
        return self

    def size(self,size):
        self.radius = size
        return self

    def fillstyle(self,style):
        self.fillstyles.append(style)
        return self

    def strokestyle(self,style):
        self.strokestyles.append(style)
        return self

    def draw(self, canvas):
        canvas.fill(self.path(), self.fillstyles)
        canvas.stroke(self.path(), self.strokestyles)



# A square marker
_square = lambda x,y,r:pyx.box.rect(x-r,y-r,2*r,2*r)

# A dictionary mapping feynML "mark" choices to marker classes
NamedMark = {"square": _square, 
             "circle": pyx.path.circle}
MarkedName = {_square: "square",
              pyx.path.circle: "circle"}
 
