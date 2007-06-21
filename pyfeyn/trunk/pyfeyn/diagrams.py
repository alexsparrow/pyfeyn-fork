"""Classes for the actual diagram containers."""

import pyx
from pyfeyn import config


## Diagram class
class FeynDiagram:
    """The main PyFeyn diagram class."""    
    currentDiagram = None
    currentCanvas = pyx.canvas.canvas()

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
            if config.getOptions().DEBUG:
                print "#objs = %d" % len(self.__objs)
            offset = 0
            if obj.__dict__.has_key("layeroffset"):
                #print "offset =", obj.layeroffset
                offset = obj.layeroffset
            self.highestautolayer += 1
            obj.setDepth(self.highestautolayer + offset)
            if config.getOptions().DEBUG:
                print "Object %s layer = %d + %d = %d" % \
                      (obj.__class__, self.highestautolayer, offset,
                       self.highestautolayer + offset)
            self.__objs.append(obj)


    def drawToCanvas(self):
        """Draw the components of this diagram in a well-defined order."""
        if config.getOptions().DEBUG:
            print "Final #objs = %d" % len(self.__objs)
        if config.getOptions().VDEBUG:
            print "Running in visual debug mode"

        ## Sort drawing objects by layer
        drawingobjs = self.__objs
        try:
            drawingobjs.sort()
        except:
            pass
            
        ## Draw each object
        for obj in drawingobjs:
            if config.getOptions().DEBUG:
                print "Depth = ", obj.getDepth()
            obj.draw(FeynDiagram.currentCanvas)

        return FeynDiagram.currentCanvas


    def draw(self, outfile):
        """Draw the diagram to a file, with the filetype (EPS or PDF)
        derived from the file extension."""
        c = self.drawToCanvas()
        if c is not None and outfile is not None:
            c.writetofile(outfile)

