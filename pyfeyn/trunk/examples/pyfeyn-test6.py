from pyfeyn.user import *

fd = FeynDiagram()

i1 = Point(-4, +2)
i2 = Point(-4, -2)
v1 = Vertex(-2, 0, mark=CircleMark())
v2 = Vertex(+2, 0, mark=CircleMark())
o1 = Point(+4, +2)
o2 = Point(+4, -2)

l1 = Fermion(i1, v1).addArrow()
l2 = Fermion(v1, i2).addArrow()
l1 = Fermion(o1, v2).addArrow()
l2 = Fermion(v2, o2).addArrow()
g = Graviton(v1, v2).bend(1.5)
g = SusyBoson(v1, v2).bend(-1.5)


fd.draw("pyfeyn-test6.pdf")
