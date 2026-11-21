"""
Primeira aula de Python: criar slides em PDF.

Este programa tem quatro partes:
1. guardar configuracoes;
2. guardar o texto dos slides;
3. desenhar cada slide;
4. juntar todos os slides em um PDF.
"""


# Bibliotecas: sao codigo pronto que podemos usar.
import os
import html
import base64

import pymupdf
from PIL import Image


# ==========================
# 1. INFORMACOES BASICAS
# ==========================

# Uma variavel guarda uma informacao.
LARGURA = 960
ALTURA = 540

# A pasta atual e a pasta onde este arquivo esta salvo.
PASTA_DO_PROGRAMA = os.path.dirname(os.path.abspath(__file__))

# Nestas variaveis, juntamos nomes de pastas e arquivos.
PASTA_DAS_IMAGENS = os.path.join(PASTA_DO_PROGRAMA, "_logos")
ARQUIVO_FINAL = os.path.join(PASTA_DO_PROGRAMA, "Slides_XBRL_5min.pdf")

# Cores escritas em formato HTML.
AZUL_ESCuro = "#12294a"
AZUL = "#1f6feb"
VERMELHO = "#c0392b"
CINZA = "#7a8699"
PRETO = "#1b1f27"
BRANCO = "#ffffff"

FONTE = "Segoe UI,Arial,Helvetica"


# ==========================
# 2. FUNCOES AUXILIARES
# ==========================

def pegar_imagem_em_texto(nome_da_imagem):
    """
    Esta funcao le uma imagem e transforma a imagem em texto.
    Isso permite colocar a imagem dentro do slide.
    """
    caminho = os.path.join(PASTA_DAS_IMAGENS, nome_da_imagem)

    arquivo = open(caminho, "rb")
    dados = arquivo.read()
    arquivo.close()

    texto = base64.b64encode(dados).decode("ascii")
    return "data:image/png;base64," + texto


def pegar_tamanho_da_imagem(nome_da_imagem):
    """
    Esta funcao descobre a proporcao da imagem.
    Proporcao significa largura dividida pela altura.
    """
    caminho = os.path.join(PASTA_DAS_IMAGENS, nome_da_imagem)
    imagem = Image.open(caminho)
    largura = imagem.width
    altura = imagem.height
    imagem.close()
    return largura / altura


def proteger_texto(texto):
    """
    Esta funcao troca alguns caracteres especiais.
    Por exemplo: o caractere < vira &lt;.
    """
    return html.escape(texto)


def criar_imagem_svg(imagem, x, y, largura, proporcao):
    """
    Esta funcao cria o texto SVG necessario para mostrar uma imagem.
    SVG e o formato usado para desenhar o slide.
    """
    altura = largura / proporcao

    codigo = (
        '<image '
        'x="' + str(x) + '" '
        'y="' + str(y) + '" '
        'width="' + str(largura) + '" '
        'height="' + str(altura) + '" '
        'xlink:href="' + imagem + '" '
        'href="' + imagem + '" '
        'preserveAspectRatio="xMidYMid meet"/>'
    )
    return codigo


# ==========================
# 3. PREPARAR AS IMAGENS
# ==========================

# Uma imagem precisa ser convertida uma unica vez.
BRASAO_UFS = pegar_imagem_em_texto("UFS_crest.png")
LOGO_PROCC = pegar_imagem_em_texto("procc_logo.png")

PROPORCAO_UFS = pegar_tamanho_da_imagem("UFS_crest.png")
PROPORCAO_PROCC = pegar_tamanho_da_imagem("procc_logo.png")


# ==========================
# 4. DESENHAR UM SLIDE
# ==========================

def desenho_do_slide(titulo, linhas, numero):
    """
    Esta funcao recebe um titulo e uma lista de linhas.
    Depois, ela cria o desenho completo de um slide.
    """

    # Comecamos o desenho em SVG.
    codigo = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="960" height="540" viewBox="0 0 960 540">',
        '<rect width="960" height="540" fill="#ffffff"/>',
        '<rect width="960" height="8" fill="' + AZUL + '"/>',
    ]

    # Se numero estiver vazio, este e o primeiro slide.
    if numero == "":
        y = 120
    else:
        y = 74

    # Numero do slide.
    if numero != "":
        codigo.append(
            '<text x="60" y="' + str(y) + '" '
            'font-family="' + FONTE + '" '
            'font-size="17" font-weight="700" '
            'fill="' + AZUL + '">' + numero + '</text>'
        )
        y = y + 40

        codigo.append(
            criar_imagem_svg(
                BRASAO_UFS,
                842,
                38,
                58,
                PROPORCAO_UFS,
            )
        )

    # Brasao e logo especiais da primeira pagina.
    if numero == "":
        codigo.append(
            criar_imagem_svg(
                BRASAO_UFS,
                812,
                40,
                88,
                PROPORCAO_UFS,
            )
        )
        codigo.append(
            criar_imagem_svg(
                LOGO_PROCC,
                380,
                418,
                200,
                PROPORCAO_PROCC,
            )
        )

    # Titulo do slide.
    codigo.append(
        '<text x="60" y="' + str(y) + '" '
        'font-family="' + FONTE + '" '
        'font-size="38" font-weight="700" '
        'fill="' + AZUL_ESCuro + '">' +
        proteger_texto(titulo) +
        '</text>'
    )

    y = y + 86

    # Linhas de texto do slide.
    for linha in linhas:
        texto = linha[0]
        tipo = linha[1]

        # Uma linha vazia deixa um espaco em branco.
        if texto == "":
            y = y + 16
            continue

        # Valores padrao: cor preta e texto comum.
        cor = PRETO
        tamanho = 27
        peso = "400"

        # Cada tipo troca o visual da linha.
        if tipo == "k":
            cor = AZUL_ESCuro
            tamanho = 33
            peso = "700"
        elif tipo == "b":
            cor = AZUL
            tamanho = 29
            peso = "700"
        elif tipo == "r":
            cor = VERMELHO
            tamanho = 27
            peso = "700"
        elif tipo == "g":
            cor = CINZA
            tamanho = 22
            peso = "400"
        elif tipo == "m":
            cor = AZUL_ESCuro
            tamanho = 28
            peso = "700"
        elif tipo == "t":
            cor = AZUL_ESCuro
            tamanho = 27
            peso = "700"
        elif tipo == "q":
            cor = AZUL_ESCuro
            tamanho = 22
            peso = "700"

        codigo.append(
            '<text x="60" y="' + str(y) + '" '
            'font-family="' + FONTE + '" '
            'font-size="' + str(tamanho) + '" '
            'font-weight="' + peso + '" '
            'fill="' + cor + '">' +
            proteger_texto(texto) +
            '</text>'
        )
        y = y + tamanho + 19

    codigo.append("</svg>")

    # Juntamos todas as partes da lista em uma unica string.
    resultado = "".join(codigo)
    return resultado


# ==========================
# 5. TEXTO DOS SLIDES
# ==========================

# Cada slide e uma lista.
# Cada linha e uma tupla: (texto, tipo).
SLIDES = [
    {
        "numero": "",
        "titulo": "Mineracao de defeitos em relatorios XBRL",
        "linhas": [
            ("Uma analise empirica em diferentes jurisdicoes", "g"),
            ("", ""),
            ("Victor Cesar Santos de Melo", "k"),
            ("Orientador: Prof. Fabio Gomes Rocha", ""),
            ("Engenharia de Software Experimental - 2026.2", "g"),
        ],
    },
    {
        "numero": "1 / 8",
        "titulo": "O problema",
        "linhas": [
            ("XBRL = padrao global de relatorio financeiro", "k"),
            ("legivel por maquina", "k"),
            ("", ""),
            ("Governos, reguladores e empresas publicam assim", ""),
            ("Mas: erros de validacao sao frequentes", "r"),
            ("=> afetam qualidade, comparabilidade e transparencia", ""),
        ],
    },
    {
        "numero": "2 / 8",
        "titulo": "A pergunta",
        "linhas": [
            ("E possivel medir defeito de validacao XBRL?", "m"),
            ("", ""),
            ("estavel?", "b"),
            ("classificavel?", "b"),
            ("reproduzivel?", "b"),
            ("", ""),
            ("O perfil varia entre jurisdicoes?", "k"),
        ],
    },
    {
        "numero": "3 / 8",
        "titulo": "Objeto e finalidade",
        "linhas": [
            ("OBJETO: a instancia XBRL", "k"),
            ("FINALIDADE: caracterizar e comparar", "b"),
            ("PERSPECTIVA: Engenharia de Software Experimental", ""),
            ("AMBIENTE: bases publicas", ""),
            ("", ""),
            ("Nao avaliamos empresas ou numeros contabeis.", "r"),
            ("Avaliamos conformidade com a especificacao.", ""),
        ],
    },
    {
        "numero": "4 / 8",
        "titulo": "O instrumento: Arelle",
        "linhas": [
            ("Processador XBRL certificado", "m"),
            ("", ""),
            ("Possui regras para varias jurisdicoes:", ""),
            ("SEC - ESEF - HMRC", "b"),
            ("", ""),
            ("A mesma ferramenta mede todos os casos.", ""),
            ("Qualquer pessoa pode reproduzir o resultado.", ""),
        ],
    },
    {
        "numero": "5 / 8",
        "titulo": "O que eu meco",
        "linhas": [
            ("Dimensao A - CLASSE", "k"),
            ("o que a regra verifica", ""),
            ("estrutural - tipo - calculo - formula", ""),
            ("", ""),
            ("Dimensao B - CAUSA-RAIZ", "k"),
            ("por que o documento falhou", ""),
            ("mapeamento - dado ausente - extensao indevida", ""),
        ],
    },
    {
        "numero": "6 / 8",
        "titulo": "Como eu valido",
        "linhas": [
            ("1. Determinismo - rodar duas vezes", "k"),
            ("2. Concordancia - duas pessoas analisam", "k"),
            ("3. Triangulacao - varias jurisdicoes", "t"),
            ("4. Reprodutibilidade - scripts publicos", "k"),
            ("", ""),
            ("Piloto com seis fases.", "b"),
        ],
    },
    {
        "numero": "7 / 8",
        "titulo": "O que me derruba",
        "linhas": [
            ("Vejo apenas o que passou pelo filtro.", "r"),
            ("", ""),
            ("Relatorios publicados ja foram aceitos.", ""),
            ("Portanto, meço conformidade residual.", ""),
            ("Nao meço toda a qualidade do documento.", ""),
            ("", ""),
            ("O estudo e observacional.", "b"),
        ],
    },
    {
        "numero": "8 / 8",
        "titulo": "Escopo",
        "linhas": [
            ("NO ARTIGO", "b"),
            ("Uma pergunta - SEC - um trimestre", ""),
            ("", ""),
            ("TRABALHO FUTURO", "b"),
            ("outras jurisdicoes - historico - causa-raiz", ""),
            ("", ""),
            ("Uma pergunta bem respondida vale mais.", "q"),
        ],
    },
]


# ==========================
# 6. CRIAR O PDF
# ==========================

# Criamos um documento vazio.
documento = pymupdf.open()

# Repetimos o processo para cada slide da lista.
for slide in SLIDES:
    numero = slide["numero"]
    titulo = slide["titulo"]
    linhas = slide["linhas"]

    codigo_svg = desenho_do_slide(titulo, linhas, numero)

    pagina_svg = pymupdf.open("svg", codigo_svg.encode("utf-8"))
    codigo_pdf = pagina_svg.convert_to_pdf()
    pagina_svg.close()

    pagina_pdf = pymupdf.open("pdf", codigo_pdf)
    documento.insert_pdf(pagina_pdf)
    pagina_pdf.close()

# Dados do PDF.
documento.set_metadata(
    {
        "title": "Mineracao de defeitos em relatorios XBRL",
        "author": "Victor Cesar Santos de Melo",
        "subject": "Engenharia de Software Experimental",
    }
)

# O comando save cria o arquivo final.
documento.save(ARQUIVO_FINAL, deflate=True)

print("PDF criado:", ARQUIVO_FINAL)
print("Quantidade de paginas:", documento.page_count)
