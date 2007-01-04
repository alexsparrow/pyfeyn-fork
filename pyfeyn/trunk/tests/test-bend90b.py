from pyfeyn import *
from pyfeyn.user import *
from pyx import color

fd = FeynDiagram()

out1c = Vertex(9, 5)
out1d = Vertex(9, 2)
vtx = Point(7.5, 3.50)

out1c = Vertex(0, 3)
out1d = Vertex(0, 0)
vtx = Point(1.5, 1.501)

f4 = Fermion(out1c, out1d).arcThru(vtx)

fd.draw("test-bend90b.pdf")
