# Quando o LLM não pode ser a fonte da verdade: lições de um laboratório de IA para o mercado financeiro brasileiro

*Artigo técnico — rascunho para publicação.*

---

## Resumo

Este artigo analisa o `br-financial-ai`, um laboratório aberto de AI Engineering para
análise do mercado financeiro brasileiro, e extrai dele um padrão de projeto
reproduzível: **separar rigorosamente o que é cálculo determinístico do que é
interpretação por modelo de linguagem**, e medir a qualidade da camada de IA com
métricas que reprovam build. O estudo cobre a arquitetura, o harness de avaliação com
gates numéricos de alucinação e *grounding*, e os resultados medidos — incluindo um
ciclo real de falha e correção em que duas execuções de release foram reprovadas por
alucinação antes de uma terceira passar. Fechamos com a lacuna central do projeto:
ele é um pipeline de dados de **três** empresas que usa um banco com `pgvector`
instalado e nunca utilizado — e discutimos por que transformar isso em escala real é
o próximo problema de pesquisa.

**Palavras-chave:** AI Engineering · LLM · *grounding* · alucinação · dados
financeiros · CVM · avaliação de sistemas

---

## 1. O problema

Colocar um LLM para responder perguntas sobre finanças de empresas é fácil. Fazer isso
de forma em que se possa **confiar** é difícil, e a diferença entre as duas coisas é
quase inteiramente uma questão de arquitetura, não de escolha de modelo.

O motivo é simples: modelos de linguagem são excelentes em produzir texto plausível e
notoriamente ruins em garantir que um número está correto. Em domínio financeiro, um
número plausível e errado é pior do que uma resposta ausente — um lucro líquido
inventado com a casa decimal trocada não parece um erro, parece um dado.

A resposta ingênua é pedir ao modelo que "não invente". A resposta de engenharia é
**tirar do modelo a possibilidade de inventar**, dando-lhe apenas valores que já foram
calculados por código determinístico, e depois **medir** se ele respeitou o que recebeu.

É esse segundo caminho que o `br-financial-ai` percorre, e é o que este artigo destrincha.

---

## 2. O estudo

`br-financial-ai` é um laboratório de estudo de AI Engineering para análise do mercado
financeiro brasileiro: versão 0.1.0, licença Apache-2.0, ~198 arquivos Python e cerca
de 19,5 mil linhas. O escopo é explicitamente delimitado — **não prevê preços** e **não
emite recomendação de compra ou venda**. A saída é uma postura analítica
(`FAVORABLE`, `NEUTRAL`, `UNFAVORABLE`), não uma ordem.

O sistema integra quatro fontes:

- **CVM** — metadados de companhias, formulários DFP (anual) e ITR (trimestral)
- **B3** — instrumentos e emissoras listadas
- **Yahoo Finance** — cotação, histórico OHLC, notícias
- **LLM local** — via Ollama, modelo padrão `llama3.1`, temperatura 0

E o resultado é servido por uma API FastAPI para um dashboard Next.js.

---

## 3. A decisão que define o projeto

Toda a arquitetura decorre de uma única frase do autor:

> "O LLM não é a fonte da verdade para números financeiros."

Materializada, essa frase vira uma fronteira com dois lados.

### Lado determinístico — os números

Valores contábeis vêm dos formulários da CVM, com a escala `MIL` normalizada
(multiplicação por mil antes de comparar com capitalização de mercado do Yahoo, que já
vem em reais). Resolução de período, mapeamento de métricas, margens, P/S, P/E,
retorno, volatilidade e drawdown são todos calculados em Python. **Nada disso passa
pelo modelo.**

### Lado do LLM — a linguagem

O modelo faz exatamente três coisas:

1. **Escolhe uma ferramenta.** Dada uma pergunta como "qual a receita da PETR4 no 2T26?",
   ele seleciona a ferramenta de consulta de métrica trimestral via `bind_tools` e
   preenche os argumentos. A ferramenta consulta o PostgreSQL. **O modelo não calcula.**
2. **Classifica notícias.** Rotula relevância, materialidade, especificidade à empresa,
   sentimento e categoria, com saída estruturada validada por Pydantic.
3. **Escreve a interpretação.** Compõe resumo, pontos positivos, riscos e quatro visões
   a partir de um contexto já montado.

### A validação que fecha o ciclo

Depois que o modelo escreve a recomendação, um parser determinístico verifica:

- o ticker bate com o do contexto;
- a postura é uma das três permitidas;
- a confiança está em `[0, 1]`;
- resumo e as quatro visões não estão vazios;
- **toda evidência citada pelo modelo existe no contexto.**

E aqui está o detalhe mais elegante do projeto: a evidência que fica **armazenada** é a
do contexto, não a cópia que o modelo escreveu. O modelo não tem como forjar uma
referência — se ele citar algo que não está no contexto, a geração é rejeitada.

---

## 4. O que quase nenhum projeto de "LLM + finanças" tem

A parte que realmente distingue este repositório é o harness de avaliação.

Existem **datasets versionados** de tool selection, classificação de notícias,
recomendação e grounding. Existem dois perfis: **FAST** (subconjunto representativo,
~4–5 min com modelo quente) e **FULL** (suíte completa, com Yahoo e E2E real). E
existem **quality gates** com limiares que fazem o comando sair com código diferente de
zero:

| Gate | Operador | Limite |
| --- | --- | --- |
| `exact_tool_call_accuracy` | ≥ | 0,95 |
| `news_relevance_accuracy` | ≥ | 0,90 |
| `company_specific_accuracy` | ≥ | 0,90 |
| `stance_accuracy` | ≥ | 0,80 |
| `factual_consistency` | ≥ | 0,95 |
| `evidence_grounding` | == | **1,00** |
| `true_hallucination_count` | == | **0** |

Repare nos dois últimos. **Grounding tem que ser perfeito e alucinação tem que ser
zero** — não é meta aspiracional, é condição de aprovação. E cada execução grava um
relatório imutável com timestamp, modelo, provedor e métricas, indexado em ordem
cronológica inversa.

Um detalhe metodológico que merece destaque: a comparação de regressão só é feita
**entre execuções do mesmo perfil**. FAST contra FULL nunca é rotulado como regressão,
porque os datasets são diferentes. Isso é o tipo de honestidade estatística que se
costuma ver faltar em relatórios de qualidade de IA.

---

## 5. Os números

### Baseline FULL aceito (`2026-09-02T174658Z`)

| Métrica | Valor |
| --- | --- |
| Acurácia exata de chamada de ferramenta (12 casos) | **1,0000** |
| Relevância de notícia (8 casos) | 1,0000 |
| Materialidade de notícia | 0,8750 |
| Concordância de sentimento | 0,8750 |
| Acurácia de postura (9 casos) | 0,8889 |
| Consistência factual | 1,0000 |
| **Grounding de evidência** | **1,0000** |
| **Alucinações verdadeiras** | **0** |

### Estabilidade

Cinco execuções consecutivas sobre a PETR4 produziram postura dominante `NEUTRAL` nas
cinco, com razão de estabilidade **1,0** e confiança média 0,8 — variância zero. Com
temperatura 0, isso é o comportamento esperado; medi-lo é o que garante que o sistema
não é uma máquina de resultados aleatórios.

### Latência — e por que ela importa

| Etapa | Segundos |
| --- | --- |
| Cotação Yahoo | 0,55 |
| Histórico Yahoo | 0,52 |
| **Classificação de notícias** | **66,91** |
| Montagem de contexto | 68,00 |
| **Recomendação** | **103,89** |
| **Análise total** | **171,89** |
| E2E HTTP (PETR4) | 227,72 |

Vale ler essa tabela com atenção. As chamadas de rede ao Yahoo somam pouco mais de
**um segundo**. A inferência local soma **170**. Ou seja: **99,4% do tempo da análise é
inferência de modelo**. É por isso que o projeto separa `GET
/api/v1/analysis/context/{ticker}` — determinístico, sem LLM — de `POST /api/v1/analysis`
— o caminho explícito de IA. O dashboard carrega o contexto imediatamente e só chama o
modelo quando o usuário pede.

### O ciclo de falha que vale mais que os números bons

A leitura do histórico de execuções revela algo que nenhum README conta. Três execuções
FULL consecutivas:

| Run | Status | Alucinações |
| --- | --- | --- |
| `2026-09-03T001742Z` | **FAIL** | 1 |
| `2026-09-03T011616Z` | **FAIL** | 1 |
| `2026-09-03T021334Z` | **PASS** | 0 |

Duas tentativas de release foram **reprovadas** pelo gate de alucinação. Entre a segunda
e a terceira, o `CHANGELOG` registra o *hardening* aplicado:

- correção de aliases de métrica para seleção de ferramenta;
- correspondência de exibição no avaliador factual;
- concorrência limitada na classificação de notícias (que também derrubou a latência de
  ~122 s para 66,9 s);
- prompt de recomendação compacto;
- **uma retentativa de geração quando há afirmação numérica sem lastro** ou evidência
  fora do contexto.

Este é o argumento mais forte do projeto, e ele é metodológico: **os gates pegaram uma
regressão real, ela foi diagnosticada, corrigida e medida**. Um sistema que nunca falha
em seus próprios testes normalmente está medindo pouco. Um sistema cujo histórico mostra
duas reprovações e uma correção está fazendo engenharia.

---

## 6. A lacuna: não há massa

Aqui o artigo vira uma crítica construtiva — e a crítica é o convite.

O projeto se propõe a ser um laboratório de dados financeiros brasileiros, mas:

- monitora **três** empresas: PETR4, BBDC4 e VALE3;
- carrega **dois** períodos: DFP 2025 e ITR 2026;
- declara as dependências `pgvector` e `langchain-postgres` e **nunca as usa** — o único
  uso de `pgvector` em todo o código é um teste que verifica que a extensão existe;
- ingere sequencialmente, sem paginação em nenhum repositório, sem particionamento, em
  um único nó PostgreSQL;
- não publica nenhuma medição de throughput.

O banco de dados é literalmente `pgvector/pgvector:0.8.6-pg16` no `compose.yaml`. A
infraestrutura para busca vetorial está provisionada e ociosa. É um convite explícito.

### Por que isso é o próximo problema de pesquisa

A literatura recente aponta que, em QA sobre documentos financeiros, **o gargalo
dominante é a recuperação, não a geração**. Um estudo sobre compreensão de relatórios
anuais por modelos de fronteira reportou que, de 11.859 falhas analisadas, 66,5% foram
problemas de recuperação e 19,2% de alucinação
([ACM ICAIF](https://dl.acm.org/doi/full/10.1145/3768292.3770417)) — isto é, o modelo
frequentemente erra porque não recebeu o trecho certo, não porque não sabe raciocinar
sobre ele. Há também benchmarks dedicados a alucinação em QA financeiro com GraphRAG
([FinReflectKG-HalluBench](https://export.arxiv.org/pdf/2603.20252)) e trabalho
comparando sistemas agênticos com RAG vetorial tradicional nesse domínio
([Rethinking Retrieval](https://export.arxiv.org/pdf/2511.18177)).

O `br-financial-ai` ocupa um nicho interessante nesse espaço: enquanto a maior parte
desses trabalhos mede QA sobre *texto*, este repositório mede **grounding sobre números
contábeis determinísticos**, com validação de identidade de evidência. E — o ponto
crucial — **ele já tem o instrumento de medição pronto**. Os gates de
`evidence_grounding` e `true_hallucination_count` existem. Basta rodar o experimento.

A pergunta de pesquisa escreve-se assim:

> Escalar este pipeline de 3 para ~700 emissores da B3: o que quebra, e a recuperação
> vetorial sobre notícias e trechos de formulários melhora o grounding medido?

E ela se decompõe em quatro medições:

1. **Ingestão** — tempo total e throughput (emissores/minuto) por faixa de volume
2. **Consulta** — p50/p95 de latência conforme o volume cresce
3. **Armazenamento** — índices necessários, particionamento, custo em `EXPLAIN ANALYZE`
4. **Qualidade de IA** — `evidence_grounding` e `true_hallucination_count` com e sem
   recuperação vetorial

As três primeiras são um estudo de escalabilidade. A quarta é um experimento controlado
de qualidade de IA. Juntas, cobrem o que a maioria dos trabalhos de dados em massa não
cobre: **a coisa escalou, mas ficou melhor ou pior?**

---

## 7. Lições transferíveis

Cinco padrões que valem além deste repositório:

**1. Tire a aritmética do modelo.** Se um número importa, calcule-o em código e passe-o
pronto. O modelo interpreta; ele não computa.

**2. Faça a evidência ser verificável.** Não basta pedir citação — exija que cada
referência exista no contexto e **descarte a cópia do modelo**, mantendo a sua. Isso
transforma "o modelo citou uma fonte" em "a fonte existe", que é uma afirmação muito
mais forte.

**3. Separe o caminho caro do caminho barato.** `GET` determinístico versus `POST` com
IA não é detalhe de API — é reconhecer que 99% da latência está na inferência e que a
maior parte das telas não precisa dela.

**4. Meça o que você teme, e faça isso reprovar build.** Grounding perfeito e zero
alucinação como *gate*, não como meta. Se o teste nunca falha, o teste é fraco.

**5. Guarde o histórico, inclusive das falhas.** O achado mais interessante deste
artigo — duas reprovações seguidas de correção — só existe porque o projeto arquiva
execuções imutáveis. Um sistema que só guarda o último resultado bom não tem história.

---

## 8. Conclusão

O `br-financial-ai` demonstra, em escala pequena mas com rigor real, que a confiabilidade
de sistemas com LLM em domínio financeiro é um **problema de arquitetura e de medição**,
não de escolha de modelo. A fronteira entre cálculo determinístico e interpretação por
linguagem, somada a um harness de avaliação com gates que reprovam build, produz um
sistema cujas falhas são detectáveis — e cujo histórico mostra que elas de fato foram
detectadas e corrigidas.

Sua lacuna declarada é também sua maior oportunidade: um pipeline desenhado para três
empresas, com busca vetorial provisionada e ociosa. Escalar para o mercado inteiro e
medir se a recuperação melhora o grounding é um programa de pesquisa com pergunta clara,
métrica existente e resultado potencialmente publicável.

E talvez a lição mais importante seja esta: o projeto é mais interessante por causa do
que ele **admite** — limitações, medições ruins, tentativas reprovadas — do que pelos
números que acerta.

---

## Referências

- Repositório: [gomesrocha/br-financial-ai](https://github.com/gomesrocha/br-financial-ai)
- *Can AI Read Like a Financial Analyst? A Financial Touchstone for Frontier Language
  Models on Long-Context Annual Report Comprehension*, ACM ICAIF —
  [dl.acm.org](https://dl.acm.org/doi/full/10.1145/3768292.3770417)
- *FinReflectKG-HalluBench: GraphRAG Hallucination Benchmark for Financial Question
  Answering Systems* — [arXiv](https://export.arxiv.org/pdf/2603.20252)
- *Rethinking Retrieval: From Traditional Retrieval Augmented Generation to Agentic and
  Non-Vector Reasoning Systems in the Financial Domain* —
  [arXiv](https://export.arxiv.org/pdf/2511.18177)
- *synetra* — pipeline de dados da CVM com Polars e Rust, como *related work* nacional —
  [github.com/leoserpa/synetra](https://github.com/leoserpa/synetra)

> **Nota de verificação:** os números deste artigo foram lidos diretamente de
> `evals/reports/latest.json`, `evals/reports/history/index.json` e
> `evals/reports/history/2026-09-02T174658Z.json` no clone do commit `7358c4e`. Os
> números da seção 5 que descrevem o baseline FULL vêm do run `2026-09-02T174658Z`; o
> `latest.json` é o run `2026-09-03T021334Z` (FULL, PASS, postura 1,0). A estatística de
> 66,5% foi obtida do resumo indexado do artigo da ACM — o texto completo estava
> inacessível no momento da redação e **deve ser confirmada antes de citação formal**.
