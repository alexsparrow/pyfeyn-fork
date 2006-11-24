#! /usr/bin/env python

from feyn import *
from hepnames import *
from pyx import *

print "Starting up..."
fd = FeynDiagram()

print "Defining things: ",
print "points,",
p1 = Point(2, -2)
p2 = Point(-2, 2)
p3 = Vertex(1.25, 1.25, "circle")
p4 = p1.midpoint(p2)
p5 = p4.midpoint(p1) # addBlob
p6 = p4.midpoint(p2) # addBlob

print "blobs,",
c1 = Circle(p1.x(), p1.y(), radius = 0.5,
            fill = [color.rgb.red], points = [p1])
c2 = Circle(p2.x(), p2.y(), radius = 0.3,
            fill = [color.rgb.green],
            points = [p2])
e1 = Ellipse(p4.x(), p4.y(), xradius = 0.5, yradius = 1.0,
             fill = [color.cmyk.MidnightBlue], points = [p4])

print "lines."
l0a = Fermion(p1, p4)
l0b = Fermion(p2, p4)
l1 = NamedLine["gluon"](p1, p2).arcThru(pos=(3,0))
l1.addLabel(r"\Pgluon", displace = 0.3)
l2 = NamedLine["photon"](p2,p1).arcThru(pos=(0,-3))
l2.addLabel(r"\Pphoton", displace = -0.5)
l3 = Gluon(p2, p3)
l4 = Photon(p1, p3)
l5 = Gluon(p5, p6).bend(-1)
l5.addLabel(r"$\Pgluon_1$", pos = 0.3, displace = -0.9)
loop1 = Line(p3, p3).arcThru(Point(1.75, 1.75)).addArrow(0.55)

print "Committing to the canvas and file..."
fd.draw("fdtest.pdf")
