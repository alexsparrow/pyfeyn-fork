#! /usr/bin/env python

from feyndiagram import *
from pyx import *

c = canvas.canvas()
fd = FeynDiagram()

p1 = FilledPoint(2, -2, 0.3)
p1.fillstyle([color.rgb.blue])
p2 = FilledPoint(-2, 2, 0.3)
p2.fillstyle([pattern.hatched135])
line = Line(p1, p2)
line.arcThru(Point(3, 0))
line.style([Arrow(0.5)])

fd.add(line)
fd.add(p1)
fd.add(p2)

fd.draw(c)

c.writeEPSfile("test")
