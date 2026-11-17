"""Logo TRUZ (branca no preto, destaque do IG) -> site/img/logo.svg e a cruz sozinha -> cruz.svg (favicon)."""
import numpy as np, potrace
from PIL import Image, ImageFilter
from scipy import ndimage
im = Image.open('_ref/logo-x4.png').convert('L').filter(ImageFilter.GaussianBlur(1.5))
a = np.array(im) > 128   # tinta = branco
def svg(a, dst):
    path = potrace.Bitmap(~a).trace(turdsize=60, alphamax=1.0, opticurve=True, opttolerance=0.2)
    ys, xs = np.where(a); pad = 4
    x0, y0, x1, y1 = xs.min()-pad, ys.min()-pad, xs.max()+pad, ys.max()+pad
    parts = []
    for c in path:
        s = c.start_point; d = [f'M{s.x-x0:.1f} {s.y-y0:.1f}']
        for seg in c.segments:
            if seg.is_corner: d.append(f'L{seg.c.x-x0:.1f} {seg.c.y-y0:.1f}L{seg.end_point.x-x0:.1f} {seg.end_point.y-y0:.1f}')
            else: d.append(f'C{seg.c1.x-x0:.1f} {seg.c1.y-y0:.1f} {seg.c2.x-x0:.1f} {seg.c2.y-y0:.1f} {seg.end_point.x-x0:.1f} {seg.end_point.y-y0:.1f}')
        parts.append(''.join(d)+'Z')
    open(dst,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x1-x0} {y1-y0}"><path fill="currentColor" fill-rule="evenodd" d="{"".join(parts)}"/></svg>')
    print(dst, len(parts), x1-x0, y1-y0)
svg(a, 'site/img/logo.svg')
lab, n = ndimage.label(a); sizes = ndimage.sum(a, lab, range(1, n+1))
svg(lab == (np.argmax(sizes)+1), 'site/img/cruz.svg')
