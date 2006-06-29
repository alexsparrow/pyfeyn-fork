import pyx
import elementtree.ElementTree as xml
import math

##### FeynDiagram class #####

class FeynDiagram:
    "Objects for holding a set of Feynman diagram components"
    __objs = []

    def add(self, obj):
        self.__objs = self.__objs + [obj]

    def draw(self, canvas):
        for obj in self.__objs:
            obj.draw(canvas)

    def to_xml(self):
        root = xml.Element("diagram")
        for obj in self.__objs:
            root.append(obj.to_xml())
        return xml.tostring(root).replace(">",">\n")
