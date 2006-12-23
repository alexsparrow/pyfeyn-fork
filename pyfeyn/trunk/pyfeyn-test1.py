from pyfeyn import *
from pyfeyn.user import *
from pyx import color

fd = FeynDiagram()

in1 = Point(-4,  2)
in2 = Point(-4, -2)
in_vtx = Vertex(-2, 0)
out1 = Point(4, -2)
out2 = Point(4,  2)
out_vtx = Vertex(2, 0)

fa1 = Fermion(in1, in_vtx).addArrow().addLabel(r"\Pelectron")
fa2 = Fermion(in_vtx, in2).addArrow().addLabel(r"\Ppositron")
bos = Photon(in_vtx, out_vtx).addLabel(r"\Pphoton/\PZ")
fb1 = Fermion(out1, out_vtx).addArrow(0.2).addLabel(r"\APquark")
fb2 = Fermion(out_vtx, out2).addArrow(0.8).addLabel(r"\Pquark")
glu = Gluon(out_vtx.midpoint(out1), out_vtx.midpoint(out2))
glu.invert().bend(0.5).addLabel("\Pgluon", displace=0.25)

fd.draw("pyfeyn-test1.pdf")
