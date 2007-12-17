#! /usr/bin/env python

from pyfeyn import *
from pyfeyn.feynml import *

fd = FeynDiagram()

in1 = Point(-4,  2)
in2 = Point(-4, -2)
in_vtx = Vertex(-2, 0)
out1 = Point(4, -2)
out2 = Point(4,  2)
out_vtx = Vertex(2, 0)
glue1 = out_vtx.midpoint(out1)
glue2 = out_vtx.midpoint(out2)

l1 = Label("Drell-Yan QCD vertex correction", x=0, y=2)
fa1 = Fermion(in1, in_vtx).addArrow().addLabel(r"\Pelectron")
fa2 = Fermion(in_vtx, in2).addArrow().addLabel(r"\Ppositron")
fa2.addParallelArrow(size=0.1, displace=-0.06, sense=-1)
bos = Photon(in_vtx, out_vtx).addLabel(r"\Pphoton/\PZ")
fb1 = Fermion(out1, glue1).addArrow().addLabel(r"\APquark")
fb1.addParallelArrow(size=0.1, displace=-0.06, sense=-1)
fi1 = Fermion(glue1, out_vtx)
fi2 = Fermion(out_vtx, glue2)
fb2 = Fermion(glue2, out2).addArrow().addLabel(r"\Pquark")
glu = Gluon(glue1, glue2)
glu.invert().bend(0.5).addLabel("\Pgluon", displace=0.25)
glu.addParallelArrow(size=0.1, displace=0.2, sense=-1)

fmlwriter = FeynMLWriter("test.xml")
fmlwriter.describe("""A sample diagram showing a QCD correction to the Drell-Yan process.""")
fmlwriter.diagramToXML(fd)
fmlwriter.close()

