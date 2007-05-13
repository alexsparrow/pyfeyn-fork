"""Various particle line types."""

import pyx, math
from pyx import color

from pyfeyn.diagrams import FeynDiagram
from pyfeyn.points import Point
from pyfeyn.deco import Arrow, LineLabel
from pyfeyn.utils import Visible, defunit


## Line base class
class Line(Visible):
    "Base class for all objects which connect points in Feynman diagrams"
    
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
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
        self.labels.append(LineLabel(text=text, line=self, pos=pos, displace=displace, angle=angle))
        if FeynDiagram.options.DEBUG:
            print "Labels = " + str(self.labels)
        return self

            
    def removeLabels(self):
        """Remove the labels from this line."""
        self.labels = []
        return self


    def fracpoint(self, frac):
        """
        Get a new Point representing the point at the given fraction along
        the fundamental line (i.e. no truncation or deformation).
        TODO: Handle units properly.
        """
        p = self.getPath() ## no truncation or deformation
        x, y = p.at(p.begin() + frac * p.arclen())
        return Point(x/defunit, y/defunit)
    

    def setArrows(self, arrows):
        """Define the arrows on this line."""
        ## TODO: Check that the arg is a list
        self.arrows = []
        for i in arrows:
            if i.__class__ == "deco.Arrow":
                self.arrows.append(i)
            else:
                self.arrows.append(Arrow(pos = i))
        return self


    def addArrow(self, position = 0.53, arrow = None):
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
        if arcpoint is not None:
            self.arcthrupoint = arcpoint
        elif x is not None and y is not None:
            self.arcthrupoint = Point(x, y)
        else:
            raise Exception("Tried to set an arcpoint with invalid arguments")
        return self


    def straighten(self):
        """Make this line a straight line between start and end."""
        self.arcthrupoint = None


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
                pyx.path.line(middle.x(), middle.y(), arcpoint.x(),
                              arcpoint.y()), [color.rgb.blue] )
        self.arcThru(arcpoint)
        if FeynDiagram.options.DEBUG:
            print self.getVisiblePath()
        if FeynDiagram.options.VDEBUG:
            FeynDiagram.currentCanvas.stroke(self.getVisiblePath(), [color.rgb.blue])
        return self


    def set3D(self, choice):
        """Make this line display in '3D'."""
        self.is3D = choice
        return self


    def getStyles(self, stylelist):
        """Get the styles associated with this line."""
        return self.styles


    def setStyles(self, stylelist):
        """Set the styles associated with this line."""
        self.styles = stylelist
        return self


    def addStyle(self, style):
        """Add a style to this line."""
        self.styles.append(style)
        return self


    def addStyles(self, stylelist):
        """Add some styles to this line."""
        self.styles = self.styles + stylelist
        return self


    def getPath(self):
        """Get the path taken by this line."""
        if self.arcthrupoint is None:
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
            n13, n23 = None, None
            ## Work out line gradients
            try:
                n13 = (self.p1.y() - self.arcthrupoint.y()) / (self.p1.x() - self.arcthrupoint.x())
            except ZeroDivisionError:
                if FeynDiagram.options.DEBUG:
                    print "Grad 1 diverges"
                n13 = 1e100
                
            try:
                n23 = (self.p2.y() - self.arcthrupoint.y()) / (self.p2.x() - self.arcthrupoint.x())
            except ZeroDivisionError:
                if FeynDiagram.options.DEBUG:
                    print "Grad 2 diverges"
                n23 = 1e100

            ## If gradients match,
            ## then we have a straight line, so bypass the complexity
            if n13 == n23:
                return pyx.path.path( pyx.path.moveto(*(self.p1.getXY())),
                                      pyx.path.lineto(*(self.p2.getXY())) )

            ## Otherwise work out conjugate gradients and midpoints
            m13, m23 = None, None
            try:
                m13 = -1.0 / n13
            except ZeroDivisionError:
                m13 = 1e100
            try:
                m23 = -1.0 / n23
            except ZeroDivisionError:
                m23 = 1e100
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

            if FeynDiagram.options.DEBUG and arcangle1 == arcangle2:
                print "Arc angles are the same - not drawing anything"

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
                    subpaths.sort(
                        lambda x, y :
                        int(pyx.unit.tocm(x.arclen() - y.arclen()) /
                            math.fabs(pyx.unit.tocm(x.arclen() - y.arclen()))) )
                    vispath = subpaths[-1]
                    if FeynDiagram.options.VDEBUG:
                        FeynDiagram.currentCanvas.stroke(subpaths[0], [color.rgb.blue])
                if FeynDiagram.options.VDEBUG:
                    for a in as:
                        ix, iy = p1path.at(a)
                        FeynDiagram.currentCanvas.fill(pyx.path.circle(ix, iy, 0.05),
                                                       [color.rgb.green])
        if p2path: 
            as, bs = p2path.intersect(vispath)
            for b in bs:
                subpaths = vispath.split(b)
                if len(subpaths) > 1:
                    if FeynDiagram.options.DEBUG:
                        print "Num subpaths 2 = %d" % len(subpaths)
                    subpaths.sort(
                        lambda x, y :
                        int(pyx.unit.tocm(x.arclen() - y.arclen()) /
                            math.fabs(pyx.unit.tocm(x.arclen() - y.arclen()))) )
                    vispath = subpaths[-1]
                    if FeynDiagram.options.VDEBUG:
                        FeynDiagram.currentCanvas.stroke(subpaths[0], [color.rgb.red])
                if FeynDiagram.options.VDEBUG:
                    for a in as:
                        ix, iy = p2path.at(a)
                        FeynDiagram.currentCanvas.fill(pyx.path.circle(ix, iy, 0.05),
                                                       [color.rgb.blue])
        if FeynDiagram.options.VDEBUG:
            FeynDiagram.currentCanvas.stroke(vispath, [color.rgb.red])
        #return pyx.path.circle(-2,-1,0.2)
        return vispath

        
    def draw(self, canvas):
        """Drwa this line on the given canvas."""
        path = self.getVisiblePath()
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
            print path
        canvas.stroke(path, styles)
        for l in self.labels:
            l.draw(canvas)


## Fermion is an alias for Line
Fermion = Line


class MultiLine(Line):
    """A class for drawing multiple parallel straight lines."""

    def draw(self, canvas):
        """Draw this multiline on the supplied canvas."""
        dist = 0.2
        n = 5
        path = pyx.deformer.parallel(-n/2.0 * dist).deform(self.getPath())
        paths = [path]
        defo = pyx.deformer.parallel(dist)
        for m in range(0, n):
            path = defo.deform(path)
            paths.append(path)
        styles = self.styles + self.arrows
        for p in paths:
            canvas.stroke(p, styles)


class Scalar(Line):
    """A scalar particle line, like a Higgs boson."""

    def draw(self, canvas):
        """Draw this scalar line on the given canvas."""
        path = self.getVisiblePath()
        styles = self.styles + [pyx.style.linestyle.dashed] + self.arrows
        ## TODO: call base class method?
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
            print path
        canvas.stroke(path, styles)
        for l in self.labels:
            l.draw(canvas)



## Higgs is an alias for Scalar
Higgs = Scalar

## Sfermion is also an alias for Scalar
Sfermion = Scalar



## DecoratedLine base class
class DecoratedLine(Line):
    """Base class for spring and sine-like lines"""

    def invert(self):
        """Reflect the line decoration about the line."""
        pass

    def getNumHalfCycles(self):
        """Get the number of half cycles in this line."""
        pass

    def getDeformedPath(self):
        """Get the deformed path."""
        return getVisiblePath()



class Gluon(DecoratedLine):
    """A line with a cycloid deformation"""
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
        self.is3D = False
        self.skipsize3D = pyx.unit.length(0.04)
        self.parity3D = 0
        self.arrows = []
        self.labels = []
        self.arcradius = pyx.unit.length(0.25)
        self.frequency = 1.3
        self.extras = 0
        self.inverted = False
        self.linetype = "gluon"
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def set3D(self, is3D=True, skipsize=pyx.unit.length(0.04), parity=0):
        self.is3D = is3D
        self.skipsize3D = skipsize
        self.parity3D = parity
        return self


    def invert(self):
        """Flip the line decoration around the line."""
        self.inverted = not self.inverted
        return self


    def getFrequency(self):
        """Get the rate of occurence of the coil decoration."""
        return self.frequency


    def setFrequency(self, freq):
        """Set the rate of occurence of the coil decoration."""
        self.frequency = freq
        return self


    def getAmplitude(self):
        """Get the radius of the coil decoration.""" 
        return self.arcradius


    def setAmplitude(self, amplitude):
        """Set the radius of the coil decoration.""" 
        self.arcradius = amplitude
        return self


    def setExtraCycles(self, extras):
        """Add some extra (possibly negative) oscillations to the coil decoration.""" 
        self.extras = extras
        return self


    def getDeformedPath(self):
        """Get the path modified by the coil warping."""
        needwindings = self.frequency * \
                       pyx.unit.tocm(self.getVisiblePath().arclen()) / \
                       pyx.unit.tocm(self.arcradius)
        ## Get the whole number of windings and make sure that it's odd so we
        ## don't get a weird double-back thing
        intwindings = int(needwindings)
        intwindings += 2 * self.extras
        if intwindings % 2 == 0:
            intwindings -= 1
        deficit = needwindings - intwindings
        sign = 1
        if self.inverted: sign = -1 
        defo = pyx.deformer.cycloid(self.arcradius, intwindings, curvesperhloop=10,
                                    skipfirst = 0.0, skiplast = 0.0, sign = sign)
        return defo.deform(self.getVisiblePath())


    def draw(self, canvas):
        """Draw the line on the supplied canvas."""
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
        mypath = self.getDeformedPath()
        if not self.is3D:
            canvas.stroke(mypath, styles)
        else:
            para = pyx.deformer.parallel(0.001)
            as, bs, cs = para.normpath_selfintersections(mypath.normpath(), epsilon=0.01)
            coil_params = []
            for b in bs:
                coil_params.append(b[self.parity3D] - self.skipsize3D)
                coil_params.append(b[self.parity3D] + self.skipsize3D)
            pathbits = mypath.split(coil_params)
            on = True
            for pathbit in pathbits:
                if on:
                    canvas.stroke(pathbit, styles)
                on = not on

        ## Labels
        for l in self.labels:
            l.draw(canvas)



class Vector(DecoratedLine):
    """A line with a sinoid deformation"""
    def __init__(self, point1, point2, amplitude=0.25, frequency=1.0):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
        self.is3D = False
        self.arrows = []
        self.labels = []
        self.inverted = False
        self.arcradius = amplitude #pyx.unit.length(0.25)
        self.linetype = "photon"
        self.frequency = frequency
        self.extrahalfs = 0
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def invert(self):
        """Reflect the decoration in the line itself."""
        self.inverted = not self.inverted
        return self


    def getFrequency(self):
        """Get the rate of occurance of the oscillation."""
        return self.frequency


    def setFrequency(self, freq):
        """Set the rate of occurance of the oscillation."""
        self.frequency = freq
        return self


    def getAmplitude(self):
        """Get the size of the oscillation."""
        return self.arcradius


    def setAmplitude(self, amplitude):
        """Set the size of the oscillation."""
        self.arcradius = amplitude
        return self


    def setExtraHalfCycles(self, extras):
        """Add some extra half cycles to the oscillation on top of those
        determined from the frequency."""
        self.extrahalfs = extras
        return self


    def getDeformedPath(self):
        """Get the path with the decorative deformation."""
        intwindings = int(self.frequency * pyx.unit.tocm(self.getVisiblePath().arclen()) /
                          pyx.unit.tocm(self.arcradius))
        intwindings += self.extrahalfs
        sign = 1
        if self.inverted: sign = -1 
        defo = pyx.deformer.cycloid(self.arcradius, intwindings, curvesperhloop=5,
                                    skipfirst=0.0, skiplast=0.0, turnangle=0, sign=sign)
        return defo.deform(self.getVisiblePath())

        
    def draw(self, canvas):
        """Draw the line on the supplied canvas."""
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
        canvas.stroke(self.getDeformedPath(), styles)
        for l in self.labels:
            l.draw(canvas)


## Photon is an alias for Vector
Photon = Vector


class Graviton(DecoratedLine):
    """A line with a double sinoid deformation"""
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
        self.is3D = False
        self.skipsize3D = pyx.unit.length(0.04)
        self.parity3D = 0
        self.inverted = False
        self.arrows = []
        self.labels = []
        self.arcradius = pyx.unit.length(0.25)
        self.linetype = "graviton"
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def set3D(self, is3D=True, skipsize=pyx.unit.length(0.04), parity=0):
        self.is3D = is3D
        self.skipsize3D = skipsize
        self.parity3D = parity
        return self


    def invert(self):
        """Reflect the decoration in the line itself."""
        self.inverted = not self.inverted
        return self


    def getDeformedPath(self, sign = 1):
        """Get the path with the decorative deformation."""
        intwindings = int(0.6 * pyx.unit.tocm(self.getVisiblePath().arclen()) /
                          pyx.unit.tocm(self.arcradius))
        defo = pyx.deformer.cycloid(self.arcradius, intwindings, curvesperhloop=5,
                                    skipfirst=0.0, skiplast=0.0, turnangle=0, sign=sign)
        return defo.deform(self.getVisiblePath())

        
    def draw(self, canvas):
        """Draw the line on the supplied canvas."""
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
        mypath1 = self.getDeformedPath(+1)
        mypath2 = self.getDeformedPath(-1)
        if self.inverted:
            mypathtmp = mypath1
            mypath1 = mypath2
            mypath2 = mypathtmp
        if not self.is3D:
            canvas.stroke(mypath1, styles)
            canvas.stroke(mypath2, styles)
        else:
            as, bs = mypath1.intersect(mypath2)
            params1, params2 = [], []

            parity1 = True
            if self.parity3D == 0:
                parity1 = False
            for a in as[1:]: ## TODO: better endpoint cut vetoing
                if parity1:
                    params1.append(a - self.skipsize3D)
                    params1.append(a + self.skipsize3D)
                parity1 = not parity1
            pathbits1 = mypath1.split(params1)
            on = True
            for pathbit in pathbits1:
                if on:
                    canvas.stroke(pathbit, styles)
                on = not on

            parity2 = False
            if self.parity3D == 0:
                parity2 = True
            for b in bs[1:]: ## TODO: better endpoint cut vetoing
                if parity2:
                    params2.append(b - self.skipsize3D)
                    params2.append(b + self.skipsize3D)
                parity2 = not parity2
            pathbits2 = mypath2.split(params2)
            on = True
            for pathbit in pathbits2:
                if on:
                    canvas.stroke(pathbit, styles)
                on = not on


        for l in self.labels:
            l.draw(canvas)



class Gaugino(DecoratedLine):
    """A line with a sinoid deformation and a normal line"""
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        self.styles = []
        self.arcthrupoint = None
        self.is3D = False
        self.skipsize3D = pyx.unit.length(0.04)
        self.parity3D = 0
        self.inverted = False
        self.arrows = []
        self.labels = []
        self.arcradius = pyx.unit.length(0.25)
        self.linetype = "susyboson"
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)


    def set3D(self, is3D=True, skipsize=pyx.unit.length(0.04), parity=0):
        self.is3D = is3D
        self.skipsize3D = skipsize
        self.parity3D = parity
        return self


    def invert(self):
        """Reflect the decoration in the line itself."""
        self.inverted = not self.inverted
        return self


    def getDeformedPath(self):
        """Get the path with the decorative deformation."""
        intwindings = int(pyx.unit.tocm(self.getVisiblePath().arclen()) /
                          pyx.unit.tocm(self.arcradius))
        sign = 1
        if self.inverted: sign = -1 
        defo = pyx.deformer.cycloid(self.arcradius, intwindings, curvesperhloop=5,
                                    skipfirst=0.0, skiplast=0.0, turnangle=0, sign=sign)
        return defo.deform(self.getVisiblePath())

        
    def draw(self, canvas):
        """Draw the line on the supplied canvas."""
        styles = self.styles + self.arrows
        if FeynDiagram.options.DEBUG:
            print "Drawing " + str(self.__class__) + " with styles = " + str(styles)
        mypath1 = self.getVisiblePath()
        mypath2 = self.getDeformedPath()
        if not self.is3D:
            canvas.stroke(mypath1, styles)
            canvas.stroke(mypath2, styles)
        else:
            as, bs = mypath1.intersect(mypath2)
            params1, params2 = [], []

            parity1 = True
            if self.parity3D == 0:
                parity1 = False
            for a in as:
                if parity1:
                    params1.append(a - self.skipsize3D)
                    params1.append(a + self.skipsize3D)
                parity1 = not parity1
            pathbits1 = mypath1.split(params1)
            on = True
            for pathbit in pathbits1:
                if on:
                    canvas.stroke(pathbit, styles)
                on = not on

            parity2 = False
            if self.parity3D == 0:
                parity2 = True
            for b in bs:
                if parity2:
                    params2.append(b - self.skipsize3D)
                    params2.append(b + self.skipsize3D)
                parity2 = not parity2
            pathbits2 = mypath2.split(params2)
            on = True
            for pathbit in pathbits2:
                if on:
                    canvas.stroke(pathbit, styles)
                on = not on

        for l in self.labels:
            l.draw(canvas)



# A dictionary for mapping FeynML line types to line classes
NamedLine = { "higgs"    : Higgs,
              "photon"   : Photon,
              "gluon"    : Gluon,
              "fermion"  : Fermion,
              "graviton" : Graviton }
