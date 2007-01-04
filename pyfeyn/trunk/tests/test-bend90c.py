from pyx import *

c = canvas.canvas()

c.stroke(path.path(
    path.moveto(0,0),
    path.arc(0, 3, 3, 270, 90)
    ))
#pt_in = Vertex(0, 0)
#pt_out = Vertex(0, 6)
##pt_out = Vertex(6, 0)
#vtx = Vertex(3, 3)

#f = Fermion(pt_in, pt_out).arcThru(vtx)

c.writetofile("test-bend90c.pdf")
