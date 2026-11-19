# Erratas de artefatos do repositório — PAA/UFS Atividade 1

**Escopo:** defeitos encontrados nos **artefatos do repositório** (scripts, CSVs, aplicação web) durante a conferência cruzada com o relatório.

**Nada foi alterado no repositório.** Cada item traz o diagnóstico, o impacto e a correção sugerida, para você aplicar quando quiser.

**Ordem de aplicação recomendada:** **E1 → regenerar → E2 → E3 → E4.** O E1 é um erro de lógica que contamina os artefatos derivados; corrigi-lo antes torna a regeneração consistente com os demais ajustes.

---

## E1 — `1_scripts/7_analise_assintotica.py`: o modelo `O(n)` é inalcançável

**Gravidade: alta.** É um erro de lógica, não de rótulo.

### Diagnóstico

Constantes (linhas 127–133):

```python
EVIDENCIA_MINIMA_O1 = 0.30
FOLGA_LOGARITMICA   = 0.30   # <-- igual ao limiar anterior
FOLGA_QUADRATICA    = 1.50
```

Cadeia de decisão (linhas 302–311):

```python
    if expoente is None:                    melhor_nome = "O(n)"
    elif expoente <= EVIDENCIA_MINIMA_O1:   melhor_nome = "O(1)"        # p <= 0,30
    elif expoente >= FOLGA_QUADRATICA:      melhor_nome = "O(n^2)"      # p >= 1,50
    elif expoente >= FOLGA_LOGARITMICA:     melhor_nome = "O(n log n)"  # p >= 0,30
    else:                                   melhor_nome = "O(n)"        # p > 0,30 e p < 0,30
```

Como `FOLGA_LOGARITMICA == EVIDENCIA_MINIMA_O1 == 0,30`, **todo expoente entre 0,30 e 1,50 é classificado como `O(n log n)`**, e o ramo final `else: "O(n)"` **é inalcançável** — exigiria `p > 0,30` e `p < 0,30` ao mesmo tempo.

O `else` só produz efeito quando `expoente is None` (falha de ajuste), que é capturado pelo primeiro ramo. Ou seja: **o classificador nunca elege `O(n)`**.

### Confirmação empírica

Em `7_resultados/analise_assintotica.json`, os 6 estágios com `p ≥ 0,50` receberam todos `modelo_eleito = "O(n log n)"`:

| Estágio | Expoente empírico | `modelo_eleito` (JSON) | `ANALISE_CORRETUDE_COMPLEXIDADE.md` §6 |
|---|---:|---|---|
| `extracao_texto` | 0,504 | O(n log n) | ruído em n pequeno |
| `normalizacao` | 1,0608 | **O(n log n)** | **Θ(L) — linear, "✓"** |
| `chunking` | 1,0736 | **O(n log n)** | **Θ(L) — linear, "✓"** |
| `indexacao` | 0,908 | **O(n log n)** | **Θ(L) — linear, "✓"** |
| `busca_linear` | 0,7786 | **O(n log n)** | **linear, "✓"** |
| `merge_sort` | 1,2884 | O(n log n) | Θ(n log n) — correto |
| `busca_indexada` | −0,1011 | O(1) | Θ(m+Q) — correto |
| `selecao_topk` | −0,0173 | O(1) | Θ(k) — correto |

**O documento da equipe está certo; o artefato JSON está errado em 5 dos 8 estágios.** A Seção 6 do `ANALISE_CORRETUDE_COMPLEXIDADE.md` classifica corretamente normalização, chunking, indexação e busca linear como lineares — e marca "✓". O `modelo_eleito` do JSON contradiz o próprio documento do grupo.

### Causa

O docstring (linhas 289–291) declara a intenção correta:

> *"toma-se o modelo de expoente teórico imediatamente abaixo de p (comparação com as medianas 0 / 1 / 2 de cada classe), **sobrescrevendo para O(n log n) quando o excedente de p sobre 1** indica o fator logarítmico"*

A intenção é um limiar **acima de 1,0**. `FOLGA_LOGARITMICA` é uma **margem** (0,30) — e nunca foi somada a 1,0. Daí o limiar efetivo ter ficado em 0,30, colidindo com `EVIDENCIA_MINIMA_O1`.

### Correção sugerida

```python
EVIDENCIA_MINIMA_O1 = 0.30   # inalterado: abaixo disso a curva é plana
FOLGA_LOGARITMICA   = 1.15   # ERA 0.30 — deve ser a margem ACIMA de 1.0
FOLGA_QUADRATICA    = 1.50   # inalterado
```

**Ancoragem do valor 1,15** (para constar no comentário da constante): no intervalo efetivamente medido para o Merge Sort (n = 256 → 2048, fator 8), `log₂n` vai de 8 a 11, de modo que `n log n` cresce por um fator `8 × (11/8) = 1,375` ao longo da varredura. O expoente log-log correspondente é `1 + log(1,375)/log(8) ≈ 1,15`. Um expoente medido acima de 1,15, portanto, indica crescimento mais rápido que o linear, compatível com o fator logarítmico — que é exatamente o critério que o docstring descreve.

**Verificação de que a correção produz o resultado esperado** (todos os 8 estágios passam a coincidir com a teoria e com o `ANALISE_CORRETUDE_COMPLEXIDADE.md` §6):

| Estágio | p | Antes | Depois |
|---|---:|---|---|
| `extracao_texto` | 0,504 | O(n log n) | **O(n)** |
| `normalizacao` | 1,0608 | O(n log n) | **O(n)** |
| `chunking` | 1,0736 | O(n log n) | **O(n)** |
| `indexacao` | 0,908 | O(n log n) | **O(n)** |
| `busca_linear` | 0,7786 | O(n log n) | **O(n)** |
| `busca_indexada` | −0,1011 | O(1) | O(1) |
| `merge_sort` | 1,2884 | O(n log n) | **O(n log n)** |
| `selecao_topk` | −0,0173 | O(1) | O(1) |

**Teste de regressão recomendado.** O projeto já aplica, no `README.md`, o princípio de que *"nunca executado" e "executado sem efeito"* devem ser distinguíveis. O mesmo vale aqui: um teste que alimente `classificar_complexidade` com uma série sintética estritamente linear e afirme que o resultado é `"O(n)"` **falharia hoje** e passaria depois da correção — exatamente o tipo de teste que pega um ramo inalcançável.

---

## E2 — `1_scripts/6_gerar_graficos.py`: cabeçalhos desalinhados na tabela assintótica

**Gravidade: média** (o artefato é legível e citável; hoje diz a coisa errada).

### Diagnóstico

Em `gerar_tabela_analise_assintotica` (linhas 875–912), a lista `colunas` tem 12 nomes e a linha escrita tem 12 valores, mas **dois estão desalinhados**:

| Coluna | Nome no cabeçalho | Valor realmente escrito | |
|---:|---|---|---|
| 7 | `complexidade_observada` | `estagio["modelo_eleito"]` | ✗ |
| 10 | `modelo_eleito` | `comparacao_modelos["modelo_preferido_por_r2"]` | ✗ |

Além disso, **a chave `complexidade_observada` não existe em `analise_assintotica.json`** (verificado: as chaves por estágio são `estagio`, `unidade_entrada`, `complexidade_teorica`, `medicoes`, `tempo_min_ms`, `tempo_max_ms`, `comparacao_modelos`, `modelo_eleito`, `expoente_empirico`, `ajustes`, `documento_amostrado`, `paginas_totais`). O cabeçalho promete uma coluna que o modelo de dados nunca teve.

### Impacto

O CSV é o artefato mais citável do projeto. Hoje ele afirma que:
- a complexidade **observada** da normalização é `O(n log n)` quando a **teórica** é `Θ(n)` — sugerindo incoerência onde o documento da equipe diz "✓";
- o **modelo eleito** para o Merge Sort é `O(n)`, quando o JSON diz `O(n log n)`.

São **6 de 8 linhas** com modelo eleito incorreto aos olhos do leitor.

### Correção sugerida

Renomear os cabeçalhos para que correspondam aos valores (os valores estão corretos; só os rótulos estão errados):

```python
    colunas = [
        "estagio",
        "unidade_entrada",
        "n_minimo",
        "n_maximo",
        "pontos_medidos",
        "complexidade_teorica",
        "modelo_eleito",            # era rotulado "complexidade_observada"
        "expoente_empirico",
        "r2_modelo_eleito",         # era "r2_melhor_ajuste" — mesmo valor, nome mais claro
        "modelo_preferido_por_r2",  # era rotulado "modelo_eleito"
        "tempo_min_ms",
        "tempo_max_ms",
    ]
```

Nenhum valor precisa mudar. O CSV corrigido está em `tabela_analise_assintotica_corrigida.csv` (gerado a partir do JSON atual, com os rótulos alinhados).

---

## E3 — `1_scripts/6_gerar_graficos.py`: coluna `tempo_busca_em_memoria_ms` mistura dois regimes de medição

**Gravidade: média.**

### Diagnóstico

Linhas 762–766:

```python
    tempo_busca_por_configuracao = {
        resumos[0]["configuracao"]: relatorio_linear["tempo_busca_segundos"] * 1000,
        resumos[1]["configuracao"]: relatorio_indexada["tempo_busca_segundos"] * 1000,
        resumos[2]["configuracao"]: relatorio_indexada["tempo_busca_segundos"] * 1000,  # C3 recebe o valor da C2
    }
```

Dois problemas distintos:

**(a) Escopos diferentes na mesma linha.** `tempo_busca_em_memoria_ms` vem dos relatórios de **execução única da Etapa 4** (`6_busca_lexical/relatorio_busca*.json`), enquanto `tempo_total_medio_ms` vem da **bateria da Etapa 5** (mediana de 5, 2 repetições). Os dois convivem na mesma linha sem qualquer nota. Pior: eles **discordam em direção** —

| Configuração | `tempo_total_medio_ms` (Etapa 5) | `tempo_busca_em_memoria_ms` (Etapa 4) | Relação |
|---|---:|---:|---|
| C1 | 32,2923 | 9,7460 | Etapa 4 é **3,3× menor** |
| C2 | 3,1101 | 9,1430 | Etapa 4 é **2,9× maior** |
| C3 | 3,0326 | 9,1430 | Etapa 4 é **3,0× maior** |

Nenhum offset constante explica a diferença — o que significa que os dois números não medem a mesma grandeza nem o mesmo escopo, e o CSV não diz isso.

**(b) C3 recebe o valor da C2.** A terceira entrada lê `relatorio_indexada` — o mesmo dicionário da segunda. A C3 **nunca teve** uma medição própria de busca isolada; o valor é literalmente copiado (9,1430 nas duas linhas).

### Correção sugerida

Remover a coluna da tabela consolidada. A bateria da Etapa 5 já reporta, por carga, a grandeza comparável (`tempo_medio_carga_1_ms`, `tempo_medio_carga_2_ms`), e a coluna da Etapa 4 não acrescenta informação — apenas ambiguidade.

Se a intenção for preservar o número da Etapa 4, então: (i) renomear para explicitar o escopo, p.ex. `tempo_busca_etapa4_ms_escopo_amplo`; (ii) registrar em nota que inclui carregamento e tokenização, ao contrário da Etapa 5; (iii) **deixar a célula da C3 vazia** em vez de copiar a da C2.

O CSV corrigido está em `tabela_resultados_corrigida.csv` (com a coluna removida e com o tempo reportado por carga, sem média conjunta).

---

## E4 — `src/utils/searchEngine.ts`: a aplicação web tokeniza o corpus a cada consulta

**Gravidade: média** (não afeta o relatório; afeta o que a interface exibe).

### Diagnóstico

Linhas 55 e 79–86:

```ts
const tInicioBusca = performance.now();
...
  const comprimentosDoc = new Map<string, number>();
  let totalTokens = 0;
  for (const chunk of chunksLista) {
    const tamanho = tokenizar(chunk.texto).length;   // O(N) por consulta
    comprimentosDoc.set(chunk.id_chunk, tamanho);
    totalTokens += tamanho;
  }
  const avgdl = N > 0 ? totalTokens / N : 0;
```

Esse laço executa **dentro** da região cronometrada (`tempoFimBusca` está na linha 144), ou seja, `tempoBuscaMs` inclui uma tokenização O(N) de todo o corpus **em cada consulta** — precisamente o trabalho que a configuração indexada existe para evitar. O comentário do próprio arquivo (linha 78) reconhece que `|D|` e `avgdl` precisam ser medidos sobre os tokens do texto "como no script Python"; o script Python, porém, faz isso **uma vez**, na construção do índice, e não a cada consulta.

### Impacto

Os tempos exibidos na aplicação **não são comparáveis** aos do relatório, e o desvio **penaliza sistematicamente a rota indexada**. Como a aplicação é um entregável publicado, e como a comparação de tempos é o eixo central do trabalho, vale corrigir.

### Correção sugerida

Pré-computar os comprimentos fora da região cronometrada, com memoização por revisão dos dados:

```ts
let cacheComprimentos: {
  chave: string;
  mapa: Map<string, number>;
  avgdl: number;
} | null = null;

function obterComprimentos(chunksLista: Chunk[], N: number, indiceData: IndiceInvertidoData) {
  const chave = `${indiceData.metadados.total_chunks_entrada ?? "?"}|${chunksLista.length}`;
  if (cacheComprimentos && cacheComprimentos.chave === chave) return cacheComprimentos;

  const mapa = new Map<string, number>();
  let total = 0;
  for (const chunk of chunksLista) {
    const tamanho = tokenizar(chunk.texto).length;
    mapa.set(chunk.id_chunk, tamanho);
    total += tamanho;
  }
  cacheComprimentos = { chave, mapa, avgdl: N > 0 ? total / N : 0 };
  return cacheComprimentos;
}
```

E, no corpo de `executarBuscaLexical`, chamar `obterComprimentos(...)` **antes** de `const tInicioBusca = performance.now();`.

**Dois pontos secundários no mesmo arquivo:**

1. Linha 76: `const N = indiceData.metadados.total_chunks_entrada || chunksLista.length || 182;` — o literal `182` é um número mágico. Se os metadados faltarem e um subconjunto estiver carregado, `N` cai silenciosamente no tamanho do corpus **integral**, enviesando o IDF. Preferir `?? chunksLista.length` sem o fallback fixo.
2. A aplicação mede busca e ordenação **separadamente** (`tempoBuscaMs` e `tempoOrdenacaoMs`), enquanto na Etapa 5 o `tempo_execucao_ms` da C3 **inclui** a ordenação (2,8027 ms contém 0,4051 ms). Isso deve constar como nota, ou os números da interface parecerão menores que os do relatório.

---

## E5 — `1_scripts/7_analise_assintotica.py`: R² negativo é indistinguível de R² zero

**Gravidade: baixa** — mas é exatamente o mesmo princípio que o próprio projeto enuncia no `README.md`.

### Diagnóstico

Em `_resultado_classificacao` (linha 324):

```python
"r2": round(max(dados["r2"], 0.0), 6),
```

O `max(..., 0.0)` converte um R² **negativo** em exatamente `0,000000`. No `analise_assintotica.json`, por exemplo, **todos os cinco modelos** do estágio `extracao_texto` reportam `r2: 0.0` — o que pode significar tanto "ajuste nulo" quanto "ajuste pior que a média" (R² negativo, comum em ajuste sem intercepto). Os dois casos têm leituras opostas sobre a qualidade do ajuste, e hoje são indistinguíveis.

O `README.md` do projeto enuncia precisamente esse princípio ao tratar dos contadores: *"nunca executado" e "executado sem efeito" devem ser distinguíveis*. Aplica-se igualmente aqui.

### Correção sugerida

Preservar o sinal:

```python
"r2": round(dados["r2"], 6),          # sem saturação em zero
"r2_negativo_saturado": dados["r2"] < 0,   # ou um campo próprio, se preferir manter o CSV legível
```

---

# O que está correto e **não** deve ser alterado

Registro isto para evitar que uma revisão futura "conserte" o que está certo:

| Item | Por que está correto |
|---|---|
| **Classificar pelo expoente log-log, e não pelo R²** | Justificado no próprio docstring (linhas 277–284): com uma década de variação de n, `O(n)` e `O(n log n)` ajustam-se com R² quase idênticos (diferença de 0,01 a 0,06), sempre a favor do `O(n)` por viés do estimador. Decidir pelo R² seria decidir por ruído. **A metodologia está certa; só o limiar está errado (E1).** |
| **Duas cargas de tamanhos diferentes** | Correto, e a decisão está documentada em `gerar_tabela_resultados` (linhas 730–732): a Carga 2 são os 91 chunks de ordem ímpar. Só falta **não** agregá-las em média única. |
| **A Carga 2 ser "ordem ímpar"** | Amostragem determinística: reprodutível e sem escolha subjetiva. Bom critério. |
| **Mediana de 5 execuções internas** | Amortece o ruído do escalonador. O relatório é que subestima o próprio desenho ao dizer "apenas 2 repetições". |
| **O `pico_memoria_bytes` medir só a memória auxiliar** | Declarado na Seção 15 do relatório e coerente com o medido (~0,13 MB, já que as estruturas estão carregadas antes da medição). Não é defeito; é escopo. |
| **A C3 ser mais lenta na Carga 2** | É o comportamento honesto dos dados, já marcado com asterisco na Seção 13. **Não** maquiar para favorecer a C3. |
| **A implementação ser 12–19× mais lenta que o Timsort** | Esperado: Python puro instrumentado contra C otimizado. A razão **cai** com n (0,0832 → 0,0515), o que é evidência de que o fator constante domina e o comportamento assintótico é o previsto. |
| **Comparar a ordem posição a posição, não só o Top-k** | Rigor correto: dois algoritmos podem coincidir no Top-k e divergir no restante. |
| **A ausência de Precision@k estar declarada** | Correto e bem fundamentado (Seção 7.3 do edital). A declaração da lacuna é mais valiosa que um número inventado. |

---

# Resumo

| ID | Arquivo | Defeito | Gravidade |
|---|---|---|---|
| **E1** | `1_scripts/7_analise_assintotica.py` | `FOLGA_LOGARITMICA = 0.30` torna `O(n)` inalcançável; 5 de 8 estágios classificados errado | **Alta** |
| **E2** | `1_scripts/6_gerar_graficos.py` | Cabeçalhos 7 e 10 desalinhados; `complexidade_observada` não existe nos dados | Média |
| **E3** | `1_scripts/6_gerar_graficos.py` | Coluna mistura Etapa 4 e Etapa 5; C3 copia o valor da C2 | Média |
| **E4** | `src/utils/searchEngine.ts` | Tokeniza o corpus a cada consulta, dentro da região cronometrada | Média |
| **E5** | `1_scripts/7_analise_assintotica.py` | `max(r2, 0.0)` torna R² negativo indistinguível de zero | Baixa |

Nenhum desses defeitos invalida um resultado apresentado no relatório. Os três primeiros tornam os artefatos internamente inconsistentes entre si; o E4 afeta apenas os tempos exibidos na aplicação web.
