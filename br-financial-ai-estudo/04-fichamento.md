# FICHAMENTO

**UNIVERSIDADE FEDERAL DE SERGIPE — PROCC**
**DISCIPLINA:** Tópicos Avançados em Engenharia de Software e Sistemas de Informação
**SEMESTRE:** 2026/2 — **Prof. Dr. Fabio Gomes Rocha**

---

## Referência bibliográfica completa

MUSE, Biruk Asmare; NAFI, Kawser Wazed; KHOMH, Foutse; ANTONIOL, Giuliano.
**Data-access performance anti-patterns in data-intensive systems.** *Empirical Software
Engineering*, v. 29, art. 144, 35 p., 2024. DOI: 10.1007/s10664-024-10535-8.

> **Nota sobre as versões (ler antes de citar).** O PDF distribuído em aula
> (`01-data-access-anti-patternsPT.pdf`) é a **versão preliminar** do artigo:
> `arXiv:2208.08918v1`, de 18 ago. 2022, com **7 páginas**, depositada como *pré-print*.
> Ela descreve o estudo em andamento — a Seção IV chama-se **"PLANO DE EXECUÇÃO"** e o
> texto afirma "os passos que *planejamos* seguir para responder às questões de pesquisa".
> A versão **publicada e definitiva** é a de *Empirical Software Engineering* (EMSE),
> v. 29, art. 144, 2024, com **35 páginas**, que traz a taxonomia consolidada e os
> resultados da pesquisa com desenvolvedores. A citação correta para um fichamento é a
> **de 2024**; o pré-print de 2022 serve como registro do *gap* e da evolução do método.
> *Atenção: a paginação das duas versões é diferente — todas as citações literais abaixo
> foram localizadas no pré-print e devem ser reposicionadas na versão EMSE.*

---

## Objetivos

- **Identificar** antipadrões de desempenho de acesso a dados prevalentes em sistemas
  intensivos em dados baseados em NoSQL e em persistência poliglota.
- **Categorizar** os antipadrões identificados em uma taxonomia de causas-raiz, agrupada
  em categorias de alto nível.
- **Validar** empiricamente a relevância e a criticidade percebidas desses antipadrões
  junto a desenvolvedores da indústria.
- **Estender** o catálogo pré-existente de antipadrões (SHAO et al., 2020), que havia sido
  derivado exclusivamente de bancos relacionais/SQL e de poucas aplicações web.

---

## Metodologia

**Estudo empírico com abordagem mista (qualitativa e quantitativa)**, organizado em torno
de duas questões de pesquisa: **RQ1** — quais são os antipadrões prevalentes? **RQ2** —
como os desenvolvedores percebem sua relevância?

A construção do corpus seguiu um **funil de seleção em cinco etapas** (mineração de
repositórios):

| Etapa | Procedimento | Resultado |
| --- | --- | --- |
| 1 | Busca na GitHub REST API v3 por repositórios que mencionem bancos NoSQL populares (lista do Eclipse JNoSQL) em título, descrição ou README | 20.340 candidatos |
| 2 | Filtro de qualidade: repositório ativo (< 1 ano), não espelhado, ≥ 100 KB, ≥ 2 estrelas | 3.264 NoSQL |
| 3 | Filtro de idioma com `langdetect` | 2.498 NoSQL / 1.604 poliglota |
| 4 | Ranqueamento por número de issues e corte nos 150 melhores de cada grupo, seguido de inspeção manual de descrição, código, README e issues | 162 sistemas (75 NoSQL + 87 poliglota) |
| 5 | Coleta de *todas* as issues resolvidas com `PyGithub` | 526.672 (NoSQL) + 257.840 (poliglota) |

Para os **sistemas poliglotas**, a partida foi o trabalho de Benats et al. (2021) sobre o
Libraries.IO: 42.176 projetos → 6.877 com ao menos dois modelos de banco → 2.172 após o
filtro temporal.

Da massa coletada, os **problemas de desempenho de acesso a dados** foram extraídos por
uma **consulta Elasticsearch** construída com três grupos de palavras-chave unidos por
`AND` — desempenho (`performance`, `slow`, `timeout`, `heavy`), acesso a dados (`read`,
`write`, `search`, `update`, `delete`, `load`) e banco de dados (`data`, `database`,
`query`, `schema`, `index`, `cache`, `table`, `partition`, `document`) — aplicada ao
**título e ao corpo** da issue, com ajustes iterativos para reduzir falsos positivos.
Resultado: **3.760 issues NoSQL + 2.645 poliglotas**.

A construção da taxonomia (RQ1) usou **codificação aberta** com dois autores rotulando em
rodadas de 100 rótulos até a **saturação**, cada issue revisada por dois autores e
conflitos resolvidos por discussão, seguidas de uma sessão de ***card sorting*** para
agrupar os rótulos em categorias de alto nível. A validação (RQ2) usa **survey** com
escala Likert de 1 a 5 (não crítico → altamente crítico), recrutamento via LinkedIn,
critério de inclusão de ao menos **um ano de experiência industrial** com NoSQL ou
persistência poliglota, meta de **≥ 40 respostas** e aprovação ética.

> **Resultado publicado (EMSE 2024):** **14 novos antipadrões** de desempenho de acesso a
> dados, organizados em **sete categorias de alto nível**, em sistemas implementados em
> Java. Os três antipadrões avaliados como **mais críticos** pelos desenvolvedores foram:
> ***Improper Handling of Node Failures***, ***Using Synchronous Connection*** e
> ***Inefficient Driver API***.

---

## Fontes

- **GitHub** — repositórios, issues (título, corpo, rótulos, estado, datas, comentários) e
  metadados de estrelas, forks e tamanho de código.
- **Eclipse JNoSQL** — lista de referência dos bancos NoSQL populares.
- **Libraries.IO** e o levantamento de **Benats et al. (2021)** — base para identificar
  projetos com persistência poliglota.
- **Elasticsearch** — indexação e busca das issues.
- **LinkedIn** — recrutamento dos participantes da survey.
- **Literatura de apoio** — principalmente KARWIN (2010), *SQL Antipatterns*; SHAO et al.
  (2020), catálogo anterior de antipadrões; trabalhos anteriores dos próprios autores
  (MUSE et al., 2020; 2022a; 2022b); e KLEPPMANN (2017), *Designing Data-Intensive
  Applications*.
- **Pacote de replicação** público dos autores, com a lista de sistemas, o conjunto de
  dados e a ferramenta de rotulagem.

---

## Principais conceitos utilizados pelo autor

> Citações verificadas no pré-print (7 p.). Reposicionar na paginação da versão EMSE.

- "Aproveitar a vasta quantidade de dados heterogêneos gerados por humanos e máquinas
  para obter insights acionáveis está se tornando o foco de atenção tanto na indústria
  quanto na comunidade de pesquisa." (p. 1)
- "Assim como o software tradicional, esses sistemas são propensos a dívidas técnicas,
  introduzidas para lidar com a pressão de restrições de tempo e recursos sobre os
  desenvolvedores." (p. 1)
- "Especificar antipadrões de desempenho no acesso a dados é importante, pois é o primeiro
  passo antes da construção de ferramentas de detecção automática que são utilizadas para
  estudar a prevalência e o impacto desses antipadrões." (p. 1)
- "Devido às diferenças nos mecanismos de acesso a dados entre bancos de dados relacionais
  e NoSQL, os antipadrões de desempenho identificados em [estudos anteriores] podem não
  ser generalizáveis para sistemas de uso intensivo de dados baseados em NoSQL." (p. 2)
- "Embora a vantagem de escolher o banco de dados com base na natureza dos dados seja
  clara, as questões associadas de projeto, implementação e manutenção não foram bem
  investigadas." (p. 2)

**Conceitos estruturantes:** *dívida técnica* (technical debt); *antipadrão de desempenho*
(comparação com *code smells* e com os antipadrões SQL de Karwin); *sistemas intensivos em
dados*; *NoSQL*; *persistência poliglota*; *codificação aberta*; *saturação de rótulos*;
*card sorting*; e *pacote de replicação* como artefato de reprodutibilidade.

---

## Principais conclusões do autor

> **Atenção metodológica:** o pré-print de 2022 **não possui seção de resultados** — suas
> seções são I. Introdução, II. Trabalhos Relacionados, III. Método de Estudo,
> IV. Plano de Execução, V. Limitações e Referências. As conclusões abaixo vêm da versão
> publicada (EMSE, 2024) e do *gap* declarado no pré-print.

- Os antipadrões de desempenho de acesso a dados catalogados para bancos **relacionais/SQL
  não são diretamente generalizáveis** para ambientes NoSQL e de persistência poliglota,
  porque os mecanismos de acesso a dados diferem entre os paradigmas.
- Foram identificados **14 novos antipadrões**, agrupados em **sete categorias de alto
  nível**, ampliando o catálogo anterior que cobria apenas SQL.
- A survey com desenvolvedores confirmou a **relevância prática** do catálogo e permitiu
  **priorizar** os antipadrões por criticidade, com destaque para *Improper Handling of
  Node Failures*, *Using Synchronous Connection* e *Inefficient Driver API*.
- A catalogação serve de **base para ferramentas de detecção automática** (análise estática
  e dinâmica) voltadas ao desempenho de sistemas intensivos em dados.
- As descobertas ajudam equipes de qualidade a **priorizar a correção** por criticidade, e
  não por ordem de descoberta.

---

## Comentário pessoal

O trabalho ocupa uma lacuna bem delimitada: enquanto a literatura de dívida técnica em
acesso a dados se consolidou sobre bancos relacionais — com catálogos de *SQL smells* e
ferramentas de detecção automática já maduras —, os paradigmas que efetivamente sustentam
sistemas intensivos em dados contemporâneos (NoSQL e persistência poliglota) permaneciam
pouco investigados. A contribuição não é apenas ampliar um catálogo: é demonstrar que **a
mudança de paradigma de persistência invalida parte do conhecimento acumulado**, porque
altera a natureza das causas-raiz.

Dois aspectos metodológicos merecem destaque. Primeiro, o **funil de mineração é
auditável**: cada etapa registra quantos artefatos entraram e saíram, o que permite ao
leitor julgar o viés de seleção em vez de apenas confiar no resultado. Segundo, a
**triangulação entre mineração de repositórios e survey** resolve uma fragilidade comum a
estudos puramente baseados em issues — o fato de que um problema relatado não é
necessariamente um problema percebido como relevante por quem desenvolve.

A principal limitação, declarada pelos próprios autores, é a **validade externa**: o
corpus é de código aberto, e os autores reconhecem que não podem garantir que os
resultados se transfiram para sistemas industriais. Há também um viés de **validade
interna** na seleção dos 162 sistemas, escolhidos entre os que possuem o maior número de
issues — decisão pragmaticamente necessária, mas que favorece projetos grandes e
maduros. O recorte em **Java** na versão publicada é uma restrição adicional de
generalidade que a leitura deve registrar.

Do ponto de vista do meu interesse em **governança de dados e transparência**, o artigo
oferece algo além do catálogo: um **método replicável**. O funil — mineração de
repositórios, filtragem por palavras-chave, codificação aberta até saturação, *card
sorting* e validação por survey — é diretamente transferível para o estudo de sistemas de
dados abertos governamentais, onde os mesmos antipadrões tendem a se manifestar com
consequências de auditoria e prestação de contas, e não apenas de desempenho. Essa
transferência de domínio é, a meu ver, a extensão mais promissora do trabalho.

---

## Palavras-chave

Antipadrões de desempenho; Sistemas intensivos em dados; NoSQL; Persistência poliglota;
Mineração de repositórios; Dívida técnica.

---

## Checklist de verificação antes da entrega

- [ ] Baixar a versão **EMSE 2024** (35 p.) pelo Portal de Periódicos da CAPES —
      DOI `10.1007/s10664-024-10535-8`
- [ ] **Reposicionar todas as citações** na paginação da versão EMSE (a do pré-print não
      serve)
- [ ] Extrair da versão publicada: as **7 categorias de alto nível** e a descrição
      dos 14 antipadrões
- [ ] Extrair os **números da survey** (nº de respondentes, distribuição de criticidade)
- [ ] Confirmar a seção de *threats to validity* da versão publicada
- [ ] Preencher o fichamento no modelo oficial e submeter em
      https://fichamento.lovable.app
- [ ] Ensaiar a apresentação oral de 10–15 min (ver guia separado)
