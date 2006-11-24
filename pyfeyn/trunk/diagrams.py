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
            if FeynDiagram.options.DEBUG:
                print "#objs = %d" % len(self.__objs)
            self.__objs.append(obj)

    def draw(self, file):
        if FeynDiagram.options.DEBUG:
            print "Final #objs = %d" % len(self.__objs)
        if FeynDiagram.options.VDEBUG:
            print "Running in visual debug mode"
        ## TODO: order of drawing...
        drawingobjs = self.__objs
        for obj in drawingobjs:
            obj.draw(FeynDiagram.currentCanvas)
        if re.search(r".*\.pdf", file):
            FeynDiagram.currentCanvas.writePDFfile(file)
        elif re.search(r".*\.eps", file):
            FeynDiagram.currentCanvas.writeEPSfile(file)


