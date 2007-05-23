"""A couple of classes for decorating diagram elements."""

import pyx, math
from pyfeyn.diagrams import FeynDiagram
from pyfeyn.utils import Visible


## Arrow decorator class
class Arrow(pyx.deco.deco, pyx.attr.attr):
    """Arrow for Feynman diagram lines"""
    def __init__(self, pos=0.5, size=6*pyx.unit.v_pt,
                 angle=45, constriction=0.8):
        self.pos = pos
        self.size = size
        self.angle = angle
        self.constriction = constriction
        
    def decorate(self, dp, texrunner):
        """Attach arrow to a path (usually a line)."""
        dp.ensurenormpath()
        constrictionlen = self.size * self.constriction * \
                          math.cos(self.angle*math.pi/360.0)
        arrowtopos = self.pos * dp.path.arclen()+0.5*self.size
        arrowtopath = dp.path.split(arrowtopos)[0]
        arrowpath = pyx.deco._arrowhead(arrowtopath, self.pos*dp.path.arclen(),
                                        1, self.size, 45, constrictionlen)
        dp.ornaments.fill(arrowpath)
        return dp


class FreeArrow(Visible):
    """Arrow not attached to any line in a diagram."""
    def __init__(self, length=0.5*pyx.unit.v_cm, size=6*pyx.unit.v_pt,
                 angle=45, constriction=0.8, pos=None, x=None, y=None,
                 direction=0):
        self.x, self.y = 0, 0
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if pos is not None:
            self.x, self.y = pos.getXY()
        self.direction = direction
        self.length = length
        self.size = size
        self.angle = angle
        self.constriction = constriction
        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)        

    def draw(self, canvas):
        """Draw this arrow on the supplied canvas."""
        endx, endy = self.x-self.length*math.sin(self.direction*math.pi/180.), \
                     self.y-self.length*math.cos(self.direction*math.pi/180.)
        linepath = pyx.deco.decoratedpath(
                       pyx.path.path(pyx.path.moveto(endx,endy),
                                     pyx.path.lineto(self.x,self.y)))
        styles = [pyx.deco.earrow(size=self.size, angle=self.angle,
                        constriction=self.constriction)]
        canvas.stroke(linepath.path,styles)


class ParallelArrow(Visible):
    """Arrow running parallel to a line, for momenta, helicities etc."""
    def __init__(self, line, pos=0.5, displace=0.3, length=0.5*pyx.unit.v_cm,
                 size=6*pyx.unit.v_pt, angle=45, constriction=0.8, sense=+1):
        self.line = line
        self.pos = pos
        self.displace = pyx.unit.length(displace)
        self.length = length
        self.size = size
        self.angle = angle
        self.constriction = constriction
        self.sense = sense

    def draw(self, canvas):
        """Draw this arrow on the supplied canvas."""
        p = self.line.getPath()
        posparam = p.begin() + self.pos * p.arclen() 
        x, y = self.line.fracpoint(self.pos).getXY()
        arrx, arry = self.line.fracpoint(self.pos+self.length/2./p.arclen()).getXY()
        endx, endy = self.line.fracpoint(self.pos-self.length/2./p.arclen()).getXY() 

        ## Calculate the displacement from the line
        displacement = self.displace
        intrinsicwidth = pyx.unit.length(0.1)
        if hasattr(self.line, "arcradius"):
            intrinsicwidth = self.line.arcradius
        if displacement > 0:
            displacement += intrinsicwidth
        else:
            displacement -= intrinsicwidth
        if FeynDiagram.options.DEBUG:
            print "Displacement = ", displacement

        ## Position the arrow on the right hand side of lines
        tangent = p.tangent(posparam, displacement)
        normal = tangent.transformed(pyx.trafo.rotate(90, x, y))
        nx, ny = normal.atend()
        nxcm, nycm = pyx.unit.tocm(nx - x), pyx.unit.tocm(ny - y)
        vx, vy = p.atbegin()
        vxcm, vycm = pyx.unit.tocm(x - vx), pyx.unit.tocm(y - vy)

        ## If the arrow is on the left, flip it by 180 degrees
        if (vxcm * nycm - vycm * nxcm) > 0:
            normal = normal.transformed(pyx.trafo.rotate(180, x, y))
            nx, ny = normal.atend()
        if displacement < 0:
            normal = normal.transformed(pyx.trafo.rotate(180, x, y))
            nx, ny = normal.atend()
        if FeynDiagram.options.VDEBUG:
            FeynDiagram.currentCanvas.stroke(normal)

        ## Displace the arrow by this normal vector
        endx, endy = endx + (nx-x), endy + (ny-y)
        arrx, arry = arrx + (nx-x), arry + (ny-y)

        if self.sense<0.:
           arrx, arry, endx, endy = endx, endy, arrx, arry

        linepath = pyx.deco.decoratedpath(
                       pyx.path.path(pyx.path.moveto(endx,endy),
                                     pyx.path.lineto(arrx,arry)))
        styles = [pyx.deco.earrow(size=self.size, angle=self.angle,
                        constriction=self.constriction)]
        canvas.stroke(linepath.path,styles)



## Label
class Label(Visible):
    """General label, unattached to any diagram elements"""
    def __init__(self, text, pos=None, x=None, y=None):
        self.x, self.y = 0, 0
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.size = pyx.text.size.normalsize
        self.text = text
        self.textattrs = []
        self.pos = pos

        ## Add this to the current diagram automatically
        FeynDiagram.currentDiagram.add(self)

    def draw(self, canvas):
        """Draw this label on the supplied canvas."""
        textattrs = pyx.attr.mergeattrs([pyx.text.halign.center,
                                         pyx.text.vshift.mathaxis,
                                         self.size] + self.textattrs)
        t = pyx.text.defaulttexrunner.text(self.x, self.y, self.text, textattrs)
        canvas.insert(t)



## PointLabel
class PointLabel(Label):
    """Label attached to points on the diagram"""
    def __init__(self, point, text, displace=0.3, angle=0):
        self.size = pyx.text.size.normalsize
        self.displace = pyx.unit.length(displace)
        self.angle = angle
        self.text = text
        self.point = point
        self.textattrs = []


    def getPoint(self):
        """Get the point associated with this label."""
        return self.point


    def setPoint(self, point):
        """Set the point associated with this label."""
        self.point = point
        return self


    def draw(self, canvas):
        """Draw this label on the supplied canvas."""
        if FeynDiagram.options.VDEBUG:
            canvas.fill(pyx.path.circle(self.point.getX(),
                                        self.point.getY(), 0.05), [pyx.color.rgb.green])
        x = self.point.getX() + self.displace * math.cos(math.radians(self.angle))
        y = self.point.getY() + self.displace * math.sin(math.radians(self.angle))
        textattrs = pyx.attr.mergeattrs([pyx.text.halign.center,
                                         pyx.text.vshift.mathaxis,
                                         self.size] + self.textattrs)
        t = pyx.text.defaulttexrunner.text(x, y, self.text, textattrs)
        canvas.insert(t)



## LineLabel
class LineLabel(Label):
    """Label for Feynman diagram lines"""
    def __init__(self, line, text, pos=0.5, displace=0.3, angle=0):
        self.pos = pos
        self.size = pyx.text.size.normalsize
        self.displace = pyx.unit.length(displace)
        self.angle = angle
        self.text = text
        self.line = line
        self.textattrs = []


    def getLine(self):
        """Get the associated line."""
        return self.line


    def setLine(self, line):
        """Set the associated line."""
        self.line = line
        return self


    def draw(self, canvas):
        """Draw this label on the supplied canvas."""
        p = self.line.getPath()
        #x, y = self.line.fracPoint(self.pos).getXY()
        posparam = p.begin() + self.pos * p.arclen()
        x, y = p.at(posparam)

        ## Calculate the displacement from the line
        displacement = self.displace
        intrinsicwidth = pyx.unit.length(0.1)
        if hasattr(self.line, "arcradius"):
            intrinsicwidth = self.line.arcradius
        if displacement > 0:
            displacement += intrinsicwidth
        else:
            displacement -= intrinsicwidth
        if FeynDiagram.options.DEBUG:
            print "Displacement = ", displacement

        ## Position the label on the right hand side of lines
        tangent = p.tangent(posparam, displacement)
        normal = tangent.transformed(pyx.trafo.rotate(90, x, y))
        nx, ny = normal.atend()
        nxcm, nycm = pyx.unit.tocm(nx - x), pyx.unit.tocm(ny - y)
        vx, vy = p.atbegin()
        vxcm, vycm = pyx.unit.tocm(x - vx), pyx.unit.tocm(y - vy)

        ## If the label is on the left, flip it by 180 degrees
        if (vxcm * nycm - vycm * nxcm) > 0:
            normal = normal.transformed(pyx.trafo.rotate(180, x, y))
            nx, ny = normal.atend()
        if displacement < 0:
            normal = normal.transformed(pyx.trafo.rotate(180, x, y)) 
            nx, ny = normal.atend()
        if FeynDiagram.options.VDEBUG:
            FeynDiagram.currentCanvas.stroke(normal)

        ## Displace the label by this normal vector
        x, y = nx, ny

        textattrs = pyx.attr.mergeattrs([pyx.text.halign.center,
                                         pyx.text.vshift.mathaxis,
                                         self.size] + self.textattrs)
        t = pyx.text.defaulttexrunner.text(x, y, self.text, textattrs)
        #t.linealign(self.displace,
        #            math.cos(self.angle * math.pi/180),
        #            math.sin(self.angle * math.pi/180))
        canvas.insert(t)

