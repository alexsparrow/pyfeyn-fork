from pyx import *

splitsize = 0.25
arcradius = 2.0

c = canvas.canvas()

p = path.path( path.moveto(0,0), path.lineto(10,10) )
coil = deformer.cycloid(arcradius, 7, curvesperhloop=10, skipfirst=0.0, skiplast=0.0, sign=+1)
para = deformer.parallel(0.1)
dp = coil.deform(p)
pp = para.deform(dp)

as, bs = pp.intersect(dp)

on = True
coil_params = []
for b in bs:
    if on:
        coil_params.append(b - splitsize)
        coil_params.append(b + splitsize)
    on = not on

pathbits = dp.split(coil_params)

c.stroke(dp, [style.linewidth.thin])
c.stroke(pp, [style.linewidth.thin, color.rgb.red])

# on = True
# for pathbit in pathbits:
#     if on:
#         c.stroke(pathbit, [style.linewidth.THICK])
#     on = not on

c.writetofile("test-3dgluon2.pdf")
