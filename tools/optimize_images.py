#!/usr/bin/env python3
"""assets/img altındaki görselleri optimize eder.

- En uzun kenarı 1920 px'i aşan görselleri küçültür (küçükleri büyütmez)
- JPEG'leri kalite 82, progressive olarak yeniden kaydeder; EXIF yönünü uygular, meta veriyi atar
- Sadece dosya küçülüyorsa üzerine yazar (geçici dosya oluşturmaz)

Kullanım (proje kökünden):  python3 tools/optimize_images.py
Gerekli: Pillow  (pip install pillow)
"""
import io
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent / "assets" / "img"
MAX_SIDE = 1920
QUALITY = 82

before_total = after_total = changed = resized = 0

for path in sorted(ROOT.rglob("*")):
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue
    before = path.stat().st_size
    before_total += before
    after = before
    try:
        buf = io.BytesIO()
        did_resize = False
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im)
            if max(im.size) > MAX_SIDE:
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
                did_resize = True
            if path.suffix.lower() in {".jpg", ".jpeg"}:
                im.convert("RGB").save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
            else:
                im.save(buf, "PNG", optimize=True)
        data = buf.getvalue()
        if len(data) < before:
            path.write_bytes(data)
            after = len(data)
            changed += 1
            resized += did_resize
    except Exception as exc:  # noqa: BLE001
        print(f"ATLANDI: {path.name}: {exc}")
    after_total += after

mb = 1024 * 1024
print(f"{changed} dosya küçüldü ({resized} tanesi yeniden boyutlandı): "
      f"{before_total / mb:.1f} MB -> {after_total / mb:.1f} MB")
