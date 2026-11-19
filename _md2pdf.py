"""Renderiza markdown -> PDF (A4) com capa institucional UFS + PROCC."""
import re
import pymupdf
BUILD = 'v9-ultimo'

SRC = r"D:\dsh-vsky\Meta_Experimental_XBRL.md"
OUT = r"D:\dsh-vsky\Meta_Experimental_XBRL.pdf"
LOGOS = r"D:\dsh-vsky\_logos"

A4W, A4H = 595.28, 841.89
ML, MR, MT, MB = 58, 58, 62, 58
NAVY = (0.07, 0.16, 0.29)
BLUE = (0.05, 0.31, 0.63)
GREY = (0.42, 0.45, 0.49)
DARK = (0.11, 0.12, 0.15)
# base-14 fonts are WinAnsi only and silently corrupt accented Portuguese and
# dashes, so every visible glyph is drawn from an embedded TTF instead.
FONTDIR = r"C:\Windows\Fonts"
FONTS = {
    "helv": (FONTDIR + r"\arial.ttf", "arial.ttf"),
    "hebo": (FONTDIR + r"\arialbd.ttf", "arialbd.ttf"),
    "heit": (FONTDIR + r"\ariali.ttf", "ariali.ttf"),
}
F, FB = "helv", "hebo"
TW = A4W - ML - MR
BODY_SZ = 9.6

doc = pymupdf.open()

# one Font object per face, reused so the TTF is embedded only once
FONTOBJ = {k: pymupdf.Font(fontfile=v[0]) for k, v in FONTS.items()}


def span_w(txt, font, size):
    """Width using the same TTF that will be embedded, so wrapping matches."""
    if font in FONTOBJ:
        return FONTOBJ[font].text_length(txt, fontsize=size)
    return pymupdf.get_text_length(txt, font, size)


def put(page, x, y, txt, font, size, color):
    """Draw one short run (cover lines) with the embedded TTF."""
    if not txt:
        return
    f = FONTOBJ.get(font)
    if f is None:
        page.insert_text((x, y), txt, fontname=font, fontsize=size, color=color)
        return
    w = pymupdf.TextWriter(page.rect)
    w.append((x, y), txt, font=f, fontsize=size)
    w.write_text(page, color=color)


def parse_inline(s):
    s = s.replace("**", "\x01")
    parts, bold, buf = [], False, ""
    for ch in s:
        if ch == "\x01":
            if buf:
                parts.append((buf, FB if bold else F, DARK))
                buf = ""
            bold = not bold
        else:
            buf += ch
    if buf:
        parts.append((buf, FB if bold else F, DARK))
    return parts or [("", F, DARK)]


def split_tokens(spans):
    """Tokens as (word, font, color, had_trailing_space)."""
    toks = []
    for txt, font, color in spans:
        buf = ""
        for ch in txt:
            if ch == " ":
                toks.append((buf, font, color, True))
                buf = ""
            else:
                buf += ch
        if buf:
            toks.append((buf, font, color, False))
    return toks


def break_long(token, font, color, size, width):
    """Break an over-wide token (e.g. a URL) into (text, font, color) pieces."""
    out, cur = [], ""
    for ch in token:
        if span_w(cur + ch, font, size) > width and cur:
            out.append((cur, font, color))
            cur = ch
        else:
            cur += ch
    if cur:
        out.append((cur, font, color))
    return out


def wrap_spans(spans, size, width):
    """Wrap to width. An over-wide token (e.g. a URL) is pre-split into pieces
    that flow like words, so nothing ever exceeds the column."""
    toks = split_tokens(spans)
    # pre-break any token wider than the column
    flat = []
    for w, font, color, sp in toks:
        if w and span_w(w, font, size) > width:
            flat.extend([(t, f, c, False) for t, f, c in break_long(w, font, color, size, width)])
        else:
            flat.append((w, font, color, sp))

    spacew = span_w(" ", F, size)
    lines, cur, curw = [], [], 0.0
    pending = False
    for w, font, color, sp in flat:
        if not w:
            pending = True
            continue
        ww = span_w(w, font, size)
        prefix = " " if (pending and cur) else ""
        if cur and curw + (spacew if prefix else 0) + ww > width:
            lines.append(cur)
            cur, curw, prefix = [], 0.0, ""
        cur.append((prefix + w, font, color))
        curw += (spacew if prefix else 0) + ww
        pending = sp
    if cur:
        lines.append(cur)
    return [l for l in lines if l]


_WRITERS = {}


def page_writer(page):
    """One TextWriter per page, so each TTF is embedded once per page."""
    w = _WRITERS.get(page.number)
    if w is None:
        w = pymupdf.TextWriter(page.rect)
        _WRITERS[page.number] = w
    return w


def flush_page(page):
    w = _WRITERS.get(page.number)
    if w is not None and w.text_rect is not None:
        w.write_text(page)


def draw_spans(page, x, y, line, size):
    """Append the whole line to one writer per page (font embedded once)."""
    w = page_writer(page)
    cx = x
    for tok, font, color in line:
        f = FONTOBJ.get(font)
        if tok and f is not None:
            w.append((cx, y), tok, font=f, fontsize=size)
        cx += span_w(tok, font, size)
    return cx


def col_widths(rows, avail):
    n = max(len(r) for r in rows)
    weights = []
    for c in range(n):
        mx = 4
        for r in rows:
            if c < len(r):
                mx = max(mx, len(re.sub(r"[*`]", "", r[c])))
        weights.append(mx ** 0.85)
    tot = sum(weights)
    return [avail * w / tot for w in weights]


class Doc:
    def __init__(self):
        self.page = None
        self.y = 0
        self.new_page()

    def new_page(self):
        self.page = doc.new_page(width=A4W, height=A4H)
        self.page.draw_rect(pymupdf.Rect(0, 0, A4W, 5), color=BLUE, fill=BLUE)
        self.y = MT

    def space(self, h):
        self.y += h

    def need(self, h):
        if self.y + h > A4H - MB - 20:
            self.new_page()

    def heading(self, text, level):
        size = {1: 17, 2: 13.6, 3: 11.6, 4: 10.6}.get(level, 10.5)
        self.space({1: 18, 2: 16, 3: 12, 4: 10}.get(level, 9))
        spans = parse_inline(text)
        lines = wrap_spans([(t, FB, NAVY) for t, _, _ in spans], size, TW)
        self.need(len(lines) * (size + 4) + 12)
        for j, ln in enumerate(lines):
            if self.y + size > A4H - MB:
                self.new_page()
            self.y += size
            draw_spans(self.page, ML, self.y, [(w, FB, NAVY) for w, _, _ in ln], size)
            self.y += 3
        if level <= 2:
            self.y += 4
            self.page.draw_line(pymupdf.Point(ML, self.y), pymupdf.Point(A4W - MR, self.y),
                                color=BLUE, width=1.0 if level == 1 else 0.6)
        self.space(6)

    def para(self, text, indent=0, quote=False, bullet=None):
        size = BODY_SZ - (0.5 if quote else 0)
        spans = parse_inline(text)
        extra = (14 if quote else 0) + (14 if bullet else 0)
        x = ML + indent + extra
        avail = TW - indent - extra
        lines = wrap_spans(spans, size, avail)
        self.need(len(lines) * (size + 3.6) + 4)
        for ln in lines:
            if self.y + size > A4H - MB:
                self.new_page()
            self.y += size + 1.4
            if bullet and ln is lines[0]:
                draw_spans(self.page, ML + indent + 2, self.y, [(bullet, FB, BLUE)], size)
            draw_spans(self.page, x, self.y, ln, size)
            self.y += 2.4
        self.space(1.8 if quote else 3.6)

    def rule(self):
        self.space(6)
        self.need(10)
        self.page.draw_line(pymupdf.Point(ML, self.y), pymupdf.Point(A4W - MR, self.y),
                            color=(0.78, 0.80, 0.83), width=0.7)
        self.space(8)

    def table(self, rows):
        size, pad = 8.2, 4.0
        headers, body = rows[0], rows[1:]
        widths = col_widths(rows, TW)
        lead = size + 2.6

        def header():
            self.need(lead + pad * 2 + 6)
            h = lead + pad * 1.6
            self.page.draw_rect(pymupdf.Rect(ML, self.y, A4W - MR, self.y + h),
                                color=None, fill=(0.925, 0.945, 0.975))
            x = ML
            for i, cell in enumerate(headers):
                put(self.page, x + pad, self.y + pad + size,
                    re.sub(r"[*`]", "", cell), FB, size, NAVY)
                x += widths[i]
            self.y += h
            self.page.draw_line(pymupdf.Point(ML, self.y), pymupdf.Point(A4W - MR, self.y),
                                color=BLUE, width=0.7)
            self.space(2)

        header()
        for r in body:
            cells = [re.sub(r"[*`]", "", c) for c in r]
            wrapped = [wrap_spans([(c, F, DARK)], size, widths[i] - pad * 2)
                       for i, c in enumerate(cells)]
            nlines = max(len(w) for w in wrapped)
            h = nlines * (size + 2.6) + pad * 1.4
            if self.y + h > A4H - MB - 20:
                self.new_page()
                header()
            for li in range(nlines):
                x = ML
                for i, w in enumerate(wrapped):
                    if li < len(w):
                        draw_spans(self.page, x + pad, self.y + size + li * (size + 2.6), w[li], size)
                    x += widths[i]
            self.y += h
            self.page.draw_line(pymupdf.Point(ML, self.y), pymupdf.Point(A4W - MR, self.y),
                                color=(0.85, 0.87, 0.90), width=0.5)
            self.space(1.5)
        self.space(7)


# ---------------- CAPA ----------------
cover = doc.new_page(width=A4W, height=A4H)
cover.draw_rect(pymupdf.Rect(0, 0, A4W, 6), color=BLUE, fill=BLUE)
lw = 92
lh = lw / 0.56
cover.insert_image(pymupdf.Rect((A4W - lw) / 2, 76, (A4W + lw) / 2, 76 + lh),
                   filename=LOGOS + r"\UFS_crest.png")
y = 76 + lh + 32
for line, size, font in (
    ("UNIVERSIDADE FEDERAL DE SERGIPE", 12, FB),
    ("CENTRO DE CIÊNCIAS EXATAS E TECNOLOGIA", 10.5, F),
    ("PROGRAMA DE PÓS-GRADUAÇÃO EM CIÊNCIA DA COMPUTAÇÃO", 10.5, F),
):
    put(cover, (A4W - span_w(line, font, size)) / 2, y, line, font, size,
        NAVY if font == FB else DARK)
    y += size + 6
cover.draw_line(pymupdf.Point(ML + 70, y + 24), pymupdf.Point(A4W - MR - 70, y + 24),
                color=BLUE, width=1.2)
y += 78
put(cover, (A4W - span_w("Meta Experimental", FB, 26)) / 2, y, "Meta Experimental",
    FB, 26, NAVY)
y += 40
for line in ("Mineração de defeitos em relatórios XBRL:",
             "uma análise empírica de padrões de erro em diferentes jurisdições"):
    put(cover, (A4W - span_w(line, FB, 13.5)) / 2, y, line, FB, 13.5, DARK)
    y += 20
y += 46
for line, size, font, color in (
    ("Victor Cesar Santos de Melo", 14, FB, NAVY),
    ("Orientador: Prof. Dr. Fábio Gomes Rocha", 11.5, F, DARK),
    ("", 0, F, DARK),
    ("Disciplina: PROCC0094 — Engenharia de Software Experimental", 10.5, F, GREY),
    ("Professor: Dr. Methanias Colaço Júnior", 10.5, F, GREY),
    ("Turma 01 — 2026.2", 10.5, F, GREY),
):
    if line:
        put(cover, (A4W - span_w(line, font, size)) / 2, y, line, font, size, color)
    y += size + 8
pw, ph = 160, 160 / 2.30
cover.insert_image(pymupdf.Rect((A4W - pw) / 2, A4H - 120 - ph, (A4W + pw) / 2, A4H - 120),
                   filename=LOGOS + r"\procc_logo.png")
for line, size, font, yb in (("São Cristóvão — Sergipe", 10.5, F, A4H - 86),
                             ("2026", 10.5, FB, A4H - 70)):
    put(cover, (A4W - span_w(line, font, size)) / 2, yb, line, font, size, DARK)

# ---------------- CONTEUDO ----------------
src = open(SRC, encoding="utf-8").read().split("\n")
D = Doc()
i = 0
while i < len(src):
    s = src[i].strip()
    if not s:
        i += 1
        continue
    if set(s) <= {"-"} and len(s) >= 3:
        D.rule(); i += 1; continue
    m = re.match(r"^(#{1,4})\s+(.*)$", s)
    if m:
        D.heading(m.group(2), len(m.group(1))); i += 1; continue
    if s.startswith("|"):
        block = []
        while i < len(src) and src[i].strip().startswith("|"):
            cells = [c.strip() for c in src[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                block.append(cells)
            i += 1
        if len(block) >= 2:
            D.table(block)
        continue
    if s.startswith(">"):
        while i < len(src) and src[i].strip().startswith(">"):
            b = src[i].strip().lstrip(">").strip()
            if b:
                D.para(b, quote=True)
            i += 1
        continue
    mb = re.match(r"^([-*]|\d+\.)\s+(.*)$", s)
    if mb:
        D.para(mb.group(2), indent=8, bullet="•" if mb.group(1) in "-*" else mb.group(1))
        i += 1
        continue
    D.para(s)
    i += 1

doc.set_metadata({
    "title": "Meta Experimental — Mineração de defeitos em relatórios XBRL",
    "author": "Victor Cesar Santos de Melo",
    "subject": "PROCC0094 — Engenharia de Software Experimental",
})
for _p in doc:
    flush_page(_p)
doc.save(OUT, deflate=True, garbage=3)
print("SALVO:", OUT, "| paginas:", doc.page_count, "| build:", BUILD)
