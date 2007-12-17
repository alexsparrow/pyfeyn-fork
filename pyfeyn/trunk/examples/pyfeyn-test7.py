#! /usr/bin/env python

from pyfeyn.user import *
from pyx import *

fd = FeynDiagram()

in1 = Point(-4,  2)
in2 = Point(-4, -2)
out1 = Point(4, -2)
out2 = Point(4,  2)
in_vtx = Vertex(-2, 0, mark=CIRCLE)
out_vtx = Vertex(2, 0, mark=CIRCLE)

fa1 = Fermion(in1, in_vtx).addArrow().addLabel(r"\Pelectron")
fa2 = Fermion(in_vtx, in2).addArrow().addLabel(r"\Ppositron")
bos = Photon(in_vtx, out_vtx).addLabel(r"\Pphoton/\PZ")
fb1 = Fermion(out1, out_vtx).addArrow(0.2).addLabel(r"\APquark")
fb2 = Fermion(out_vtx, out2).addArrow(0.8).addLabel(r"\Pquark")
glu = Gluon(midpoint(out_vtx, out1), midpoint(out_vtx, out2))
glu.invert().bend(0.5).addLabel("\Pgluon", displace=0.25)

numcopies = 10
angle = 0.8
c1 = fd.drawToCanvas()
c2 = canvas.canvas()
c2.insert(c1, [trafo.rotate(-numcopies*angle)])

c = canvas.canvas()
for i in range(numcopies):
    trans = 1 - ((i+1)/float(numcopies))**8
    c.insert(c2, [trafo.rotate((i+1)*angle), color.transparency(trans)])
    c.insert(c1, [trafo.translate(0.1 - 0.01*(i+1), -5 + 0.05*(i+1)), color.transparency(trans)])

c.writetofile("pyfeyn-test7.pdf")
