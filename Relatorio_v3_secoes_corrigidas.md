# Relatório Técnico — Atividade 1 — Correções para a versão 3

**Fonte de verdade:** repositório `luanvsky/PAA_UFS_2026_2_Bispo_Diego_Marques_Gabriel_Andrade_Laryssa_Santos_Kaio_Farias_Franzone_Melo_Victor`, commit **`1cdf6cf5463a178d7679a58e83237fc75f2def6d`** (23/09/2026).

**Regra aplicada:** o PDF v2 está desatualizado em relação ao repositório. Onde os dois divergem, **o repositório prevalece** — porque os dados versionados são a execução corrigida, e o PDF carrega a execução anterior.

**Nada foi alterado no repositório.** Todo o material abaixo é texto de substituição para você colar na fonte do documento.

---

## 1. Nota de revisão (inserir logo após a Tabela 1, como nota de rodapé ou parágrafo)

> **Nota de revisão.** A Tabela 1 desta versão substitui a da versão anterior. As medições da Etapa 5 foram refeitas *in-process* no commit `b113108` (*"mede as baterias in-process e adiciona a analise assintotica"*), após a identificação do erro descrito na Seção 15: a versão inicial cronometrava o subprocesso inteiro, e o tempo de `import` dominava a busca, produzindo dispersão de até 42% entre execuções da mesma célula. A versão anterior da tabela reportava médias de 154,63 ms / 148,24 ms / 145,93 ms, nas quais as três configurações diferiam em menos de 6% — diferença indistinguível do ruído. Com a cronometragem corrigida, a mesma comparação passa a 32,29 ms / 3,11 ms / 3,03 ms. Todos os números desta versão são rastreáveis a `7_resultados/relatorio_experimentos.json` no commit indicado.

Essa nota é importante: ela explica por que os números mudaram e transforma uma aparente contradição entre versões em evidência de rigor metodológico.

---

## 2. Seção 11 — Metodologia experimental (substituir os parágrafos finais)

> **Ambiente computacional.** Todas as medições foram realizadas em uma única máquina, condição necessária para que a comparação entre configurações seja válida. O ambiente completo é registrado automaticamente em `7_resultados/relatorio_experimentos.json`: **Windows 11** (`Windows-11-10.0.26200-SP0`), arquitetura **AMD64**, processador `Intel64 Family 6 Model 142 Stepping 12, GenuineIntel`, **Python 3.14.7** (interpretador `Python314\python.exe`).
>
> **Cargas de dados.** A *Carga 1* corresponde ao **corpus integral**, com os **182 chunks** produzidos na Etapa 2. A *Carga 2* corresponde ao **corpus reduzido**, com **91 chunks** obtidos por amostragem determinística — os chunks de **ordem ímpar** —, o que preserva a reprodutibilidade sem introduzir escolha subjetiva.
>
> **Unidade de medição.** Cada uma das 12 baterias é reportada como a **mediana de 5 execuções** da região algoritmicamente relevante, cronometradas com `time.perf_counter()` (precisão de nanossegundos, imune a ajustes do relógio do sistema). Cada bateria foi repetida **2 vezes**, totalizando **10 medições cronometradas por célula** (3 configurações × 2 cargas × 2 repetições × 5 execuções = **60 execuções cronometradas**). O pico de memória é aferido com `tracemalloc`, restrito à região cronometrada (ver Seção 15).
>
> **Reprodução.** O fluxo completo e a ordem de execução estão descritos no `README.md`, Seção *Reprodução*; os experimentos são produzidos por `1_scripts/5_experimentar.py`, a análise assintótica por `1_scripts/7_analise_assintotica.py`, a avaliação de robustez por `1_scripts/8_avaliar_robustez.py` e a consolidação por `1_scripts/6_gerar_graficos.py`.

---

## 3. Seção 12 — Resultados e gráficos (substituir integralmente)

### Tabela 1 — Tempos de recuperação por bateria (Etapa 5)

Fonte: `7_resultados/relatorio_experimentos.json`. Cada valor é a **mediana de 5 execuções** *in-process*.

| ID | Configuração | Carga | Rep. | Tempo de consulta (ms) | Tempo de ordenação (ms) |
|---:|---|---|---:|---:|---:|
| 01 | C1 — Busca Linear | Carga 1 (182) | R1 | 41,6755 | — |
| 02 | C1 — Busca Linear | Carga 1 (182) | R2 | 41,2409 | — |
| 03 | C1 — Busca Linear | Carga 2 (91) | R1 | 24,3084 | — |
| 04 | C1 — Busca Linear | Carga 2 (91) | R2 | 21,9445 | — |
| 05 | C2 — Índice Invertido | Carga 1 (182) | R1 | 3,0205 | — |
| 06 | C2 — Índice Invertido | Carga 1 (182) | R2 | 4,2769 | — |
| 07 | C2 — Índice Invertido | Carga 2 (91) | R1 | 2,8592 | — |
| 08 | C2 — Índice Invertido | Carga 2 (91) | R2 | 2,2837 | — |
| 09 | C3 — Indexada + Merge Sort Top-k | Carga 1 (182) | R1 | 2,8027 | 0,4051 |
| 10 | C3 — Indexada + Merge Sort Top-k | Carga 1 (182) | R2 | 2,5966 | 0,6433 |
| 11 | C3 — Indexada + Merge Sort Top-k | Carga 2 (91) | R1 | 3,1448 | 0,1926 |
| 12 | C3 — Indexada + Merge Sort Top-k | Carga 2 (91) | R2 | 3,5862 | 0,1585 |

### Tabela 2 — Síntese por carga (média ± desvio-padrão da célula)

| Configuração | Carga 1 — 182 chunks | Carga 2 — 91 chunks |
|---|---|---|
| C1 — Busca Linear | **41,4582 ± 0,2173 ms** | **23,1264 ± 1,1819 ms** |
| C2 — Índice Invertido | **3,6487 ± 0,6282 ms** | **2,5715 ± 0,2877 ms** |
| C3 — Indexada + Merge Sort Top-k | **2,6997 ± 0,1031 ms** | **3,3655 ± 0,2207 ms** |

*Nota:* as cargas **não** são agregadas em uma média única. Como a Carga 1 e a Carga 2 têm tamanhos diferentes (182 e 91 chunks), uma média conjunta misturaria o efeito de escala na dispersão e produziria um desvio-padrão que não mede ruído de medição. A média global, quando citada, é identificada como tal.

### Análise e interpretação dos resultados

**1. A indexação reduz o tempo de consulta em uma ordem de grandeza.** Na Carga 1, a busca linear consome **41,4582 ms** e a busca indexada **3,6487 ms**: um fator de **11,4×**. Na Carga 2, **23,1264 ms** contra **2,5715 ms**: **9,0×**. A diferença (≈ 37,8 ms na Carga 1) é cerca de **80 vezes** o desvio-padrão combinado das duas células, de modo que está muito além do ruído de medição. Este é o resultado central do trabalho: **o custo amortizado da construção do índice se paga já na primeira consulta**, e a poda proporcionada pelas listas de postings — 90 postings consultadas contra 910 comparações termo-a-termo — é o mecanismo que produz a diferença.

**2. O custo do Merge Sort é baixo e mensurável.** A ordenação consome entre **0,1585 ms** e **0,6433 ms** (média de 0,5242 ms na Carga 1 e 0,1756 ms na Carga 2), o que representa **19,4%** do tempo total da C3 na Carga 1 e **5,2%** na Carga 2. Esse é o custo do fator `n_c log n_c` isolado pela Configuração 3, e ele é pequeno o suficiente para não comprometer a vantagem da busca indexada.

**3. Não se afirma superioridade entre C2 e C3.** Na Carga 1 a C3 é 0,9490 ms mais rápida que a C2; na Carga 2 é 0,7940 ms mais lenta. Com **2 repetições por célula**, essa diferença está a poucos desvios-padrão e **não pode ser atribuída ao algoritmo**. O que os dados sustentam é: (i) o custo do Merge Sort é pequeno e mensurável; (ii) a ordenação é **necessária** — as três configurações devem devolver resultados ordenados e determinísticos (ver Seção 14); (iii) a diferença entre C2 e C3 **não** é conclusiva nesta escala. Uma bateria com mais repetições resolveria a questão (ver Observação metodológica).

**4. Escala com o tamanho do corpus.** Ao reduzir o corpus de 182 para 91 chunks (fator 2), a C1 cai de 41,4582 ms para 23,1264 ms — fator **1,79×**, compatível com custo **linear** em N. A C2 cai de 3,6487 ms para 2,5715 ms — fator **1,42×** —, **sublinear**, como previsto: o custo da C2 escala com o número de postings consultadas, e não com N. A C3 sobe para 3,3655 ms (fator 0,80×), comportamento atribuído à dispersão da célula e ao custo fixo da ordenação, e não a um efeito algorítmico.

**5. Taxa de sucesso.** **0 falhas** nas 12 baterias, sem resposta vazia para a consulta avaliada. A taxa de falhas é de **0%**.

**6. Memória.** O pico médio medido foi de **0,1340 MB** (C1), **0,1301 MB** (C2) e **0,1317 MB** (C3). Os valores são próximos entre si porque o `tracemalloc` mede apenas a **memória auxiliar da região cronometrada** — as estruturas de dados já estão carregadas quando a medição começa. A interpretação está delimitada na Seção 15.

**Observação metodológica.** Com o corpus desta escala, uma bateria completa custa cerca de **2 segundos**. Aumentar o número de repetições para 30 ou mais permitiria reportar intervalo de confiança e aplicar um teste de hipótese à comparação C2 × C3, que hoje permanece inconclusiva. Registra-se como trabalho futuro imediato, não como limitação dos resultados apresentados.

---

## 4. Seção 13 — Discussão de escalabilidade (substituir)

A tabela **já está correta** no PDF; o que precisa de correção é **uma grandeza citada em texto**.

**Correção:** o texto afirma que a ordenação tem *"expoente empírico 1,1864"*. O valor correto é:

- **1,2884** para o **tempo** de ordenação (fonte: `7_resultados/analise_assintotica.json`, estágio `merge_sort`);
- **1,19** para a **contagem de comparações** (fonte: `ANALISE_CORRETUDE_COMPLEXIDADE.md`, Seção 6).

O valor 1,1864 não corresponde a nenhuma das duas grandezas em nenhum artefato. Substituir por:

> *"a ordenação tem expoente empírico **1,29** medido sobre o tempo, e **1,19** medido sobre a contagem de comparações — sendo esta última a evidência mais limpa, por não estar sujeita ao ruído do escalonador."*

**Correção adicional — citar a fonte.** A tabela da Seção 13 hoje não indica origem. Acrescentar:

> *Fonte: `7_resultados/relatorio_experimentos.json` (tempos por carga) e `7_resultados/analise_assintotica.json` (expoentes). Carga 1 = 182 chunks; Carga 2 = 91 chunks.*

---

## 5. Seção 14 — um ajuste de precisão

A frase *"contexto vazio é silencioso (55,6% das consultas patológicas)"* está **correta** e agora é auditável. Acrescentar a qualificação:

> *"...(55,6% das consultas patológicas — 10 de 18 execuções da bateria de robustez; **nenhuma consulta relevante ou mista retornou vazio**, ver Anexo A)."*

---

## 6. Seção 15 — dois ajustes

**(a) Substituir o item "Conclusão":**

> **Conclusão.** As baterias têm **2 repetições externas por célula, cada uma correspondendo à mediana de 5 execuções cronometradas** — 10 medições por célula, 60 execuções cronometradas no total. A dispersão é reportada (§12, Tabela 2). As baterias comparam **custo**, não qualidade: as três configurações devolvem o mesmo Top-k. As cargas sintéticas são determinísticas (semente `20260923`); só os tempos variam entre máquinas.

A redação anterior ("apenas 2 repetições por célula") subestimava o próprio desenho experimental: a mediana de 5 execuções internas é o mecanismo que amortece o ruído do escalonador, e ela está implementada em `medir_operacao(..., repeticoes_internas=5)`.

**(b) Corrigir a frase final, que contradiz o corpo do relatório.** Hoje consta:

> ~~*"A etapa de chunking e a validação experimental ainda serão produzidas."*~~

Isso contraria a Seção 5 (chunking implementado, com `chunks.json` versionado), a Seção 11 (matriz de 12 baterias) e a Seção 12 (resultados medidos). Trata-se de remanescente de uma versão preliminar. **Remover a frase** ou substituir por:

> *"A validação experimental quanto à qualidade da recuperação — Precision@k e Recall@k — não foi realizada por ausência de conjunto de relevância anotado; ver Anexo C."*

---

## 7. Seção 16 — separar as duas baterias

A seção diz *"18 execuções, 0 falhas"*. As 18 execuções **existem** e estão versionadas em `7_resultados/avaliacao_robustez.json`, mas são de **outra bateria** que não a de cronometragem. Substituir por:

> ● **Verificações:** 14 testes `pytest`; identidade posicional com `sorted()` (Timsort) e `heapq.nsmallest` sobre a ordem completa; identidades aritméticas (2n−1 chamadas recursivas, 1+⌈log₂n⌉ de profundidade, Σ DF); **60 execuções cronometradas** na bateria de desempenho (12 baterias × mediana de 5) e **18 execuções** na bateria de robustez (9 consultas × 2 configurações), com **0 falhas** em ambas; semente fixa.

---

## 8. Seções 3 e 18 — preencher os marcadores

| Onde | Hoje | Corrigir para |
|---|---|---|
| Seção 3 | `URL: GitHub` | A URL do repositório (a mesma que consta no `README.md`) |
| Seção 3 | `Commit, tag ou release avaliado: Main` | **`1cdf6cf5463a178d7679a58e83237fc75f2def6d`** — "Main" não é fixo e contradiz a promessa de auditoria ponta a ponta da própria Seção 15 |
| Seção 18 | `URL pública: Youtube` | `https://youtu.be/6Qv1OSFnZBo` (consta no `README.md`) |
| Seção 11 | `Python 3.11+` | **Python 3.14.7** (a versão realmente medida, registrada em `relatorio_experimentos.json`) |

*Verificar também:* os badges do `README.md` apontam para o Colab em `diegofnf/PAA_UFS_2026_2_...`, enquanto o repositório é `luanvsky/PAA_UFS_2026_2_...`. Confirmar qual é o canônico.

---

## 9. Anexo A — Avaliação de robustez (Etapa 8) — **novo, hoje ausente do relatório**

O repositório contém uma bateria completa de robustez (`7_resultados/tabela_robustez.csv`, `avaliacao_robustez.json`, `8_avaliar_robustez.py`) que **não é apresentada em nenhuma seção do PDF**. São **9 consultas × 2 configurações = 18 execuções**.

| Categoria | Consulta | Candidatos | Retornados | Vazio? |
|---|---|---:|---:|---|
| Relevante | critérios para atribuição de bolsas | 54 | 5 | não |
| Relevante | aproveitamento de estudos | 18 | 5 | não |
| Relevante | estrutura curricular do mestrado | 57 | 5 | não |
| Mista | de bolsas xilofone | 22 | 5 | não |
| Nula | *(string vazia)* | 0 | 0 | **sim** |
| Nula | `"   "` | 0 | 0 | **sim** |
| Nula | `!!! ??? ---` | 0 | 0 | **sim** |
| Apenas stopwords | de da do para com os as um uma | 0 | 0 | **sim** |
| Fora do vocabulário | xilofone quântico blockchain astrofísica | 0 | 0 | **sim** |

**Leitura do resultado.** Das 18 execuções, **10 retornaram vazio (55,6%)** — e **todas as dez pertencem às categorias patológicas** (nula, apenas stopwords, fora do vocabulário), onde o vazio é o comportamento **correto por construção**. Nas **3 consultas relevantes** e na **consulta mista**, ambas as configurações retornaram os 5 resultados, sem falhas. Ou seja: **nenhuma consulta legítima ficou sem resposta**, e a degradação é confinada aos casos em que não há o que recuperar. Nenhuma exceção não tratada em 18 execuções.

---

## 10. Anexo B — Baseline de ordenação contra implementações de referência — **novo, hoje ausente do relatório**

Fonte: `7_resultados/tabela_baseline_ordenacao.csv`. A ordenação da equipe é comparada com `sorted()` (Timsort) e `heapq.nsmallest`.

| n | Scores distintos | Empates | Comparações | Equipe (ms) | Timsort (ms) | heapq (ms) | Timsort/Equipe | Ordem idêntica? |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 75 | 61 | 14 | 369 | 0,3390 | 0,0282 | 0,0290 | 0,0832 | **sim** |
| 75 | 63 | 12 | 388 | 0,3140 | 0,0271 | 0,0274 | 0,0863 | **sim** |
| 150 | 123 | 27 | 921 | 0,7257 | 0,0592 | 0,0512 | 0,0816 | **sim** |
| 300 | 231 | 69 | 2 158 | 1,6519 | 0,1346 | 0,0878 | 0,0815 | **sim** |
| 600 | 473 | 127 | 4 932 | 3,7543 | 0,3099 | 0,1650 | 0,0825 | **sim** |
| 1 200 | 911 | 289 | 11 104 | 9,7731 | 0,7026 | 0,3708 | 0,0719 | **sim** |
| 2 400 | 1 827 | 573 | 24 622 | 18,9299 | 1,3438 | 0,6140 | 0,0710 | **sim** |
| 4 800 | 3 498 | 1 302 | 54 145 | 64,1645 | 3,3020 | 1,3552 | 0,0515 | **sim** |

**Leitura do resultado.** Dois fatos merecem registro. Primeiro, **a ordem produzida é idêntica à das duas referências em todas as 8 cargas**, o que é evidência empírica de corretude independente da prova formal — e cobre exatamente o risco apontado na análise: dois algoritmos podem coincidir no Top-k e divergir no restante, por isso a comparação é feita **posição a posição sobre a ordem completa**. Segundo, a implementação da equipe é de **12× a 19× mais lenta** que o Timsort — razão que **diminui** com n (0,0832 → 0,0515). Esse hiato é esperado e não indica defeito algorítmico: o Timsort é implementado em C com otimizações específicas (detecção de runs, *galloping*), enquanto a implementação da equipe é Python puro instrumentado para contar operações elementares. A comparação correta é **assintótica**, e não de fator constante — que é precisamente o que a instrumentação permite verificar.

---

## 11. Anexo C — Conjunto de relevância ausente (declaração)

Seção sugerida para declarar a lacuna de forma explícita e sugerir o caminho:

> Não se reportam Precision@k, Recall@k ou nDCG porque o trabalho não construiu conjunto de relevância anotado, e o edital exige essas métricas apenas "quando houver referência de relevância" (Seção 7.3). Consequentemente, **as três configurações são comparadas por custo, não por qualidade** — e, como devolvem o mesmo Top-k, a comparação de qualidade entre elas seria trivialmente empatada. O que permanece aberto é a **qualidade do Top-k do BM25 em si**: sendo a métrica lexical, ela acerta na terminologia do domínio e tende a falhar em paráfrase e sinonímia (Seção 14). Medir essa lacuna exigiria um conjunto de relevância — ainda que *silver*, gerado por um modelo de julgamento e declarado como tal — e um controle para evitar circularidade entre o juiz e o avaliado.

---

## 12. Checklist de alterações

| # | Onde | Ação | Seção deste documento |
|---|---|---|---|
| 1 | Após a Tabela 1 | Inserir nota de revisão | §1 |
| 2 | Seção 11 | Substituir parágrafos finais | §2 |
| 3 | Seção 12 | Substituir integralmente (2 tabelas + análise) | §3 |
| 4 | Seção 13 | Corrigir expoente 1,1864 → 1,29 (tempo) / 1,19 (comparações); citar fonte | §4 |
| 5 | Seção 14 | Qualificar a frase dos 55,6% | §5 |
| 6 | Seção 15 | Reescrever "Conclusão" e remover frase obsoleta | §6 |
| 7 | Seção 16 | Separar 60 execuções cronometradas de 18 de robustez | §7 |
| 8 | Seções 3, 11, 18 | Preencher URL, commit, vídeo e versão do Python | §8 |
| 9 | Novo Anexo A | Inserir tabela de robustez | §9 |
| 10 | Novo Anexo B | Inserir baseline de ordenação | §10 |
| 11 | Novo Anexo C | Declarar a ausência de conjunto de relevância | §11 |
| 12 | `7_resultados/tabela_analise_assintotica.csv` | Corrigir cabeçalhos | Documento separado: *Erratas de artefatos* |
| 13 | `7_resultados/tabela_resultados.csv` | Remover/qualificar coluna de escopo misto | Documento separado: *Erratas de artefatos* |
| 14 | `1_scripts/7_analise_assintotica.py` | Corrigir limiar que torna `O(n)` inalcançável | Documento separado: *Erratas de artefatos* |
| 15 | `src/utils/searchEngine.ts` | Pré-computar comprimentos de documento | Documento separado: *Erratas de artefatos* |
| 16 | `1_scripts/7_analise_assintotica.py` | Não saturar R² negativo em zero | Documento separado: *Erratas de artefatos* |

**Observação sobre os itens 12 a 16:** são defeitos em **artefatos do repositório**, não no relatório. Nenhum deles invalida um resultado do PDF, mas os três primeiros tornam os artefatos internamente inconsistentes — e o item 14 é um erro de lógica que merece correção antes de qualquer publicação do código.
