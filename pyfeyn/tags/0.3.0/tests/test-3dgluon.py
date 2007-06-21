from pyx import *

splitsize = 0.25
arcradius = 2.0

c = canvas.canvas()

p = path.path( path.moveto(0,0), path.lineto(10,10) )
coil = deformer.cycloid(arcradius, 11, curvesperhloop=10, skipfirst = 0.0, skiplast = 0.0, sign = +1)
para = deformer.parallel(0.415 * arcradius)
dp = coil.deform(p)
pp = para.deform(p)

as, bs = pp.intersect(dp)

on = True
coil_params = []
for b in bs:
    if on:
        coil_params.append(b - splitsize)
        coil_params.append(b + splitsize)
    on = not on

pathbits = dp.split(coil_params)

#c.stroke(dp, [style.linewidth.THICK])
on = True
for pathbit in pathbits:
    if on:
        c.stroke(pathbit, [style.linewidth.THICK])
    on = not on

c.writetofile("test-3dgluon.pdf")
