from pyx import *
import re

## Diagram class
class FeynDiagram:
    currentDiagram = None
    currentCanvas = None
    options = None

    "Objects for holding a set of Feynman diagram components"
    def __init__(self, objects = []):
        self.__objs = objects
        FeynDiagram.currentCanvas = canvas.canvas()
        FeynDiagram.currentDiagram = self

    def add(self, *objs):
        for obj in objs:
            #print "Adding " + str(obj)
            self.__objs.append( obj )

    def draw(self, file):
        if FeynDiagram.options.VDEBUG:
            print "Running in visual debug mode"
        ## TODO: order of drawing...
        for obj in self.__objs:
            obj.draw(FeynDiagram.currentCanvas)
        if re.search(r".*\.pdf", file):
            FeynDiagram.currentCanvas.writePDFfile(file)
        elif re.search(r".*\.eps", file):
            FeynDiagram.currentCanvas.writeEPSfile(file)
