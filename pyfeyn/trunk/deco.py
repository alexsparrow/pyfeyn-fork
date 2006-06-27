import pyx
import math

##### Arrow decorator class #####

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
        arrowtopos = self.pos*dp.path.arclen()+0.5*self.size
        arrowtopath = dp.path.split(arrowtopos)[0]
        arrowpath = pyx.deco._arrowhead(arrowtopath, self.pos*dp.path.arclen(), 1, self.size, 45, constrictionlen)
        dp.ornaments.fill(arrowpath)
        return dp

##### TeXLabel decorator class #####

class TeXLabel(pyx.deco.deco, pyx.attr.attr):
    """TeX label for Feynman diagram lines"""
    def __init__(self, text, pos=0.5, size=pyx.text.size.normalsize, displace=0.5, angle=0, textattrs=[]):
        self.pos = pos
        self.size = size
        self.displace = displace
        self.angle = angle
        self.text = text
        self.textattrs = textattrs

    def decorate(self, dp, texrunner):
        dp.ensurenormpath()
        x, y = dp.path.at(dp.path.begin() + self.pos*dp.path.arclen())
        textattrs = pyx.attr.mergeattrs([pyx.text.halign.center,
                                         pyx.text.vshift.mathaxis] +
                                        [self.size] + self.textattrs)
        t = texrunner.text(x,y,self.text,self.textattrs)
        t.linealign(self.displace, math.cos(self.angle*math.pi/180),
                                   math.sin(self.angle*math.pi/180))
        dp.ornaments.insert(t)

##### Coil decorator class #####

class Coil(pyx.deformer.deformer):
    """Fancy version of the PyX default cycloid deformer, with an oscillating
    x-velocity and a 3D-look option.
    This appears to be broken at the moment.
    """

    def __init__(self, radius=0.5*pyx.unit.t_cm, halfloops=10,
                 skipfirst=1*pyx.unit.t_cm, skiplast=1*pyx.unit.t_cm,
                 curvesperhloop=3, sign=1, turnangle=45):
        self.skipfirst = skipfirst
        self.skiplast = skiplast
        self.radius = radius
        self.halfloops = halfloops
        self.curvesperhloop = curvesperhloop
        self.sign = sign
        self.turnangle = turnangle

    def __call__(self, radius=None, halfloops=None,
                 skipfirst=None, skiplast=None,
                 curvesperhloop=None, sign=None, turnangle=None):
        if radius is None:
            radius = self.radius
        if halfloops is None:
            halfloops = self.halfloops
        if skipfirst is None:
            skipfirst = self.skipfirst
        if skiplast is None:
            skiplast = self.skiplast
        if curvesperhloop is None:
            curvesperhloop = self.curvesperhloop
        if sign is None:
            sign = self.sign
        if turnangle is None:
            turnangle = self.turnangle
        return gluon(radius=radius, halfloops=halfloops,
                     skipfirst=skipfirst, skiplast=skiplast,
                     curvesperhloop=curvesperhloop,
                     sign=sign, turnangle=turnangle)

    def deform(self, abasepath):
        basepath = abasepath.normpath()
        for sp in basepath.normsubpaths:
            if sp == basepath.normsubpaths[0]:
                cycloidpath = self.deformsubpath(sp)
            else:
                cycloidpath.join(self.deformsubpath(sp))
        return cycloidpath


    def deformsubpath(self, subpath):
        skipfirst = abs(pyx.unit.topt(self.skipfirst))
        skiplast = abs(pyx.unit.topt(self.skiplast))
        radius = abs(pyx.unit.topt(self.radius))
        turnangle = self.turnangle * math.pi / 180.0

        cosTurn = math.cos(turnangle)
        sinTurn = math.sin(turnangle)

        # make list of the lengths and parameters at points on subpath where we will add cycloid-points
        totlength = subpath.arclen_pt()
        if totlength <= skipfirst + skiplast + 2*radius*sinTurn:
            sys.stderr.write("*** PyX Warning: subpath is too short for deformation with cycloid -- skipping...\n")
            return pyx.path.normpath([subpath])

        # parametrisation is in rotation-angle around the basepath
        # differences in length, angle ... between two basepoints
        # and between basepoints and controlpoints
        Dphi = math.pi / self.curvesperhloop
        phis = [i * Dphi for i in range(self.halfloops * self.curvesperhloop + 1)]
        DzDphi = (totlength - skipfirst - skiplast - 2*radius*sinTurn) * 1.0 / (self.halfloops * math.pi * cosTurn)
        Dz = (totlength - skipfirst - skiplast - 2*radius*sinTurn) * 1.0 / (self.halfloops * self.curvesperhloop * cosTurn)
        zs = [i * Dz for i in range(self.halfloops * self.curvesperhloop + 1)]
        # from path._arctobcurve:
        # optimal relative distance along tangent for second and third control point
        L = 4 * radius * (1 - math.cos(Dphi/2)) / (3 * math.sin(Dphi/2))

        # Now the transformation of z into the turned coordinate system
        Zs = [ skipfirst + radius*sinTurn # here the coordinate z starts
             - sinTurn*radius*math.cos(phi) + cosTurn*DzDphi*phi # the transformed z-coordinate
             for phi in phis]
        params = subpath._arclentoparam_pt(Zs)[0]

        # get the positions of the splitpoints in the cycloid
        points = []
        for phi, param in zip(phis, params):
            # the cycloid is a circle that is stretched along the subpath
            # here are the points of that circle
            basetrafo = subpath.trafo([param])[0]

            # The point on the cycloid, in the basepath's local coordinate system
            baseZ, baseY = 0, radius*math.sin(phi)

            # The tangent there, also in local coords
            tangentX = -cosTurn*radius*math.sin(phi) + sinTurn*DzDphi
            tangentY = radius*math.cos(phi)
            tangentZ = sinTurn*radius*math.sin(phi) + DzDphi*cosTurn
            norm = math.sqrt(tangentX*tangentX + tangentY*tangentY + tangentZ*tangentZ)
            tangentY, tangentZ = tangentY/norm, tangentZ/norm

            # Respect the curvature of the basepath for the cycloid's curvature
            # XXX this is only a heuristic, not a "true" expression for
            #     the curvature in curved coordinate systems
            pathradius = subpath.curveradius_pt([param])
            if pathradius is not None:
                factor = (pathradius[0] - baseY) / pathradius[0]
                factor = abs(factor)
            else:
                factor = 1
            l = L * factor

            # The control points prior and after the point on the cycloid
            preeZ, preeY = baseZ - l * tangentZ, baseY - l * tangentY
            postZ, postY = baseZ + l * tangentZ, baseY + l * tangentY

            # Now put everything at the proper place
            points.append(basetrafo.apply(preeZ, self.sign * preeY) +
                          basetrafo.apply(baseZ, self.sign * baseY) +
                          basetrafo.apply(postZ, self.sign * postY))

        if len(points) <= 1:
            sys.stderr.write("*** PyX Warning: subpath is too short for deformation with cycloid -- skipping...\n")
            return pyx.path.normpath([subpath])

        # Build the path from the pointlist
        # containing (control x 2,  base x 2, control x 2)
        if skipfirst > subpath.epsilon:
            newpath = subpath.segments(params)[0]
            newpath.append(pyx.path.normcurve_pt(*(points[0][2:6] + points[1][0:4])))
            cycloidpath = pyx.path.normpath([newpath])
        else:
            cycloidpath = pyx.path.normpath([pyx.path.normsubpath([pyx.path.normcurve_pt(*(points[0][2:6] + points[1][0:4]))], 0)])
        for i in range(1, len(points)-1):
            cycloidpath.normsubpaths[-1].append(pyx.path.normcurve_pt(*(points[i][2:6] + points[i+1][0:4])))
        if skiplast > subpath.epsilon:
            cycloidpath.join(pyx.path.normpath([subpath.split([params[-1]])[-1]]))

        # That's it
        return cycloidpath
