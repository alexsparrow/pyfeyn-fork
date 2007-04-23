"""Various blob shapes to represent generic interactions."""

from pyx import *
import math

from diagrams import FeynDiagram
from points import Point
from utils import Visible
from deco import PointLabel


## Blob base class
class Blob(Point, Visible):
    "Base class for all blob-like objects in Feynman diagrams"
    def __init__(self):
        raise Exception("Blobs are an abstract base class: you can't make them!")
    
    def setStrokeStyle(self, strokestyle):
        self.strokestyles = [strokestyle]
        return self

    def clearStrokeStyles(self):
        self.strokestyles = []
        return self

    def setFillStyle(self, fillstyle):
        self.fillstyles = [fillstyle]
        return self

    def clearFillStyles(self):
        self.fillstyles = []
        return self

    def addTrafo(self, trafo):
        self.trafos.append(trafo)
        return self

    def clearTrafos(self):
        self.trafos = []
        return self

    def setPoints(self, points):
        if points:
            self.points = points
            for p in self.points:
                p.blob = self
        else:
            self.points = []

    def addLabel(self, text, displace=-0.15, angle = 0):
        if FeynDiagram.options.DEBUG:
            print "Adding label: " + text
        self.labels.append(PointLabel(text=text, point=self, displace=displace, angle=angle))
        if FeynDiagram.options.DEBUG:
            print "Labels = " + str(self.labels)
        return self

    def removeLabels(self):
        self.labels = []
        return self







## Circle class (a kind of Blob)
class Circle(Blob):
    "A circular blob"
    blobshape = "circle"

    def __init__(self,
                 x = None, y = None,
                 center = None,
                 radius = None,
                 fill = [color.rgb.white],
                 stroke = [color.rgb.black],
                 points = None):
        if radius:
            self.radius = float(radius)
        else:
            raise Exception("No (or zero) radius specified for blob.")

        if x is not None and y is not None:
            self.setXY(x, y)
        elif center is not None:
            self.setXY(center.getX(), center.getY())
        else:
            raise Exception("No center specified for blob.")
        
        self.setPoints(points)
        self.fillstyles = fill
        self.strokestyles = stroke
        self.trafos = []
        self.labels = []
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)
        
    def getPath(self):
        return path.circle(self.getX(), self.getY(), self.radius)

    def draw(self, canvas):
        canvas.fill(self.getPath(), [color.rgb.white])
        canvas.fill(self.getPath(), self.fillstyles)
        canvas.stroke(self.getPath(), self.strokestyles)
        for l in self.labels:
            l.draw(canvas)



## Ellipse class (a kind of Blob)
class Ellipse(Blob):
    "An elliptical blob"
    blobshape = "ellipse"

    def __init__(self,
                 x = None, y = None,
                 center = None,
                 xradius = None, yradius = None,
                 fill = [color.rgb.white],
                 stroke = [color.rgb.black],
                 points = None):
        
        if x is not None and y is not None:
            self.setXY(x, y)
        elif center is not None:
            self.setXY(center.getX(), center.getY())
        else:
            raise Exception("No center specified for blob.")

        if xradius:
            self.setXRadius(xradius)
        elif yradius:
            self.setXRadius(yradius)
        else:
            raise Exception("No viable candidate for x-radius")

        if yradius:
            self.setYRadius(yradius)
        elif xradius:
            self.setYRadius(xradius)
        else:
            raise Exception("No viable candidate for y-radius")

        self.setPoints(points)
        self.fillstyles = fill
        self.strokestyles = stroke
        self.trafos = []
        self.labels = []
    
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def getXRadius(self):
        return self.xrad


    def setXRadius(self, xrad):
        self.xrad = float(xrad)
        return self


    def getYRadius():
        return self.yrad


    def setYRadius(self, yrad):
        self.yrad = float(yrad)
        return self


    def getXYRadius():
        return self.getXRadius(), self.getYRadius()


    def setXYRadius(self, xrad, yrad):
        self.setXRadius(xrad)
        self.setYRadius(yrad)
        return self


    def getPath(self):
        ucircle = path.circle(self.xpos, self.ypos, 1.0)
        mytrafo = trafo.scale(self.xrad, self.yrad, self.xpos, self.ypos)
        epath = ucircle.transformed(mytrafo)
        return epath


    def draw(self, canvas):
        canvas.fill(self.getPath(), [color.rgb.white])
        canvas.fill(self.getPath(), self.fillstyles)
        #canvas.stroke(self.getPath(), [color.rgb.white])
        canvas.stroke(self.getPath(), self.strokestyles)
        for l in self.labels:
            l.draw(canvas)


## A dictionary to map feynML blob shape choices to blob classes
NamedBlob = {
    "circle" : Circle,
    "ellipse" : Ellipse
    } 
