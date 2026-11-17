# Remove a marca d'agua TRUZ (canto inferior direito) com LaMa ONNX.
import sys, os, json, numpy as np, cv2, onnxruntime as ort
LAMA = os.path.expanduser('~/Documents/PROJETOS LRGZ/_ferramentas/lama/lama_fp32.onnx')
sess = ort.InferenceSession(LAMA)

def find(img):
    H, W = img.shape[:2]
    x0, y0 = int(W*.52), int(H*.40)
    reg = img[y0:, x0:]
    hsv = cv2.cvtColor(reg, cv2.COLOR_BGR2HSV)
    wht = ((hsv[...,2] > 205) & (hsv[...,1] < 40)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(wht)
    # componentes finos/altos do logo: descartar manchas grandes (pele/luz)
    keep = np.zeros_like(wht)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 6: continue
        fill = a/(w*h)
        if a > 0.02*reg.shape[0]*reg.shape[1] and fill > .5: continue
        keep[lab == i] = 1
    big = cv2.dilate(keep, np.ones((int(W*.03),)*2, np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(big)
    if n < 2: return None
    # escolher o aglomerado com mais pixels brancos do logo
    best, bs = None, 0
    for i in range(1, n):
        s = keep[lab == i].sum()
        x, y, w, h, a = st[i]
        if h < H*.08 or w > W*.4: continue
        if s > bs: best, bs = i, s
    if best is None: return None
    x, y, w, h, a = st[best]
    m = np.zeros((H, W), np.uint8)
    pad = int(W*.012)
    m[y0+y-pad:y0+y+h+pad, x0+x-pad:x0+x+w+pad] = 255
    return m, (x0+x+w/2, y0+y+h/2, w/2+pad, h/2+pad)

def lama(img, m, box):
    cx, cy, rx, ry = box
    H, W = img.shape[:2]
    side = int(max(rx, ry)*2*1.8); side = min(side, W, H)
    x0 = int(np.clip(cx-side/2, 0, W-side)); y0 = int(np.clip(cy-side/2, 0, H-side))
    ci = img[y0:y0+side, x0:x0+side]; cm = m[y0:y0+side, x0:x0+side]
    a = cv2.resize(ci, (512,512), interpolation=cv2.INTER_AREA)[..., ::-1].astype(np.float32)/255
    b = (cv2.resize(cm, (512,512), interpolation=cv2.INTER_NEAREST) > 127).astype(np.float32)
    a = a*(1-b[...,None])
    out = sess.run(None, {'image': a.transpose(2,0,1)[None], 'mask': b[None,None]})[0][0].transpose(1,2,0)
    if out.max() <= 1.5: out = out*255
    out = np.clip(out,0,255).astype(np.uint8)[..., ::-1]
    out = cv2.resize(out, (side, side), interpolation=cv2.INTER_CUBIC)
    f = cv2.GaussianBlur(cv2.dilate(cm, np.ones((9,9),np.uint8)), (0,0), 4).astype(np.float32)[...,None]/255
    res = img.copy(); res[y0:y0+side, x0:x0+side] = (out*f + ci*(1-f)).astype(np.uint8)
    return res

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
    rep = {}
    for n in sys.argv[3:]:
        img = cv2.imread(os.path.join(src, n+'.jpg'))
        r = find(img)
        if r is None: print('sem selo', n); cv2.imwrite(os.path.join(dst, n+'.png'), img); continue
        out = lama(img, *r)
        cv2.imwrite(os.path.join(dst, n+'.png'), out); rep[n] = [int(v) for v in r[1]]
        print('ok', n, rep[n])
