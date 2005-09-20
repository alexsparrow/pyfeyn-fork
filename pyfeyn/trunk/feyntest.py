#! /usr/bin/env python

from feyndiagram import *
from pyx import *

c = canvas.canvas()
fd = FeynDiagram()

p1 = FilledPoint(1, -1, 0.15)
p1.fillstyle([color.rgb.blue])
p2 = Point(-1, 1, 0.15)
line = Line(p1, p2)
line.style([deco.barrow.normal, deco.earrow.normal])
line.arcThru(Point(0, 0))

fd.add(line)
fd.add(p1)
fd.add(p2)

fd.draw(c)

#c.stroke(path.line(0, 1, 2, 2), [deco.barrow.normal, deco.earrow.normal])

c.writeEPSfile("test")
