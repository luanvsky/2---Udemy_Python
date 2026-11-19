import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

base_dir = r'D:\dsh-vsky'
fichamento_files = [
    'fichamento_art1_boehm.txt',
    'fichamento_art2_nosilverbullet.txt', 
    'fichamento_art3_painpaper.txt',
    'fichamento_art4_dataaccess.txt',
    'fichamento_art5_travelogue.txt',
    'fichamento_art6_legacyncloud.txt',
    'fichamento_art7_qual.txt',
    'fichamento_art8_agile.txt',
    'fichamento_art9_darkside.txt',
    'fichamento_art10_devops.txt'
]

# Create document
master_doc = Document()

# Set default font
style = master_doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

# Configure margins
for section in master_doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# Title page
master_doc.add_paragraph()
master_doc.add_paragraph()
title = master_doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('FICHAMENTOS DE ARTIGOS DE ENGENHARIA DE SOFTWARE')
run.bold = True
run.font.size = Pt(16)
run.font.name = 'Times New Roman'

subtitle = master_doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Baseado no modelo: Tópicos Avançados em Engenharia de Software e Sistemas de Informação')
run.font.size = Pt(12)
run.font.name = 'Times New Roman'

master_doc.add_paragraph()
master_doc.add_paragraph()

info = master_doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = info.add_run('Disciplina: Tópicos Avançados em Engenharia de Software e Sistemas de Informação')
run.font.size = Pt(11)
run.font.name = 'Times New Roman'

run = info.add_run('Semestre: 2026/2')
run.font.size = Pt(11)
run.font.name = 'Times New Roman'

run = info.add_run('Prof. Dr. Fabio Gomes Rocha')
run.font.size = Pt(11)
run.font.name = 'Times New Roman'

master_doc.add_paragraph()
master_doc.add_paragraph()

# Model structure keys
model_structure = [
    '[7] FICHAMENTO',
    '[10] REFERÊNCIA BIBLIOGRÁFICA COMPLETA: (com base no artigo selecionado)',
    '[12] ASMARE',
    '[14] OBJETIVOS: (iniciar com verbos... de 3 a 5 objetivos a verificar na introdução do autor)',
    '[16] IDENTIFICAR OS ANTIPADRÕES:',
    '[17] CATEGORIZAR E CONSTRUIR UMA TAXONOMIA:',
    '[18] VALIDAR EMPIRICAMENTE:',
    '[19] INVESTIGAR O IMPACTO:',
    '[22] METODOLOGIA: (como foi desenvolvido o estudo? Que tipo de pesquisa? Como está estruturado?)',
    '[24] ESTUDO EMÍPICO COM ABORDAGEM QUALITATIVA E QUANTITATIVA:',
    '[26] FONTES: (de onde saíram as informações)',
    '[28] REPOSITÓRIOS:',
    '[29] RELATÓRIOS DE BUGS E COMMITS:',
    '[30] RESPOSTAS E OPINIÕES COLETADAS VIA QUESTIONÁRIO:',
    '[31] LITERATURA ACADÊMICA SOBRE:',
    '[34] PRINCIPAIS CONCEPTS UTILIZADOS PELO AUTOR (identificar e transcrever os principais conceitos localizando as páginas):',
    '[36] "Aproveitar a vasta quantidade de dados heterogêneos gerados por humanos e máquinas para obter insights acionáveis" (p. 1)',
    '[37] "Assim como o software tradicional, esses sistemas sAo propensos a dúvidas tÉcnicas, introduzidas para lidar com a pressão de restrições de tempo e recursos sobre os desenvolvedores." (p. 1)',
    '[38] "Especificar antipadrões de desempenho no acesso a dados É importante, pois É o primeiro passo antes da construÇÃo de ferramentas de detecÇÃo automÀtica que sÃo utilizadas para estudar a prevalÊncia e o impacto desses antipadrões." (p. 1)',
    '[41] PRINCIPAIS CONCLUSÕES DO AUTOR (identificar e transcrever as principais conclusões localizando as páginas):',
    '[43] "Devido às diferenças nos mecanismos de acesso a dados entre bancos de dados relacionais e NoSQL, os antipadrões de desempenho identificados em [estudos anteriores] podem nÃo ser generalizÁveis para sistemas de uso intensivo de dados baseados em NoSQL." (p. 1)',
    '[44] "Embora a vantagem de escolher o banco de dados com base na natureza dos dados seja clara, as questões associadas de projeto, implementaÇÃo e manutenÇÃo nÃo foram bem investigadas." (p. 1)',
    '[45] "A catalogaÇÃo dos antipatrões de acesso a dados em arquiteturas NoSQL e poliglota fornece a base essencial para o desenvolvimento de ferramentas de anÁlise estÁtica e dinÂmica focadas no desempenho de Big Data." (p. 1)',
    '[47] COMENTÁRIO PESSOAL:',
    '[51] PALAVRAS-CHAVE: (5 palavras-chave significativas relativas ao texto)',
    '[55] (máximo de 2 páginas)',
    '[58] AQUI ESTÁ UMA EXPLICAÇÃO SIMPLES E PRÁTICA, PONTO POR PONTO, DO QUE SIGNIFICA CADA PARTE DO FICHAMENTO PARA VOCÊ DOMINAR O CONTEÚDO DO ARTIGO:',
    '[60] 1. OBJETIVOS (O que os autores queriam fazer)',
    '[62] 2. METODOLOGIA (Como a pesquisa foi realizada)',
    '[70] 3. FONTES (De onde saíram as informações)',
    '[72] 4. PRINCIPAIS CONCEPTS (Termos-chave)',
    '[76] 5. PRINCIPAIS CONCLUSÕES (O que o estudo provou)',
    '[98] 6. PALAVRAS-CHAVE EXPLICADAS'
]

# Title page content
title_lines = [
    '',
    'FICHAMENTOS DE ARTIGOS DE ENGENHARIA DE SOFTWARE',
    '',
    'Baseado no modelo: Tópicos Avançados em Engenharia de Software e Sistemas de Informação',
    '',
    'Disciplina: Tópicos Avançados em Engenharia de Software e Sistemas de Informação',
    'Semestre: 2026/2',
    'Prof. Dr. Fabio Gomes Rocha',
    '',
    ''
]

for line in title_lines:
    p = master_doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(line)
    if not line.strip():
        run.font.size = Pt(16 if line == 'FICHAMENTOS DE ARTIGOS DE ENGENHARIA DE SOFTWARE' else 16)
    else:
        run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    if line == 'FICHAMENTOS DE ARTIGOS DE ENGENHARIA DE SOFTWARE':
        run.bold = True

# Process each fichamento
for i, filename in enumerate(fichamento_files):
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        master_doc.add_heading(f'ARQUIVO {i+1}: {filename.replace(".txt", ".pptx")} - ARQUIVO NÃO ENCONTRADO', level=1)
        master_doc.add_page_break()
        continue
    
    master_doc.add_heading(f'ARQUIVO {i+1}: {filename.replace(".txt", ".pptx")}', level=1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Organize content by model sections
    current_key = None
    section_items = []
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Check if this is a model structure key
        found_key = None
        for key in model_structure:
            # Check exact match or key followed by colon
            base_key = key.split('[')[1].split(']')[0] if '[' in key else key
            if line_stripped == key:
                found_key = key
                break
            # Check if line starts with key content after the brackets
            if line_stripped.startswith(base_key + ':'):
                found_key = key
                break
        
        if found_key:
            # Save previous section
            if current_key and section_items:
                master_doc.add_heading(current_key, level=2)
                for item in section_items:
                    master_doc.add_paragraph(item)
            
            current_key = found_key
            section_items = []
        else:
            section_items.append(line_stripped)
    
    # Don't forget last section
    if current_key and section_items:
        master_doc.add_heading(current_key, level=2)
        for item in section_items:
            master_doc.add_paragraph(item)
    
    if i < len(fichamento_files) - 1:
        master_doc.add_page_break()

# Save
output_path = os.path.join(base_dir, 'fichamentos_academicos.docx')
master_doc.save(output_path)
print(f'Documento acadêmico criado: {output_path}')