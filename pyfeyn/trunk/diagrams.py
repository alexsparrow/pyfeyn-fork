import pyx
import math

## TODO: Eliminate dependency on external modules as much as possible:
## standard Pyfeyn doesn't need to be able to "do" XML --- at least not
## yet! XML conversion (in both directions) should probably be done by
## an external module of some kind. Additionally, etree is standard
## in Python 2.5 onwards - once 2.5 is widespread, we can maybe relax
## this restriction a bit.
import elementtree.ElementTree as xml

##### FeynDiagram class #####
class FeynDiagram:
    currentDiagram = None
    currentCanvas = None

    "Objects for holding a set of Feynman diagram components"
    def __init__(self, objects = []):
        self.__objs = objects
        FeynDiagram.currentCanvas = pyx.canvas.canvas()
        FeynDiagram.currentDiagram = self

    def add(self, *objs):
        for obj in objs:
            self.__objs.append( obj )

    def draw(self):
        ## TODO: order of drawing...
        for obj in self.__objs:
            obj.draw(FeynDiagram.currentCanvas)

    ## TODO: Put this in an external class? And CamelCase is the chosen
    ## "standard" for method names (I've moved to_xml() to toXML() for now)
    def toXML(self):
        root = xml.Element("diagram")
        for obj in self.__objs:
            root.append(obj.to_xml())
        return xml.tostring(root).replace(">",">\n")
