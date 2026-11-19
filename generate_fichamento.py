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

print("FICHAMENTO - SLIDES ENGENHARIA DE SOFTWARE")
print("=" * 60)
print()

for pptx_file in files:
    path = os.path.join(pptx_dir, pptx_file)
    if not os.path.exists(path):
        print(f"NOT FOUND: {pptx_file}")
        continue
    
    try:
        prs = Presentation(path)
        slide_count = len(prs.slides)
        
        # Collect all text from slides
        all_text = []
        for i, slide in enumerate(prs.slides):
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for para in shape.text_frame.paragraphs:
                        if para.text.strip():
                            all_text.append(f"Slide {i+1}: {para.text[:60]}")
        
        # Get first slide title
        first_slide = prs.slides[0]
        first_text = ""
        for shape in first_slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    if para.text.strip():
                        first_text = para.text[:60]
                        break
                break
        
        print(f"--- {pptx_file} ---")
        print(f"  Slides: {slide_count}")
        print(f"  Título: {first_text}")
        print(f"  Conteúdo: {len(all_text)} parágrafos de texto")
        print()
        
    except Exception as e:
        print(f"ERRO: {pptx_file} - {type(e).__name__}: {e}")
        print()