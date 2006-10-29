from pyx import *
import math, md5
import elementtree.ElementTree as xml

from points import Point
from deco import Coil


## Line base class
class Line:
    "Base class for all objects which connect points in Feynman diagrams"
    
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.__arcthrupoint = None
        self.bendamount = 0
        self.is3D = False
    
    def arrows(self):
        ## TODO!
        pass

    def arcThru(self, arcpoint):
        self.__arcthrupoint = arcpoint
        self.bendamount = None
        return self

    def bend(self, amount):
        middle = self.p1.midpoint(self.p2)
        normal = (middle.y()-self.p1.y(),self.p1.x()-middle.x())
        arcpoint = Point(middle.x()+amount*normal[0],
                         middle.y()+amount*normal[1])
        self.__arcthrupoint = arcpoint
        self.bendamount = amount
        return self
    
    def set3D(self, choice):
        self.is3D = choice
        return self

    def style(self, stylelist):
        self.styles = self.styles + stylelist
        return self

    def path(self):
        if self.__arcthrupoint == None:
            ## This is a simple straight line
            return path.path( path.moveto(*(self.p1.pos())),
                                  path.lineto(*(self.p2.pos())) )
        elif (self.p1.x()==self.p2.x() and self.p1.y()==self.p2.y()):
            ## This is a tadpole-type loop and needs special care;
            ## we shall assume that the arcthrupoint is meant to be
            ## the antipode of the basepoint
            arccenter = self.p1.midpoint(self.__arcthrupoint)
            arcradius = self.p1.distance(self.__arcthrupoint) / 2.
            arcangle1 = arccenter.arg(self.p1)
            arcangle2 = arccenter.arg(self.p1)+360
            arcargs = (arccenter.x(), arccenter.y(), arcradius, arcangle1, arcangle2)
            return path.path( path.arc(*arcargs) )
        else:
            ## Work out line gradients
            try: n13 = (self.p1.y() - self.__arcthrupoint.y()) / (self.p1.x() - self.__arcthrupoint.x())
            except ZeroDivisionError: n13 = 1e100
            try: n23 = (self.p2.y() - self.__arcthrupoint.y()) / (self.p2.x() - self.__arcthrupoint.x())
            except ZeroDivisionError: n23 = 1e100

            ## If gradients match,
            ## then we have a straight line, so bypass the complexity
            if n13 == n23:
                return path.path( path.moveto(*(self.p1.pos())),
                                      path.lineto(*(self.p2.pos())) )

            ## Otherwise work out conjugate gradients and midpoints
            try: m13 = - 1.0 / n13
            except ZeroDivisionError: m13 = 1e100
            try: m23 = - 1.0 / n23
            except ZeroDivisionError: m23 = 1e100
            mid13 = self.p1.midpoint(self.__arcthrupoint)
            mid23 = self.p2.midpoint(self.__arcthrupoint)
            
            ## Line y-intercepts
            c13 = mid13.y() - m13 * mid13.x()
            c23 = mid23.y() - m23 * mid23.x()
            
            ## Find the centre of the arc
            xcenter =  - (c23 - c13) / (m23 - m13)
            ycenter = m13 * xcenter + c13
            arccenter = Point(xcenter, ycenter)

            ## Get the angles required for drawing the arc
            arcradius = arccenter.distance(self.__arcthrupoint)
            arcangle1 = arccenter.arg(self.p1)
            arcangle2 = arccenter.arg(self.p2)
            arcangle3 = arccenter.arg(self.__arcthrupoint)
            arcargs = (arccenter.x(), arccenter.y(), arcradius, arcangle1, arcangle2)

            ## Calculate cross product to determine direction of arc
            vec12 = [self.p2.x()-self.p1.x(), self.p2.y()-self.p1.y(), 0.0]
            vec13 = [self.__arcthrupoint.x()-self.p1.x(), self.__arcthrupoint.y()-self.p1.y(), 0.0]
            crossproductZcoord = vec12[0]*vec13[1] - vec12[1]*vec13[0]

            if crossproductZcoord < 0:
                return path.path( path.moveto(*(self.p1.pos())),
                                      path.arc(*arcargs))
            else:
                return path.path( path.moveto(*(self.p1.pos())),
                                      path.arcn(*arcargs))
        
    def draw(self, canvas):
        p1path = self.p1.path()
        p2path = self.p2.path()
        if p1path:
            as, bs = p1path.intersect(self.path())
            ix, iy = p1path.at(as[0])
            canvas.fill(path.circle(ix, iy, 1.0), [color.rgb.green])
            ## TODO: split path here and only deform the central section
        if p2path: 
            as, bs = p2path.intersect(self.path())
            ix, iy = p2path.at(as[0])
            canvas.fill(path.circle(ix, iy, 1.0), [color.rgb.blue])
            ## TODO: split path here and only deform the central section
        canvas.stroke(self.path(), self.styles)

    def to_xml(self):
        attribs = {"id":"P%s"%md5.md5(str((self.p1.xpos,self.p1.ypos,self.p2.xpos,self.p2.ypos,self.__arcthrupoint and (self.__arcthrupoint.xpos,self.__arcthrupoint.ypos)))).hexdigest(),
               "source":"V%s"%md5.md5(str((self.p1.xpos,self.p1.ypos))).hexdigest(),
               "target":"V%s"%md5.md5(str((self.p2.xpos,self.p2.ypos))).hexdigest(),
               "type":hasattr(self,"linetype") and self.linetype or "fermion"}
        if self.bendamount:
           attribs["bend"] = str(self.bendamount)
        ele = xml.Element("propagator",attribs)
        #xml.dump(ele)
        return ele


## DecoratedLine base class
class DecoratedLine(Line):
    """Base class for spring and sine-like lines"""
    def invert(self):
        pass

    def numHalfPeriods(self):
        pass

    def strikeThru(self):
        pass



##### Specific kinds of DecoratedLine #####

class Gluon(DecoratedLine):
    """A line with a cycloid deformation"""
#    p1 # inherited
#    p2 # inherited
#    styles = [] # inherited
#    __arcthrupoint = None # inherited
#    bendamount = 0 # inherited
#    is3D = False # inherited
    arcradius = 0.25
    elasticity = 1.38268
    linetype = "gluon"

    def tension(self, value):
        self.elasticity = value
        return self

    def draw(self, canvas):
        needwindings = self.elasticity * \
                       unit.tocm(self.path().arclen()) / self.arcradius
        intwindings = int(needwindings)
        deficit = needwindings-intwindings
        canvas.stroke(self.path(), self.styles +
             [ deformer.cycloid(self.arcradius, intwindings,
               skipfirst=0.5*deficit*self.arcradius,
               skiplast=0.5*deficit*self.arcradius) ])



class Photon(DecoratedLine):
    """A line with a sinoid deformation"""
#    p1 # inherited
#    p2 # inherited
#    styles = [] # inherited
#    __arcthrupoint = None # inherited
#    bendamount = 0 # inherited
#    is3D = False # inherited
    arcradius = 0.25
    linetype = "photon"

    def draw(self, canvas):
        canvas.stroke(self.path(), self.styles +
             [deformer.cycloid(self.arcradius,
                  int(1.5 * unit.tocm(self.path().arclen()) / self.arcradius),
                  skipfirst=0, skiplast=0, turnangle=0) ])



# A dictionary for mapping FeynML line types to line classes
NamedLine = {"photon":Photon,"gluon":Gluon,"fermion":DecoratedLine}

 
