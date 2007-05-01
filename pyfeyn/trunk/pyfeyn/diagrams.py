"""Classes for the actual diagram containers."""

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
            offset = 0
            if obj.__dict__.has_key("layeroffset"):
                #print "offset =", obj.layeroffset
                offset = obj.layeroffset
            self.highestautolayer += 1
            obj.setDepth(self.highestautolayer + offset)
            if FeynDiagram.options.DEBUG:
                print "Object %s layer = %d + %d = %d" % \
                      (obj.__class__, self.highestautolayer, offset,
                       self.highestautolayer + offset)
            self.__objs.append(obj)


    def drawToCanvas(self):
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

        return FeynDiagram.currentCanvas


    def draw(self, outfile):
        """Draw the diagram to a file, with the filetype (EPS or PDF)
        derived from the file extension."""
        c = self.drawToCanvas()
        if c is not None and outfile is not None:
            c.writetofile(outfile)

