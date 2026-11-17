"""Auditoria: http local, overflow horizontal em vários tamanhos, prints, quadros do hero e teste do formulário."""
import subprocess, sys, time, os
from playwright.sync_api import sync_playwright
os.makedirs('_ref/ver', exist_ok=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765', '-d', 'site'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
U = 'http://localhost:8765/'
W = [(320,640),(375,812),(390,844),(430,932),(768,1024),(1024,768),(1366,768),(1920,1080),(844,390)]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(channel='msedge')
        for w, h in W:
            pg = b.new_page(viewport={'width': w, 'height': h}); erros = []
            pg.on('console', lambda m: erros.append(m.text) if m.type == 'error' else None)
            pg.goto(U); pg.wait_for_timeout(1800)
            ov = pg.evaluate("""()=>{const W=document.documentElement.clientWidth;const bad=[];document.querySelectorAll('body *').forEach(e=>{if(e.closest('.orn,.lb,iframe'))return;const r=e.getBoundingClientRect();if(r.width&&(r.right>W+1||r.left<-1)&&getComputedStyle(e).position!=='fixed')bad.push(e.tagName+'.'+e.className+' '+Math.round(r.left)+'/'+Math.round(r.right))});return [document.documentElement.scrollWidth-W,bad.slice(0,6)]}""")
            print(w, h, 'overflow', ov, 'erros', erros[:3])
            pg.screenshot(path=f'_ref/ver/hero-{w}x{h}.png')
            if w in (390, 1366):
                pg.evaluate("document.querySelectorAll('.rev').forEach(e=>e.classList.add('vis'))"); pg.wait_for_timeout(900)
                pg.screenshot(path=f'_ref/ver/full-{w}.png', full_page=True)
            pg.close()
        # quadros do hero
        pg = b.new_page(viewport={'width': 1366, 'height': 768}); pg.goto(U)
        pg.wait_for_function("document.getElementById('hPeca').textContent!=='Fechamento de costas'", timeout=15000)
        t0 = time.time()
        for t in (0.3, 0.7, 1.1, 1.6):
            pg.wait_for_timeout(max(0, int((t - (time.time()-t0))*1000)))
            pg.locator('#quadro').screenshot(path=f'_ref/ver/q-{t}.png')
        b.close()
finally:
    srv.terminate()
