from pyfeyn import *
from pyfeyn.user import *

fd = FeynDiagram()

pt_in = Vertex(0, 0)
pt_out = Vertex(0, 6)
#pt_out = Vertex(6, 0)
vtx = Vertex(3, 3)

f = Fermion(pt_in, pt_out).arcThru(vtx)

fd.draw("test-bend90a.pdf")
