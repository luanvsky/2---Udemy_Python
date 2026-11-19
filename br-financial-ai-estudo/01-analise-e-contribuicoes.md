# BR Financial AI — Análise técnica e mapa de contribuições

> Documento de trabalho. Toda afirmação factual abaixo foi verificada no clone local
> (`D:\dsh-vsky\br-financial-ai`, tag `v0.1.0`, commit `7358c4e`) ou na API do GitHub.
> Onde eu não consegui verificar, está marcado explicitamente.

---

## 1. O que o projeto é (modelo mental em 5 minutos)

`br-financial-ai` é um **laboratório de estudo de AI Engineering** aplicado ao mercado
financeiro brasileiro. Não é um produto de corretora e não prevê preço de ação.

O autor define o escopo com uma frase que é a tese central do projeto:

> "O LLM não é a fonte da verdade para números financeiros."

Tudo no repositório deriva dessa decisão. Existem **três camadas** com fronteiras rígidas:

### Camada 1 — Determinística (números)
Os números vêm de fontes oficiais e são calculados em Python, nunca pelo modelo:

| O quê | De onde vem |
| --- | --- |
| Balanços anuais e trimestrais | CVM (DFP / ITR), escala `MIL` normalizada ×1000 |
| Cotações, histórico OHLC, retorno, volatilidade, drawdown | Yahoo Finance via `yfinance` |
| Identidade do emissor (ticker → empresa) | B3 `ListedCompanies`, `InstrumentsConsolidated`, CVM `cad_cia_aberta.csv` |
| Margens, P/S, P/E | `domain/valuation.py` |
| Perfil financeiro (banco vs. indústria) | `SETOR_ATIV` oficial da CVM |

### Camada 2 — LLM (linguagem)
O modelo faz exatamente três coisas, e só três:

1. **Seleção de ferramenta** — escolhe qual métrica trimestral buscar (`bind_tools`).
2. **Classificação de notícias** — rotula relevância, materialidade, sentimento, categoria.
3. **Interpretação da recomendação** — escreve `FAVORABLE` / `NEUTRAL` / `UNFAVORABLE`
   com resumo, pontos positivos, riscos e quatro visões.

Note o vocabulário: **não é BUY / HOLD / SELL**. É postura analítica. Essa escolha é
deliberada e o parser de recomendação rejeita o vocabulário de trading.

### Camada 3 — Avaliação (prova)
O que diferencia este repositório de 99% dos projetos "LLM + finanças" do GitHub:

- Datasets de eval versionados em `evals/datasets/*.json`
- Harness de eval com perfis **FAST** e **FULL**
- **Quality gates** numéricos com limiares que reprovam build (`--fail-on-regression`)
- Histórico imutável de execuções em `evals/reports/history/`
- Métricas de **alucinação**, **grounding de evidência** e **consistência factual**
- Dashboard `/quality` no frontend que só lê JSON exportado

### O pipeline, de ponta a ponta

```
Ticker (PETR4)
  ↓
Security local → B3 ListedCompanies → InstrumentsConsolidated + CVM CSV   (descoberta)
  ↓
Company / Securities → DFP / ITR → TrackedCompany                          (persistência)
  ↓
PostgreSQL  ← CVM, B3, Yahoo (adapters + normalização)
  ↓
serviços determinísticos (financial_query, valuation, market)
  ↓
ferramentas independentes de framework  ← alvo do bind_tools
  ↓
RecommendationContext (com identificadores de evidência explícitos)
  ↓
RecommendationEngine (LLM, opcional)
  ↓
validação determinística (ticker, stance, evidência, campos)
  ↓
FastAPI → Next.js
```

**Detalhe de arquitetura que vale ouro:** a rota `GET /api/v1/analysis/context/{ticker}`
é 100% determinística e **nunca** chama o Ollama. Só `POST /api/v1/analysis` aciona IA.
Isso é separação de responsabilidade levada a sério, não marketing.

---

## 2. Estado real medido (não o que o README promete)

| Dimensão | Valor medido | Como verifiquei |
| --- | --- | --- |
| Versão / tag | `0.1.0`, tag `v0.1.0` | `pyproject.toml`, `git tag` |
| Licença | Apache-2.0 | API GitHub |
| Tamanho | 1,2 MB, 198 arquivos `.py` | `Get-ChildItem` |
| Linhas de Python | ~19.475 | contagem de linhas em `*.py` |
| Arquivos de teste | 59 | `tests/**/test_*.py` |
| Suítes de eval | 15 arquivos em `evals/` | listagem |
| Execuções de eval registradas | **7** em `history/index.json` | leitura do índice |
| Empresas monitoradas | **3** (PETR4, BBDC4, VALE3) | `config/monitored_companies.yaml` |
| Períodos carregados | DFP 2025, ITR 2026 | idem |
| Migrations | 7 | `migrations/versions/` |
| CI | **ausente** | `.github` não existe |
| Issues abertas | **0** | API GitHub |
| PRs (todos fechados) | 2 | API GitHub |
| Stars / forks | 5 / 0 | API GitHub |
| Último push | 2026-09-03 | API GitHub |

### Os números de qualidade (baseline FULL `2026-09-02T174658Z`)

| Métrica | Valor |
| --- | --- |
| `exact_tool_call_accuracy` (12 casos) | 1,0000 |
| `news_relevance_accuracy` (8 casos) | 1,0000 |
| `news_materiality_accuracy` | 0,8750 |
| `sentiment_agreement` | 0,8750 |
| `stance_accuracy` (9 casos) | 0,8889 |
| `factual_consistency` | 1,0000 |
| `evidence_grounding` | **1,0000** |
| `true_hallucination_count` | **0** |
| Estabilidade (5× PETR4) | dominante `NEUTRAL`, razão 1,0, confiança média 0,8 |
| Latência: notícias | 66,91 s |
| Latência: recomendação | 103,89 s |
| Latência: análise total | 171,89 s |
| E2E HTTP PETR4 | 227,72 s |

### Gates que reprovam build

```
exact_tool_call_accuracy   >= 0.95
news_relevance_accuracy    >= 0.90
company_specific_accuracy  >= 0.90
stance_accuracy            >= 0.80
factual_consistency        >= 0.95
evidence_grounding         == 1.00
true_hallucination_count   == 0
```

### Uma história interessante escondida no histórico

Lendo `evals/reports/history/index.json`, os três runs FULL mais recentes contam uma
narrativa que **a documentação ainda não conta**:

| Run | Status | Observação |
| --- | --- | --- |
| `2026-09-03T001742Z` | **FAIL** | `true_hallucination_count = 1` — tentativa de release |
| `2026-09-03T011616Z` | **FAIL** | `true_hallucination_count = 1` de novo |
| `2026-09-03T021334Z` | **PASS** | `latest.json` atual: stance 1,0, factual 1,0, 0 alucinações |

Entre o segundo FAIL e o PASS houve o *hardening* descrito no `CHANGELOG.md`: aliases de
métrica, correspondência de exibição no avaliador factual, concorrência limitada na
classificação de notícias, prompt de recomendação compacto e **uma retentativa de geração
quando há afirmação numérica sem lastro**. Isso é engenharia de confiabilidade de LLM feita
de verdade, com medição antes e depois.

---

## 3. Mapa de contribuições (ordenado por risco crescente)

O repositório tem **zero issues abertas**. Isso significa que não existe lista de tarefas
para pegar: as contribuições precisam ser propostas. Abaixo, o que eu encontrei com
evidência no código.

### 🟢 Nível 0 — Porta de entrada (1–3 horas cada, risco quase nulo)

**0.1 — Corrigir `docs/evaluation.md` desatualizado** ⭐ *melhor primeiro PR*

A seção "Historical runs in this repository" afirma listar o que o
`history/index.json` "currently contains" e mostra **5 runs**. O arquivo real tem **7**.
Faltam justamente as duas execuções mais interessantes:

- `2026-09-03T011616Z` (FULL, FAIL) — não aparece
- `2026-09-03T021334Z` (FULL, PASS) — não aparece, e **é o `latest.json` atual**

A tabela também descreve `2026-09-03T001742Z` como "Release FULL attempt" com falha,
sugerindo que o estado atual é reprovado — quando o estado atual é **aprovado**.
A seção "Metrics in the accepted FULL baseline" continua descrevendo `174658Z`
(stance 0,8889) enquanto o `latest.json` tem stance **1,0**.
*Evidência:* `docs/evaluation.md` vs. `evals/reports/history/index.json` vs.
`evals/reports/latest.json`.
*Por que vale:* é uma correção factual, verificável, e mostra que você leu os artefatos
gerados — não só o README.

**0.2 — Remover o `main.py` morto da raiz**

`main.py` na raiz é resquício de scaffolding:

```python
def main():
    print("Hello from br-financial-ai!")
```

O entrypoint real é `br_financial_ai.cli:main` (declarado em `[project.scripts]`).
É código morto que confunde quem chega.

**0.3 — Adicionar CI (`.github/workflows/ci.yml`)** ⭐ *alto valor estratégico*

Não existe `.github/` no repositório. Um workflow que rode `ruff check` e `pytest -q` é
autocontido e de valor imediato. **Ponto de atenção técnico** (e é aqui que você mostra
competência): `pytest -q` inclui `tests/integration/`, que exige PostgreSQL **com a extensão
pgvector** — veja `tests/integration/test_database.py::test_pgvector_extension_is_available`.
O serviço precisa subir a imagem `pgvector/pgvector:0.8.6-pg16` (a mesma do `compose.yaml`)
como *service container*, não `postgres:16` puro. Errar isso é o jeito mais rápido de ter
o PR rejeitado; acertar demonstra que você entendeu a stack.

### 🟡 Nível 1 — Lacunas reais de engenharia (1–2 semanas)

**1.1 — Tornar o onboarding durável**

O próprio README admite a falha:

> "Onboarding continues in an in-process background task and is **not durable across
> process crashes**."

O que existe hoje: `POST /api/v1/companies/onboard` grava um `CompanyOnboardingJob`,
devolve HTTP 202 e continua numa `BackgroundTask` do FastAPI. Se o processo cair, o job
fica órfão. E o gancho já está pronto — a documentação diz que "a later worker can call
`CompanyOnboardingService.run_job`", e o modelo `onboarding_job.py` tem índices para
consulta de job ativo.

*O que falta:* um worker que faça claim do job com lock (`SELECT ... FOR UPDATE SKIP LOCKED`),
retry com backoff, marcação de estado terminal e idempotência. Roda como processo separado
ou no startup.
*Por que vale:* é uma lacuna que o autor **documentou como conhecida mas não resolveu**.

**1.2 — Paginação e índices para escala**

Nenhum repositório pagina. `TrackedCompanyRepository.list_active_records()`,
`SecurityRepository.list_by_company_id()`, `FinancialStatementItemRepository.list_by_filing_id()`
retornam listas completas. O único `limit` do código está em
`NewsArticleRepository.list_recent_by_company()`. Com 3 empresas isso é irrelevante;
com centenas, deixa de ser.

**1.3 — Ligar o `pgvector` (ver Nível 3)**

### 🔵 Nível 2 — Roadmap declarado pelo autor

O README lista trabalho futuro explicitamente. São alvos legítimos porque **o autor já
declarou que quer**:

```
company comparison          recommendation history
scheduled analyses          watchlists
multi-model evaluation      multi-provider market/news
additional FinancialProfiles   advanced banking metrics
portfolio analytics
```

Dois destaques:

- **`multi-model evaluation`** — hoje 100% do eval roda `llama3.1` local. O harness
  já registra `model_provider` / `model_name` por run e compara "same profile only".
  Estender para multi-modelo é quase plug-and-play e produz uma **tabela comparativa**,
  que é exatamente o tipo de resultado que rende figura em artigo.
- **`additional FinancialProfiles`** — hoje só existem `NON_FINANCIAL` e
  `FINANCIAL_INSTITUTION`, e `Bancos` é o único `SETOR_ATIV` mapeado para o segundo.
  Seguradoras, fundos e holdings ainda caem em `NON_FINANCIAL`, o que produz métricas
  semanticamente erradas. Há uma tabela de catálogo em `docs/architecture.md` pronta
  para ser estendida.

### 🔴 Nível 3 — A âncora para o mestrado (o que realmente impressiona)

Detalhada na seção 4. É aqui que o projeto deixa de ser "estudo de AI Engineering" e vira
**pesquisa em dados em massa**.

---

## 4. A proposta-âncora: de 3 empresas para o mercado inteiro

### 4.1 O diagnóstico brutal

O repositório se chama "dados em massa" em espírito, mas **não tem massa nenhuma**:

- 3 empresas
- 2 períodos (DFP 2025, ITR 2026)
- `pgvector` e `langchain-postgres` **instalados como dependência e nunca usados**
  (o único uso de `pgvector` no código é um teste de que a extensão existe)
- ingestão sequencial, sem paginação, sem particionamento
- um único nó PostgreSQL
- nenhuma medição de throughput

Isso não é crítica — é o **enunciado do problema**. E é exatamente o que faz a ponte com a
sua disciplina.

### 4.2 A pergunta de pesquisa

> **O que quebra quando este pipeline sai de 3 para ~700 emissores da B3?**

Essa pergunta tem quatro sub-perguntas mensuráveis, cada uma virando uma seção de artigo:

| # | Sub-pergunta | Métrica |
| --- | --- | --- |
| Q1 | A ingestão CVM escala? | tempo total, throughput (empresas/min), tamanho de `financial_statement_item` |
| Q2 | As consultas continuam respondendo? | p50/p95 de `FinancialQueryService` por faixa de volume |
| Q3 | O schema aguenta? | necessidade de índices compostos, particionamento por período, custo de `EXPLAIN ANALYZE` |
| Q4 | A recuperação semântica melhora o *grounding*? | `evidence_grounding`, `factual_consistency`, `true_hallucination_count` do harness existente |

A Q4 é a joia: **o repositório já tem o instrumento de medição pronto**. O harness de eval
mede grounding e alucinação com gates numéricos. Você não precisa inventar métrica — precisa
rodar o experimento e mostrar se a recuperação vetorial sobre notícias e trechos de DFP move
o ponteiro.

### 4.3 Por que isso é defensável academicamente

A literatura recente aponta a recuperação como o gargalo dominante em QA financeiro. Um
estudo sobre comprehension de relatórios anuais reportou que, de 11.859 falhas analisadas,
**66,5% foram problemas de recuperação**, seguidos por 19,2% de alucinação — ou seja, o
gargalo *não* é o modelo, é o que se coloca no contexto dele
([ACM ICAIF](https://dl.acm.org/doi/full/10.1145/3768292.3770417) — *não consegui abrir o
texto completo, o número vem do resumo indexado; confirme antes de citar em artigo*).

Existe também um benchmark específico para alucinação em QA financeiro com GraphRAG
([FinReflectKG-HalluBench](https://export.arxiv.org/pdf/2603.20252)) e trabalho sobre
sistemas agênticos versus RAG vetorial tradicional em finanças
([Rethinking Retrieval](https://export.arxiv.org/pdf/2511.18177)). E, como *related work*
nacional, existe um pipeline de dados da CVM com Polars + Rust
([synetra](https://github.com/leoserpa/synetra)) — útil como comparação de abordagem de ETL.

O diferencial do seu trabalho: **a maioria desses trabalhos mede QA sobre texto; este
repositório mede grounding sobre números contábeis determinísticos com validação de
evidência**. Esse recorte é bem mais raro e é honestamente publicável.

### 4.4 Roteiro em 4 fases

**Fase A — Medir o baseline (2 semanas)**
Não mude nada ainda. Instrumente e meça o pipeline atual com 3 empresas, depois 30, depois
100. Produza a curva. Você precisa do "antes" antes de propor o "depois".

**Fase B — Escalar a ingestão (3–4 semanas)**
Concorrência com *backpressure* na coleta CVM/B3, *upsert* idempotente por versão de
formulário, ingestão incremental, carga em lote (`add_all`, `COPY`). Meta: universo completo.

**Fase C — Camada de armazenamento (2–3 semanas)**
Índices compostos guiados por `EXPLAIN ANALYZE`, particionamento de
`financial_statement_item` por período, paginação por *keyset*, materialized views para as
métricas mais consultadas.

**Fase D — Recuperação vetorial e o experimento de grounding (3–4 semanas)**
Embeddings de notícias e de trechos de DFP no `pgvector` que já está lá. Compare o harness
de eval **com e sem** recuperação. O resultado esperado é uma tabela de antes/depois em
`evidence_grounding` e `true_hallucination_count`.

### 4.5 Como isso vira nota e elogio do orientador

- **Fase A + B** entregam gráficos de escalabilidade (throughput × volume) — o vocabulário
  da disciplina de dados em massa.
- **Fase C** entrega análise de índice e plano de consulta (`EXPLAIN ANALYZE`) — mostra que
  você sabe *por que* um banco fica lento, não só que ficou.
- **Fase D** entrega um experimento controlado com métrica de qualidade de IA — a parte que
  a maioria dos trabalhos de dados em massa não tem.
- E tudo isso dentro de um repositório real, com licença Apache-2.0, do próprio professor
  da disciplina. Isso não é exercício de laboratório: é contribuição para software que
  existe.

---

## 5. Como abordar o autor (etiqueta de contribuição)

Como não há issues abertas e o projeto é solo, a ordem importa:

1. **Abra uma issue antes do PR** descrevendo o que você pretende fazer. Em projeto de
   autor único, PR surpresa grande costuma morrer sem review.
2. **Comece pelo PR 0.1** (correção do `docs/evaluation.md`). É pequeno, correto, e
   estabelece que você lê os artefatos com atenção. Isso compra credibilidade para o PR maior.
3. **Um PR por assunto.** O autor usa Cursor Bugbot e CodeRabbit (visíveis nos corpos dos
   PRs #1 e #2) — ou seja, revisão automatizada já está no fluxo. PRs grandes e mistos
   geram ruído.
4. **Respeite as invariantes do projeto** (seção 6). São a parte não-negociável.
5. **Proponha a Fase D como colaboração**, não como PR. Investigação de pesquisa se combina
   antes, ainda mais se vai virar artigo com o nome dele.

---

## 6. Armadilhas — o que NÃO fazer

Ler os docs com atenção poupa você de um PR rejeitado:

| Armadilha | Por quê |
| --- | --- |
| Deixar o LLM calcular ou arredondar número | Quebra a princípio central; validação e eval tratam o valor determinístico como correto |
| Adicionar um *scheduler* dentro da aplicação | `docs/evaluation.md` diz explicitamente: "Do not add an application scheduler" — automação é externa |
| Fazer `pytest` padrão entrar em `evals/` | `testpaths = ["tests"]` é deliberado; eval é lento e exige Ollama |
| Encher métricas ausentes com zero | O projeto mantém `null` para token desconhecido e `Not applicable` para métrica não suportada — nunca `0` |
| Adicionar provider de filesystem "normal" sobre o sandbox | Invariante de composição; quebra o carregamento do profile |
| Trocar `unavailable` por erro | `METRIC_UNSUPPORTED_FOR_PROFILE` é semanticamente distinto de formulário ausente |
| Usar vocabulário BUY/SELL/HOLD | A postura é `FAVORABLE`/`NEUTRAL`/`UNFAVORABLE`, analítica |

---

## 7. Resumo executivo

| | |
| --- | --- |
| **O que é** | Estudo de AI Engineering sobre dados financeiros brasileiros, com fronteira rígida entre cálculo determinístico e interpretação por LLM |
| **O que mais impressiona** | O harness de avaliação: gates numéricos de grounding e alucinação, com histórico imutável |
| **Maior força** | Disciplina arquitetural — o LLM nunca é fonte da verdade |
| **Maior fraqueza** | Não tem "massa": 3 empresas, 2 períodos, `pgvector` instalado e morto |
| **Primeiro PR** | Corrigir `docs/evaluation.md` (tabela de runs desatualizada) |
| **PR de maior valor** | CI com service container `pgvector` |
| **Âncora de mestrado** | Escalar de 3 → ~700 emissores, medir o que quebra, e testar se recuperação vetorial melhora o grounding |
