from pyx import *
import math

def sign(x):
    if x < 0: return -1
    if x > 0: return 1
    if x == 0: return 0
    

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
    xpos = 0.0
    ypos = 0.0

    def __init__(self, xpos, ypos):
        self.setpos(xpos, ypos)

    def draw(self, canvas):
        pass

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

    def setpos(self, xpos, ypos):
        self.xpos = float(xpos)
        self.ypos = float(ypos)


class Blob:
    fillstyles = [color.rgb.white]
    strokestyles = [color.rgb.black]
    trafos = []
    #def __init__(self, centre):

    def strokestyle(self, stylelist):
        self.strokestyles = self.strokestyles + stylelist
        return self

    def fillstyle(self, stylelist):
        self.fillstyles = self.fillstyles + stylelist
        return self

    def trafo(self, trafolist):
        self.trafos = self.trafos + trafolist
        return self


class Circle(Blob):
    def __init__(self, xpos, ypos, rad):
        self.centre = Point(xpos, ypos)
        self.radius = float(rad)

    def draw(self, canvas):
        canvas.fill(path.circle(self.centre.x(), self.centre.y(), self.radius), [color.rgb.white])
        canvas.fill(path.circle(self.centre.x(), self.centre.y(), self.radius), self.fillstyles)
        #canvas.fill(path.circle(self.xpos, self.ypos, self.radius), self.fillstyles)
        canvas.stroke(path.circle(self.centre.x(), self.centre.y(), self.radius), self.strokestyles)


class Ellipse(Blob):
    def __init__(self, xpos, ypos, xrad, yrad):
        self.centre = Point(xpos, ypos)
        self.xrad = float(xrad)
        self.yrad = float(yrad)

    def draw(self, canvas):
        canvas.fill(path.circle(self.centre.x(), self.centre.y(), 1.0),
                    [color.rgb.white] + [trafo.scale(self.xrad, self.yrad, self.centre.x(), self.centre.y())]
                    + self.fillstyles)
        #canvas.fill(path.circle(self.xpos, self.ypos, self.radius), self.fillstyles)
        canvas.stroke(path.circle(self.centre.x(), self.centre.y(), 1.0),
                      [trafo.scale(self.xrad, self.yrad, self.centre.x(), self.centre.y())]
                      + self.strokestyles)


#############################
        

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
        return self
    
    def set3D(self, choice):
        self.is3D = choice
        return self

    def style(self, stylelist):
        self.styles = self.styles + stylelist
        return self
        
    def draw(self, canvas):
        line = None
        if self.__arcthrupoint == None:
            line = path.path( path.moveto(*(self.p1.pos())), path.lineto(*(self.p2.pos())) )
        else:
            ## Work out line gradients
            try: n13 = (self.p1.y() - self.__arcthrupoint.y()) / (self.p1.x() - self.__arcthrupoint.x())
            except ZeroDivisionError: n13 = 1e100
            try: n23 = (self.p2.y() - self.__arcthrupoint.y()) / (self.p2.x() - self.__arcthrupoint.x())
            except ZeroDivisionError: n23 = 1e100

            ## If gradients match, then we have a straight line, so bypass the complexity
            if n13 == n23:
                line = StraightLine(self.p1, self.p2)
                line.style(self.styles)
                line.draw(canvas)
                return

            ## Otherwise work out conjugate gradients and midpoints
            try: m13 = - 1.0 / n13
            except ZeroDivisionError: m13 = 1e100
            try: m23 = - 1.0 / n23
            except ZeroDivisionError: m23 = 1e100
            #print n13, n23
            #print m13, m23
            mid13 = self.p1.midpoint(self.__arcthrupoint)
            mid23 = self.p2.midpoint(self.__arcthrupoint)
            
            ## Line y-intercepts
            c13 = mid13.y() - m13 * mid13.x()
            c23 = mid23.y() - m23 * mid23.x()
            #print c13, c23
            
            ## Find the centre of the arc
            xcenter =  - (c23 - c13) / (m23 - m13)
            ycenter = m13 * xcenter + c13
            arccenter = Point(xcenter, ycenter)

            ## Get the angles required for drawing the arc
            arcradius = arccenter.distance(self.__arcthrupoint)
            tangent1 = StraightLine(arccenter, self.p1).tangent()
            tangent2 = StraightLine(arccenter, self.p2).tangent()
            #print tangent1, tangent2
            arcangle1 = arccenter.arg(self.p1)
            arcangle2 = arccenter.arg(self.p2)
            arcangle3 = arccenter.arg(self.__arcthrupoint)
            #print arcradius, arcangle1, arcangle2, arcangle3
            arcargs = (arccenter.x(), arccenter.y(), arcradius, arcangle1, arcangle2)

            ## Debug drawings
            #self.__arcthrupoint.draw(canvas)
            #mid13.draw(canvas)
            #mid23.draw(canvas)
            #StraightLine(mid13, Point(mid13.x() + 1, mid13.y() + m13)).draw(canvas)
            #StraightLine(mid23, Point(mid23.x() + 1, mid23.y() + m23)).draw(canvas)
            #Point(0, c13).draw(canvas)
            #Point(0, c23).draw(canvas)
            #arccenter.draw(canvas)
            #StraightLine(arccenter, Point(arccenter.x() - 1, arccenter.y() - tangent1)).draw(canvas)
            #StraightLine(arccenter, Point(arccenter.x() - 1, arccenter.y() - tangent2)).draw(canvas)

            ## Calculate cross product to determine direction of arc
            vec12 = [self.p2.x()-self.p1.x(), self.p2.y()-self.p1.y(), 0.0]
            vec13 = [self.__arcthrupoint.x()-self.p1.x(), self.__arcthrupoint.y()-self.p1.y(), 0.0]
            crossproductZcoord = vec12[0]*vec13[1] - vec12[1]*vec13[0]
            #print crossproductZcoord


            
            if crossproductZcoord < 0:
                line = path.path( path.moveto(*(self.p1.pos())), path.arc(*arcargs))
            else:
                line = path.path( path.moveto(*(self.p1.pos())), path.arcn(*arcargs))
        canvas.stroke(line, self.styles)


class StraightLine(Line):
    def length(self):
        return math.hypot(self.p1.x()-self.p2.x(), self.p1.y()-self.p2.y())

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
        return math.degrees(arg)
        

class DecoratedLine(Line):
    "Base class for spring and sine-like lines"
    def invert(self):
        pass

    def numHalfPeriods(self):
        pass

    def strikeThru(self):
        pass


class Arrow(deco.deco, attr.attr):
    "Arrow for Feynman diagram lines"
    def __init__(self, pos=0.5, size=6*unit.v_pt, angle=45, constriction=0.8):
        self.pos = pos
        self.size = size
        self.angle = angle
        self.constriction = constriction
        
    def decorate(self, dp):
        dp.ensurenormpath()
        constrictionlen = self.size*self.constriction*math.cos(self.angle*math.pi/360.0)
        arrowtopos = self.pos*dp.path.arclen()+0.5*self.size
        arrowtopath = dp.path.split(arrowtopos)[0]
        arrowpath = deco._arrowhead(arrowtopath, self.size, 45, constrictionlen, 1)
        dp.ornaments.fill(arrowpath)
        return dp
    
