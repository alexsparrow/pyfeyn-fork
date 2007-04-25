"""Diagramming classes - currently just FeynDiagram"""

import pyx


class OptionSet:
    """A container for options."""
    def __init__(self):
        self.DEBUG = None
        self.VDEBUG = None


## Diagram class
class FeynDiagram:
    """The main PyFeyn diagram class."""    
    currentDiagram = None
    currentCanvas = pyx.canvas.canvas()
    options = OptionSet() 
    options.DEBUG = None
    options.VDEBUG = None

    def __init__(self, objects=None):
        """Objects for holding a set of Feynman diagram components."""
        self.__objs = objects
        if self.__objs is None:
            self.__objs = []
        self.highestautolayer = 0
        FeynDiagram.currentCanvas = pyx.canvas.canvas()
        FeynDiagram.currentDiagram = self

    def add(self, *objs):
        """Add an object to the diagram."""
        for obj in objs:
            if FeynDiagram.options.DEBUG:
                print "#objs = %d" % len(self.__objs)
            obj.setDepth(self.highestautolayer + 1)
            self.highestautolayer += 1
            self.__objs.append(obj)

    def draw(self, outfile):
        """Draw the components of this diagram in a well-defined order."""
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
        if FeynDiagram.currentCanvas is not None:
            FeynDiagram.currentCanvas.writetofile(outfile)

