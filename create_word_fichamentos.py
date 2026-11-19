import os
from docx import Document
from docx.shared import Pt

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

master_doc = Document()
master_doc.add_heading('FICHAMENTOS DE ARTIGOS DE ENGENHARIA DE SOFTWARE', level=0)
master_doc.add_paragraph('Baseado no modelo: Tópicos Avançados em Engenharia de Software e Sistemas de Informação')
master_doc.add_paragraph('')

for i, filename in enumerate(fichamento_files):
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        master_doc.add_heading(f'--- {filename}: ARQUIVO NÃO ENCONTRADO ---', level=1)
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    master_doc.add_heading(f'ARQUIVO {i+1}: {filename.replace(".txt", ".pptx")}', level=1)
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            p = master_doc.add_paragraph(line)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(1)
    
    if i < len(fichamento_files) - 1:
        master_doc.add_page_break()

output_path = os.path.join(base_dir, 'fichamentos_completos_word.docx')
master_doc.save(output_path)
print(f'Documento criado: {output_path}')