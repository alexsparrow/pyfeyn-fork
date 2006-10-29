from pyx import *
import elementtree.ElementTree as xml
import md5, math

from points import Point


## Blob base class
class Blob:
    "Base class for all blob-like objects in Feynman diagrams"
    def __init__(self):
        self.fillstyles = [color.rgb.white]
        self.strokestyles = [color.rgb.black]
        self.trafos = []

    def strokestyle(self, stylelist):
        self.strokestyles.append(stylelist)
        return self

    def fillstyle(self, stylelist):
        self.fillstyles.append(stylelist)
        return self

    def trafo(self, trafolist):
        self.trafos.append(trafolist)
        return self

    def toXML(self):
        ele = xml.Element("blob",
                          {"id" : "V%s" % md5.md5(str((self.centre.xpos,self.centre.ypos))).hexdigest(),
                           "x" : str(self.centre.xpos),
                           "y" : str(self.centre.ypos),
                           "shape" : hasattr(self,"blobshape") and self.blobshape or "circle"})
        #xml.dump(ele)
        return ele


## Circle class (a kind of Blob)
class Circle(Blob):
    "A circular blob"
    blobshape = "circle"

    def __init__(self, xpos, ypos, radius,
                 fillstyles = [color.rgb.white], strokestyles = [color.rgb.black]):
        self.centre = Point(xpos, ypos)
        self.radius = float(radius)
        ## Can I inherit these by calling the base class __init__?
        self.fillstyles = fillstyles  #[color.rgb.white]
        self.strokestyles = strokestyles  #[color.rgb.black]
        self.trafos = []

    def draw(self, canvas):
        canvas.fill(path.circle(self.centre.x(), self.centre.y(), self.radius), [color.rgb.white])
        canvas.fill(path.circle(self.centre.x(), self.centre.y(), self.radius), self.fillstyles)
        canvas.stroke(path.circle(self.centre.x(), self.centre.y(), self.radius), self.strokestyles)


## Ellipse class (a kind of Blob)
class Ellipse(Blob):
    "An elliptical blob"
    blobshape = "ellipse"

    def __init__(self, xpos, ypos, xradius, yradius=None,
                 fillstyles = [color.rgb.white], strokestyles = [color.rgb.black]):
        self.centre = Point(xpos, ypos)
        self.xrad = float(xradius)
        if yradius:
           self.yrad = float(yradius)
        else:
           self.yrad = self.xrad
        ## Can I inherit these by calling the base class __init__?
        self.fillstyles = fillstyles #[color.rgb.white]
        self.strokestyles = strokestyles #[color.rgb.black]
        self.trafos = []


    def draw(self, canvas):
        ucircle = path.circle(self.centre.x(), self.centre.y(), 1.0)
        mytrafo = trafo.scale(self.xrad, self.yrad, self.centre.x(), self.centre.y())
        canvas.fill(ucircle, [color.rgb.white] + [mytrafo] + self.fillstyles)
        canvas.stroke(ucircle, [color.rgb.white] + [mytrafo] + self.strokestyles)


## A dictionary to map feynML blob shape choices to blob classes
## TODO: move XML stuff to an external class?
NamedBlob = {"circle" : Circle, "ellipse" : Ellipse}
