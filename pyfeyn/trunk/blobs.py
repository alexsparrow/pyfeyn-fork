import pyx
import math

from points import Point

##### Blob base class #####

class Blob:
    "Base class for all blob-like objects in Feynman diagrams"
    fillstyles = [pyx.color.rgb.white]
    strokestyles = [pyx.color.rgb.black]
    trafos = []
    #def __init__(self, centre):

    def strokestyle(self, stylelist):
        self.strokestyles = self.strokestyles + stylelist
        return self

    def fillstyle(self, stylelist):
        self.fillstyles = self.fillstyles + stylelist
        return self

    def trafo(self, trafolist):
        self.trafos = self.trafos + trafolist
        return self

##### Circle class (a kind of Blob) #####

class Circle(Blob):
    def __init__(self, xpos, ypos, rad):
        self.centre = Point(xpos, ypos)
        self.radius = float(rad)

    def draw(self, canvas):
        canvas.fill(pyx.path.circle(self.centre.x(), self.centre.y(), self.radius), [pyx.color.rgb.white])
        canvas.fill(pyx.path.circle(self.centre.x(), self.centre.y(), self.radius), self.fillstyles)
        canvas.stroke(pyx.path.circle(self.centre.x(), self.centre.y(), self.radius), self.strokestyles)

##### Ellipse class (a kind of Blob) #####

class Ellipse(Blob):
    def __init__(self, xpos, ypos, xrad, yrad=None):
        self.centre = Point(xpos, ypos)
        self.xrad = float(xrad)
        if yrad:
           self.yrad = float(yrad)
        else:
           self.yrad = self.xrad

    def draw(self, canvas):
        canvas.fill(pyx.path.circle(self.centre.x(), self.centre.y(), 1.0),
                    [pyx.color.rgb.white] + 
                    [pyx.trafo.scale(self.xrad, self.yrad,
                                     self.centre.x(), self.centre.y())]
                    + self.fillstyles)
        canvas.stroke(pyx.path.circle(self.centre.x(), self.centre.y(), 1.0),
                      [pyx.trafo.scale(self.xrad, self.yrad,
                                       self.centre.x(), self.centre.y())]
                      + self.strokestyles)


NamedBlob = {"circle":Circle, "ellipse":Ellipse}
