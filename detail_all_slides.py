from pptx import Presentation
import os

pptx_dir = r'D:\1 - PROCC\1-Disciplinas\Semestre-2\ENGENHARIA DE SOFTWARE'
files = [
    "Aula_-_Intro.pptx",
    "Parte_1_-_EngSW.pptx", 
    "Parte_2_-_SWEBOKs.pptx",
    "Parte_3_-_Requisitos_de_SW.pptx",
    "Parte_4_-_Casos_de_Uso.pptx",
    "Parte_5_-_Definio_de_Arquitetura_de_Software.pptx",
    "Parte_6_-_Atributos_de_Qualidade_e_Arquitetura.pptx",
    "Parte_7_-_Padroes_de_Arquitetura_de_Software.pptx",
    "Parte_8_-_Normas_de_Arquitetura.pptx",
    "Parte_9_-_ISO42010.pptx",
    "Parte_10_-_Arquitetura_4_mais_1.pptx",
    "Parte_11_-_O_que_faz_o_Arquiteto_de_Software.pptx",
    "Parte_12_-_IntroDesignSW.pptx"
]

print("DETALHAMENTO COMPLETO DE TODOS OS SLIDES")
print("=" * 70)
print()

for pptx_file in files:
    path = os.path.join(pptx_dir, pptx_file)
    if not os.path.exists(path):
        print(f"ARQUIVO NÃO ENCONTRADO: {pptx_file}")
        print()
        continue
    
    try:
        prs = Presentation(path)
        slide_count = len(prs.slides)
        
        print(f"=== {pptx_file} ===")
        print(f"Total de slides: {slide_count}")
        print()
        
        for i, slide in enumerate(prs.slides):
            slide_texts = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for para in shape.text_frame.paragraphs:
                        if para.text.strip():
                            slide_texts.append(para.text.strip())
            
            # Also check tables
            for shape in slide.shapes:
                if shape.has_table:
                    table = shape.table
                    for row in table.rows:
                        row_text = []
                        for cell in row.cells:
                            row_text.append(cell.text.strip())
                        if row_text[0]:
                            slide_texts.append(" | ".join(row_text))
            
            if slide_texts:
                print(f"--- Slide {i+1} ---")
                for text in slide_texts:
                    # Remove problematic characters
                    clean_text = text.replace('\u2011', '-').replace('\u274c', '!')
                    print(f"  {clean_text}")
                print()
            else:
                print(f"--- Slide {i+1} --- (sem texto detectado)")
                print()
        
        print(f"Total de slides com texto: {slide_count}")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"ERRO: {pptx_file} - {type(e).__name__}: {e}")
        print()
        print("=" * 70)
        print()

print("=== FIM DO PROCESSAMENTO ===")