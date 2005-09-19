from pyx import *

class FeynDiagram:
    "Objects for holding a set of Feynman diagram components"
    __objs = {}
    #    def __init__(self):

    def add(self, key, obj):
        self.__objs[key] = obj

    def draw(self, canvas):
        for key, obj in self.__objs.iteritems():
            obj.draw(canvas)


class Point:
    "Base class for all pointlike objects in Feynman diagrams"
    xpos = 0
    ypos = 0
    radius = 1

    def __init__(self, xpos, ypos, rad=0.3):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = rad

    def draw(self, canvas):
        canvas.stroke(path.circle(self.xpos, self.ypos, self.radius))

    def x(self):
        return self.xpos

    def y(self):
        return self.ypos

    def pos(self):
        return self.xpos, self.ypos


class FilledPoint(Point):
    "Filled point"
    def draw(self, canvas):
        canvas.fill(path.circle(self.xpos, self.ypos, self.radius))

        
class Vertex(Point):
    pass


class Line:
    "Base class for all objects which connect points in Feynman diagrams"
    styles = []
    
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
    
    def arrows(self):
        pass
    
    def arcThru(self, arcpoint):
        pass
    
    def arcThru(self, xarcpos, yarcpos):
        pass
    
    def width(self, linewidth):
        pass

    def set3D(self, choice):
        pass

    def addstyle(self, style):
        self.styles = self.styles + [style]

    def addstyles(self, stylelist):
        self.styles = self.styles + stylelist

    def draw(self, canvas):
        line = path.path( path.moveto(*(self.p1.pos())), path.lineto(*(self.p2.pos())), path.closepath() )
        canvas.stroke(line, self.styles)


class DecoratedLine(Line):
    "Base class for spring and sine-like lines"
    def invert(self):
        pass

    def numHalfPeriods(self):
        pass

    def strikeThru(self):
        pass
