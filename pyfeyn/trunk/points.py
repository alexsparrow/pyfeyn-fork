import pyx
import math


##### Point base class #####

class Point:
    "Base class for all pointlike objects in Feynman diagrams"
    xpos = 0.0
    ypos = 0.0

    def __init__(self, xpos, ypos):
        self.setpos(xpos, ypos)

    def draw(self, canvas):
        pass

    def midpoint(self, otherpoint):
        return Point( (self.x() + otherpoint.x()) / 2.0,
                      (self.y() + otherpoint.y()) / 2.0 )

    def distance(self, otherpoint):
        return math.hypot(self.x()-otherpoint.x(), self.y()-otherpoint.y()) 

    def intercept(self,otherpoint):
        return self.y() - self.tangent(otherpoint) * self.x()

    def tangent(self,otherpoint):
        return (otherpoint.y() - self.y()) / (otherpoint.x() - self.x())

    def arg(self, otherpoint):
        arg = math.atan( (otherpoint.y() - self.y()) /
                         (otherpoint.x() - self.x()) )
        # Handle tangent sign ambiguity
        if otherpoint.x() < self.x():
            arg = arg + math.pi
        # Convert to degrees
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

##### Decorated Point class #####

class DecoratedPoint(Point):

    def __init__(self, xpos, ypos, mark=None, size=4*pyx.unit.t_pt, fillstyles=[pyx.color.rgb.black], strokestyles=[pyx.color.rgb.black]):
        self.setpos(xpos, ypos)
        if mark is not None:
           self.mark = mark(xpos,ypos,size)
        else:
           self.mark = pyx.box.rect(xpos-size,ypos-size,2*size,2*size)
        self.fillstyles = fillstyles
        self.strokestyles = strokestyles

    def draw(self, canvas):
        canvas.fill(self.mark.path(),self.fillstyles)
        canvas.stroke(self.mark.path(),self.strokestyles)


