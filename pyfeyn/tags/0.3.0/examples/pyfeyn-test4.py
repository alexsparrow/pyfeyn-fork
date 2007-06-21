from pyfeyn.user import *

fd = FeynDiagram()

in1  = Point(-3, 0)
out1 = Point( 3, 0)
vtx1 = Vertex(-1, 0)
vtx2 = Vertex( 1, 0)

higgs1 = Higgs(in1, vtx1).addLabel(r"\PHiggs")
higgs2 = Higgs(vtx2, out1).addLabel(r"\PHiggs")
loop1 = Fermion(vtx1, vtx2).bend(-1).addArrow().addLabel(r"\APtop")
loop1 = Fermion(vtx2, vtx1).bend(-1).addArrow().addLabel(r"\Ptop")

fd.draw("pyfeyn-test4.pdf")
