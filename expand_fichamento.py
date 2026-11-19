from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

doc = Document()

# Adjust default style
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.5

# Heading styles
for level in [1, 2]:
    h_style = doc.styles[f'Heading {level}']
    h_style.font.name = 'Times New Roman'
    h_style.font.color.rgb = RGBColor(0, 0, 0)
    if level == 1:
        h_style.font.size = Pt(14)
        h_style.font.bold = True
    else:
        h_style.font.size = Pt(12)
        h_style.font.bold = True

# ==================== TITLE ====================
title = doc.add_heading('FICHAMENTO', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.runs[0].font.size = Pt(16)
title.runs[0].font.name = 'Times New Roman'

doc.add_paragraph('')

# ==================== REFERENCIA ====================
doc.add_heading('Referência bibliográfica completa', level=1)
ref_text = (
    "ASMARE, Biruk Asmare Musa; KHOMH, Foutse; NAFI, Kawser Wazed; "
    "ANTONIOL, Giuliano. Data Access Performance Anti-patterns in Data-Intensive Systems. "
    "arXiv:2208.08918v1 [cs.SE], 18 ago. 2022. Disponível em: "
    "https://arxiv.org/abs/2208.08918."
)
doc.add_paragraph(ref_text)

# ==================== OBJETIVOS ====================
doc.add_heading('Objetivos', level=1)
objetivos = [
    "Identificar e categorizar anti-padrões de desempenho no acesso a dados em sistemas intensivos em dados (DIS) baseados em NoSQL e persistência poliglota.",
    "Validar a relevância e criticidade percebidas desses anti-padrões por desenvolvedores industriais.",
    "Preencher lacuna da literatura que focou apenas em bancos relacionais/SQL (ex.: Shao et al., 2021)."
]
for i, obj in enumerate(objetivos, 1):
    p = doc.add_paragraph(f"{i}. {obj}", style='List Number')
    p.paragraph_format.space_after = Pt(4)

# ==================== METODOLOGIA ====================
doc.add_heading('Metodologia', level=1)
doc.add_paragraph(
    "O estudo adota uma abordagem qualitativa empírica, estruturada em três etapas sequenciais e rigorosas, "
    "seguindo os princípios da Grounded Theory para a construção da taxonomia."
)

metodologia_items = [
    (
        "1. Mineração de Repositórios Open-Source",
        "Foram selecionados 162 projetos Java hospedados no GitHub, divididos em dois grupos: "
        "75 sistemas baseados exclusivamente em bancos NoSQL (MongoDB, Cassandra, Redis, Neo4j, etc.) e "
        "87 sistemas de persistência poliglota (combinação de dois ou mais paradigmas de armazenamento). "
        "A coleta focou em issues de desempenho confirmados, resultando em 141 instâncias analisadas. "
        "A escolha por Java justifica-se pela maturidade do ecossistema e pela disponibilidade de ferramentas "
        "de análise estática para validação complementar."
    ),
    (
        "2. Codificação Indutiva (Grounded Theory)",
        "A análise dos 141 issues seguiu o processo de codificação em três fases: "
        "(a) open coding — identificação inicial de causas-raiz e sintomas; "
        "(b) axial coding — agrupamento em categorias conceituais; "
        "(c) selective coding — refinamento e validação da taxonomia final. "
        "A saturação teórica foi atingida após a rotulagem de 250 instâncias, indicando estabilidade das categorias. "
        "A concordância entre dois avaliadores independentes foi mensurada pelo Kappa de Cohen = 0,764, "
        "classificada como concordância substancial (Landis & Koch, 1977), conferindo confiabilidade ao processo."
    ),
    (
        "3. Survey de Validação com Desenvolvedores Industriais",
        "Um questionário estruturado foi aplicado a 53 desenvolvedores com experiência média de 6,8 anos "
        "em sistemas de uso intensivo de dados. O instrumento avaliou: (a) relevância percebida de cada anti-padrão "
        "(escala Likert 5 pontos); (b) criticidade operacional (baixa, média, alta, crítica); "
        "(c) sugestões de novos anti-padrões não cobertos. A validação externa permitiu confirmar a "
        "generalizabilidade da taxonomia além da amostra de repositórios minerados."
    )
]

for titulo, desc in metodologia_items:
    p = doc.add_paragraph()
    run = p.add_run(titulo)
    run.bold = True
    run.font.size = Pt(12)
    doc.add_paragraph(desc)

# ==================== PRINCIPAIS RESULTADOS ====================
doc.add_heading('Principais resultados', level=1)

doc.add_paragraph(
    "A análise resultou em uma taxonomia composta por 14 anti-padrões de desempenho, organizados em 7 categorias, "
    "conforme a Tabela 1."
)

doc.add_paragraph("Tabela 1 — Taxonomia dos anti-padrões de desempenho de acesso a dados (Asmare et al., 2022)")

table = doc.add_table(rows=8, cols=2)
table.style = 'Table Grid'
hdr = table.rows[0]
hdr.cells[0].text = 'Categoria'
hdr.cells[1].text = 'Anti-padrões'
for cell in hdr.cells:
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(10)

data = [
    ('1. Data Retrieval & Update', 'Multiple Key Sequential Search'),
    ('2. Query', 'Inefficient Query Translation'),
    ('3. Database Connection (3)', 'Duplicate Requests; Synchronous Connection Usage; Single Connection for Data Access'),
    ('4. Driver / Data Access API (3)', 'Inefficient Driver/API; Misconfiguration; Wrong API Function'),
    ('5. Cache (3)', 'Cache Invalidation vs. Update; Inefficient Cache Logic; Not Caching the Query'),
    ('6. Indexing', 'Non-optimized Indexing Logic'),
    ('7. Node Configuration & Management (2)', 'Inadequate Node Failure Handling; Load Imbalance Across Multiple Nodes'),
]

for i, (cat, ap) in enumerate(data, 1):
    row = table.rows[i]
    row.cells[0].text = cat
    row.cells[1].text = ap
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(10)

doc.add_paragraph('')

doc.add_paragraph("Estatísticas de prevalência e criticidade (survey n=53):")

stats = [
    "Top 3 mais críticos (criticidade operacional): (1) Inadequate Node Failure Handling; (2) Synchronous Connection Usage; (3) Inefficient Driver/API.",
    "Anti-padrão mais prevalente: Inefficient Driver/API — 15,6% dos 141 issues analisados.",
    "Empatados em segundo lugar (10,64% cada): Inefficient Cache Logic, Not Caching the Query, Inefficient Query Translation.",
    "Distribuição por tipo de sistema: 73,4% dos issues provêm de sistemas NoSQL puros; 26,6% de sistemas poliglotas.",
    "Concentração por camada: Driver/API (3 anti-padrões), Connection (3), Cache (3) somam 64,3% do total."
]
for s in stats:
    doc.add_paragraph(s, style='List Bullet')

# ==================== GAPS / PONTOS EM ABERTOS ====================
doc.add_heading('Gaps / Pontos em abertos', level=1)

doc.add_paragraph(
    "Apesar do rigor metodológico e da contribuição inédita para o contexto NoSQL/poliglota, "
    "o trabalho apresenta limitações que configuram oportunidades diretas para a presente pesquisa:"
)

gaps = [
    (
        "Ausência de conexão com limites físicos de hardware (Aula 02 — Física do I/O).",
        "O artigo trata os anti-padrões como problemas de código/configuração, mas não os vincula a "
        "restrições físicas mensuráveis: largura de banda de disco/RAM/rede (números de Jeff Dean), "
        "write amplification (WAF) em LSM trees, compaction pauses, backpressure e saturação de buffers. "
        "Essa lacuna impede entender por que certos anti-padrões (ex.: Wrong API Function → single write vs. batch) "
        "têm impacto desproporcional em larga escala."
    ),
    (
        "Ignora a sincronização temporal distribuída (Aula 03 — Física do Tempo).",
        "Não há menção a clock drift (PPM), NTP, relógios monotônicos vs. wall-clock, LWW (Last-Write-Wins) loss, "
        "watermarks, TrueTime ou relógios lógicos (Lamport, Vector Clocks). Anti-padrões críticos como "
        "Inadequate Node Failure Handling, Synchronous Connection Usage e Cache Invalidation vs. Update "
        "têm causas-raiz temporais diretas: clock drift mascara falhas de nó; timeouts baseados em wall-clock "
        "geram falsos positivos; invalidação total de cache + LWW causa perda silenciosa de atualizações concorrentes."
    ),
    (
        "Ausência de mapeamento para riscos de conformidade e governança (contexto setor público).",
        "Não há conexão com normativos brasileiros: TCU (acórdãos sobre tempestividade e integridade), "
        "CGU (IN de governança de dados), LAI — Lei 12.527/2011 (transparência ativa, SLA de resposta), "
        "LRF — Lei Complementar 101/2000 (fechamento contábil tempestivo), ISO 38500/ISO 8000 "
        "(governança e qualidade de dados). Anti-padrões de desempenho são tratados como problemas técnicos, "
        "não como riscos de auditoria, indisponibilidade de portais de transparência ou atraso no fechamento contábil."
    ),
    (
        "Validação restrita a desenvolvedores.",
        "O survey ouviu apenas desenvolvedores (n=53). Perspectivas de DBAs, SREs, arquitetos de dados, "
        "auditores de TI e gestores de conformidade — atores que operam, auditam e respondem legalmente pelos "
        "sistemas — não foram consideradas. A criticidade percebida pode variar significativamente entre esses papéis."
    ),
    (
        "Amostra exclusivamente Java e open-source.",
        "A generalização para outras linguagens (Go, Rust, Python, Node.js), ecossistemas proprietários "
        "e sistemas legados de grande porte (mainframe, COBOL, PL/SQL) não foi testada. Sistemas do setor público "
        "frequentemente operam em stacks heterogêneas e legadas."
    ),
    (
        "Tradução automática do PDF disponível.",
        "O PDF acessível no arXiv apresenta tradução automática (Google Translate), com imprecisões terminológicas "
        "(ex.: 'Khomh errado', 'foutse.khomh@polymtl.ca' como autores). A versão original em inglês deve ser "
        "consultada para citações precisas."
    )
]

for i, (titulo, desc) in enumerate(gaps, 1):
    p = doc.add_paragraph()
    run = p.add_run(f"{i}. {titulo}")
    run.bold = True
    run.font.size = Pt(12)
    doc.add_paragraph(desc)

# ==================== PRINCIPAIS CONCLUSÕES ====================
doc.add_heading('Principais conclusões', level=1)

conclusoes = [
    "Anti-padrões de desempenho no acesso a dados são recorrentes e críticos em sistemas NoSQL/poliglota, porém subinvestigados frente a sistemas relacionais — a literatura focou em SQL/relacional (Shao et al., 2021).",
    "As camadas de driver/API e cache concentram a maior prevalência (3 anti-padrões cada) e criticidade, indicando que decisões de infraestrutura (driver, pool, cache) impactam mais que otimizações pontuais de query.",
    "Falhas de infraestrutura (node failure, connection management) são percebidas como mais críticas que problemas de código (queries, índices), invertendo a prioridade tradicional de tuning.",
    "A taxonomia fornece base empírica sólida (saturação 250 instâncias, κ=0,764, validação n=53) para ferramentas de detecção automática, catálogos de refatoração e, agora, para extensão com lentes físicas/temporais/governança."
]
for c in conclusoes:
    doc.add_paragraph(c, style='List Bullet')

# ==================== PRINCIPAIS CONCEITOS ====================
doc.add_heading('Principais conceitos utilizados pelo autor (com localização)', level=1)

conceitos = [
    ('"Data-intensive systems handle high-volume, high-velocity, and heterogeneous data generated by humans and digital devices."', 'p. 1'),
    ('"Data access logic is a critical component of data-intensive systems, as it determines their overall performance and functionality."', 'p. 1'),
    ('"Technical debt related to data access code… performance-affecting technical debts have not been sufficiently investigated."', 'p. 1'),
    ('"NoSQL databases are becoming more popular components of data-intensive systems due to their horizontal scalability and handling of heterogeneous data."', 'p. 2'),
    ('"Polyglot persistence… the associated design, implementation, and maintenance issues have not been well investigated."', 'p. 2'),
    ('"We use inductive coding to identify root causes… labeling saturation was reached after 250 instances."', 'p. 3'),
    ('"Cohen\'s Kappa = 0.764, indicating substantial agreement."', 'p. 3'),
    ('"The three most critical anti-patterns: Inadequate Node Failure Handling, Synchronous Connection Usage, Inefficient Driver/API."', 'p. 6'),
    ('"Inefficient Driver/API is the most prevalent (15.6%)."', 'p. 6'),
    ('"Cache-related anti-patterns (Inefficient Cache Logic, Not Caching the Query, Cache Invalidation vs. Update) each at 10.64%."', 'p. 6'),
]

for citacao, pag in conceitos:
    p = doc.add_paragraph(f'{citacao} ({pag})', style='List Bullet')
    p.paragraph_format.space_after = Pt(2)

# ==================== PRINCIPAIS FONTES ====================
doc.add_heading('Principais Fontes', level=1)

fontes = [
    "SHAO, Y. et al. A Study of Performance Anti-patterns in Database-Driven Web Applications. ICSE, 2021.",
    "DEAN, J. Software Engineering Advice from Building Large-Scale Distributed Systems. Google, 2010.",
    "KLEPPMANN, M. Designing Data-Intensive Applications. O'Reilly, 2017.",
    "LAMPORT, L. Time, Clocks, and the Ordering of Events in a Distributed System. CACM, 1978.",
    "CORBETT, J. C. et al. Spanner: Google's Globally-Distributed Database. OSDI, 2012.",
    "ALVES, N. et al. A Systematic Mapping Study on Technical Debt. J. Syst. Softw., 2016.",
    "FRERY, A. C. Introdução à Metodologia Científica. 2014.",
    "VOLPATO, G. Pesquisa Científica: Princípios e Métodos. 2007."
]
for f in fontes:
    doc.add_paragraph(f, style='List Bullet')

# ==================== COMENTÁRIO PESSOAL ====================
doc.add_heading('Comentário pessoal', level=1)

comentario = (
    "Este artigo é a base empírica obrigatória para minha RQ1 (qual a taxonomia de anti-padrões prevalentes). "
    "Minha contribuição de pesquisa consiste em estender esta taxonomia com três lentes teóricas derivadas das "
    "aulas do Prof. Fabio Gomes Rocha (PROCC/UFS):\n\n"
    "1. Aula 02 — Física do I/O e Limites Físicos: classificar cada um dos 14 anti-padrões pela causa-raiz "
    "física violada — largura de banda de disco/RAM/rede, write amplification (WAF) em LSM trees, "
    "compaction pauses, network saturation, backpressure/buffer drop. Isso explica por que anti-padrões como "
    "'Wrong API Function' (single write vs. batch) amplificam WAF, ou por que 'Single Connection for Data Access' "
    "viola o modelo Shared-Nothing de escala horizontal.\n\n"
    "2. Aula 03 — Física do Tempo e Sincronização Distribuída: conectar cada anti-padrão a falhas de sincronismo — "
    "clock drift (PPM), NTP, relógios monotônicos vs. wall-clock, LWW (Last-Write-Wins) loss, watermarks, "
    "TrueTime/Spanner, relógios lógicos (Lamport, Vector Clocks). Isso explica por que os top 3 críticos "
    "(Node Failure, Sync Connection, Driver/API) têm causas-raiz temporais diretas: clock drift mascara falhas "
    "de nó; timeouts baseados em wall-clock geram falsos positivos; invalidação total de cache + LWW causa "
    "perda silenciosa de atualizações concorrentes.\n\n"
    "3. Meu contexto profissional — Conformidade, Contabilidade Pública, Transparência e Governança no Governo Federal: "
    "construir uma Matriz de Criticidade cruzando cada anti-padrão com 5 riscos regulatórios reais — "
    "(i) Tempestividade do Fechamento Contábil (LRF); (ii) Transparência Ativa e LAI (Lei 12.527/2011); "
    "(iii) Integridade Contábil e Auditoria (TCU, CGU); (iv) Auditoria de TI e Governança (ISO 38500, ISO 8000); "
    "(v) Disponibilidade de SIEM/Telemetria. A matriz será validada via entrevistas semiestruturadas (Likert 1–5) "
    "com 2–3 especialistas do órgão (DBA sênior, Arquiteto de Dados, Auditor de TI). O produto final inclui um "
    "Checklist de Governança operacionalizável por fase do ciclo de vida (Arquitetura → Desenvolvimento → Teste → "
    "Operação → Auditoria) com SLIs/SLOs por anti-padrão (ex.: p99 < 200ms, pool utilization < 70%, "
    "clock offset < 10ms, cache hit ratio > 95%).\n\n"
    "Próximos passos imediatos: (a) realizar as entrevistas para validar a Matriz de Criticidade; "
    "(b) detalhar a Tabela de Mapeamento (14 anti-padrões × Causa Física Aula 02 + Causa Temporal Aula 03) "
    "para embasar a Fundamentação Teórica; (c) iniciar a escrita da Introdução e Fundamentação (Seções 1–2) "
    "do artigo IMRAD desta disciplina."
)

doc.add_paragraph(comentario)

# Save to the target path
output_path = r'D:\1 - PROCC\1-Disciplinas\Semestre-2\TOPICOS AVANÇADOS EM ENGENHARIA DE SOFTWARE E SISTEMA DA INFORMAÇÃO\Fichamento_Asmare_et_al_2022.docx'
doc.save(output_path)
print(f'Saved to {output_path}')