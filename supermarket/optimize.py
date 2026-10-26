#!/usr/bin/env python3
"""Optimiza las imágenes de una carpeta ya lista para publicar (no toca originales).

Uso:  python3 optimize.py CARPETA_SITIO
  - JPG/JPEG/PNG/GIF -> WebP (animado si es GIF animado), ancho máx. MAX_W
  - reescribe las referencias en .html/.css/.js
  - og:image / twitter:image se dejan en su formato original (WhatsApp, LinkedIn,
    etc. no siempre leen WebP): esas imágenes se achican pero siguen siendo JPG/PNG.
Parámetros ajustables abajo.
"""
import os, re, sys
from multiprocessing import Pool
from urllib.parse import unquote
from PIL import Image

MAX_W   = 2000   # ancho máximo en px (pantallas retina de ~1000 px de ancho de imagen)
QUALITY = 82     # calidad WebP (80-85 es indistinguible a simple vista)
MIN_KB  = 60     # archivos más chicos que esto no se tocan (logos, iconos)
OG_W    = 1600

root = sys.argv[1].rstrip('/')
IMG  = os.path.join(root, 'assets', 'images')
EXT  = ('.jpg', '.jpeg', '.png', '.gif')

def text_files():
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith(('.html', '.css', '.js')):
                yield os.path.join(d, f)

# imágenes usadas como og:image / twitter:image
og = set()
for p in text_files():
    if p.endswith('.html'):
        s = open(p, encoding='utf-8', newline='').read()
        for m in re.finditer(r'(?:og|twitter):image"\s+content="[^"]*?(assets/images/[^"]+)"', s):
            og.add(unquote(m.group(1)))

def convert(path):
    rel = os.path.relpath(path, root).replace(os.sep, '/')
    before = os.path.getsize(path)
    try:
        im = Image.open(path)
        animated = getattr(im, 'is_animated', False)
        if rel in og:                      # se queda en su formato, solo más liviana
            im = im.convert('RGB') if path.lower().endswith(('.jpg', '.jpeg')) else im
            if im.width > OG_W: im = im.resize((OG_W, round(im.height * OG_W / im.width)), Image.LANCZOS)
            if path.lower().endswith(('.jpg', '.jpeg')): im.save(path, 'JPEG', quality=84, optimize=True, progressive=True)
            else: im.save(path, optimize=True)
            return rel, None, before, os.path.getsize(path)
        if before < MIN_KB * 1024: return rel, None, before, before
        out = os.path.splitext(path)[0] + '.webp'
        if animated:
            frames, durs = [], []
            for i in range(im.n_frames):
                im.seek(i); fr = im.convert('RGBA')
                if fr.width > MAX_W: fr = fr.resize((MAX_W, round(fr.height * MAX_W / fr.width)), Image.LANCZOS)
                frames.append(fr); durs.append(im.info.get('duration', 80))
            frames[0].save(out, 'WEBP', save_all=True, append_images=frames[1:], duration=durs,
                           loop=im.info.get('loop', 0), quality=70, method=4)
        else:
            has_a = im.mode in ('RGBA', 'LA', 'P') and ('transparency' in im.info or im.mode != 'P')
            im = im.convert('RGBA' if has_a else 'RGB')
            if im.width > MAX_W: im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(out, 'WEBP', quality=QUALITY, method=6)
        after = os.path.getsize(out)
        if after >= before:                # el WebP no ayudó: se descarta
            os.remove(out); return rel, None, before, before
        os.remove(path)
        return rel, os.path.relpath(out, root).replace(os.sep, '/'), before, after
    except Exception as e:
        print('  ! no se pudo convertir', rel, e); return rel, None, before, before

if __name__ == '__main__':
    files = [os.path.join(d, f) for d, _, fs in os.walk(IMG) for f in fs if f.lower().endswith(EXT)]
    with Pool() as pool: res = pool.map(convert, files, chunksize=4)
    changed = {r: n for r, n, _, _ in res if n}
    tb = sum(r[2] for r in res); ta = sum(r[3] for r in res)
    print(f'{len(files)} imágenes: {tb/1048576:.0f} MB -> {ta/1048576:.0f} MB, {len(changed)} pasaron a WebP')

    pat = re.compile(r'assets/images/[^"\'<>)\s]+?\.(?:jpe?g|png|gif)', re.I)
    for p in text_files():
        s = open(p, encoding='utf-8', newline='').read()
        def sub(m):
            ref = unquote(m.group(0))
            new = changed.get(ref)
            return os.path.splitext(m.group(0))[0] + '.webp' if new else m.group(0)
        t = pat.sub(sub, s)
        if t != s: open(p, 'w', encoding='utf-8', newline='').write(t)
