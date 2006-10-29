#! /usr/bin/env python

from feyn import *
from hepnames import *
from pyx import *

print "Starting up..."

c = pyx.canvas.canvas()
fd = FeynDiagram()

print "Defining things: ",
print "points,",
# A simple point
p1 = Point(2, -2)
# A decorated point
p2 = DecoratedPoint(-2, 2, pyx.path.circle)
# A decorated points with styles applied
p3 = DecoratedPoint(1, 1).mark(NamedMark["square"]).fillstyle(pyx.color.rgb.green)
# Some automatically computed points
p4 = p1.midpoint(p2)
p5 = p4.midpoint(p1)
p6 = p4.midpoint(p2)

print "blobs,",
# some blobs with styles applied
c1 = Circle(p1.x(), p1.y(), radius = 0.5, fillstyles = [color.rgb.red])
e1 = Ellipse(0, 0, xradius = 0.5, yradius = 1.0, fillstyles = [pattern.hatched135])

print "lines."
# A decorated line (by name)
l0 = NamedLine["fermion"](c1, p2)
# Some decorated lines (by name) with styles applied
l1 = NamedLine["gluon"](p1, p2).arcThru(Point(3, 0)).style([Arrow(),TeXLabel(hepnames_dict["gluon"])])
l2 = NamedLine["photon"](p2,p1).arcThru(Point(0,-3)).style([Arrow(),TeXLabel(hepnames_dict["photon"])])
# Some decorated lines (by call) with styles applied
l3 = Gluon(p2, p3).style([Arrow()])
l4 = Photon(p1, p3).style([Arrow()])
l5 = Gluon(p5, p6).bend(-1).style([TeXLabel("$\\bar{\\mathbf{q}}$",displace=-0.5)]).tension(1.2)
# A decorated line with styles applied, which is a tadpole-style loop
loop1 = Line(p3, p3).arcThru(Point(1.5,1.5)).style([Arrow(),TeXLabel("$"+hepnames_dict["pi+"]+"(k)$",pos=0.66,displace=0.2)])


print "Drawing them: ",
print "points,",
fd.add( p1, p2, p3, p4, p5, p6 )
print "lines,",
fd.add( l0, l1, l2, l3, l4, l5, loop1 )
print "blobs."
fd.add( c1, e1 )

print "Committing to the canvas..."
fd.draw(c)

print "Writing to file..."
c.writeEPSfile("thetest")

#print fd.toXML()

