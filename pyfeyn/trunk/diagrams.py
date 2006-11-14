import pyx
import math

## Diagram class
class FeynDiagram:
    currentDiagram = None
    currentCanvas = None
    options = None

    "Objects for holding a set of Feynman diagram components"
    def __init__(self, objects = []):
        self.__objs = objects
        FeynDiagram.currentCanvas = pyx.canvas.canvas()
        FeynDiagram.currentDiagram = self

    def add(self, *objs):
        for obj in objs:
            #print "Adding " + str(obj)
            self.__objs.append( obj )

    def draw(self):
        if FeynDiagram.options.VDEBUG:
            print "Running in visual debug mode"
        ## TODO: order of drawing...
        for obj in self.__objs:
            obj.draw(FeynDiagram.currentCanvas)

