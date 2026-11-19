from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color scheme
DARK_BLUE = RGBColor(0x1B, 0x2A, 0x4A)
MEDIUM_BLUE = RGBColor(0x2E, 0x86, 0xC1)
LIGHT_BLUE = RGBColor(0xD6, 0xEA, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
ACCENT_GREEN = RGBColor(0x27, 0xAE, 0x60)
ACCENT_RED = RGBColor(0xE7, 0x4C, 0x3C)
ACCENT_ORANGE = RGBColor(0xF3, 0x9C, 0x12)

def add_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text_box(slide, left, top, width, height, text, font_size=18, bold=False, color=DARK_GRAY, alignment=PP_ALIGN.LEFT, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_bullet_list(slide, left, top, width, height, items, font_size=16, color=DARK_GRAY, bold_first=False, spacing=Pt(6)):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = 'Calibri'
        p.space_after = spacing
        if bold_first and i == 0:
            p.font.bold = True
    return txBox

def add_shape_bg(slide, left, top, width, height, color, transparency=0):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

# ============================================================
# SLIDE 1 — TÍTULO
# ============================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
add_background(slide1, DARK_BLUE)

# Accent line
add_shape_bg(slide1, 0, 2.8, 13.333, 0.08, ACCENT_GREEN)

add_text_box(slide1, 1, 1.0, 11.333, 1.5,
    'Anti-padrões de Desempenho em Acesso a Dados\nem Sistemas Intensivos em Dados (NoSQL/Poliglota)',
    font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

add_text_box(slide1, 1, 2.9, 11.333, 0.8,
    'Fichamento: Asmare et al. (2022) — arXiv:2208.08918v1',
    font_size=22, color=LIGHT_BLUE, alignment=PP_ALIGN.CENTER)

add_text_box(slide1, 1, 3.8, 11.333, 0.5,
    'Disciplina: Tópicos Avançados em Eng. Software e SI — PROCC/UFS',
    font_size=18, color=RGBColor(0xBB, 0xCC, 0xDD), alignment=PP_ALIGN.CENTER)

add_text_box(slide1, 1, 4.4, 11.333, 0.5,
    'Aluno: Victor Cesar Santos de Melo  |  Orientador: Prof. Dr. Fabio Gomes Rocha',
    font_size=16, color=RGBColor(0x99, 0xAA, 0xBB), alignment=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 2 — PROBLEMA & LACUNA
# ============================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide2, WHITE)
add_shape_bg(slide2, 0, 0, 13.333, 1.1, DARK_BLUE)
add_text_box(slide2, 0.5, 0.15, 12, 0.8, 'PROBLEMA & LACUNA', font_size=32, bold=True, color=WHITE, alignment=PP_ALIGN.LEFT)

# Left column - Problema
add_shape_bg(slide2, 0.5, 1.5, 5.8, 5.0, LIGHT_BLUE)
add_text_box(slide2, 0.8, 1.6, 5.2, 0.5, 'PROBLEMA', font_size=22, bold=True, color=DARK_BLUE)
add_bullet_list(slide2, 0.8, 2.2, 5.2, 4.0, [
    'Sistemas intensivos em dados (DIS) usam NoSQL + persistência poliglota',
    'Dívida técnica de acesso a dados afeta latência, throughput, disponibilidade',
    'Literatura anterior (Shao et al., 2021) cobre APENAS bancos relacionais/SQL',
    'Nenhuma taxonomia validada de anti-padrões de DESEMPENHO para NoSQL/poliglota',
    'Falta de validação com profissionais da indústria'
], font_size=17, color=DARK_GRAY)

# Right column - Lacuna
add_shape_bg(slide2, 6.8, 1.5, 5.8, 5.0, RGBColor(0xFD, 0xF2, 0xE9))
add_text_box(slide2, 7.1, 1.6, 5.2, 0.5, 'LACUNA', font_size=22, bold=True, color=ACCENT_ORANGE)
add_bullet_list(slide2, 7.1, 2.2, 5.2, 4.0, [
    '❌ Zero taxonomia de anti-padrões de desempenho para NoSQL/poliglota',
    '❌ Sem conexão com limites físicos de hardware (I/O, CPU, rede)',
    '❌ Ignora sincronização temporal distribuída (clock drift, LWW, watermarks)',
    '❌ Não mapeia riscos de conformidade (TCU, LAI, CVM, ISO 38500)',
    '❌ Validação apenas com devs — sem DBAs, SREs, auditores'
], font_size=17, color=DARK_GRAY)

# ============================================================
# SLIDE 3 — MÉTODO
# ============================================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide3, WHITE)
add_shape_bg(slide3, 0, 0, 13.333, 1.1, DARK_BLUE)
add_text_box(slide3, 0.5, 0.15, 12, 0.8, 'MÉTODO — Rigor Qualitativo em 3 Etapas', font_size=32, bold=True, color=WHITE)

# Three columns
steps = [
    ('1️⃣ MINERAÇÃO', MEDIUM_BLUE, [
        '162 repositórios Java open-source',
        '75 NoSQL puros + 87 poliglotas',
        '141 issues de desempenho confirmados',
        'Projetos reais, não sintéticos'
    ]),
    ('2️⃣ CODIFICAÇÃO INDUTIVA', ACCENT_GREEN, [
        'Open, axial, selective coding',
        '14 anti-padrões → 7 categorias',
        'Saturação: 250 instâncias rotuladas',
        'Kappa de Cohen = 0,764 (substancial)'
    ]),
    ('3️⃣ SURVEY VALIDAÇÃO', ACCENT_ORANGE, [
        '53 desenvolvedores industriais',
        'Experiência média: 6,8 anos',
        'Avaliaram relevância + criticidade',
        'Sugestões de novos anti-padrões'
    ])
]

for i, (title, color, items) in enumerate(steps):
    left = 0.5 + i * 4.2
    add_shape_bg(slide3, left, 1.4, 3.8, 0.7, color)
    add_text_box(slide3, left + 0.1, 1.45, 3.6, 0.6, title, font_size=20, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
    add_shape_bg(slide3, left, 2.2, 3.8, 4.2, LIGHT_GRAY)
    add_bullet_list(slide3, left + 0.2, 2.3, 3.4, 3.8, items, font_size=16, color=DARK_GRAY)

# ============================================================
# SLIDE 4 — TAXONOMIA
# ============================================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide4, WHITE)
add_shape_bg(slide4, 0, 0, 13.333, 1.1, DARK_BLUE)
add_text_box(slide4, 0.5, 0.15, 12, 0.8, 'TAXONOMIA — 7 Categorias, 14 Anti-padrões', font_size=32, bold=True, color=WHITE)

# Table
rows, cols = 8, 2
table_shape = slide4.shapes.add_table(rows, cols, Inches(0.5), Inches(1.4), Inches(12.3), Inches(5.5))
table = table_shape.table

# Style table
table.columns[0].width = Inches(4.5)
table.columns[1].width = Inches(7.8)

headers = ['Categoria', 'Anti-padrões']
data = [
    ('1. Data Retrieval & Update', 'Multiple Key Sequential Search'),
    ('2. Query', 'Inefficient Query Translation'),
    ('3. Database Connection (3)', 'Duplicate Requests\nSynchronous Connection Usage\nSingle Connection for Data Access'),
    ('4. Driver / Data Access API (3)', 'Inefficient Driver/API ⭐\nMisconfiguration\nWrong API Function'),
    ('5. Cache (3)', 'Cache Invalidation vs. Update\nInefficient Cache Logic\nNot Caching the Query'),
    ('6. Indexing', 'Non-optimized Indexing Logic'),
    ('7. Node Config & Mgmt (2)', 'Inadequate Node Failure Handling ⭐\nLoad Imbalance Across Multiple Nodes'),
]

for j, h in enumerate(headers):
    cell = table.cell(0, j)
    cell.text = h
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.size = Pt(14)
        paragraph.font.bold = True
        paragraph.font.color.rgb = WHITE
        paragraph.alignment = PP_ALIGN.CENTER
    cell.fill.solid()
    cell.fill.fore_color.rgb = DARK_BLUE

for i, (cat, ap) in enumerate(data, 1):
    table.cell(i, 0).text = cat
    table.cell(i, 1).text = ap
    for j in range(2):
        cell = table.cell(i, j)
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(13)
            paragraph.font.color.rgb = DARK_GRAY
        if i % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_GRAY

# Legend
add_text_box(slide4, 0.5, 7.0, 12, 0.4, '⭐ = Top 3 mais críticos', font_size=14, bold=True, color=ACCENT_RED)

# ============================================================
# SLIDE 5 — TOP 3 CRÍTICOS + PREVALENTE
# ============================================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide5, WHITE)
add_shape_bg(slide5, 0, 0, 13.333, 1.1, DARK_BLUE)
add_text_box(slide5, 0.5, 0.15, 12, 0.8, 'RESULTADOS-CHAVE — Críticos vs. Prevalentes', font_size=32, bold=True, color=WHITE)

# Left - Top 3 Críticos
add_shape_bg(slide5, 0.5, 1.5, 5.8, 5.0, RGBColor(0xFD, 0xED, 0xED))
add_text_box(slide5, 0.8, 1.6, 5.2, 0.5, '🏆 TOP 3 MAIS CRÍTICOS (Survey n=53)', font_size=20, bold=True, color=ACCENT_RED)

criticos = [
    '1. Inadequate Node Failure Handling',
    '    Falha de nó não detectada → requisições roteadas para nó "zumbi"',
    '    Split brain, erro em cascata, indisponibilidade silenciosa',
    '',
    '2. Synchronous Connection Usage',
    '    Thread blocking esperando I/O → pool exhaustion',
    '    Timeouts espúrios por wall-clock + clock drift',
    '',
    '3. Inefficient Driver/API',
    '    Path length alto, buffer management ruim, sem async I/O',
    '    Afeta TODOS os sistemas que usam o driver'
]
add_bullet_list(slide5, 0.8, 2.2, 5.2, 4.0, criticos, font_size=16, color=DARK_GRAY, spacing=Pt(4))

# Right - Prevalência
add_shape_bg(slide5, 6.8, 1.5, 5.8, 5.0, RGBColor(0xE8, 0xF8, 0xF5))
add_text_box(slide5, 7.1, 1.6, 5.2, 0.5, '📊 PREVALÊNCIA (141 issues)', font_size=20, bold=True, color=ACCENT_GREEN)

preval = [
    '🥇 Inefficient Driver/API → 15,6%',
    '',
    '🥈 Empatados em 10,64% cada:',
    '   • Inefficient Cache Logic',
    '   • Not Caching the Query',
    '   • Inefficient Query Translation',
    '',
    '📈 73,4% issues → sistemas NoSQL puros',
    '📈 26,6% issues → sistemas poliglotas',
    '',
    '💡 Cache + Driver + Connection = 60%+ dos problemas'
]
add_bullet_list(slide5, 7.1, 2.2, 5.2, 4.0, preval, font_size=16, color=DARK_GRAY, spacing=Pt(4))

# ============================================================
# SLIDE 6 — GAPS QUE MINHA PESQUISA ATACA
# ============================================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide6, WHITE)
add_shape_bg(slide6, 0, 0, 13.333, 1.1, DARK_BLUE)
add_text_box(slide6, 0.5, 0.15, 12, 0.8, 'GAPS DO ARTIGO BASE → MINHA EXTENSÃO (Aulas 02 + 03)', font_size=30, bold=True, color=WHITE)

gaps = [
    ('LIMITE DO ARTIGO BASE', 'MINHA EXTENSÃO', DARK_BLUE),
    ('❌ Sem física de I/O', '✅ Disk bandwidth, WAF, compaction pauses, backpressure', ACCENT_GREEN),
    ('❌ Sem tempo distribuído', '✅ Clock drift (PPM), LWW loss, monotonic clocks, watermarks', MEDIUM_BLUE),
    ('❌ Sem governança/conformidade', '✅ Matriz: Anti-padrão × TCU/LAI/CVM/ISO 38500', ACCENT_ORANGE),
    ('❌ Só devs validaram', '✅ DBAs, SREs, Arquitetos, Auditores TI', RGBColor(0x8E, 0x44, 0xAD)),
    ('❌ Amostra só Java', '✅ Generalização + validação em contexto setor público', RGBColor(0x2C, 0x3E, 0x50)),
]

# Table for gaps
rows, cols = len(gaps), 3
table_shape = slide6.shapes.add_table(rows, cols, Inches(0.5), Inches(1.4), Inches(12.3), Inches(5.5))
table = table_shape.table
table.columns[0].width = Inches(4.0)
table.columns[1].width = Inches(7.0)
table.columns[2].width = Inches(1.3)

for i, (gap, ext, color) in enumerate(gaps):
    table.cell(i, 0).text = gap
    table.cell(i, 1).text = ext
    table.cell(i, 2).text = '→'
    for j in range(3):
        cell = table.cell(i, j)
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(15)
            paragraph.font.color.rgb = DARK_GRAY if j < 2 else color
            if j == 1:
                paragraph.font.bold = True
                paragraph.font.color.rgb = color
        if i == 0:
            paragraph.font.bold = True
            paragraph.font.color.rgb = WHITE
            paragraph.font.size = Pt(16)
        if i == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = DARK_BLUE
        elif i % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_GRAY

# ============================================================
# SLIDE 7 — MINHA CONTRIBUIÇÃO PREVISTA
# ============================================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide7, WHITE)
add_shape_bg(slide7, 0, 0, 13.333, 1.1, DARK_BLUE)
add_text_box(slide7, 0.5, 0.15, 12, 0.8, 'MINHA CONTRIBUIÇÃO — Artigo IMRAD da Disciplina', font_size=32, bold=True, color=WHITE)

contribs = [
    ('1', 'Taxonomia Estendida', '14 anti-padrões × Causa Física (Aula 02) + Causa Temporal (Aula 03)\nTabela 3.3 pronta: limites físicos violados + falhas de sincronismo'),
    ('2', 'Matriz de Criticidade Validada', 'Anti-padrão × 5 Riscos: Fechamento Contábil, LAI/Transparência,\nIntegridade Contábil, Auditoria TCU, SIEM\nEntrevistas com 2–3 especialistas do órgão (DBA, Arquiteto, Auditor TI)'),
    ('3', 'Checklist de Governança Operacionalizável', 'Por fase do ciclo de vida: Arquitetura → Dev → Teste → Operação → Auditoria\nCom SLIs/SLOs por anti-padrão (ex.: p99 < 200ms, pool < 70%, clock offset < 10ms)'),
    ('4', 'Validação em Contexto Real', 'Estudo de caso: incidente anonimizado no órgão (SICONFI/SIAFI)\nOu experimento controlado: injetar anti-padrões no Arelle/SICONFI')
]

for i, (num, title, desc) in enumerate(contribs):
    top = 1.4 + i * 1.35
    # Number circle
    circle = slide7.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8), Inches(top), Inches(0.7), Inches(0.7))
    circle.fill.solid()
    circle.fill.fore_color.rgb = MEDIUM_BLUE
    circle.line.fill.background()
    tf = circle.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = num
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].space_before = Pt(0)
    tf.paragraphs[0].space_after = Pt(0)

    add_text_box(slide7, 1.7, top - 0.05, 10.5, 0.5, title, font_size=22, bold=True, color=DARK_BLUE)
    add_text_box(slide7, 1.7, top + 0.45, 10.5, 0.8, desc, font_size=15, color=DARK_GRAY)

# Bottom note
add_shape_bg(slide7, 0.5, 6.2, 12.3, 0.8, LIGHT_BLUE)
add_text_box(slide7, 0.8, 6.3, 11.7, 0.6,
    '📄 Entregáveis da disciplina: Artigo IMRAD completo + Fichamento (modelo do prof.) + Apresentação oral + Peer Review em grupo\n🔮 Futuro: Capítulo de dissertação integrando RS XBRL (outra disciplina) + Artigo DIS + Validação SICONFI/Arelle',
    font_size=14, bold=False, color=DARK_BLUE, alignment=PP_ALIGN.CENTER)

# Save
output_path = r'D:\dsh-vsky\Apresentacao_Fichamento_Asmare.pptx'
prs.save(output_path)
print(f'Saved to {output_path}')