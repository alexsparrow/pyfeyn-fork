from pyx import *
import math

class FeynDiagram:
    "Objects for holding a set of Feynman diagram components"
    __objs = []

    def add(self, obj):
        self.__objs = self.__objs + [obj]

    def draw(self, canvas):
        for obj in self.__objs:
            obj.draw(canvas)


class Point:
    "Base class for all pointlike objects in Feynman diagrams"
    xpos = 0
    ypos = 0
    radius = 1

    def __init__(self, xpos, ypos, rad=0.01):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = rad

    def draw(self, canvas):
        canvas.stroke(path.circle(self.xpos, self.ypos, self.radius))

    def midpoint(self, otherpoint):
        return StraightLine(self, otherpoint).midpoint()

    def distance(self, otherpoint):
        return StraightLine(self, otherpoint).length()

    def arg(self, otherpoint):
        return StraightLine(self, otherpoint).arg()

    def x(self):
        return self.xpos

    def y(self):
        return self.ypos

    def pos(self):
        return self.xpos, self.ypos


class FilledPoint(Point):
    "Filled point"
    fillstyles = [color.rgb.white]
    strokestyles = [color.rgb.black]

    def strokestyle(self, stylelist):
        self.strokestyles = self.strokestyles + stylelist

    def fillstyle(self, stylelist):
        self.fillstyles = self.fillstyles + stylelist

    def draw(self, canvas):
        canvas.fill(path.circle(self.xpos, self.ypos, self.radius), self.fillstyles)
        canvas.stroke(path.circle(self.xpos, self.ypos, self.radius), self.strokestyles)
        
        
class Vertex(Point):
    pass


class Line:
    "Base class for all objects which connect points in Feynman diagrams"
    styles = []
    __arcthrupoint = None
    is3D = False
    
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
    
    def arrows(self):
        pass

    def arcThru(self, arcpoint):
        self.__arcthrupoint = arcpoint
    
    def set3D(self, choice):
        self.is3D = choice

    def style(self, stylelist):
        self.styles = self.styles + stylelist

    def draw(self, canvas):
        line = None
        if self.__arcthrupoint == None:
            line = path.path( path.moveto(*(self.p1.pos())), path.lineto(*(self.p2.pos())) )
        else:
            #self.__arcthrupoint.draw(canvas)
            m13 = -1 / (( self.p1.y() - self.__arcthrupoint.y() ) / ( self.p1.x() - self.__arcthrupoint.x() ))
            m23 = -1 / (( self.p2.y() - self.__arcthrupoint.y() ) / ( self.p2.x() - self.__arcthrupoint.x() ))
            #print m13, m23
            mid13 = self.p1.midpoint(self.__arcthrupoint)
            mid23 = self.p2.midpoint(self.__arcthrupoint)
            #mid13.draw(canvas)
            #mid23.draw(canvas)
            #Line(mid13, Point(mid13.x() + 1, mid13.y() + m13)).draw(canvas)
            #Line(mid23, Point(mid23.x() + 1, mid23.y() + m23)).draw(canvas)
            
            c13 = mid13.y() - m13 * mid13.x()
            c23 = mid23.y() - m23 * mid23.x()
            #print c13, c23
            #Point(0, c13).draw(canvas)
            #Point(0, c23).draw(canvas)
            
            xcenter =  - (c23 - c13) / (m23 - m13)
            ycenter = m13 * xcenter + c13
            arccenter = Point(xcenter, ycenter)
            #arccenter.draw(canvas)
            arcradius = arccenter.distance(self.__arcthrupoint)
            tangent1 = StraightLine(arccenter, self.p1).tangent()
            tangent2 = StraightLine(arccenter, self.p2).tangent()
            #print tangent1, tangent2
            #StraightLine(arccenter, Point(arccenter.x() - 1, arccenter.y() - tangent1)).draw(canvas)
            #StraightLine(arccenter, Point(arccenter.x() - 1, arccenter.y() - tangent2)).draw(canvas)
            arcangle1 = arccenter.arg(self.p1)
            arcangle2 = arccenter.arg(self.p2)
            #print arcradius, arcangle1, arcangle2
            arcargs = (arccenter.x(), arccenter.y(), arcradius, arcangle1, arcangle2)
            if arcangle1 < arcangle2:
                line = path.path( path.moveto(*(self.p1.pos())), path.arc(*arcargs) )
            else:
                line = path.path( path.moveto(*(self.p1.pos())), path.arcn(*arcargs) )
        canvas.stroke(line, self.styles)


class StraightLine(Line):
    def length(self):
        return math.sqrt( (self.p1.x() - self.p2.x())**2 + (self.p1.y() - self.p2.y())**2 )

    def intercept(self):
        return self.p1.y() - self.tangent() * self.p1.x()

    def tangent(self):
        return (self.p2.y() - self.p1.y()) / (self.p2.x() - self.p1.x())

    def midpoint(self):
        return Point( (self.p1.x() + self.p2.x()) / 2.0, (self.p1.y() + self.p2.y()) / 2.0 )

    def arg(self):
        arg = math.atan(self.tangent())
        # Handle tangent sign ambiguity
        if self.p2.x() < self.p1.x():
            arg = arg + math.pi
        # Convert to degrees
        return (180 / math.pi) * arg
        

class DecoratedLine(Line):
    "Base class for spring and sine-like lines"
    def invert(self):
        pass

    def numHalfPeriods(self):
        pass

    def strikeThru(self):
        pass
