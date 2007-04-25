from pyx import *

splitsize = 0.15
arcradius = 1.0

c = canvas.canvas()

p = path.path( path.moveto(0,0), path.lineto(10,10) )
coil = deformer.cycloid(arcradius, 15, curvesperhloop=10, skipfirst=0.0, skiplast=0.0, sign=+1)
para = deformer.parallel(0.1)
dp = coil.deform(p)

as, bs, cs = para.normpath_selfintersections(dp.normpath(), 0.01)
#print as, "\n"
#print bs, "\n"
#print cs, "\n"

## Get the appropriate split points around each intersection
coil_params = []
for b in bs:
    coil_params.append(b[0] - splitsize)
    coil_params.append(b[0] + splitsize)
pathbits = dp.split(coil_params)

## Draw the underlying line with some transparency
c.stroke(dp, [style.linewidth.THICK, color.cmyk.Violet, color.transparency(0.8)])

on = True
for pathbit in pathbits:
    if on:
        c.stroke(pathbit, [color.rgb.red, style.linewidth.thick])
    #else:
    #    c.stroke(pathbit, [color.rgb.blue])
    on = not on

c.writetofile("test-3dgluon2.pdf")
