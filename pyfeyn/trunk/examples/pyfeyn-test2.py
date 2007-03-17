from pyfeyn import *
from pyfeyn.user import *

fd = FeynDiagram()

p1 = Point(2, -2)
p2 = Point(-2, 2)
p3 = Vertex(1.25, 1.25, "circle")
p4 = p1.midpoint(p2)
p5 = p4.midpoint(p1)
p6 = p4.midpoint(p2)

c1 = Circle(center=p1, radius=0.5, fill=[color.rgb.red], points=[p1])
c2 = Circle(center=p2, radius=0.3, fill=[color.rgb.green], points=[p2])
e1 = Ellipse(center=p4, xradius=0.5, yradius=1.0,
             fill=[color.cmyk.MidnightBlue], points=[p4])

l0a = Fermion(p1, p4)
l0b = Fermion(p2, p4)
l1 = NamedLine["gluon"](p2, p1).arcThru(x=3, y=0)
l2 = NamedLine["photon"](p1, p2).arcThru(x=0, y=-3)
l3 = Gluon(p2, p3)
l4 = Photon(p1, p3)
l5 = Gluon(p5, p6).bend(-p5.distance(p6)/2.0)
loop1 = Line(p3, p3).arcThru(x=1.75, y=1.75).addArrow(0.55)

l1.addLabel(r"\Pgluon")
l2.addLabel(r"\Pphoton")
l5.addLabel(r"$\Pgluon_1$")

fd.draw("pyfeyn-test2.pdf")
