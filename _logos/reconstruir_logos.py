"""Reconstroi os logos institucionais: brasao UFS (do Manual da Marca) e PROCC."""
import os
import urllib.request
import pymupdf
from PIL import Image
import io, colorsys

OUT = r"D:\dsh-vsky\_logos"
os.makedirs(OUT, exist_ok=True)
MANUAL = os.path.join(OUT, "MANUAL_MARCA_UFS.pdf")


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print("ja existe:", dest)
        return
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36"})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())
    print("baixado:", dest, os.path.getsize(dest), "bytes")


# ---- 1) brasao UFS: pagina 17 do Manual da Marca, detectado por cor ----
fetch("http://www.ufs.br/uploads/MANUAL_MARCA_UFS.pdf", MANUAL)

d = pymupdf.open(MANUAL)
Z = 10
pix = d[16].get_pixmap(matrix=pymupdf.Matrix(Z, Z))
im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
W, H = im.size
px = im.load()


def is_crest(r, g, b):
    if r < 130 and b > 110 and b > r + 45:      # azul UFS
        return True
    if r > 170 and g < 200 and b < 120 and r > b + 70:   # chama / dourado
        return True
    return False


X0, Y0, X1, Y1 = int(130 * Z), int(105 * Z), int(300 * Z), int(310 * Z)
x0, y0, x1, y1 = W, H, -1, -1
for y in range(Y0, Y1):
    for x in range(X0, X1):
        if is_crest(*px[x, y]):
            x0, y0 = min(x0, x), min(y0, y)
            x1, y1 = max(x1, x), max(y1, y)
print(f"bbox brasao: ({x0},{y0},{x1},{y1}) = {x1-x0+1} x {y1-y0+1} px")

pad = 8
crop = im.crop((max(0, x0 - pad), max(0, y0 - pad),
                min(W, x1 + pad + 1), min(H, y1 + pad + 1))).convert("RGBA")
cp = crop.load()
for y in range(crop.height):
    for x in range(crop.width):
        r, g, b, _ = cp[x, y]
        lum = (r + g + b) / 3.0
        if lum >= 246:
            cp[x, y] = (r, g, b, 0)
        elif lum <= 226:
            cp[x, y] = (r, g, b, 255)
        else:
            cp[x, y] = (r, g, b, int(255 * (246 - lum) / 20))
crop.save(os.path.join(OUT, "UFS_crest.png"), optimize=True)
print("UFS_crest.png:", crop.size, f"ratio={crop.width/crop.height:.2f}")

# ---- 2) PROCC: logo oficial do SIGAA ----
PROCC_JPG = os.path.join(OUT, "_procc_src.jpg")
try:
    req = urllib.request.Request(
        "https://www.sigaa.ufs.br/sigaa/public/programa/img/logo_programa.jpg",
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.sigaa.ufs.br/"})
    with urllib.request.urlopen(req, timeout=60) as r, open(PROCC_JPG, "wb") as f:
        f.write(r.read())
    print("PROCC oficial:", os.path.getsize(PROCC_JPG), "bytes")
except Exception as e:
    print("falhou PROCC oficial:", e)
    PROCC_JPG = None

if PROCC_JPG and os.path.exists(PROCC_JPG):
    src = Image.open(PROCC_JPG).convert("RGBA")
    # limpa o fundo branco
    px2 = src.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px2[x, y]
            if r > 243 and g > 243 and b > 243:
                px2[x, y] = (r, g, b, 0)
    # upscale 6x para uso em impressao
    big = src.resize((src.width * 6, src.height * 6), Image.LANCZOS)
    big.save(os.path.join(OUT, "procc_logo.png"), optimize=True)
    print("procc_logo.png:", big.size)

    # variante azul (paleta da apresentacao)
    blue = big.copy()
    pb = blue.load()
    for y in range(blue.height):
        for x in range(blue.width):
            r, g, b, a = pb[x, y]
            if a == 0:
                continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if ss >= 0.15 and 55 <= hh * 360 <= 185:
                r2, g2, b2 = colorsys.hsv_to_rgb(0.615, ss, vv)
                pb[x, y] = (int(r2 * 255), int(g2 * 255), int(b2 * 255), a)
    blue.save(os.path.join(OUT, "procc_logo_azul.png"), optimize=True)
    print("procc_logo_azul.png:", blue.size)

print("\nOK - logos reconstruidos em", OUT)
