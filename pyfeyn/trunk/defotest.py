from pyx import *
from math import sin, cos

c = canvas.canvas()
mypath = path.curve(0.0, 0.0, 10.0, 30.0, 30.0, 30.0, 40.0, 0.0)
numsegs = 100
omega  = 100.0
mag = 2.5

lenperseg = mypath.arclen()/float(numsegs)
lengths = [i*lenperseg for i in range(0,numsegs+1)]

#mypathsegs = mypath.split(lengths[1:-1])
#for seg in mypathsegs[::2]:
#    c.stroke(seg)

prevpos = mypath.atbegin()
prevgrad = (0,0) # fix!
for l in lengths:
    tr = mypath.trafo(l)
    rot = mypath.rotation(l)
    start = prevpos
    end = tr.apply(0.0, mag * sin(omega * l.t))
    m1 = [prevpos[i] + prevgrad[i] for i in [0,1]]
    grad = rot.apply(0.01, 0.01 * omega * mag * cos(omega * l.t))
    #print "pos =", end[0], end[1]
    #print "grad =", grad[0], grad[1]
    m2 = [end[i] - grad[i] for i in [0,1]]
    ###
    s1 = start + end
    line = path.line(*s1)
    c.stroke(line)
    ###
    s2 = (start[0], start[1], m1[0], m1[1], m2[0], m2[1], end[0], end[1])
    curve = path.curve(*s2)
    c1 = path.circle(m1[0], m1[1], 0.2)
    c2 = path.circle(m2[0], m2[1], 0.2)
    c.fill(c1, [color.rgb.red])
    c.stroke(c1)
    c.stroke(c2)
    l1 = path.line(start[0], start[1], m1[0], m1[1])
    l2 = path.line(end[0], end[1], m2[0], m2[1])
    c.stroke(l1)
    c.stroke(l2)
    #c.stroke(curve)
    ###
    prevpos = end
    prevgrad = grad

c.writePDFfile("defotest")
