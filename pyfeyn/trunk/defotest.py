from pyx import *

c = canvas.canvas()
mypath = path.curve(0.0, 0.0, 1.0, 3.0, 3.0, 3.0, 4.0, 0.0)
print mypath.arclen()
mypathsegs = mypath.split([mypath.arclen()/10.0 for i in range(1,11)])
for seg in mypathsegs[::2]:
    print seg
    c.stroke(seg)
c.writePDFfile("defotest")
