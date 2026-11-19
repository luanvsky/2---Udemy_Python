from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# Page setup for 2 pages max - narrow margins
for section in doc.sections:
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

# Style configuration
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(11)
style.paragraph_format.space_after = Pt(3)
style.paragraph_format.line_spacing = 1.15

for level in [1, 2]:
    h_style = doc.styles[f'Heading {level}']
    h_style.font.name = 'Times New Roman'
    h_style.font.color.rgb = RGBColor(0, 0, 0)
    if level == 1:
        h_style.font.size = Pt(12)
        h_style.font.bold = True
        h_style.paragraph_format.space_before = Pt(6)
        h_style.paragraph_format.space_after = Pt(3)
    else:
        h_style.font.size = Pt(11)
        h_style.font.bold = True
        h_style.paragraph_format.space_before = Pt(4)
        h_style.paragraph_format.space_after = Pt(2)

# Reduce list spacing
for list_style in ['List Bullet', 'List Number']:
    ls = doc.styles[list_style]
    ls.paragraph_format.space_after = Pt(1)
    ls.paragraph_format.line_spacing = 1.1

# ==================== TITLE ====================
title = doc.add_heading('FICHAMENTO', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.runs[0].font.size = Pt(14)
title.runs[0].font.name = 'Times New Roman'
title.paragraph_format.space_after = Pt(6)

# ==================== REFERÊNCIA ====================
doc.add_heading('Referência', level=1)
doc.add_paragraph(
    "ASMARE, B. A. M.; KHOMH, F.; NAFI, K. W.; ANTONIOL, G. "
    "Data Access Performance Anti-patterns in Data-Intensive Systems. "
    "arXiv:2208.08918v1 [cs.SE], 2022."
)

# ==================== OBJETIVOS ====================
doc.add_heading('Objetivos', level=1)
for i, obj in enumerate([
    "Identificar e categorizar anti-padrões de desempenho no acesso a dados em DIS baseados em NoSQL/poliglota.",
    "Validar relevância e criticidade com desenvolvedores industriais.",
    "Preencher lacuna da literatura focada apenas em bancos relacionais/SQL (Shao et al., 2021)."
], 1):
    doc.add_paragraph(f"{i}. {obj}", style='List Number').paragraph_format.space_after = Pt(1)

# ==================== METODOLOGIA ====================
doc.add_heading('Metodologia', level=1)
doc.add_paragraph(
    "Estudo qualitativo empírico em três etapas: (1) Mineração de 162 repositórios Java (75 NoSQL + 87 poliglotas) → 141 issues; "
    "(2) Codificação indutiva (Grounded Theory) → 14 anti-padrões, 7 categorias, saturação em 250 instâncias, κ=0,764; "
    "(3) Survey com 53 desenvolvedores industriais (6,8 anos exp.) validando relevância e criticidade."
)

# ==================== RESULTADOS ====================
doc.add_heading('Principais Resultados', level=1)

# Table
table = doc.add_table(rows=8, cols=2)
table.style = 'Table Grid'
table.autofit = True
hdr = table.rows[0]
hdr.cells[0].text = 'Categoria'
hdr.cells[1].text = 'Anti-padrões'
for cell in hdr.cells:
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: r.bold = True; r.font.size = Pt(9)

data = [
    ('1. Data Retrieval', 'Multiple Key Sequential Search'),
    ('2. Query', 'Inefficient Query Translation'),
    ('3. Connection (3)', 'Duplicate Requests; Synchronous Connection; Single Connection'),
    ('4. Driver/API (3)', 'Inefficient Driver/API; Misconfiguration; Wrong API Function'),
    ('5. Cache (3)', 'Invalidation vs Update; Inefficient Logic; Not Caching Query'),
    ('6. Indexing', 'Non-optimized Indexing Logic'),
    ('7. Node Mgmt (2)', 'Inadequate Node Failure Handling; Load Imbalance'),
]
for i, (cat, ap) in enumerate(data, 1):
    row = table.rows[i]
    row.cells[0].text = cat
    row.cells[1].text = ap
    for cell in row.cells:
        for p in cell.paragraphs:
            for r in p.runs: r.font.size = Pt(9)

doc.add_paragraph("")
for s in [
    "Top 3 críticos: Node Failure Handling, Synchronous Connection, Inefficient Driver/API.",
    "Mais prevalente: Inefficient Driver/API (15,6%). Cache+Connection+Driver = 64% dos 141 issues.",
    "73,4% issues em NoSQL puro; 26,6% poliglota."
]:
    doc.add_paragraph(s, style='List Bullet').paragraph_format.space_after = Pt(1)

# ==================== GAPS ====================
doc.add_heading('Gaps / Oportunidades', level=1)
for i, (gap, extensao) in enumerate([
    ("Sem física de I/O", "Aula 02: bandwidth, WAF, compaction, backpressure"),
    ("Sem tempo distribuído", "Aula 03: clock drift/PPM, LWW, monotonic, watermarks"),
    ("Sem governança/conformidade", "Gov Federal: Matriz 5 riscos (TCU, LAI, LRF, ISO, SIEM)"),
    ("Só devs validaram", "DBAs, SREs, Arquitetos, Auditores TI"),
    ("Só Java/open-source", "Generalização + sistemas legados gov"),
    ("Tradução automática", "Consultar original em inglês")
], 1):
    p = doc.add_paragraph(style='List Number')
    run = p.add_run(f"{gap}: ")
    run.bold = True
    p.add_run(extensao).font.size = Pt(11)
    p.paragraph_format.space_after = Pt(1)

# ==================== CONCLUSÕES ====================
doc.add_heading('Conclusões', level=1)
for c in [
    "Anti-padrões de desempenho em NoSQL/poliglota são críticos e subinvestigados vs. relacionais.",
    "Driver/API e Cache concentram prevalência e criticidade — decisões de infraestrutura > tuning de query.",
    "Falhas de infraestrutura (node failure, connection) superam problemas de código em criticidade.",
    "Taxonomia empírica sólida (saturação 250, κ=0,764, n=53) base para detecção automática e extensão teórica."
]:
    doc.add_paragraph(c, style='List Bullet').paragraph_format.space_after = Pt(1)

# ==================== CONCEITOS-CHAVE ====================
doc.add_heading('Conceitos-chave (páginas)', level=1)
for cit, pag in [
    ('"Data-intensive systems handle high-volume, high-velocity, heterogeneous data..."', 'p.1'),
    ('"Data access logic… determines overall performance and functionality."', 'p.1'),
    ('"Technical debt… performance-affecting… not sufficiently investigated."', 'p.1'),
    ('"NoSQL databases… horizontal scalability and handling of heterogeneous data."', 'p.2'),
    ('"We use inductive coding… saturation reached after 250 instances."', 'p.3'),
    ('"Cohen\'s Kappa = 0.764, indicating substantial agreement."', 'p.3'),
    ('"Top 3 critical: Node Failure, Sync Connection, Inefficient Driver/API."', 'p.6'),
    ('"Inefficient Driver/API most prevalent (15.6%)."', 'p.6'),
    ('"Cache-related anti-patterns each at 10.64%."', 'p.6'),
]:
    p = doc.add_paragraph(f'{cit} ({pag})', style='List Bullet')
    p.paragraph_format.space_after = Pt(0)

# ==================== FONTES ====================
doc.add_heading('Fontes Principais', level=1)
for f in [
    "SHAO et al. ICSE 2021; DEAN, Google 2010; KLEPPMANN, O'Reilly 2017; "
    "LAMPORT, CACM 1978; CORBETT et al. OSDI 2012; ALVES et al. JSS 2016; "
    "FRERY 2014; VOLPATO 2007."
]:
    doc.add_paragraph(f, style='List Bullet').paragraph_format.space_after = Pt(0)

# ==================== COMENTÁRIO PESSOAL ====================
doc.add_heading('Comentário Pessoal', level=1)
doc.add_paragraph(
    "Base empírica para RQ1. Minha contribuição: estender a taxonomia com 3 lentes das aulas do Prof. Fabio:\n"
    "1) Aula 02 (Física I/O): mapear 14 anti-padrões a causas físicas (bandwidth, WAF, compaction, backpressure).\n"
    "2) Aula 03 (Tempo Distribuído): mapear a causas temporais (clock drift/PPM, LWW, monotonic, watermarks).\n"
    "3) Contexto Gov Federal: Matriz Criticidade (anti-padrão × 5 riscos: Fechamento/LRF, LAI, Integridade/TCU, ISO 38500, SIEM) "
    "validada com 2–3 especialistas (DBA, Arquiteto, Auditor TI) + Checklist Governança com SLIs/SLOs por anti-padrão.\n"
    "Próximos passos: entrevistas p/ Matriz, Tabela Mapeamento 14×(Física+Tempo), escrita IMRAD (8 sem.)."
).paragraph_format.space_after = Pt(0)

# Save
output_path = r'D:\dsh-vsky\Fichamento_Asmare_2paginas.docx'
doc.save(output_path)
print(f'Saved to {output_path}')