#! /usr/bin/env python

from pyfeyn.user import *

fd = FeynDiagram()

p1 = Point(-2, 0)
p2 = Point( 2, 0)
fa1 = MultiLine(p1, p2).bend(0.5).addArrow()
c1 = Circle(center=p1, radius=0.5, fill=[color.rgb.red], points=[p1])
c2 = Circle(center=p2, radius=0.5, fill=[color.rgb.blue], points=[p2])

fd.draw("pyfeyn-test5.pdf")
