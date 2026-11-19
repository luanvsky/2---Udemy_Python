import pymupdf, html, base64, os
from PIL import Image

W, H = 960, 540
NAVY, BLUE, RED, GREY, DARK = "#12294a", "#1f6feb", "#c0392b", "#7a8699", "#1b1f27"
FONT = "Segoe UI,Arial,Helvetica"
LOGOS = r"D:\dsh-vsky\_logos"


def _b64(name):
    with open(os.path.join(LOGOS, name), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def _ratio(name):
    im = Image.open(os.path.join(LOGOS, name))
    return im.size[0] / im.size[1]


UFS_MARK = _b64("UFS_crest.png")          # brasão UFS (ratio ~0.56)
PROCC_MARK = _b64("procc_logo.png")       # PROCC (ratio ~2.30)

R_UFS = _ratio("UFS_crest.png")
R_PROCC = _ratio("procc_logo.png")


def esc(s):
    return html.escape(s)


def img_tag(uri, x, y, width, ratio):
    """Image at top-left (x, y) with given width, height from aspect ratio."""
    return (
        f'<image x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{width / ratio:.1f}" '
        f'xlink:href="{uri}" href="{uri}" preserveAspectRatio="xMidYMid meet"/>'
    )


def slide(title, lines, footer, tag=None):
    is_title = tag is None
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<rect x="0" y="0" width="{W}" height="8" fill="{BLUE}"/>',
    ]

    if is_title:
        # title slide: UFS crest top-right, PROCC mark centred at the bottom
        out.append(img_tag(UFS_MARK, W - 60 - 88, 40, 88, R_UFS))
        out.append(img_tag(PROCC_MARK, (W - 200) / 2, 418, 200, R_PROCC))

    y = 120 if is_title else 74
    if tag:
        out.append(
            f'<text x="60" y="{y}" font-family="{FONT}" font-size="17" font-weight="700" '
            f'fill="{BLUE}" letter-spacing="1.2">{esc(tag)}</text>'
        )
        y += 40
        # institutional mark top-right on every content slide
        out.append(img_tag(UFS_MARK, W - 60 - 58, 38, 58, R_UFS))
    out.append(
        f'<text x="60" y="{y}" font-family="{FONT}" font-size="38" font-weight="700" '
        f'fill="{NAVY}">{esc(title)}</text>'
    )
    y += 30
    # title slide stops its rule before the crest so nothing overlaps
    rule_x1 = 792 if is_title else (W - 60)
    out.append(f'<line x1="60" y1="{y}" x2="{rule_x1}" y2="{y}" stroke="{BLUE}" stroke-width="2.5"/>')
    y += 56

    if is_title:
        # title slide: text block centred under the rule
        y = 268
        for text, style in lines:
            if not text.strip():
                y += 12
                continue
            is_author = style == "k"
            size = 30 if is_author else (23 if style == "g" else 25)
            weight = "700" if is_author else "400"
            color = NAVY if is_author else (GREY if style == "g" else DARK)
            out.append(
                f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="{FONT}" '
                f'font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>'
            )
            y += size + 20
        out.append("</svg>")
        return "".join(out)

    for text, style in lines:
        # blank line = small spacer, not a full line height
        if not text.strip():
            y += 16
            continue
        color, size, weight = DARK, 27, "400"
        if style == "k":
            color, size, weight = NAVY, 33, "700"
        elif style == "b":
            color, size, weight = BLUE, 29, "700"
        elif style == "r":
            color, size, weight = RED, 27, "700"
        elif style == "g":
            color, size, weight = GREY, 22, "400"
        elif style == "s":
            color, size, weight = DARK, 23, "400"
        elif style == "m":
            color, size, weight = NAVY, 28, "700"
        elif style == "n":
            color, size, weight = RED, 25, "700"
        elif style == "t":
            color, size, weight = NAVY, 27, "700"
        elif style == "q":
            color, size, weight = NAVY, 22, "700"
        out.append(
            f'<text x="60" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}">{esc(text)}</text>'
        )
        y += size + 19

    out.append(
        f'<text x="60" y="{H - 30}" font-family="{FONT}" font-size="16" '
        f'fill="{GREY}">{esc(footer)}</text>'
    )
    out.append("</svg>")
    return "".join(out)


PROGRESS = [f"{i} / 8" for i in range(1, 9)]
_p = iter(PROGRESS)

SLIDES = [
    dict(
        tag=None,
        footer="",
        title="Mineração de defeitos em relatórios XBRL",
        lines=[
            ("Uma análise empírica em diferentes jurisdições", "g"),
            ("", "s"),
            ("Victor Cesar Santos de Melo", "k"),
            ("Orientador: Prof. Fábio Gomes Rocha", ""),
            ("Engenharia de Software Experimental — 2026.2", "g"),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="O problema",
        lines=[
            ("XBRL = padrão global de relatório financeiro", "k"),
            ("legível por máquina", "k"),
            ("", "s"),
            ("Governos, reguladores e empresas publicam assim", ""),
            ("Mas: erros de validação são frequentes", "r"),
            ("→ afetam qualidade, comparabilidade e transparência", ""),
            ("", "s"),
            ("Bases públicas: SEC · ESMA · Companies House", "g"),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="A pergunta",
        lines=[
            ("É possível medir defeito de validação XBRL de forma...", "m"),
            ("", "s"),
            ("estável?     ·     classificável?     ·     reprodutível?", "b"),
            ("", "s"),
            ("E o perfil de defeito varia entre jurisdições?", "k"),
            ("", "s"),
            ("Primeiro: DÁ PARA MEDIR?   Depois: o que a medição mostra?", "g"),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="Objeto e finalidade",
        lines=[
            ("OBJETO: o artefato de software — a instância XBRL", "k"),
            ("FINALIDADE: caracterizar  (depois, comparar)", "b"),
            ("PERSPECTIVA: Engenharia de Software Experimental", ""),
            ("AMBIENTE: bases públicas, medição local", ""),
            ("", "s"),
            ("Não avalio a empresa. Não avalio o número contábil.", "r"),
            ("Avalio conformidade com a especificação.", ""),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="O instrumento: Arelle",
        lines=[
            ("Processador XBRL certificado pela XBRL International", "m"),
            ("Já traz os conjuntos de regras de cada jurisdição:", ""),
            ("SEC  efm      ·      UE  esef      ·      Reino Unido  hmrc", "b"),
            ("", "s"),
            ("1.  A mesma ferramenta mede todas as jurisdições", ""),
            ("2.  Não dependo do regulador publicar nada", ""),
            ("3.  Qualquer pessoa reproduz o resultado", ""),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="O que eu meço",
        lines=[
            ("Dimensão A — CLASSE  (o que a regra verifica)", "k"),
            ("estrutural · tipo · cálculo · fórmula · dimensional · extensão", "s"),
            ("", "s"),
            ("Dimensão B — CAUSA-RAIZ  (por que falhou)", "k"),
            ("mapeamento · dado ausente · extensão indevida", "s"),
            ("Causa-raiz NÃO é observável na saída do validador", "r"),
            ("", "s"),
            ("Medida principal: defeitos POR FATO (não por arquivo)", "b"),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="Como eu valido",
        lines=[
            ("1.  Determinismo — rodar 2x e comparar", "k"),
            ("2.  Concordância — 2 codificadores, kappa de Cohen", "k"),
            ("3.  Triangulação — mesma taxonomia, várias jurisdições", "t"),
            ("4.  Reprodutibilidade — scripts e versões públicos", "k"),
            ("", "s"),
            ("Piloto: 6 fases, critério de decisão declarado ANTES", "b"),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="O que me derruba",
        lines=[
            ("Eu só vejo o que passou pelo filtro.", "r"),
            ("Instância publicada já foi aceita pelo regulador", ""),
            ("→ meço conformidade RESIDUAL, não qualidade dos relatórios", ""),
            ("", "s"),
            ("Jurisdição ≠ qualidade — conjuntos de regras diferentes", "r"),
            ("", "s"),
            ("Estudo OBSERVACIONAL — não é experimento controlado", "b"),
        ],
    ),
    dict(
        tag=next(_p),
        footer="",
        title="Escopo",
        lines=[
            ("NO ARTIGO", "b"),
            ("1 pergunta · SEC · 1 trimestre · classe de defeito", ""),
            ("", "s"),
            ("TRABALHO FUTURO", "b"),
            ("outras jurisdições · série histórica · causa-raiz · classificador", ""),
            ("", "s"),
            ("Uma pergunta bem respondida vale mais que quatro mal respondidas.", "q"),
        ],
    ),
]

doc = pymupdf.open()
for s in SLIDES:
    svg = slide(s["title"], s["lines"], s["footer"], s["tag"])
    d = pymupdf.open("svg", svg.encode("utf-8"))
    pdfbytes = d.convert_to_pdf()
    d.close()
    src = pymupdf.open("pdf", pdfbytes)
    doc.insert_pdf(src)
    src.close()

doc.set_metadata(
    {
        "title": "Mineração de defeitos em relatórios XBRL — Apresentação 5 min",
        "author": "Victor Cesar Santos de Melo",
        "subject": "Engenharia de Software Experimental — PROCC0094",
    }
)
out = r"D:\dsh-vsky\Slides_XBRL_5min.pdf"
doc.save(out, deflate=True)
print("OK:", out, "| paginas:", doc.page_count)
