# Guia da apresentação oral (10–15 min) — e a nota sobre o modelo fornecido

---

## PARTE 1 — A NOTA IMPORTANTE: confira antes de apresentar

O arquivo `Modelo_para_fichamento.doc` que você recebeu **não descreve o PDF que foi
distribuído com ele**. Isso precisa ser entendido antes da apresentação, porque a
diferença é justamente do tipo que o professor cobra.

### O que o modelo afirma

> "Em segundo lugar, **realizaram** uma pesquisa (survey) com desenvolvedores industriais
> para avaliar a relevância prática dos problemas catalogados."

> "O texto está estruturado com introdução, motivação, trabalhos relacionados, metodologia
> de coleta, **taxonomia desenvolvida**, **validação dos resultados** e ameaças à validade."

### O que o PDF de 7 páginas realmente contém

Seções: **I. Introdução · II. Trabalhos Relacionados · III. Método de Estudo ·
IV. Plano de Execução · V. Limitações · Referências.**

A Seção IV diz textualmente:

> "Atualmente, concluímos as etapas de coleta e extração de dados do método de estudo.
> Portanto, descreveremos a seguir os passos que **planejamos** seguir para responder às
> questões de pesquisa."

E enumera **oito passos futuros** — preparar a ferramenta de rotulagem, iniciar a primeira
rodada, repetir até saturação, fazer *card sorting*, recrutar participantes, obter
aprovação ética, aplicar a survey, analisar as respostas. Ou seja: **a taxonomia ainda não
existia e a survey ainda não havia sido feita.** É um *research proposal*, não um estudo
concluído. Verifiquei também que o arXiv **não tem versão posterior** (`2208.08918` possui
apenas a v1).

### Por que o modelo diz o contrário — e por que ele não está "errado"

Existe uma **versão publicada e completa**: *Empirical Software Engineering*, v. 29,
art. 144, 2024, 35 páginas, DOI `10.1007/s10664-024-10535-8`. É lá que estão os
**14 antipadrões**, as **7 categorias de alto nível** e os resultados da survey. O modelo
descreve corretamente **essa** versão — mas a referencia como `arXiv:2208.08918v1`, que é
o pré-print de 2022, sem resultados.

Provavelmente a versão EMSE é a que o professor pretende (as slides exigem "periódicos
ISI/Scopus ou conferências A1/A2", e a EMSE é exatamente isso). O PDF de 7 páginas é
apenas o texto de acesso livre.

### Dois problemas concretos no modelo

1. **Referência:** cita o pré-print em vez do artigo de periódico. Para um fichamento de
   disciplina que exige veículo de alto impacto, a citação correta é a de 2024.
2. **Nome do primeiro autor:** o modelo traz "ASMARE, Musa Biruk". O correto é
   **MUSE, Biruk Asmare** — "Asmare" é o nome do meio, e "Muse" é o sobrenome. O erro vem
   da tradução automática do PDF, que ainda produziu um artefato visível no cabeçalho:
   *"Khomh errado"* (o tradutor verteu "Foutse Khomh" + "wrong" para o português). **Não
   replique isso**: em citação, o sobrenome é `MUSE`.

### Como usar isso a seu favor (em vez de virar problema)

Não aponte o erro do modelo em sala. **Transforme em demonstração de método.** Diga:

> "Ao localizar o artigo, apliquei o *cone do futuro* que vimos na Aula 1: parti do
> pré-print de 2022, verifiquei quem o citou depois e encontrei a versão consolidada
> publicada na *Empirical Software Engineering* em 2024, com 35 páginas. O pré-print
> descreve o plano; o artigo de periódico traz os resultados — 14 antipadrões em 7
> categorias. Fiquei com a versão de 2024 para o fichamento."

Isso mostra exatamente a competência que a Aula 1 cobra, e resolve a divergência sem
constrangimento para ninguém. **Antes disso, baixe a versão EMSE** pelo Portal de
Periódicos da CAPES (o próprio Slide 15 da Aula 1 lembra que o acesso está disponível
para alunos do PROCC/UFS).

---

## PARTE 2 — ROTEIRO DA APRESENTAÇÃO

### 0:00–1:30 · Hook (por que isso importa)

Não comece pelo título. Comece pelo problema concreto:

> "Um sistema que lê e grava em três bancos diferentes — MongoDB para o catálogo, Redis
> para sessão, PostgreSQL para transações — pode ficar lento por um motivo que não aparece
> em nenhum *profiler* de CPU: a **forma como o código acessa os dados**. E o catálogo de
> boas práticas que usamos para detectar isso foi construído **inteiramente sobre bancos
> relacionais**."

Frase de efeito para fechar o bloco: *o conhecimento que temos sobre antipadrões de acesso
a dados não foi validado para a arquitetura que realmente usamos hoje.*

### 1:30–3:30 · Gap (o que a literatura não resolveu)

Apresente o gap em três camadas, do mais amplo ao mais específico:

1. **Dívida técnica em DIS é pouco investigada** — a literatura de *code smells* e dívida
   técnica amadureceu sobre software tradicional.
2. **O catálogo existente é enviesado** — Shao et al. (2020) compilaram 24 antipadrões da
   literatura + 10 novos, mas analisando **7 aplicações web baseadas em bancos
   relacionais**. A conclusão do próprio artigo: esses antipadrões **podem não ser
   generalizáveis** para NoSQL, porque o mecanismo de acesso é diferente.
3. **Persistência poliglota é o caso menos estudado** — usar vários bancos no mesmo
   sistema traz vantagem clara, mas "as questões associadas de projeto, implementação e
   manutenção não foram bem investigadas".

Cite a RQ1 e a RQ2 e diga que o artigo as responde.

### 3:30–6:00 · Método (a parte que o professor vai cobrar)

Aqui **não leia o método: mostre o funil**. Desenhe no slide a redução de números, porque
é ela que prova o rigor:

```
20.340 repositórios candidatos
   → 3.264 após filtro de qualidade (ativo, não-espelhado, ≥100 KB, ≥2 estrelas)
   → 2.498 após filtro de idioma (langdetect)
   → 150 melhores por nº de issues, inspeção manual
   → 162 sistemas (75 NoSQL + 87 poliglota)
   → 526.672 + 257.840 issues coletadas (PyGithub)
   → 3.760 + 2.645 issues de desempenho (query Elasticsearch)
   → codificação aberta até saturação → card sorting → taxonomia
   → survey (LinkedIn, ≥1 ano de experiência, Likert 1–5, ≥40 respostas)
```

Destaque **três decisões de método** e por que elas importam:

- **Palavras-chave com `AND`, aplicadas a título *e* corpo** — reduz falso positivo e é
  detalhe que os autores descrevem como iterativo.
- **Cada issue rotulada por dois autores, conflitos por discussão** — mitiga viés do
  pesquisador. É *inter-rater agreement* sem a estatística formal, e vale comentar.
- **Triangulação mineração + survey** — responde à objeção óbvia: "issue aberta" não é o
  mesmo que "problema relevante para quem programa".

### 6:00–9:00 · Resultados

- **14 novos antipadrões**, em **7 categorias de alto nível** (sistemas em Java).
- Os três mais críticos na percepção dos desenvolvedores:
  1. ***Improper Handling of Node Failures***
  2. ***Using Synchronous Connection***
  3. ***Inefficient Driver API***
- Comente o que esses três têm em comum: **nenhum é erro de sintaxe ou de algoritmo** —
  todos são decisões de arquitetura de acesso a dados sob premissas de falha e
  concorrência. Amarre com a Aula 1: são exatamente os pilares de Kleppmann
  (confiabilidade, escalabilidade, manutenibilidade) aparecendo como antipadrão.
- Cite que o artigo referencia **Kleppmann, *Designing Data-Intensive Applications***
  (referência [18]) — o livro-base da disciplina. É uma conexão que o professor vai notar.

### 9:00–11:30 · Crítica e ameaças à validade

Esta é a seção que separa quem leu de quem resumiu. Use a taxonomia da própria Aula 1
(Slide 34):

| Tipo | Ameaça no artigo | Sua avaliação |
| --- | --- | --- |
| **Validade interna** | Sistemas escolhidos entre os que têm **mais issues** → favorece projetos grandes e maduros | Necessário por viabilidade, mas enviesa para projetos ativos; projetos pequenos e abandonados ficam fora |
| **Validade interna** | Rótulos dependem de julgamento humano, mesmo com dois revisores | Mitigado por dupla rotulagem; faltou relatar concordância formal (ex.: kappa) |
| **Validade externa** | Corpus é de **código aberto**, e os próprios autores reconhecem que não garantem transferência para a indústria | Limitação declarada e honesta |
| **Validade externa** | Versão publicada restringe a **Java** | Reduz generalidade para outras linguagens/ecossistemas |
| **Validade de construto** | "Issue resolvida" como proxy de "antipadrão real" | Descrições de issue são frequentemente incompletas ou ambíguas — os autores declaram isso |

**Adicione um ponto que é seu**, não do artigo: a **taxa de issues com descrição
inadequada não é quantificada**. Um número ali — "X% das issues foram descartadas por
descrição insuficiente" — mudaria a confiança no corpus. Isso é contribuição de leitor
crítico.

### 11:30–13:00 · Conexão com a disciplina e com a sua pesquisa

Amarre em três frentes (detalhadas no documento de alinhamento):

1. **NoSQL e LWW** — a Aula 3 mostrou que "maior timestamp vence" pode **descartar dado
   silenciosamente**. Vários antipadrões de acesso a dados são exatamente o padrão de
   escrita que ativa esse risco. Antipadrão de desempenho e perda de dado são o mesmo
   fenômeno visto de dois ângulos.
2. **Persistência poliglota e microsserviços** — a Aula 1 trata persistência poliglota
   como escolha arquitetural central; o artigo mostra o **custo oculto** dessa escolha.
3. **MSR como método** — a Aula 1 apresenta Mineração de Repositórios como método de
   primeira classe. O artigo é um caso exemplar de MSR aplicado, e é replicável para
   **sistemas de dados abertos governamentais**, que é a sua linha de interesse.

### 13:00–15:00 · Preparação para perguntas

Perguntas prováveis do professor e respostas curtas:

**"Qual é a contribuição real, se já existia um catálogo?"**
→ O catálogo anterior era derivado de SQL/relacional. O artigo demonstra que a mudança de
paradigma **invalida parte do conhecimento** e produz 14 antipadrões novos, priorizados
por criticidade percebida.

**"Por que survey e não só mineração?"**
→ Porque issue relatada ≠ problema relevante. A survey valida e **ordena por criticidade**,
o que é o que permite priorizar correção.

**"Isso se aplica a sistemas brasileiros?"**
→ O método sim; os resultados exigem replicação. É exatamente a lacuna que pretendo
atacar.

**"Onde está o threat to validity mais grave?"**
→ Validade externa: corpus de código aberto, restrito a Java na versão publicada, e
selecionado por volume de issues.

**"O que você faria diferente?"**
→ Quantificar a taxa de descarte por descrição inadequada e reportar concordância formal
entre rotuladores.

---

## PARTE 3 — CHECKLIST FINAL

- [ ] Baixar a versão **EMSE 2024** (CAPES) e ler as 35 páginas
- [ ] Confirmar as 7 categorias e o número de respondentes da survey
- [ ] Reler as citações literais **na paginação da EMSE**
- [ ] Montar o slide do funil (é o slide mais importante)
- [ ] Montar a tabela de ameaças à validade
- [ ] Treinar em 12 minutos (o limite é 15)
- [ ] Ter o DOI à mão para a referência
- [ ] Submeter o fichamento em https://fichamento.lovable.app
