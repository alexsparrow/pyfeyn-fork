"""Diagramming classes - currently just FeynDiagram"""

import pyx
import re

## Diagram class
class FeynDiagram:
    """The main PyFeyn diagram class."""
    
    currentDiagram = None
    currentCanvas = None
    options = None

    "Objects for holding a set of Feynman diagram components"
    def __init__(self, objects = []):
        self.__objs = objects
        self.highestautolayer = 0
        FeynDiagram.currentCanvas = pyx.canvas.canvas()
        FeynDiagram.currentDiagram = self

    def add(self, *objs):
        for obj in objs:
            if FeynDiagram.options.DEBUG:
                print "#objs = %d" % len(self.__objs)
            obj.setDepth(self.highestautolayer + 1)
            self.highestautolayer += 1
            self.__objs.append(obj)

    def draw(self, file):
        if FeynDiagram.options.DEBUG:
            print "Final #objs = %d" % len(self.__objs)
        if FeynDiagram.options.VDEBUG:
            print "Running in visual debug mode"

        ## Sort drawing objects by layer
        drawingobjs = self.__objs
        drawingobjs.sort()

        ## Draw each object
        for obj in drawingobjs:
            if FeynDiagram.options.DEBUG:
                print "Depth = ", obj.getDepth()
            obj.draw(FeynDiagram.currentCanvas)
        FeynDiagram.currentCanvas.writetofile(file)

