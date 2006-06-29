#! /usr/bin/env python

from feyn import *
from hepnames import *
import pyx

print "Starting up..."

c = pyx.canvas.canvas()
fd = FeynDiagram()

print "Defining things:"

print " points,"
p1 = Point(2, -2)
p2 = DecoratedPoint(-2, 2, pyx.path.circle)
p3 = DecoratedPoint(1, 1)
p4 = p1.midpoint(p2)
p5 = p4.midpoint(p1)
p6 = p4.midpoint(p2)
print " lines,"
l0 = NamedLine["fermion"](p1, p2)
l1 = NamedLine["gluon"](p1, p2).arcThru(Point(3, 0)).style([Arrow(),TeXLabel(hepnames_dict["gluon"])])
l2 = NamedLine["photon"](p2,p1).arcThru(Point(0,-3)).style([Arrow(),TeXLabel(hepnames_dict["photon"])])
l3 = Gluon(p2, p3).style([Arrow()])
l4 = Photon(p1, p3).style([Arrow()])
l5 = Gluon(p5, p6).bend(-1).style([TeXLabel("$\\bar{\\mathbf{q}}$",displace=-0.5)]).tension(1.2)
loop1 = Line(p3, p3).arcThru(Point(1.5,1.5)).style([Arrow(),TeXLabel("$"+hepnames_dict["pi+"]+"(k)$",pos=0.66,displace=0.2)])
print " and blobs."
c1 = Circle(p1.x(), p1.y(), 0.5).fillstyle([pyx.color.rgb.red])
c2 = Circle(p2.x(), p2.y(), 0.5).fillstyle([pyx.color.rgb.blue])
e1 = Ellipse(0, 0, 0.5, 1.0).fillstyle([pyx.pattern.hatched135])

print "Drawing them:"

print " points,"
fd.add( p1 )
fd.add( p2 )
fd.add( p3 )
print " lines,"
fd.add( l0 )
fd.add( l1 )
fd.add( l2 )
fd.add( l3 )
fd.add( l4 )
fd.add( l5 )
fd.add( loop1 )
print " and blobs."
fd.add( c1 )
#fd.add( c2 )
fd.add( e1 )
print "Committing to the canvas..."
fd.draw(c)

print "Writing to file..."

c.writeEPSfile("thetest")

print fd.to_xml()

