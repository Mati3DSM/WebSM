#!/usr/bin/env python3
"""Optimiza de forma PERMANENTE las imágenes de assets/images/Works (en el lugar).

Uso (desde la raíz del repo, con la rama commiteada y limpia):
    python supermarket/optimize_source.py supermarket

Qué hace:
  1. JPG/JPEG/PNG/GIF de assets/images/Works -> WebP (GIF animado -> WebP animado),
     ancho máx. MAX_W. Borra el original solo si el WebP pesa menos.
  2. Reescribe las rutas en build.py y data/projects/*.json.
  3. Después corré `python build.py` para regenerar los HTML.
El backup es git: si algo no te gusta, `git restore .` / `git clean -fd`.
"""
import os, re, sys
from multiprocessing import Pool
from urllib.parse import unquote
from PIL import Image

MAX_W, QUALITY, MIN_KB = 2000, 82, 60
SUBDIR = os.path.join('assets', 'images', 'Works')

site = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
if not site or not os.path.isdir(os.path.join(site, SUBDIR)):
    sys.exit('Uso: python supermarket/optimize_source.py supermarket  (la carpeta que contiene assets/images/Works)')
assets = os.path.join(site, 'assets')

def convert(path):
    rel = os.path.relpath(path, assets).replace(os.sep, '/')      # images/Works/X/y.jpg
    before = os.path.getsize(path)
    if before < MIN_KB * 1024: return rel, None, before, before
    try:
        im = Image.open(path)
        out = os.path.splitext(path)[0] + '.webp'
        if getattr(im, 'is_animated', False):
            frames, durs = [], []
            for i in range(im.n_frames):
                im.seek(i); fr = im.convert('RGBA')
                if fr.width > MAX_W: fr = fr.resize((MAX_W, round(fr.height * MAX_W / fr.width)), Image.LANCZOS)
                frames.append(fr); durs.append(im.info.get('duration', 80))
            frames[0].save(out, 'WEBP', save_all=True, append_images=frames[1:], duration=durs,
                           loop=im.info.get('loop', 0), quality=70, method=4)
        else:
            has_a = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
            im = im.convert('RGBA' if has_a else 'RGB')
            if im.width > MAX_W: im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(out, 'WEBP', quality=QUALITY, method=6)
        im.close() if hasattr(im, 'close') else None
        after = os.path.getsize(out)
        if after >= before:
            os.remove(out); return rel, None, before, before
        os.remove(path)
        return rel, os.path.relpath(out, assets).replace(os.sep, '/'), before, after
    except Exception as e:
        print('  ! no se pudo convertir', rel, e); return rel, None, before, before

if __name__ == '__main__':
    files = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(site, SUBDIR))
             for f in fs if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    print(f'Convirtiendo {len(files)} imágenes (puede tardar varios minutos)...')
    with Pool() as pool: res = pool.map(convert, files, chunksize=4)
    changed = {r: n for r, n, _, _ in res if n}
    tb, ta = sum(r[2] for r in res), sum(r[3] for r in res)
    print(f'{tb/1048576:.0f} MB -> {ta/1048576:.0f} MB ({len(changed)} pasaron a WebP)')

    targets = [os.path.join(site, 'build.py')]
    pdir = os.path.join(site, 'data', 'projects')
    targets += [os.path.join(pdir, f) for f in os.listdir(pdir) if f.endswith('.json')]
    pat = re.compile(r'images/Works/[^"\'<>\s]+?\.(?:jpe?g|png|gif)', re.I)
    n = 0
    for p in targets:
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8', newline='').read()
        def sub(m):
            global n
            if unquote(m.group(0)) in changed:
                n += 1; return os.path.splitext(m.group(0))[0] + '.webp'
            return m.group(0)
        t = pat.sub(sub, s)
        if t != s: open(p, 'w', encoding='utf-8', newline='').write(t)
    print(f'{n} referencias actualizadas. Ahora corré: python build.py')
