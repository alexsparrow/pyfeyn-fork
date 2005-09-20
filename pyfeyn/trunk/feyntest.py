#! /usr/bin/env python

from feyndiagram import *
from pyx import * 

c = canvas.canvas()
fd = FeynDiagram()

p1 = FilledPoint(1, -1, 0.15)
p1.fillstyle([color.rgb.blue])
p2 = FilledPoint(-1, 1, 0.15)
line = Line(p1, p2)
line.arcThru(Point(0, 0))

fd.add(line)
fd.add(p1)
fd.add(p2)

fd.draw(c)
c.writeEPSfile("test")
