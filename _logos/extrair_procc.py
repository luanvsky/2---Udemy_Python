"""Extrai o logo do PROCC da capa da dissertacao (unica fonte confiavel do
wordmark 'PROCC' verde) e gera a variante azul.

Nota: a URL do SIGAA chamada logo_programa.jpg serve, na verdade, o brasao da
UFS - nao o logo do PROCC. Por isso a fonte e a capa enviada pelo usuario.
"""
import os
import pymupdf
from PIL import Image
import io, colorsys

OUT = r"D:\dsh-vsky\_logos"
COVER = (r"C:\Users\victo.000\.dsh\attachments\v1\objects\26"
         r"\263cefe52bdf54fea97a1a774fba3aaf3b2e5972212940209db7f71cda161361")

if not os.path.exists(COVER):
    raise SystemExit(f"capa nao encontrada: {COVER}")

d = pymupdf.open(COVER)

# faixa do logo PROCC detectada na capa (em pontos), com folga
RECT = pymupdf.Rect(153.2, 392.1, 235.9, 443.0)
Z = 18
pix = d[0].get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=RECT)
im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
print("bruto:", im.size)

LOW, HIGH = 226, 250
px = im.load()
for y in range(im.height):
    for x in range(im.width):
        r, g, b, _ = px[x, y]
        lum = (r + g + b) / 3.0
        if lum >= HIGH:
            px[x, y] = (r, g, b, 0)
        elif lum <= LOW:
            px[x, y] = (r, g, b, 255)
        else:
            px[x, y] = (r, g, b, int(255 * (HIGH - lum) / (HIGH - LOW)))

bb = im.getbbox()
im = im.crop(bb)
# reduz para o tamanho realmente usado em impressao (~160 pt a 300 dpi)
if im.width > 700:
    r = 700 / im.width
    im = im.resize((700, max(1, round(im.height * r))), Image.LANCZOS)
im.save(os.path.join(OUT, "procc_logo.png"), optimize=True)
print("procc_logo.png:", im.size, os.path.getsize(os.path.join(OUT, "procc_logo.png")) // 1024, "KB")

blue = im.copy()
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
print("OK")
