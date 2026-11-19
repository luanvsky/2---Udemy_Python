import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE

doc = Document()

# Styles
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

# Heading styles
for level in range(1, 4):
    heading_style = doc.styles[f'Heading {level}']
    heading_style.font.name = 'Calibri'
    heading_style.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
    if level == 1:
        heading_style.font.size = Pt(16)
        heading_style.font.bold = True
    elif level == 2:
        heading_style.font.size = Pt(14)
        heading_style.font.bold = True
    elif level == 3:
        heading_style.font.size = Pt(12)
        heading_style.font.bold = True

def add_table_with_style(doc, headers, rows, col_widths=None):
    """Add a formatted table to the document."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light List Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        for paragraph in hdr_cells[i].paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)
                run.font.name = 'Calibri'
    
    # Data rows
    for row_idx, row_data in enumerate(rows):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_text in enumerate(row_data):
            cell = row_cells[col_idx]
            cell.text = str(cell_text)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)
                    run.font.name = 'Calibri'
    
    # Set column widths if provided
    if col_widths:
        for i, width in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(width)
    
    return table

def add_code_block(doc, text):
    """Add a formatted code block."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)

def add_heading_with_number(doc, text, level):
    """Add a numbered heading."""
    heading = doc.add_heading(text, level=level)
    return heading

# ============================================================
# BUILD DOCUMENT
# ============================================================

# Title Page
for _ in range(4):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('Protocolo de Revisão Sistemática')
run.bold = True
run.font.size = Pt(22)
run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Defeitos de validação em instâncias XBRL: uma revisão sistemática da literatura em Engenharia de Software')
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()
doc.add_paragraph()

# Metadata table
meta_table = doc.add_table(rows=6, cols=2)
meta_table.style = 'Light List Accent 1'
meta_data = [
    ('Aluno', 'Victor Cesar Santos de Melo'),
    ('Orientador', 'Prof. Fábio Gomes Rocha'),
    ('Programa', 'Mestrado em Ciência da Computação — UFS'),
    ('Disciplina', 'Engenharia de Software Experimental — 2026.2'),
    ('Data', '08/10/2026'),
    ('Versão', '0.1 (preliminar)')
]
for i, (label, value) in enumerate(meta_data):
    meta_table.rows[i].cells[0].text = label
    meta_table.rows[i].cells[1].text = value
    for cell in meta_table.rows[i].cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(10)

doc.add_page_break()

# ============================================================
# 1. Contexto e justificativa
# ============================================================
doc.add_heading('1. Contexto e justificativa', level=1)

doc.add_paragraph(
    'O XBRL (eXtensible Business Reporting Language) é o padrão global para relatórios financeiros legíveis por máquina. '
    'Governos, reguladores e empresas publicam dados nesse formato. Apesar da ampla adoção, erros de validação são frequentes '
    'e afetam a qualidade, a comparabilidade e a transparência da informação.'
)

doc.add_paragraph(
    'A literatura sobre XBRL concentra-se em benefícios contábeis e financeiros, mas há uma lacuna sobre seus benefícios '
    'para a Engenharia de Software. Não existem taxonomias consolidadas de defeitos XBRL, nem métricas de qualidade '
    'específicas para o setor público.'
)

doc.add_paragraph(
    'Esta Revisão Sistemática (RS) busca consolidar esse conhecimento, identificando tipos de defeitos, '
    'ferramentas de validação e métricas utilizadas, e apontando lacunas para pesquisa futura.'
)

# ----------------------------------------------------------
# 2. Objetivo
# ----------------------------------------------------------
doc.add_heading('2. Objetivo', level=1)

doc.add_paragraph(
    'Identificar, caracterizar e classificar os estudos empíricos sobre defeitos de validação em instâncias XBRL, '
    'com foco em:'
)

objectives = [
    'Tipos de defeitos reportados;',
    'Ferramentas e métodos de validação utilizados;',
    'Métricas de qualidade empregadas;',
    'Lacunas para pesquisa futura em Engenharia de Software Experimental.'
]
for obj in objectives:
    p = doc.add_paragraph(obj, style='List Bullet')
    for run in p.runs:
        run.font.size = Pt(11)

# ----------------------------------------------------------
# 3. Questão de pesquisa (PICO)
# ----------------------------------------------------------
doc.add_heading('3. Questão de pesquisa (PICO)', level=1)

# PICO Table
pico_headers = ['Componente', 'Definição']
pico_rows = [
    ('Population (P)', 'Estudos empíricos sobre instâncias XBRL e seus processos de validação'),
    ('Intervention (I)', 'Ferramentas, regras e métodos de validação XBRL (Arelle, EFM, ESEF, HMRC, SICONFI etc.)'),
    ('Comparison (C)', 'Comparação entre ferramentas, jurisdições, versões de taxonomia ou abordagens de validação'),
    ('Outcome (O)', 'Classes de defeitos, frequência, causas-raiz, métricas de qualidade, acurácia de validação'),
]
add_table_with_style(doc, ['Componente', 'Definição'], [
    ('Population (P)', 'Estudos empíricos sobre instâncias XBRL e seus processos de validação'),
    ('Intervention (I)', 'Ferramentas, regras e métodos de validação XBRL (Arelle, EFM, ESEF, HMRC, SICONFI etc.)'),
    ('Comparison (C)', 'Comparação entre ferramentas, jurisdições, versões de taxonomia ou abordagens de validação'),
    ('Outcome (O)', 'Classes de defeitos, frequência, causas-raiz, métricas de qualidade, acurácia de validação'),
], col_widths=[4, 12])

doc.add_paragraph()
doc.add_heading('Questão principal', level=2)
p = doc.add_paragraph()
run = p.add_run('Quais tipos de defeitos de validação são reportados em instâncias XBRL, como são classificados e quais ferramentas e métricas são utilizadas para detectá-los?')
run.italic = True
run.font.size = Pt(11)

doc.add_heading('Questões secundárias', level=2)
secondary_qs = [
    'Quais jurisdições e setores são mais estudados?',
    'Quais ferramentas de validação aparecem com mais frequência?',
    'Quais métricas de qualidade são usadas (ex.: κ de Cohen, precisão, recall)?',
    'Quais lacunas a literatura aponta para pesquisa futura?'
]
for q in secondary_qs:
    doc.add_paragraph(q, style='List Bullet')

# ----------------------------------------------------------
# 4. Estratégia de busca
# ----------------------------------------------------------
doc.add_heading('4. Estratégia de busca', level=1)

doc.add_heading('4.1 Fontes de busca (indexadas)', level=2)

sources_headers = ['Fonte', 'Obrigatória?', 'Justificativa']
sources_rows = [
    ('Web of Science', 'Sim', 'Indexação consolidada, evita periódicos predatórios'),
    ('Scopus', 'Sim', 'Cobertura ampla, indexação consolidada'),
    ('IEEE Xplore', 'Complementar', 'Foco em Engenharia de Software'),
    ('ACM Digital Library', 'Complementar', 'Foco em Engenharia de Software'),
    ('Engineering Village', 'Complementar', 'Cobertura de engenharia'),
]
add_table_with_style(doc, ['Fonte', 'Obrigatória?', 'Justificativa'], [
    ('Web of Science', 'Sim', 'Indexação consolidada, evita periódicos predatórios'),
    ('Scopus', 'Sim', 'Cobertura ampla, indexação consolidada'),
    ('IEEE Xplore', 'Complementar', 'Foco em Engenharia de Software'),
    ('ACM Digital Library', 'Complementar', 'Foco em Engenharia de Software'),
    ('Engineering Village', 'Complementar', 'Cobertura de engenharia'),
], col_widths=[3, 2, 11])

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Google Scholar: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('não será usado como fonte principal. Apenas para snowballing (busca de referências cruzadas), conforme orientação.')
run.font.size = Pt(11)

# ----------------------------------------------------------
# 4.2 String de busca (rascunho)
# ----------------------------------------------------------
doc.add_heading('4.2 String de busca (rascunho)', level=2)

search_string = '''("XBRL" OR "eXtensible Business Reporting Language" OR "Inline XBRL" OR "iXBRL")
AND
(validation OR error OR defect OR fault OR inconsistency OR "data quality" OR non-compliance)
AND
(software OR tool OR framework OR "empirical study" OR benchmark)'''

add_code_block(doc, search_string)

doc.add_heading('4.3 Passos de calibração', level=2)
calibration_steps = [
    'Buscar termos-chave nos campos do PICO;',
    'Identificar sinônimos de cada termo;',
    'Usar OR entre sinônimos;',
    'Usar AND entre facetas do PICO;',
    'Testar em 2 bases;',
    'Calibrar com especialista;',
    'Ajustar conforme necessário.'
]
for step in [
    'Buscar termos-chave nos campos do PICO;',
    'Identificar sinônimos de cada termo;',
    'Usar OR entre sinônimos;',
    'Usar AND entre facetas do PICO;',
    'Testar em 2 bases;',
    'Calibrar com especialista;',
    'Ajustar conforme necessário.'
]:
    doc.add_paragraph(step, style='List Bullet')

# ----------------------------------------------------------
# 5. Critérios de inclusão e exclusão
# ----------------------------------------------------------
doc.add_heading('5. Critérios de inclusão e exclusão', level=1)

doc.add_heading('5.1 Inclusão', level=2)
inclusion = [
    'Estudos empíricos que analisam defeitos/erros em instâncias XBRL;',
    'Estudos que descrevem ou avaliam ferramentas de validação XBRL;',
    'Estudos que propõem taxonomias, métricas ou classificações de defeitos XBRL;',
    'Estudos indexados em Web of Science ou Scopus;',
    'Publicações em inglês, português ou espanhol, de 2000 em diante.'
]
for item in inclusion:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading('5.2 Exclusão', level=2)
exclusion = [
    'Estudos puramente teóricos, sem análise empírica de defeitos ou validação;',
    'Estudos sobre XBRL sem foco em qualidade ou validação;',
    'Artigos de opinião, editoriais, tutoriais sem dados empíricos;',
    'Duplicatas ou versões preliminares de um mesmo estudo;',
    'Artigos não indexados em WoS ou Scopus (evitar periódicos predatórios).'
]
for item in exclusion:
    doc.add_paragraph(item, style='List Bullet')

# ----------------------------------------------------------
# 6. Critérios de qualidade
# ----------------------------------------------------------
doc.add_heading('6. Critérios de qualidade', level=1)

doc.add_paragraph(
    'Checklist baseado em Kitchenham & Charters (2007), adaptado ao contexto:'
)

quality_headers = ['#', 'Questão de qualidade', 'Sim / Parcial / Não']
quality_rows = [
    ('1', 'Os objetivos da pesquisa estão claramente definidos?', '☐'),
    ('2', 'O contexto (jurisdição, setor, tipo de XBRL) está descrito?', '☐'),
    ('3', 'A ferramenta ou método de validação está especificado?', '☐'),
    ('4', 'Os defeitos são classificados de forma explícita?', '☐'),
    ('5', 'Há métricas quantitativas (frequência, precisão, κ etc.)?', '☐'),
    ('6', 'Os dados e scripts estão disponíveis para reprodutibilidade?', '☐'),
    ('7', 'As ameaças à validade são discutidas?', '☐'),
]
add_table_with_style(doc, quality_headers, quality_rows, col_widths=[1, 14, 3])

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Piloto: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('aplicar o checklist em 2–3 estudos antes da extração completa.')
run.font.size = Pt(11)

# ----------------------------------------------------------
# 7. Formulário de extração de dados
# ----------------------------------------------------------
doc.add_heading('7. Formulário de extração de dados', level=1)

extraction_headers = ['Campo', 'Descrição']
extraction_rows = [
    ('ID do estudo', 'Identificador único'),
    ('Autores / Ano', 'Dados bibliométricos'),
    ('Venue / Base', 'Onde foi publicado'),
    ('Jurisdição', 'EUA, UE, Brasil, Reino Unido etc.'),
    ('Tipo de XBRL', 'XML, iXBRL, CSV, JSON, GL'),
    ('Ferramenta de validação', 'Arelle, EFM, ESEF, SICONFI etc.'),
    ('Defeitos reportados', 'Lista e classificação'),
    ('Métricas', 'Frequência, precisão, recall, κ etc.'),
    ('Qualidade', 'Pontuação no checklist'),
    ('Lacunas apontadas', 'Trabalhos futuros sugeridos'),
]
add_table_with_style(doc, extraction_headers, extraction_rows, col_widths=[4, 12])

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Piloto: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('testar o formulário em 2–3 estudos antes da extração completa.')
run.font.size = Pt(11)

# ----------------------------------------------------------
# 8. Processo de seleção (PRISMA)
# ----------------------------------------------------------
doc.add_heading('8. Processo de seleção (PRISMA)', level=1)

prisma_steps = [
    'Busca nas bases → exportar para Zotero/StArt;',
    'Remoção de duplicatas;',
    'Seleção por título e resumo (2 revisores independentes);',
    'Seleção por texto completo (2 revisores independentes);',
    'Resolução de conflitos por consenso ou terceiro revisor;',
    'Avaliação de qualidade;',
    'Extração de dados;',
    'Síntese.'
]
for step in prisma_steps:
    doc.add_paragraph(step, style='List Bullet')

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Diagrama PRISMA será incluído no relatório final.')
run.italic = True
run.font.size = Pt(11)

# ----------------------------------------------------------
# 9. Síntese de dados
# ----------------------------------------------------------
doc.add_heading('9. Síntese de dados', level=1)

synthesis_items = [
    'Tabelas quantitativas: distribuição por ano, jurisdição, ferramenta, tipo de defeito;',
    'Visualizações: mapa de calor (ano × tipo de defeito), rede de coocorrência de ferramentas;',
    'Meta-análise: não prevista (dados heterogêneos), mas κ de Cohen será usado para concordância entre revisores.'
]
for item in synthesis_items:
    doc.add_paragraph(item, style='List Bullet')

# ----------------------------------------------------------
# 10. Plano de atualização futura
# ----------------------------------------------------------
doc.add_heading('10. Plano de atualização futura', level=1)

update_headers = ['Item', 'Definição']
update_rows = [
    ('Frequência', 'A cada 2 anos'),
    ('Protocolo', 'Reutilizar 100%'),
    ('Equipe', 'Manter ao menos 1 membro'),
    ('String', 'Reutilizar e recalibrar'),
    ('Dados', 'Integrar novos + anteriores'),
]
add_table_with_style(doc, update_headers, update_rows, col_widths=[4, 12])

# ----------------------------------------------------------
# 11. Ferramentas de apoio
# ----------------------------------------------------------
doc.add_heading('11. Ferramentas de apoio', level=1)

tools_headers = ['Ferramenta', 'Uso']
tools_rows = [
    ('Parsifal', 'Registro e gestão do protocolo'),
    ('StArt', 'Seleção e extração (alternativa)'),
    ('Zotero', 'Gerenciamento bibliográfico'),
    ('VTM (Visual Text Mining)', 'Apoio à seleção (opcional)'),
    ('Excel / Google Sheets', 'Formulário de extração'),
]
add_table_with_style(doc, tools_headers, tools_rows, col_widths=[6, 10])

# ----------------------------------------------------------
# 12. Cronograma preliminar
# ----------------------------------------------------------
doc.add_heading('12. Cronograma preliminar', level=1)

schedule_headers = ['Etapa', 'Prazo']
schedule_rows = [
    ('Protocolo + PICO + string', 'Até 15/10'),
    ('Registro no parsif.al', 'Até 20/10'),
    ('Piloto de seleção', 'Até 30/10'),
    ('Execução da RS', 'Até 20/11'),
    ('Síntese + redação', 'Até 05/12'),
    ('Revisão + submissão', 'Até 15/12'),
]
add_table_with_style(doc, schedule_headers, schedule_rows, col_widths=[8, 4])

# ----------------------------------------------------------
# 13. Referências
# ----------------------------------------------------------
doc.add_heading('13. Referências', level=1)

references = [
    'Kitchenham, B.; Charters, S. (2007). Guidelines for performing Systematic Literature Reviews in Software Engineering. EBSE.',
    'Kitchenham, B.; Brereton, P. (2013). A systematic review of systematic review process research in software engineering.',
    'Petersen, K. et al. (2008, 2015). Systematic Mapping Studies in Software Engineering.',
    'Felizardo, K. R.; Nakagawa, E. Y. (2017). Revisão Sistemática da Literatura em Engenharia de Software: Teoria e Prática. Elsevier.',
    'Biolchini, J. et al. (2005). Systematic Review in Software Engineering.',
    'Wohlin, C. et al. (2014). Writing for Synthesis of Evidence in Empirical Software Engineering.'
]
for ref in references:
    doc.add_paragraph(ref, style='List Bullet')

# ----------------------------------------------------------
# 14. Checklist de conformidade
# ----------------------------------------------------------
doc.add_heading('14. Checklist de conformidade', level=1)

compliance_headers = ['Item', 'Status']
compliance_rows = [
    ('Questão de pesquisa estruturada (PICO)', '☐'),
    ('String de busca calibrada', '☐'),
    ('Fontes definidas (WoS, Scopus, IEEE, ACM)', '☐'),
    ('Critérios de inclusão/exclusão derivados do PICO', '☐'),
    ('Critérios de qualidade (checklist + piloto)', '☐'),
    ('Formulário de extração padronizado', '☐'),
    ('Protocolo registrado no parsif.al', '☐'),
    ('Plano de atualização futura', '☐'),
    ('Ferramentas definidas (Parsifal, StArt, Zotero)', '☐'),
]
add_table_with_style(doc, compliance_headers, compliance_rows, col_widths=[14, 3])

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Observação: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('este protocolo é uma versão preliminar. A execução depende de ajustes após orientação e do cronograma da disciplina.')
run.font.size = Pt(11)
run.italic = True

# Save
output_path = r'D:\dsh-vsky\Protocolo_RS_XBRL.docx'
doc.save(output_path)
print(f'Documento salvo em: {output_path}')