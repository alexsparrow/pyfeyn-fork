import pyx, math

from diagrams import FeynDiagram
from utils import Visible


## Arrow decorator class
class Arrow(pyx.deco.deco, pyx.attr.attr):
    """Arrow for Feynman diagram lines"""
    def __init__(self, pos=0.5, size=6*pyx.unit.v_pt, angle=45, constriction=0.8):
        self.pos = pos
        self.size = size
        self.angle = angle
        self.constriction = constriction
        
    def decorate(self, dp, texrunner):
        dp.ensurenormpath()
        constrictionlen = self.size*self.constriction*math.cos(self.angle*math.pi/360.0)
        arrowtopos = self.pos * dp.path.arclen()+0.5*self.size
        arrowtopath = dp.path.split(arrowtopos)[0]
        arrowpath = pyx.deco._arrowhead(arrowtopath, self.pos*dp.path.arclen(), 1, self.size, 45, constrictionlen)
        dp.ornaments.fill(arrowpath)
        return dp


## Label
class Label(Visible):
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
        return self.line


    def setLine(self, line):
        self.line = line
        return self


    def draw(self, canvas):
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

        textattrs = pyx.attr.mergeattrs([pyx.text.halign.center, pyx.text.vshift.mathaxis, self.size] + self.textattrs)
        t = pyx.text.defaulttexrunner.text(x, y, self.text, textattrs)
        #t.linealign(self.displace,
        #            math.cos(self.angle * math.pi/180),
        #            math.sin(self.angle * math.pi/180))
        canvas.insert(t)

