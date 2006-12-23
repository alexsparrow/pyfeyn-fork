"""Various particle line types."""

import pyx, math
from pyx import color

from diagrams import FeynDiagram
from points import Point
from deco import Arrow, Label
from utils import Visible


## Line base class
class Line(Visible):
    "Base class for all objects which connect points in Feynman diagrams"
    
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
        self.bendamount = 0
        self.is3D = False
        self.arrows = []
        self.labels = []

        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def addLabel(self, text, pos=0.5, displace=-0.25, angle = 0):
        """Add a LaTeX label to this line, either via parameters or actually as
        a TeXLable object."""
        if FeynDiagram.options.DEBUG:
            print "Adding label: " + text
        #if text.__class__ == "Label":
        #    self.labels.append(label)
        #else:
        self.labels.append(Label(text=text, line=self, pos=pos, displace=displace, angle=angle))
        if FeynDiagram.options.DEBUG:
            print "Labels = " + str(self.labels)
        return self

            
    def removeLabels(self):
        self.labels = []
        return self


    def fracpoint(self, frac):
        """Get a new Point representing the point at the given fraction along
        the fundamental line (i.e. no truncation or deformation).
        TODO: Handle units properly."""
        p = self.getPath() ## no truncation or deformation
        x, y = p.at(p.begin() + frac * p.arclen())
        return Point(x, y)
    

    def setArrows(self, arrows):
        ## TODO Check that the arg is a list
        self.arrows = []
        for i in arrows:
            if i.__class__ == "deco.Arrow":
                self.arrows.append(i)
            else:
                self.arrows.append(Arrow(pos = i))
        return self


    def addArrow(self, position = 0.5, arrow = None):
        """Add an arrow to the line at the specified position, which is a number
        between 0 and 1, representing the fraction along the line at which the
        arrow should be placed. The default arrow style can be overridden by
        explicitly supplying an arrow object as the 'arrow' argument, in which
        case the position argument will be ignored."""
        if arrow:
            self.arrows.append(arrow)
        else:
            self.arrows.append(Arrow(pos=position))
        return self


    def removeArrows(self):
        """Remove all arrows from this line."""
        self.arrows = []
        return self


    def arcThru(self, arcpoint = None, x = None, y = None):
        """Set the point through which this line will arc. Either pass a Point
        or set x, y as floats."""
        if arcpoint != None:
            self.arcthrupoint = arcpoint
        elif x != None and y != None:
            self.arcthrupoint = Point(x, y)
        else:
            raise Exception("Tried to set an arcpoint with invalid arguments")
        self.bendamount = None
        return self


    def straighten(self):
        """Make this line a straight line between start and end."""
        self.arcthrupoint = None
        self.bendamount = None


    def bend(self, amount):
        """Bend the line to the right by a given distance."""
        middle = self.p1.midpoint(self.p2)
        nx = (middle.y() - self.p1.y()) / abs(self.p1.distance(middle))
        ny = (self.p1.x() - middle.x()) / abs(self.p1.distance(middle))
        vx = middle.x() - self.p1.x()
        vy = middle.y() - self.p1.y()
        if (vx * ny - vy * nx) > 0:
            nx *= -1
            ny *= -1
            
        arcpoint = Point(middle.x() + amount * nx, middle.y() + amount * ny)
        if FeynDiagram.options.VDEBUG:
            FeynDiagram.currentCanvas.stroke(
                pyx.path.line(middle.x(), middle.y(), arcpoint.x(), arcpoint.y()), [color.rgb.blue] )
        self.arcThru(arcpoint)
        self.bendamount = amount
        return self

    
    def set3D(self, choice):
        self.is3D = choice
        return self


    def getStyles(self, stylelist):
        return self.styles


    def setStyles(self, stylelist):
        self.styles = stylelist
        return self


    def addStyle(self, style):
        self.styles.append(style)
        return self


    def addStyles(self, stylelist):
        self.styles = self.styles + stylelist
        return self


    def getPath(self):
        if self.arcthrupoint == None:
            ## This is a simple straight line
            return pyx.path.path( pyx.path.moveto( *(self.p1.getXY()) ),
                              pyx.path.lineto( *(self.p2.getXY()) ) )
        elif (self.p1.x() == self.p2.x() and self.p1.y() == self.p2.y()):
            ## This is a tadpole-type loop and needs special care;
            ## We shall assume that the arcthrupoint is meant to be
            ## the antipode of the basepoint
            arccenter = self.p1.midpoint(self.arcthrupoint)
            arcradius = self.p1.distance(self.arcthrupoint) / 2.0
            
            ## TODO Why does a circle work and an arc doesn't?
            cargs = (arccenter.x(), arccenter.y(), arcradius)
            circle = pyx.path.circle(*cargs)
            line = pyx.path.line( self.p1.x(), self.p1.y(), arccenter.x(), arccenter.y())
            if FeynDiagram.options.VDEBUG:
                FeynDiagram.currentCanvas.stroke(line, [color.rgb.green])
            as, bs = circle.intersect(line)
            subpaths = circle.split(as[0])
            cpath = subpaths[0]
            return cpath

            ## or, with an arc...
            arcangle1 = arccenter.arg(self.p1)
            arcangle2 = arccenter.arg(self.p1) + 360
            arcargs = (arccenter.x(), arccenter.y(), arcradius, arcangle1, arcangle2)
            return pyx.path.path( pyx.path.arc(*arcargs) )

        else:
            ## Work out line gradients
            try: n13 = (self.p1.y() - self.arcthrupoint.y()) / (self.p1.x() - self.arcthrupoint.x())
            except ZeroDivisionError: n13 = 1e100
            try: n23 = (self.p2.y() - self.arcthrupoint.y()) / (self.p2.x() - self.arcthrupoint.x())
            except ZeroDivisionError: n23 = 1e100

            ## If gradients match,
            ## then we have a straight line, so bypass the complexity
            if n13 == n23:
                return pyx.path.path( pyx.path.moveto(*(self.p1.getXY())),
                                      pyx.path.lineto(*(self.p2.getXY())) )

            ## Otherwise work out conjugate gradients and midpoints
            try: m13 = - 1.0 / n13
            except ZeroDivisionError: m13 = 1e100
            try: m23 = - 1.0 / n23
            except ZeroDivisionError: m23 = 1e100
            mid13 = self.p1.midpoint(self.arcthrupoint)
            mid23 = self.p2.midpoint(self.arcthrupoint)
            
            ## Line y-intercepts
            c13 = mid13.y() - m13 * mid13.x()
            c23 = mid23.y() - m23 * mid23.x()
            
            ## Find the centre of the arc
            xcenter =  - (c23 - c13) / (m23 - m13)
            ycenter = m13 * xcenter + c13
            arccenter = Point(xcenter, ycenter)

            ## Get the angles required for drawing the arc
            arcradius = arccenter.distance(self.arcthrupoint)
            arcangle1 = arccenter.arg(self.p1)
            arcangle2 = arccenter.arg(self.p2)
            arcangle3 = arccenter.arg(self.arcthrupoint)
            arcargs = (arccenter.x(), arccenter.y(), arcradius, arcangle1, arcangle2)

            ## Calculate cross product to determine direction of arc
            vec12 = [self.p2.x()-self.p1.x(), self.p2.y()-self.p1.y(), 0.0]
            vec13 = [self.arcthrupoint.x()-self.p1.x(), self.arcthrupoint.y()-self.p1.y(), 0.0]
            crossproductZcoord = vec12[0]*vec13[1] - vec12[1]*vec13[0]

            if crossproductZcoord < 0:
                return pyx.path.path( pyx.path.moveto(*(self.p1.getXY())),
                                      pyx.path.arc(*arcargs))
            else:
                return pyx.path.path( pyx.path.moveto(*(self.p1.getXY())),
                                      pyx.path.arcn(*arcargs))


    def getVisiblePath(self):
        """Find the subpath between the endpoints which isn't overshadowed by a blob of some kind"""
        p1path = self.p1.getPath()
        p2path = self.p2.getPath()
        vispath = self.getPath()
        if FeynDiagram.options.VDEBUG:
            FeynDiagram.currentCanvas.stroke(vispath, [color.rgb.green])
        if p1path:
            as, bs = p1path.intersect(vispath)
            for b in bs:
                subpaths = vispath.split(b)
                if len(subpaths) > 1:
                    if FeynDiagram.options.DEBUG:
                        print "Num subpaths 1 = %d" % len(subpaths)
                    subpaths.sort( lambda x, y : int(pyx.unit.tocm(x.arclen() - y.arclen())/math.fabs(pyx.unit.tocm(x.arclen() - y.arclen()))) )
                    vispath = subpaths[-1]
                    if FeynDiagram.options.VDEBUG:
                        FeynDiagram.currentCanvas.stroke(subpaths[0], [color.rgb.blue])
                if FeynDiagram.options.VDEBUG:
                    for a in as:
                        ix, iy = p1path.at(a)
                        FeynDiagram.currentCanvas.fill(pyx.path.circle(ix, iy, 0.05), [color.rgb.green])
        if p2path: 
            as, bs = p2path.intersect(vispath)
            for b in bs:
                subpaths = vispath.split(b)
                if len(subpaths) > 1:
                    if FeynDiagram.options.DEBUG:
                        print "Num subpaths 2 = %d" % len(subpaths)
                    subpaths.sort( lambda x, y : int(pyx.unit.tocm(x.arclen() - y.arclen())/math.fabs(pyx.unit.tocm(x.arclen() - y.arclen()))) )
                    vispath = subpaths[-1]
                    if FeynDiagram.options.VDEBUG:
                        FeynDiagram.currentCanvas.stroke(subpaths[0], [color.rgb.red])
                if FeynDiagram.options.VDEBUG:
                    for a in as:
                        ix, iy = p2path.at(a)
                        FeynDiagram.currentCanvas.fill(pyx.path.circle(ix, iy, 0.05), [color.rgb.blue])
        if FeynDiagram.options.VDEBUG:
            FeynDiagram.currentCanvas.stroke(vispath, [color.rgb.red])
        #return pyx.path.circle(-2,-1,0.2)
        return vispath

        
    def draw(self, canvas):
        path = self.getVisiblePath()
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
        canvas.stroke(path, styles)
        for l in self.labels:
            l.draw(canvas)


class Fermion(Line):
    pass


## DecoratedLine base class
class DecoratedLine(Line):
    """Base class for spring and sine-like lines"""
    def invert(self):
        pass

    def numHalfPeriods(self):
        pass

    def strikeThru(self):
        pass

    def getDeformedPath(self):
        return getVisiblePath()


class Gluon(DecoratedLine):
    """A line with a cycloid deformation"""
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
        self.bendamount = 0
        self.is3D = False
        self.arrows = []
        self.labels = []
        self.arcradius = pyx.unit.length(0.25)
        self.elasticity = 1.3
        self.inverted = False
        self.linetype = "gluon"
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def invert(self):
        self.inverted = not self.inverted
        return self


    def getTension(self):
        return self.elasticity
    

    def setTension(self, value):
        self.elasticity = value
        return self


    def getDeformedPath(self):
        needwindings = self.elasticity * \
                       pyx.unit.tocm(self.getVisiblePath().arclen()) / pyx.unit.tocm(self.arcradius)
        ## Get the whole number of windings and make sure that it's odd so we
        ## don't get a weird double-back thing
        intwindings = int(needwindings)
        if intwindings % 2 == 0:
            intwindings -= 1
        deficit = needwindings - intwindings
        sign = 1
        if self.inverted: sign = -1 
        defo = pyx.deformer.cycloid(self.arcradius, intwindings, curvesperhloop=10, skipfirst = 0.0, skiplast = 0.0, sign = sign)
        return defo.deform(self.getVisiblePath())


    def draw(self, canvas):
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
        canvas.stroke(self.getDeformedPath(), styles)
        for l in self.labels:
            l.draw(canvas)



class Photon(DecoratedLine):
    """A line with a sinoid deformation"""
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
        self.bendamount = 0
        self.is3D = False
        self.arrows = []
        self.labels = []
        self.inverted = False
        self.arcradius = pyx.unit.length(0.25)
        self.linetype = "photon"
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def invert(self):
        self.inverted = not self.inverted
        return self


    def getDeformedPath(self):
        intwindings = int(1.0 * pyx.unit.tocm(self.getVisiblePath().arclen()) / pyx.unit.tocm(self.arcradius))
        sign = 1
        if self.inverted: sign = -1 
        defo = pyx.deformer.cycloid(self.arcradius, intwindings, curvesperhloop=5, skipfirst=0.0, skiplast=0.0, turnangle=0, sign=sign)
        return defo.deform(self.getVisiblePath())

        
    def draw(self, canvas):
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
        canvas.stroke(self.getDeformedPath(), styles)
        for l in self.labels:
            l.draw(canvas)



# A dictionary for mapping FeynML line types to line classes
NamedLine = {"photon" : Photon, "gluon" : Gluon, "fermion" : DecoratedLine}
