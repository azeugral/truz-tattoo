"""Adornos do traço do Truz: lírio fineline (Ch53UMENJMA) e ramo nas costas (DAHySUENS5g).
Real-ESRGAN x4 antes; máscara por polígono (coords na escala 1x do recorte)."""
import cv2, numpy as np
P = {
 'lirio': [(60,140),(180,60),(270,25),(310,40),(390,110),(425,200),(410,380),(340,420),(300,425),(200,490),(130,465),(90,320),(55,260)],
 'ramo': [(360,100),(420,45),(460,60),(470,200),(510,330),(505,420),(470,510),(400,580),(380,680),(350,760),(270,820),(220,950),(200,1080),(60,1080),(60,830),(90,680),(200,470),(330,380),(360,250),(355,140)],
}
COR = (218, 228, 236)  # BGR osso
for n, pts in P.items():
    im = cv2.imread(f'_ref/orn/{n}-x4.png')
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    r = g/(cv2.GaussianBlur(g, (0,0), 45)+1)
    ink = np.clip((0.90-r)/0.32, 0, 1)
    m = np.zeros(g.shape, np.float32); cv2.fillPoly(m, [(np.array(pts)*4).astype(np.int32)], 1)
    a = ink*cv2.GaussianBlur(m, (0,0), 15); a[a < .18] = 0
    b = (a > .25).astype(np.uint8)
    k, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
    keep = np.zeros(k, bool); keep[1:] = st[1:, 4] > 500
    a = np.where(cv2.dilate(keep[lab].astype(np.uint8), np.ones((9,9))) > 0, a, 0)
    a = np.clip(cv2.GaussianBlur(a, (0,0), 1.2)**.75*1.15, 0, 1)
    a = (a*255).astype(np.uint8)
    ys, xs = np.nonzero(a > 30); p = 40
    a = a[max(ys.min()-p,0):ys.max()+p, max(xs.min()-p,0):xs.max()+p]
    rgba = np.dstack([np.full_like(a, COR[0]), np.full_like(a, COR[1]), np.full_like(a, COR[2]), a])
    s = 1200/a.shape[0]; rgba = cv2.resize(rgba, (int(a.shape[1]*s), 1200), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'_ref/orn/{n}.png', rgba)
    prev = np.zeros(rgba.shape[:2]+(3,), np.uint8); prev[:] = (12,12,13)
    al = rgba[...,3:4]/255; prev = (prev*(1-al) + rgba[...,:3]*al).astype(np.uint8)
    cv2.imwrite(f'_ref/orn/{n}-prev.jpg', prev); print(n, rgba.shape)
