from pyx import *
import elementtree.ElementTree as xml
import md5, math

from points import Point


## Blob base class
class Blob(Point):
    "Base class for all blob-like objects in Feynman diagrams"
    def __init__(self, xpos, ypos, fillstyles = [color.rgb.white], strokestyles = [color.rgb.black]):
        raise Exception("Blob is an abstract base class: you can't make 'em!")
        #self.fillstyles = fillstyles
        #self.strokestyles = strokestyles
        #self.trafos = []

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
                          {"id" : "V%s" % md5.md5(str(self.xpos, self.ypos)).hexdigest(),
                           "x" : str(self.xpos), "y" : str(self.ypos),
                           "shape" : hasattr(self,"blobshape") and self.blobshape or "circle"})
        #xml.dump(ele)
        return ele


## Circle class (a kind of Blob)
class Circle(Blob):
    "A circular blob"
    blobshape = "circle"

    def __init__(self, xpos, ypos, radius,
                 fillstyles = [color.rgb.white], strokestyles = [color.rgb.black]):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = float(radius)
        ## Can I inherit these by calling the base class __init__?
        self.fillstyles = fillstyles  #[color.rgb.white]
        self.strokestyles = strokestyles  #[color.rgb.black]
        self.trafos = []

    def path(self):
        return path.circle(self.xpos, self.ypos, self.radius)

    def draw(self, canvas):
        canvas.fill(self.path(), [color.rgb.white])
        canvas.fill(self.path(), self.fillstyles)
        canvas.stroke(self.path(), self.strokestyles)


## Ellipse class (a kind of Blob)
class Ellipse(Blob):
    "An elliptical blob"
    blobshape = "ellipse"

    def __init__(self, xpos, ypos, xradius, yradius=None,
                 fillstyles = [color.rgb.white], strokestyles = [color.rgb.black]):
        self.xpos = xpos
        self.ypos = ypos
        self.xrad = float(xradius)
        if yradius:
           self.yrad = float(yradius)
        else:
           self.yrad = self.xrad
        ## Can I inherit these by calling the base class __init__?
        self.fillstyles = fillstyles #[color.rgb.white]
        self.strokestyles = strokestyles #[color.rgb.black]
        self.trafos = []

    def path(self):
        ucircle = path.circle(self.xpos, self.ypos, 1.0)
        mytrafo = trafo.scale(self.xrad, self.yrad, self.xpos, self.ypos)
        epath = ucircle.transformed(mytrafo)
        return epath

    def draw(self, canvas):
        canvas.fill(self.path(), [color.rgb.white] + self.fillstyles)
        canvas.stroke(self.path(), [color.rgb.white] + self.strokestyles)


## A dictionary to map feynML blob shape choices to blob classes
## TODO: move XML stuff to an external class?
NamedBlob = {"circle" : Circle, "ellipse" : Ellipse}
