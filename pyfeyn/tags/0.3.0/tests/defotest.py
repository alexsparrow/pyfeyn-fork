from pyx import *
from math import sin, cos

c = canvas.canvas()

mypath = path.curve( 2.0*unit.cm, 2.0*unit.cm,
                     4.0*unit.cm, 8.0*unit.cm,
                     8.0*unit.cm, 8.0*unit.cm,
                    10.0*unit.cm, 2.0*unit.cm)
#mypath = path.line(0.0*unit.cm, 0.0*unit.cm, 10.0*unit.cm, 0.0*unit.cm,)

#def deform:
#    gradfactor, gradfactor * omega * mag / unit.cm * cos(omega * l / unit.cm

numhalfperiods = 19
numsegs = 50
mag = 0.3*unit.cm
straightlen1 = 1.0*unit.cm
straightlen2 = 1.0*unit.cm

pathsegs = mypath.split([straightlen1, mypath.arclen() - straightlen2])
newpath = pathsegs[0]

mysubpath = pathsegs[1]
arclength = mysubpath.arclen()
lenperseg = arclength/float(numsegs)
lengths = [i*lenperseg for i in range(0,numsegs+1)]

## Calc omega specifically for this function (period length = 
omega = 3.14 * unit.cm / arclength * numhalfperiods
#print omega

gradfactor = lenperseg / 3.0
prevpos = mysubpath.atbegin()
prevgrad = mysubpath.rotation(0.0).apply(gradfactor,
                                      gradfactor * omega * mag / unit.cm)
for l in lengths[1:]:
    tr = mysubpath.trafo(l)
    rot = mysubpath.rotation(l)
    start = prevpos
    end = tr.apply(0.0*unit.cm, mag * sin(omega * l / unit.cm))
    grad1 = prevgrad
    grad2 = rot.apply(gradfactor,
                      gradfactor * omega * mag / unit.cm * cos(omega * l / unit.cm))
    m1 = [start[i] + grad1[i] for i in [0,1]]
    m2 = [end[i]   - grad2[i] for i in [0,1]]
    ###
    s1 = start + end
    line = path.line(*s1)
    #c.stroke(line)
    ###
    s2 = (start[0], start[1], m1[0], m1[1], m2[0], m2[1], end[0], end[1])
    curve = path.curve(*s2)
    newpath = newpath << curve
    #c.stroke(curve)
    ###
    c1 = path.circle(m1[0], m1[1], 0.05)
    c2 = path.circle(m2[0], m2[1], 0.05)
    l1 = path.line(start[0], start[1], m1[0], m1[1])
    l2 = path.line(end[0], end[1], m2[0], m2[1])
    #c.stroke(l1)
    #c.stroke(l2)
    c.fill(c1, [color.rgb.red])
    c.stroke(c1)
    #c.stroke(c2)
    ###
    prevpos = end
    prevgrad = grad2

newpath = newpath << pathsegs[2]
c.stroke(newpath, [color.rgb.black])

c.writePDFfile("defotest")
