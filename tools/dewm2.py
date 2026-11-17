# Marca d'agua TRUZ: acha a cruz por template multiescala e apaga com LaMa (dewm.lama).
import sys, os, numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
from dewm import lama
T = cv2.imread(os.path.join(os.path.dirname(__file__), '..', '_ref', 'logo-x4.png'), 0)
_, tb = cv2.threshold(T, 128, 255, cv2.THRESH_BINARY)
n, lab, st, _ = cv2.connectedComponentsWithStats(tb)
i = 1 + np.argmax(st[1:, 4]); x, y, w, h, _ = st[i]
CRUZ = cv2.GaussianBlur(T[y:y+h, x:x+w], (0,0), 2)

def find(img):
    H, W = img.shape[:2]
    x0, y0 = int(W*.45), int(H*.30)
    g = cv2.cvtColor(img[y0:, x0:], cv2.COLOR_BGR2GRAY)
    best = (-1,)
    for hh in np.linspace(H*.10, H*.36, 22):
        s = hh/CRUZ.shape[0]; t = cv2.resize(CRUZ, (max(8,int(CRUZ.shape[1]*s)), int(hh)), interpolation=cv2.INTER_AREA)
        if t.shape[0] >= g.shape[0] or t.shape[1] >= g.shape[1]: continue
        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(r)
        if mv > best[0]: best = (mv, ml, t.shape)
    mv, (mx, my), (th, tw) = best
    cx, cy = x0+mx+tw/2, y0+my+th/2
    # emblema completo (TRUZ em cima, TATTOO embaixo, moldura): caixa maior que a cruz
    rx, ry = tw*1.05+W*.01, th*0.72+H*.01
    m = np.zeros((H, W), np.uint8)
    m[int(max(cy-ry,0)):int(min(cy+ry,H)), int(max(cx-rx,0)):int(min(cx+rx,W))] = 255
    return mv, m, (cx, cy, rx, ry)

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
    for n in sys.argv[3:]:
        img = cv2.imread(os.path.join(src, n+'.jpg'))
        mv, m, box = find(img)
        if mv < .42: print('fraco', n, round(mv,2)); cv2.imwrite(os.path.join(dst, n+'.png'), img); continue
        cv2.imwrite(os.path.join(dst, n+'.png'), lama(img, m, box)); print('ok', n, round(mv,2))
