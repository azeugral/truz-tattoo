"""Gera as imagens do site a partir de _ref/limpo2 (sem selo) e _ref/ig (originais sem selo)."""
import os, subprocess, json
from PIL import Image
R = '_ref'; S = 'site/img'
ESR = os.path.abspath('../_ferramentas/realesrgan/realesrgan-ncnn-vulkan.exe')
def src(n):
    for p in (f'{R}/limpo2/{n}.png', f'{R}/ig/{n}.jpg'):
        if os.path.exists(p): return p
    raise SystemExit('falta '+n)
def up(n):
    o = f'{R}/x4/{n}.png'
    if not os.path.exists(o):
        os.makedirs(f'{R}/x4', exist_ok=True)
        subprocess.run([ESR, '-i', os.path.abspath(src(n)), '-o', os.path.abspath(o), '-n', 'realesrgan-x4plus', '-s', '4'], capture_output=True)
    return o
def crop45(im, fx=.5, fy=.5):
    W, H = im.size
    if W/H > .8: w, h = int(H*.8), H
    else: w, h = W, int(W/.8)
    x = int(min(max(fx*W - w/2, 0), W - w)); y = int(min(max(fy*H - h/2, 0), H - h))
    return im.crop((x, y, x+w, y+h))
def out(im, dst, w, q=84):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.convert('RGB').resize((w, int(w*im.height/im.width)), Image.LANCZOS).save(dst, quality=q, method=6)
J = json.load(open('tools/imagens.json', encoding='utf-8'))
for dst, n, w, fx, fy, hd in J['lista']:
    p = up(n) if hd else src(n)
    im = Image.open(p)
    out(crop45(im, fx, fy) if dst.endswith('.webp') and not dst.endswith('truz.webp') else im, f'{S}/{dst}', w)
    print(dst)
for n in J['grade']:
    out(crop45(Image.open(src(n)), *J.get('foco', {}).get(n, [.5, .5])), f'{S}/g/{n}.webp', 640, 80)
print('grade', len(J['grade']))
