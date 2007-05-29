from pyfeyn.user import *
from pyfeyn.feynml import *

fd = FeynDiagram()

in1 = Point(1, 7)
loop_in = Vertex(4, 7)
loop_out = Vertex(7, 7)
out1a = Point(11, 7)
out1b = Point(11, 5)
in2 = Point(1, 0)
out2a = Point(11, 2)
out2b = Point(11, 0)
out1c = Vertex(out1b.x() - 2, out1b.y())
out1d = Vertex(out2a.x() - 2, out2a.y())
vtx = Vertex(out1c.midpoint(out1d).x() - 1.5, out1c.midpoint(out1d).y()).setMark(SQUARE)

f_spec = Fermion(out2b, in2).addArrow().addLabel(r"\APdown")
f1 = Fermion(in1, loop_in).addArrow().addLabel(r"\Pbottom")
f2 = Fermion(loop_out, out1a).addArrow().addLabel(r"\Pstrange")
bos1 = Photon(loop_in, loop_out).bend(-1.5).addLabel(r"\PWplus")
f_loop = Fermion(loop_in, loop_out).bend(+1.5).addArrow() \
         .addLabel(r"\Pup,\,\Pcharm,\,\Ptop")
bos2 = Photon(f_loop.fracpoint(0.6), vtx).addLabel(r"\Pphoton/\PZ", displace=0.5).bend(0.5)
f3 = Fermion(out1b, out1c).addArrow(0.8).addLabel(r"\APup")
f4 = Fermion(out1c, out1d).arcThru(vtx)
f5 = Fermion(out1d, out2a).addArrow(0.2).addLabel(r"\Pup")

in_blob = Ellipse(x=1, y=3.5, xradius=1, yradius=3.5).setFillStyle(CROSSHATCHED45)
out_blob1 = Ellipse(x=11, y=6, xradius=0.6, yradius=1).setFillStyle(HATCHED135)
out_blob2 = Ellipse(x=11, y=1, xradius=0.6, yradius=1).setFillStyle(HATCHED135)

fmlwriter = FeynMLWriter("test.xml")
fmlwriter.describe("""A B-meson colour-suppressed penguin decay diagram.""")
fmlwriter.diagramToXML(fd,convertlegs=False)
fmlwriter.close()
