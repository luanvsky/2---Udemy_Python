from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

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
    "Identificar e categorizar anti-padrões de desempenho em sistemas de autoscale cloud baseados em sistemas distribuídos.",
    "Validar relevância e criticidade com engenheiros cloud/SREs via survey e análise de issues reais (GitHub).",
    "Estender a taxonomia de Asmare et al. (2022) para o contexto de autoscale cloud, integrando falhas de prognóstico e sincronização distribuída."
], 1):
    doc.add_paragraph(f"{i}. {obj}", style='List Number').paragraph_format.space_after = Pt(1)

# ==================== METODOLOGIA ====================
doc.add_heading('Metodologia', level=1)
doc.add_paragraph(
    "Estudo empírico misto em três frentes: (1) Extensão da taxonomia Asmare et al. (2022) — 14 anti-padrões, 7 categorias — "
    "para o domínio de autoscale cloud, adicionando dimensões de falhas de prognóstico e sincronização distribuída; "
    "(2) Survey com 25 profissionais (engenheiros cloud, SREs, DBAs cloud) via LinkedIn/IFS, avaliando relevância e criticidade "
    "de anti-padrões em autoscale (Likert 5 pontos + criticidade operacional); "
    "(3) Análise qualitativa de 20 issues reais de autoscale em repositórios open-source (Kubernetes, AWS Autoscaler, "
    "HashiCorp Nomad, etcd, Consul) com codificação indutiva para classificar causas-raiz. "
    "Equipe: Victor (liderança, escrita, fundamentação teórica), Alisson (prognósticos, survey cloud, issues AWS/K8s), "
    "Erik (sistemas distribuídos, issues clock drift/partições etcd/Consul/Raft, survey SREs)."
)

# ==================== RESULTADOS ESPERADOS ====================
doc.add_heading('Resultados Esperados', level=1)

# Table
table = doc.add_table(rows=8, cols=2)
table.style = 'Table Grid'
table.autofit = True
hdr = table.rows[0]
hdr.cells[0].text = 'Categoria (Estendida)'
hdr.cells[1].text = 'Anti-padrões (Exemplos)'
for cell in hdr.cells:
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs: r.bold = True; r.font.size = Pt(9)

data = [
    ('1. Falhas de Prognóstico (Novo)', 'Predição Inacurada de Carga; Reação Tardia; Over/Under-provisioning'),
    ('2. Falhas de Sincronização (Novo)', 'Clock Drift em Decisão; Partição de Rede Silenciosa; Consenso Falho'),
    ('3. Connection (3)', 'Duplicate Requests; Synchronous Decision; Single Decision Point'),
    ('4. Driver/API (3)', 'Inefficient Cloud SDK; Misconfiguration Autoscaler; Wrong API Function'),
    ('5. Cache/Estado (3)', 'Stale Metrics Cache; Invalidation vs Update; Not Caching Decision'),
    ('5. Indexing/Metadados', 'Non-optimized Metrics Indexing'),
    ('7. Node/Cluster Mgmt (2)', 'Inadequate Node Failure Handling; Load Imbalance Across AZs'),
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
    "Taxonomia estendida: 7 categorias (2 novas: Prognóstico + Sincronização) → ~18 anti-padrões.",
    "Artefatos: Taxonomia estendida + Checklist mitigação (anti-padrão × SLI alvo) + Survey dataset.",
    "Validação: Survey 25 profissionais + 20 issues reais classificados."
]:
    doc.add_paragraph(s, style='List Bullet').paragraph_format.space_after = Pt(1)

# ==================== GAPS ====================
doc.add_heading('Gaps / Oportunidades', level=1)
for i, (gap, extensao) in enumerate([
    ("Literatura de anti-padrões foca em acesso a dados genérico", "Estender para autoscale cloud + prognósticos + sincronização"),
    ("Taxonomia Asmare não cobre falhas de prognóstico", "Nova categoria: Falhas de Prognóstico (predição, latência, over/under)"),
    ("Clock drift/partições tratados isoladamente", "Integrar sincronização distribuída como causa-raiz de decisões ruins"),
    ("Governança cloud ausente em anti-padrões", "Checklist mitigação com SLIs/SLOs por anti-padrão (p99, drift <10ms, etc.)"),
    ("Validação só com devs", "Survey com SREs, DBAs cloud, engenheiros plataforma + issues reais"),
    ("Generalização Java apenas", "Issues multi-linguagem (Go, Rust, Python) + cloud-managed services")
], 1):
    p = doc.add_paragraph(style='List Number')
    run = p.add_run(f"{gap}: ")
    run.bold = True
    p.add_run(extensao).font.size = Pt(11)
    p.paragraph_format.space_after = Pt(1)

# ==================== CONCLUSÕES ESPERADAS ====================
doc.add_heading('Conclusões Esperadas', level=1)
for c in [
    "Anti-padrões em autoscale cloud são críticos e subinvestigados — lacuna entre literatura de anti-padrões (dados) e prática cloud (prognósticos/distribuídos).",
    "Duas novas categorias (Prognóstico + Sincronização) explicam a maioria dos incidentes graves de autoscale em produção.",
    "Checklist operacionalizável (SLIs/SLOs por anti-padrão) permite mitigação imediata por equipes cloud/platform.",
    "Base empírica sólida (survey n=25 + 20 issues reais) para ferramentas de detecção automática em pipelines CI/CD e observabilidade."
]:
    doc.add_paragraph(c, style='List Bullet').paragraph_format.space_after = Pt(1)

# ==================== CONCEITOS-CHAVE ====================
doc.add_heading('Conceitos-chave (páginas)', level=1)
for cit, pag in [
    ('"Data-intensive systems handle high-volume, high-velocity, heterogeneous data..."', 'Asmare p.1'),
    ('"Technical debt… performance-affecting… not sufficiently investigated."', 'Asmare p.1'),
    ('"Cohen\'s Kappa = 0.764, indicating substantial agreement."', 'Asmare p.3'),
    ('"Top 3 critical: Node Failure, Sync Connection, Inefficient Driver/API."', 'Asmare p.6'),
    ('"Autoscaling decisions depend on accurate load prediction and timely reaction."', 'Mao et al., 2019'),
    ('"Clock drift in distributed systems causes inconsistent state and erroneous decisions."', 'Lamport, 1978'),
    ('"Prognostic failures in autoscaling lead to over/under-provisioning cascades."', 'Gandhi et al., 2014'),
    ('"Observability gaps in distributed systems mask root causes of scaling failures."', 'Sigelman et al., 2010'),
]:
    p = doc.add_paragraph(f'{cit} ({pag})', style='List Bullet')
    p.paragraph_format.space_after = Pt(0)

# ==================== FONTES ====================
doc.add_heading('Fontes Principais', level=1)
for f in [
    "ASMARE et al. arXiv 2022; SHAO et al. ICSE 2021; DEAN, Google 2010; KLEPPMANN, O'Reilly 2017; "
    "LAMPORT, CACM 1978; MAO et al., ACM Computing Surveys 2019; GANDHI et al., ICAC 2014; "
    "SIGELMAN et al., Dapper, 2010; FRERY 2014; VOLPATO 2007."
]:
    doc.add_paragraph(f, style='List Bullet').paragraph_format.space_after = Pt(0)

# ==================== COMENTÁRIO PESSOAL ====================
doc.add_heading('Comentário Pessoal', level=1)
doc.add_paragraph(
    "Artigo base (Asmare) dá a taxonomia de anti-padrões de acesso a dados. Minha contribuição no grupo: "
    "estender para **autoscale cloud**, adicionando **duas categorias inéditas** — Falhas de Prognóstico "
    "(predição de carga, latência de reação, over/under-provisioning) e Falhas de Sincronização Distribuída "
    "(clock drift, partições silenciosas, consenso falho) — conectando as especialidades dos três integrantes: "
    "Victor (anti-padrões DIS + escrita), Alisson (prognósticos cloud, survey/cloud issues), Erik (sistemas "
    "distribuídos, clock drift/partições, survey SREs). Metodologia empírica mista (survey 25 profissionais + "
    "20 issues reais GitHub: K8s, AWS, Nomad, etcd, Consul) viável em 2 semanas. Artefatos: Taxonomia estendida "
    "(~18 anti-padrões), Checklist mitigação com SLIs/SLOs, Dataset survey/issues. Submissão IEEE/ACM 8 págs."
).paragraph_format.space_after = Pt(0)

# Save
output_path = r'D:\dsh-vsky\Fichamento_Grupo_Autoscale_2paginas.docx'
doc.save(output_path)
print(f'Saved to {output_path}')