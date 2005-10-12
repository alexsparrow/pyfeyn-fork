#! /usr/bin/env python

from feyn import *
#from pyx import *

c = canvas.canvas()
fd = FeynDiagram()

p1 = Point(2, -2)
p2 = Point(-2, 2)
#line = Line(p1, p2)
line = Gluon(p1, p2).arcThru(Point(3, 0)).style([Arrow(0.5)])
e1 = Ellipse(0, 0, 1, 2).fillstyle([pattern.hatched135])

fd.add( line )
fd.add( Circle(p1.x(), p1.y(), 0.5).fillstyle([color.rgb.red]) )
fd.add( Circle(p2.x(), p2.y(), 0.5).fillstyle([color.rgb.blue]) )
fd.add( e1 )
fd.draw(c)

c.writeEPSfile("thetest")
