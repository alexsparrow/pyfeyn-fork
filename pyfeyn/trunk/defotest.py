from pyx import *
from math import sin, cos

c = canvas.canvas()
mypath = path.curve(0.0, 0.0, 10.0, 30.0, 30.0, 30.0, 40.0, 0.0)
omega  = 200.0
numsegs = 100
mag = 2.0*unit.t_cm

arclength = mypath.arclen()
lenperseg = arclength/float(numsegs)
lengths = [i*lenperseg for i in range(0,numsegs+1)]

prevpos = mypath.atbegin()
prevgrad = (0,0) # fix!
controlfactor = arclength.t / 3.0
for l in lengths:
    tr = mypath.trafo(l)
    rot = mypath.rotation(l)
    start = prevpos
    end = tr.apply(0.0*unit.t_cm, mag * sin(omega * l / unit.t_cm))
    grad = rot.apply(1.0*unit.t_cm, omega * mag * cos(omega * l / unit.t_cm))
    #print "pos =", end[0], end[1]
    #print "grad =", grad[0], grad[1]
    m1 = [prevpos[i] + controlfactor * prevgrad[i] for i in [0,1]]
    m2 = [end[i] - controlfactor * grad[i] for i in [0,1]]
    ###
    s1 = start + end
    line = path.line(*s1)
    #c.stroke(line)
    ###
    s2 = (start[0], start[1], m1[0], m1[1], m2[0], m2[1], end[0], end[1])
    curve = path.curve(*s2)
    c.stroke(curve)
    ###
    c1 = path.circle(m1[0], m1[1], 0.05)
    c2 = path.circle(m2[0], m2[1], 0.05)
    c.fill(c1, [color.rgb.red])
    c.stroke(c1)
    c.stroke(c2)
    l1 = path.line(start[0], start[1], m1[0], m1[1])
    l2 = path.line(end[0], end[1], m2[0], m2[1])
    #c.stroke(l1)
    #c.stroke(l2)
    ###
    prevpos = end
    prevgrad = grad

c.writePDFfile("defotest")
