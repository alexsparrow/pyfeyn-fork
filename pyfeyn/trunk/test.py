#! /usr/bin/env python

from feyndiagram import *
from pyx import *

c = canvas.canvas()
fd = FeynDiagram()

p1 = Point(2, -2)
p2 = Point(-2, 2)
line = Line(p1, p2)
line.arcThru(Point(3, 0))
line.style([Arrow(0.5)])
e1 = Ellipse(0, 0, 1, 2).fillstyle([pattern.hatched135])

fd.add( line )
fd.add( Circle(p1.x(), p1.y(), 0.5).fillstyle([color.rgb.red]) )
fd.add( Circle(p2.x(), p2.y(), 0.5).fillstyle([color.rgb.blue]) )
fd.add( e1 )
fd.draw(c)

c.stroke( path.path( path.moveto(0,0), path.lineto(4,0) ), [deformer.cycloid(0.25, 21, skipfirst=0, skiplast=0)] )

c.writeEPSfile("test")
