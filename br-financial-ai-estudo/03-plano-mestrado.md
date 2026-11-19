# Plano de mestrado — do estudo do professor a um projeto de dados em massa

> Como transformar o `br-financial-ai` em trabalho da disciplina de dados em massa, com
> desenho experimental defensável e contribuição real ao repositório.

---

## 1. A jogada estratégica

Você tem uma combinação incomum e ela deve ser explicitada desde a primeira conversa:

1. O repositório foi **indicado pelo próprio professor da disciplina**.
2. Ele é **público, Apache-2.0, e tem zero issues abertas** — ou seja, há trabalho a
   fazer e a porta está aberta.
3. A maior fraqueza declarada do projeto (3 empresas, `pgvector` ocioso) é **exatamente
   o tema da disciplina**: dados em massa.

A frase que resume a proposta para o orientador:

> "O projeto do professor implementa um pipeline correto e bem avaliado para 3 empresas.
> Minha proposta é investigar o que acontece quando ele vai para ~700, e se a camada de
> recuperação vetorial — que já está provisionada mas não usada — melhora o grounding
> medido pelo harness de avaliação que o próprio projeto já tem."

Isso é forte por três motivos: **não é invenção** (o gap é real e verificável), **não é
trabalho de reimplementação** (você contribui, não reescreve), e **tem métrica
preexistente** (você não precisa convencer ninguém de que sua métrica é válida).

---

## 2. Por que isso É um problema de dados em massa

Um orientador de dados em massa vai perguntar: "onde está o volume?". A resposta precisa
estar pronta.

### 2.1 De onde vem a massa

O universo-alvo é o cadastro de companhias abertas da CVM (`cad_cia_aberta.csv`) cruzado
com os instrumentos listados da B3 — algumas centenas de emissores. Para cada emissor,
por ano:

- 1 formulário DFP (anual), com **versões** de reapresentação
- 3 formulários ITR (trimestrais)
- cada formulário contém **centenas de linhas** de contas contábeis

A tabela `financial_statement_item` é a que explode: `contas × formulários × empresas ×
anos`. Multiplicando, chega-se confortavelmente à casa dos **milhões de linhas** — e é
exatamente aí que decisões de índice, particionamento e plano de consulta deixam de ser
acadêmicas.

Além disso, o objeto JSON/CSV bruto da CVM por formulário é grande, e o arquivo público
`InstrumentsConsolidated` da B3 também. Só isso já justifica uma discussão de ingestão em
lotes, streaming versus batch e custo de I/O.

### 2.2 As quatro dimensões de "massa"

| Dimensão | Situação atual | O que a disciplina cobre |
| --- | --- | --- |
| **Volume** | 3 empresas, 2 períodos | milhões de linhas, particionamento |
| **Velocidade** | ingestão sequencial, sem throughput medido | concorrência, *backpressure*, ingestão incremental |
| **Variedade** | CSV/JSON da CVM, JSON do Yahoo, texto de notícias | normalização, schema evolution, dados sujos |
| **Veracidade** | gates de grounding e alucinação já existem | qualidade de dado *e* qualidade de IA |

A quarta coluna é o diferencial: a maioria dos projetos de dados em massa para na
variedade. Este vai até veracidade **de modelo**.

---

## 3. Desenho experimental

Esta é a seção que impressiona. Não é "vou escalar o projeto"; é um desenho com
hipóteses, variáveis e ameaças à validade declaradas.

### 3.1 Hipóteses

**H1 (escalabilidade da ingestão).** O tempo de ingestão cresce linearmente com o número
de emissores até um ponto de saturação determinado por concorrência e I/O do banco.

**H2 (degradação de consulta).** Sem índices compostos e particionamento, a latência de
`FinancialQueryService` degrada de forma superlinear com o volume — porque o motor passa
a escolher *sequential scan* sobre `financial_statement_item`.

**H3 (recuperação melhora grounding).** Adicionar recuperação vetorial sobre notícias e
trechos de formulários **aumenta** `evidence_grounding` e/ou **reduz**
`true_hallucination_count` em relação ao baseline sem recuperação.

**H4 (custo da recuperação).** O ganho de qualidade de H3 tem custo de latência
mensurável, e existe um ponto de troca aceitável.

### 3.2 Variáveis

| Tipo | Variável |
| --- | --- |
| Independente (Fases A–C) | volume de emissores: 3, 30, 100, ~700 |
| Independente (Fase D) | estratégia de contexto: sem recuperação / com recuperação vetorial |
| Dependente (desempenho) | throughput (emissores/min), p50/p95 de consulta, tempo total de ingestão |
| Dependente (qualidade) | `evidence_grounding`, `factual_consistency`, `true_hallucination_count`, `stance_accuracy` |
| Dependente (custo) | latência de recomendação, tokens de entrada |
| Controle | mesmo modelo (`llama3.1`), temperatura 0, mesmo hardware, mesmos datasets de eval |

**O grupo de controle é o ponto forte:** como o harness de eval é determinístico no
conjunto de fixtures e o modelo roda com temperatura 0, você consegue comparar
"com/sem recuperação" mantendo tudo o mais constante. Isso é raro em trabalhos com LLM.

### 3.3 Ameaças à validade (declare antes que o orientador pergunte)

- **Validade interna:** a Fase D roda sobre os mesmos datasets da Fase A — se os
  datasets forem pequenos (12 casos de tool selection, 8 de notícia, 9 de recomendação),
  o poder estatístico é baixo. *Mitigação:* reportar intervalos e tratar como estudo
  exploratório, não como teste de significância.
- **Validade externa:** `llama3.1` local não representa modelos de fronteira. *Mitigação:*
  o roadmap do projeto já prevê `multi-model evaluation`; replicar com 2–3 modelos é uma
  extensão natural e aumenta muito a contribuição.
- **Validade de construto:** "grounding" aqui é definido pelo avaliador do projeto, com
  suas próprias regras (ignora datas ISO, aceita menção a P/B desde que descrita como
  indisponível). *Mitigação:* documentar a definição operacional e discutir os limites.
- **Validade de conclusão:** latência de inferência local varia com carga da máquina.
  *Mitigação:* múltiplas repetições, mediana, e reportar o desvio.

### 3.4 Reproducibilidade

O projeto já dá o essencial de graça: runs com timestamp, `git_commit` e `git_branch`
registrados no relatório; datasets versionados; gates parametrizados em
`br_financial_ai.eval.thresholds`. Documente a versão de hardware e o comando exato de
cada medição. Guarde os JSONs.

---

## 4. Cronograma de um semestre

### Semanas 1–2 — Fundação
- Rodar o projeto localmente de ponta a ponta: `uv sync`, `docker compose up -d`,
  `alembic upgrade head`, `bootstrap`, `sync-news PETR4`, API, e um `eval --profile fast`.
- **Entregável:** ambiente funcionando + suas primeiras medições do baseline de 3
  empresas (o "antes" de tudo).
- **Paralelo:** abrir a primeira issue no repositório.

### Semanas 3–4 — Primeiro PR e instrumentação
- PR 0.1: corrigir `docs/evaluation.md` (tabela de runs desatualizada — ver documento 01).
- PR 0.2: CI com *service container* `pgvector`.
- Instrumentar e medir a ingestão atual: quanto tempo para 3 empresas, quanto por
  formulário.
- **Entregável:** 1–2 PRs mergeados + curva baseline.

### Semanas 5–8 — Fase A e B: escalar a ingestão
- Coleta concorrente com *backpressure*; *upsert* idempotente por versão de formulário;
  ingestão incremental.
- Rodar para 30, 100 e o universo completo.
- **Entregável:** gráfico de escalabilidade (throughput × volume) + tabela de tamanho de
  tabela por faixa.

### Semanas 9–11 — Fase C: armazenamento
- `EXPLAIN ANALYZE` nas consultas quentes; propor índices compostos; particionar
  `financial_statement_item` por período; paginação por *keyset*.
- **Entregável:** tabela antes/depois de plano de consulta e latência p50/p95. Este é o
  material mais "clássico" de dados em massa e o mais fácil de defender.

### Semanas 12–15 — Fase D: recuperação vetorial e o experimento
- Popular `pgvector` com embeddings de notícias e de trechos de DFP.
- Rodar o harness de eval **com e sem** recuperação, múltiplas vezes.
- **Entregável:** a tabela central do artigo — grounding e alucinação com/sem recuperação,
  mais o custo de latência associado.

### Semana 16 — Escrita
- Artigo (documento 02 é o rascunho), pôster ou apresentação.
- **Entregável:** submissão.

> Se o semestre for mais curto, **corte a Fase D e vá até a C**. Um estudo de
> escalabilidade completo vale mais que quatro fases pela metade.

---

## 5. O que levar para a primeira conversa com o orientador

Leve cinco coisas, nesta ordem:

1. **Uma página de diagnóstico.** O projeto é sólido e bem avaliado; sua fraqueza é
   escala — 3 empresas, 2 períodos, `pgvector` instalado e não usado. Números medidos,
   não impressões.
2. **A pergunta de pesquisa** em uma frase (seção 1).
3. **As quatro hipóteses** (seção 3.1) — mostra que você sabe formular, não só executar.
4. **O cronograma** (seção 4) com entregáveis e um ponto de corte declarado.
5. **A oferta de contribuição:** PRs com o nome dele no projeto dele. Deixe claro que
   você quer contribuir, não só extrair.

**Perguntas para fazer a ele:**
- Posso abrir issues e PRs no repositório, ou prefere que eu trabalhe em fork?
- O escopo pode incluir o universo completo da B3, ou há restrição de rate limit na
  CVM/B3 que eu deva considerar?
- Você tem preferência entre priorizar a Fase C (armazenamento) ou a D (recuperação)?
- A disciplina aceita artigo curto ou exige relatório técnico?

---

## 6. Como não perder tempo (erros comuns)

| Erro | Consequência | Como evitar |
| --- | --- | --- |
| Começar pela Fase D (a parte vistosa) | Sem baseline, não há comparação; o experimento vira anedota | Sempre meça o "antes" primeiro |
| Reescrever o projeto com Spark/Airflow | Você perde o semestre em infra e não contribui | Escale **dentro** da stack existente; justifique cada nova peça |
| Rodar eval com o dataset FAST e concluir sobre o FULL | Conclusão inválida — os datasets diferem | Nunca compare FAST com FULL |
| Mexer no caminho determinístico | Quebra a invariante central do projeto | O LLM nunca calcula; não relaxe isso |
| Otimizar antes de medir | Índice que o planejador ignora | `EXPLAIN ANALYZE` **antes** de criar índice |
| Deixar o LLM no caminho de `GET` | Quebra a separação de 99% da latência | `GET` é determinístico, `POST` é IA |
| Ignorar o rate limit da CVM/B3 | Ingestão quebra no meio e você perde o dia | *Backpressure* e retry com backoff desde o início |

---

## 7. O que isso rende

| Produto | Valor |
| --- | --- |
| 2–4 PRs em repositório real do professor | Participação em projeto aberto, Apache-2.0 |
| Curva de escalabilidade (throughput × volume) | Núcleo de um artigo de dados em massa |
| Análise de plano de consulta e índices | Mostra domínio de banco, não só de framework |
| Experimento de grounding com/sem recuperação | A parte que a maioria dos trabalhos não tem |
| Artigo publicado | Rascunho pronto no documento 02 |

---

## 8. Próximos 7 dias (checklist)

- [ ] `git clone` e rodar `uv sync`
- [ ] `docker compose up -d` e `uv run alembic upgrade head`
- [ ] `uv run br-financial-ai bootstrap` e `sync-news PETR4 --limit 10`
- [ ] Subir a API e bater em `GET /health`
- [ ] Instalar Ollama e puxar `llama3.1`
- [ ] Rodar `uv run pytest -q` (primeiro sem banco, para ver o que falha, depois com)
- [ ] Ler `docs/architecture.md` e `docs/evaluation.md` com o documento 01 do lado
- [ ] Abrir a issue 0.1 (correção da doc de avaliação)
- [ ] Medir o tempo de `bootstrap` com as 3 empresas — **este é o seu primeiro dado**
