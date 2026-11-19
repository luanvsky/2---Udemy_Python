"""Reduz os logos para o tamanho realmente usado (~160 pt a 300 dpi), sem perda visivel."""
from PIL import Image
import os

OUT = r"D:\dsh-vsky\_logos"
# 160 pt at 300 dpi ~= 667 px
TARGET_W = 700

for name in ("procc_logo.png", "procc_logo_azul.png", "UFS_crest.png"):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        print("falta:", name)
        continue
    before = os.path.getsize(p)
    im = Image.open(p).convert("RGBA")
    if im.width > TARGET_W:
        r = TARGET_W / im.width
        im = im.resize((TARGET_W, max(1, round(im.height * r))), Image.LANCZOS)
    im.save(p, optimize=True)
    after = os.path.getsize(p)
    print(f"{name}: {im.size}  {before//1024} KB -> {after//1024} KB")
