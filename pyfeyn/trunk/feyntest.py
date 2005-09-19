#! /usr/bin/env python

from feyndiagram import *
from pyx import * 

c = canvas.canvas()
fd = FeynDiagram()

p1 = Point(-1,-1)
p2 = FilledPoint(1,1)
line = Line(p1, p2)
line.addstyles([style.linewidth.Thin, style.linewidth.Thick])

fd.add("l1", line)
fd.add("p1", p1)
fd.add("p2", p2)

fd.draw(c)
c.writeEPSfile("test")
