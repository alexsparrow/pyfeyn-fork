"""Various blob shapes to represent generic interactions."""

import pyx

from pyfeyn.diagrams import FeynDiagram
from pyfeyn.points import Point
from pyfeyn.utils import Visible
from pyfeyn.deco import PointLabel
from pyfeyn import config


## Blob base class
class Blob(Point, Visible):
    "Base class for all blob-like objects in Feynman diagrams"

    def __init__(self):
        """Dysfunctional constructor, since this is an abstract base class."""
        self.trafos = []
        self.strokestyles = []
        self.fillstyles = []
        self.layeroffset = 1000
        raise Exception("Blobs are an abstract base class: you can't make them!")
    
    def setStrokeStyle(self, strokestyle):
        """Set the stroke style."""
        self.strokestyles = [strokestyle]
        return self

    def clearStrokeStyles(self):
        """Remove all the current stroke styles."""
        self.strokestyles = []
        return self

    def setFillStyle(self, fillstyle):
        """Set the fill style."""
        self.fillstyles = [fillstyle]
        return self

    def clearFillStyles(self):
        """Remove all the current fill styles."""
        self.fillstyles = []
        return self

    def addTrafo(self, trafo):
        """Add a transformation."""
        self.trafos.append(trafo)
        return self

    def clearTrafos(self):
        """Remove transformations."""
        self.trafos = []
        return self

    def setPoints(self, points):
        """Set the points to which this blob is attached."""
        if points:
            self.points = points
            for p in self.points:
                p.blob = self
        else:
            self.points = []

    def addLabel(self, text, displace=-0.15, angle = 0):
        """Add a label."""
        if config.getOptions().DEBUG:
            print "Adding label: " + text
        self.labels.append(PointLabel(text=text, point=self,
                                      displace=displace, angle=angle))
        if config.getOptions().DEBUG:
            print "Labels = " + str(self.labels)
        return self

    def clearLabels(self):
        """Remove all current labels."""
        self.labels = []
        return self



## Circle class (a kind of Blob)
class Circle(Blob):
    """A circular blob"""
    blobshape = "circle"

    def __init__(self,
                 x = None, y = None,
                 center = None,
                 radius = None,
                 fill = [pyx.color.rgb.white],
                 stroke = [pyx.color.rgb.black],
                 points = None):
        """Constructor."""
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
        self.layeroffset = 1000
        self.trafos = []
        self.labels = []
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)
        
    def getPath(self):
        """Get the path of this circle blob."""
        return pyx.path.circle(self.getX(), self.getY(), self.radius)

    def draw(self, canvas):
        """Draw this circle blob."""
        canvas.fill(self.getPath(), [pyx.color.rgb.white])
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
                 fill = [pyx.color.rgb.white],
                 stroke = [pyx.color.rgb.black],
                 points = None):
        """Constructor."""
        self.layeroffset = 1000
        
        if x is not None and y is not None:
            self.setXY(x, y)
        elif center is not None:
            self.setXY(center.getX(), center.getY())
        else:
            raise Exception("No center specified for blob.")

        self.xrad = None
        if xradius:
            self.setXRadius(xradius)
        elif yradius:
            self.setXRadius(yradius)
        else:
            raise Exception("No viable candidate for x-radius")
        self.yrad = None
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
        """Get the component of the radius in the x-direction."""
        return self.xrad


    def setXRadius(self, xrad):
        """Set the component of the radius in the x-direction."""
        self.xrad = float(xrad)
        return self


    def getYRadius(self):
        """Get the component of the radius in the y-direction."""
        return self.yrad


    def setYRadius(self, yrad):
        """Set the component of the radius in the y-direction."""
        self.yrad = float(yrad)
        return self


    def getXYRadius(self):
        """Get the components of the radius in the x and y
        directions at the same time."""
        return self.getXRadius(), self.getYRadius()


    def setXYRadius(self, xrad, yrad):
        """Get the components of the radius in the x and y
        directions at the same time."""
        self.setXRadius(xrad)
        self.setYRadius(yrad)
        return self


    def getPath(self):
        """Get the path for this blob."""
        ucircle = pyx.path.circle(self.xpos, self.ypos, 1.0)
        mytrafo = pyx.trafo.scale(self.xrad, self.yrad, self.xpos, self.ypos)
        epath = ucircle.transformed(mytrafo)
        return epath


    def draw(self, canvas):
        """Draw this blob on the given canvas."""
        canvas.fill(self.getPath(), [pyx.color.rgb.white])
        canvas.fill(self.getPath(), self.fillstyles)
        #canvas.stroke(self.getPath(), [pyx.color.rgb.white])
        canvas.stroke(self.getPath(), self.strokestyles)
        for l in self.labels:
            l.draw(canvas)


## A dictionary to map feynML blob shape choices to blob classes
NamedBlob = {
    "circle" : Circle,
    "ellipse" : Ellipse
    } 
