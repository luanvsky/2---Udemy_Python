# Modelo de Artigo — Anti-padrões de Desempenho em Acesso a Dados em Sistemas Intensivos em Dados (DIS)
## Conectando a Taxonomia de Asmare et al. (2022) com Física de I/O, Sincronização Distribuída e Governança de Dados no Setor Público

---

**Disciplina:** Tópicos Avançados em Eng. de Software e Sistemas de Informação  
**Programa:** PROCC / UFS — Mestrado/Doutorado  
**Professor:** Dr. Fabio Gomes Rocha  
**Estrutura exigida:** IMRAD + Fichamento Individual + Peer Review em grupo  

---

## 1. TÍTULO PROPOSTO (versão de trabalho)

> **Anti-padrões de Desempenho no Acesso a Dados em Sistemas Intensivos em Dados: Uma Análise sob a Ótica dos Limites Físicos de I/O, Sincronização Temporal e Conformidade em Ambientes de Persistência Poliglota**

**Subtítulo alternativo (mais aplicado ao seu contexto):**  
> **Da Taxonomia de Anti-padrões à Prática de Governança: Mapeamento de Riscos de Desempenho em Sistemas Contábeis e de Transparência Baseados em NoSQL/Poliglota**

---

## 2. ESTRUTURA IMRAD DETALHADA COM ORIENTAÇÕES POR SEÇÃO

---

### **ABSTRACT** (150–250 palavras)
**Deve conter:** Contexto (DIS + persistência poliglota), Lacuna (anti-padrões de desempenho pouco estudados em NoSQL/poliglota), Método (estudo qualitativo + survey validation), Resultados principais (14 anti-padrões, 7 categorias, top 3 críticos), Implicações para governança/conformidade (seu diferencial), Conclusão.

---

### **1. INTRODUÇÃO** (∼2–3 páginas)

#### 1.1 Contextualização do Problema (O "Porquê")
- **Sistemas Intensivos em Dados (DIS)** como paradigma dominante (Aula 02): gargalo não é CPU, é **I/O-bound** (barramento disco/RAM/rede).
- **Persistência Poliglota** como norma arquitetural: NoSQL (documentos, chave-valor, colunar, grafo) + relacional coexistendo.
- **Pressão de entrega** → dívida técnica de acesso a dados (código que lê/escreve) → **anti-padrões de desempenho** (não apenas bugs funcionais).

#### 1.2 Lacuna de Pesquisa (O "O quê falta")
- Literatura clássica foca em **bancos relacionais/SQL** (Shao et al., 2021; anti-padrões de acesso a dados tradicionais).
- **Poucos estudos** em **NoSQL + persistência poliglota** (Asmare et al., 2022 — *o artigo base*).
- **Ausência de conexão** entre anti-padrões de desempenho e **limites físicos** (latência, write amplification, clock drift, backpressure) + **governança/conformidade** (seu nicho).

#### 1.3 Perguntas de Pesquisa (RQs)
| RQ | Formulação | Origem |
|----|------------|--------|
| **RQ1** | Quais anti-padrões de desempenho de acesso a dados são prevalentes em sistemas DIS baseados em NoSQL/poliglota? | Asmare et al. (2022) — RQ1 original |
| **RQ2** | Como esses anti-padrões se manifestam sob a ótica dos **limites físicos de I/O** (Aula 02) e **sincronização temporal distribuída** (Aula 03)? | **Nova — sua contribuição teórica** |
| **RQ3** | Quais os impactos desses anti-padrões em **conformidade, auditoria e transparência** em sistemas do setor público federal? | **Nova — seu contexto de aplicação** |

#### 1.4 Objetivo Geral e Específicos
- **Geral:** Estender a taxonomia de Asmare et al. (2022) incorporando a **física do I/O** e a **sincronização temporal** como lentes explicativas, e mapear implicações para **governança de dados no setor público**.
- **Específicos:**
  1. Classificar os 14 anti-padrões conforme **causa-raiz física** (I/O, rede, tempo, CPU).
  2. Correlacionar anti-padrões com **riscos de conformidade** (TCU, CGU, LAI, LRF).
  3. Propor **checklist de governança** para arquitetos/DBAs/auditores de TI.

#### 1.5 Contribuições
1. **Teórica:** Extensão da taxonomia com dimensões físicas/temporais (Aulas 02–03).
2. **Metodológica:** Fichamento estruturado + matriz de criticidade anti-padrão × risco de conformidade.
3. **Prática:** Checklist de governança aplicável a SIAFI, SICONV, Portal Transparência, e-SIC, Data Lakes gov.br.

---

### **2. FUNDAMENTAÇÃO TEÓRICA / TRABALHOS RELACIONADOS** (∼3–4 páginas)

#### 2.1 Paradigma Data-Intensive e Limites Físicos (Aula 02)
| Conceito | Referência da Aula | Relevância para o Artigo |
|----------|-------------------|--------------------------|
| **Compute vs. Data-Intensive** | Slide 5 | Justifica por que anti-padrões de *acesso a dados* são o gargalo central |
| **Blocos de construção DIS** | Slide 6 | DB, Cache, Índice, Stream — cada um é superfície de anti-padrões |
| **Três dimensões (Volume, Velocidade, Variabilidade)** | Slide 7 | Variabilidade ⇄ esquema flexível NoSQL ⇄ anti-padrões de *query translation* |
| **Modelos de escalabilidade** (Shared-Memory/Disk/Nothing) | Slide 8 | Anti-padrão "Single Connection for Data Access" viola Shared-Nothing |
| **Largura de banda de barramento** (Jeff Dean numbers) | Bloco 2 | Base quantitativa para argumentar *custo* de cada anti-padrão |
| **LSM Trees, Write Amplification (WAF), Compaction pauses** | Bloco 2 | Explicam anti-padrões de *Indexação* e *Driver/API Ineficiente* |
| **Bounded vs. Unbounded datasets** (Batch vs. Streams) | Bloco 3 | Anti-padrões de *Cache* e *Connection* afetam streams diferentemente |
| **Axioma do Log / Backpressure / Drop vs. Buffer** | Bloco 4 | Conecta anti-padrão "Inadequate Node Failure Handling" a *drop silencioso* |

#### 2.2 Física do Tempo e Sincronização Distribuída (Aula 03)
| Conceito | Referência da Aula | Conexão com Anti-padrões |
|----------|-------------------|--------------------------|
| **Clock drift (PPM), NTP, monotonic clocks** | Bloco 1 | Anti-padrão "Duplicate Requests" + "Synchronous Connection" → *race conditions* temporais |
| **LWW (Last-Write-Wins) — perda silenciosa** | Bloco 3 | Anti-padrão "Inefficient Cache Invalidation" + "Wrong API Function" → *dados perdidos sem log* |
| **TrueTime, Lamport, Vector Clocks** | Bloco 4 | Alternativas a LWW para *ordenação causal* em sistemas poliglotas |
| **SIEM/Telemetria: watermarks, correlação causal** | Bloco 5 | Anti-padrões geram *ruído* em logs → falsos positivos/negativos em SOC |

#### 2.3 Dívida Técnica e Anti-padrões de Acesso a Dados
- **Definição:** Dívida técnica = decisões subótimas intencionais/non-intencionais que comprometem qualidade futura (Alves et al., 2016).
- **Anti-padrão de desempenho:** Solução recorrente que *parece funcionar* mas degrada *latência, throughput, escalabilidade, disponibilidade*.
- **Trabalhos base:**
  - Shao et al. (2021): Anti-padrões em SQL/relacional.
  - **Asmare et al. (2022) — ARTIGO BASE:** 14 anti-padrões, 7 categorias, NoSQL + poliglota, validação com desenvolvedores (Kappa=0,764).

#### 2.4 Governança de Dados, Conformidade e Setor Público
| Normativo/Referencial | Exigência Relacionada a Desempenho de Acesso a Dados |
|----------------------|--------------------------------------------------------|
| **ISO 38500 / ISO 8000** | Governança de TI / Qualidade de dados (disponibilidade, integridade, tempestividade) |
| **LAI (Lei 12.527/11)** | Acesso à informação em tempo razoável → *latência de consulta* |
| **Decreto 10.139/19 (Dados Abertos)** | APIs performáticas, SLA de resposta |
| **LRF / Lei 4.320/64** | Tempestividade do fechamento contábil → *batch windows* |
| **Acórdãos TCU (ex: 2022/2023)** | Indisponibilidade de sistemas estruturantes = achado de auditoria |
| **IN STN/CGU** | Padronização de stacks, monitoramento, gestão de incidentes |

---

### **3. METODOLOGIA** (∼2 páginas)

#### 3.1 Estratégia de Pesquisa
- **Estudo qualitativo exploratório** (como Asmare et al.) + **extensão teórica** (lentes físicas/temporais) + **estudo de caso aplicado** (setor público).
- **Fases:**
  1. **Fichamento estruturado** do artigo base (modelo do professor).
  2. **Análise de conteúdo** dos 14 anti-padrões → mapeamento para causas-raiz físicas/temporais.
  3. **Validação com especialistas** (2–3 DBAs/Arquitetos/Auditores de TI do órgão) — *mini-survey* inspirado na validação original.
  4. **Construção da Matriz de Criticidade** (Anti-padrão × Risco de Conformidade × Causa Física).
  5. **Elaboração do Checklist de Governança.**

#### 3.2 Fichamento do Artigo Base (Obrigatório pelo Professor)
> **Use o modelo fornecido (`Modelo_para_fichamento.doc`)**  
> Campos essenciais: Referência completa, Problema, Objetivo, Método, Resultados Principais, Lacunas Identificadas, Conexão com seu Trabalho, Crítica/Observações.

#### 3.3 Mapeamento Anti-padrão → Causa Física/Temporal (Sua Análise Nova)
| Anti-padrão (Asmare et al.) | Categoria | Causa-Raiz Física (Aula 02) | Causa-Raiz Temporal (Aula 03) |
|----------------------------|-----------|------------------------------|-------------------------------|
| Multiple Key Sequential Search | Data Retrieval | Full scan = I/O bound (disk bandwidth) | — |
| Inefficient Query Translation | Query | CPU + I/O (plano ruim) | — |
| Duplicate Requests | Connection | Network saturation + connection pool exhaustion | Clock drift → retries desnecessários |
| Synchronous Connection Usage | Connection | Thread blocking = CPU idle waiting I/O | Wall-clock timeout não considera monotonic |
| Single Connection for Data Access | Connection | Violates Shared-Nothing parallelism | — |
| Inefficient Driver/API | Driver/API | Driver path length + syscall overhead | — |
| Misconfiguration | Driver/API | Suboptimal buffer sizes, timeouts | NTP sync interval vs. timeout config |
| Wrong API Function | Driver/API | Batch vs. single write = WAF amplification | — |
| Cache Invalidation vs. Update | Cache | Write amplification no cache layer | LWW no cache → perda silenciosa |
| Inefficient Cache Logic | Cache | Memory pressure + GC pauses | — |
| Not Caching the Query | Cache | Repeated parse/plan = CPU + I/O | — |
| Non-optimized Indexing Logic | Indexing | LSM compaction pauses, write path | — |
| Inadequate Node Failure Handling | Node Mgmt | Partial failure = norma em DIS | Clock drift mascara falha → *split brain* |
| Load Imbalance Across Nodes | Node Mgmt | Hot partitions = I/O skew | Watermark misalignment em streams |

#### 3.4 Matriz de Criticidade (Anti-padrão × Risco de Conformidade)
*Escala 1–5 (1=Baixo, 5=Crítico) — Preenchida com especialistas*

| Anti-padrão | Tempestividade Fechamento | Transparência Ativa (LAI) | Integridade Contábil | Auditoria TCU | Disponibilidade SIEM | **Média** |
|-------------|---------------------------|---------------------------|----------------------|---------------|----------------------|-----------|
| Inadequate Node Failure Handling | 5 | 5 | 4 | 5 | 5 | **4,8** |
| Synchronous Connection Usage | 5 | 4 | 4 | 4 | 3 | **4,0** |
| Inefficient Driver/API | 4 | 4 | 3 | 4 | 4 | **3,8** |
| ... | ... | ... | ... | ... | ... | ... |

---

### **4. RESULTADOS E ANÁLISE** (∼4–5 páginas)

#### 4.1 Taxonomia Estendida: 14 Anti-padrões × 7 Categorias × 2 Dimensões Físicas
> **Tabela principal do artigo** — cada anti-padrão com:
> - Descrição (resumida do paper original)
> - **Causa-raiz física** (I/O, CPU, Rede, Memória)
> - **Causa-raiz temporal** (clock drift, LWW, watermark, ordering)
> - **Efeito em cascata** (ex: "Synchronous Connection → Thread Pool Exhaustion → Cascade Timeout → Falha de Fechamento")
> - **Evidência da literatura** (citação do paper + *Jeff Dean numbers* + *PPM drift*)

#### 4.2 Top 3 Críticos — Análise Profunda (Connecting the Dots)
Para cada um dos 3 mais críticos (Node Failure, Sync Connection, Driver/API):

**Exemplo: Inadequate Node Failure Handling**
- **Mecanismo físico:** Nó falha (disco/rede) → load balancer continua roteando → requests falham/timeout → *retry storm* → cascata.
- **Dimensão temporal:** Clock drift entre nós + NTP infrequente → *health check* usa *wall clock* desatualizado → nó "zumbi" considerado vivo.
- **Impacto SIEM:** Logs de falha chegam *fora de ordem* (LWW perde causalidade) → correlação forense falha.
- **Risco conformidade:** Portal Transparência indisponível > 30 min = violação LAI + achado TCU.

#### 4.3 Prevalência por Categoria (Dados do Paper Original + Sua Análise)
| Categoria | % no Paper (141 issues) | Sua Estimativa Setor Público* | Justificativa |
|-----------|------------------------|------------------------------|---------------|
| Driver/API | 15,6% | **Alta** | Stacks heterogêneas, drivers legados, configuração padrão |
| Cache (3 anti-padrões) | 10,6% cada | **Muito Alta** | Cache mal dimensionado, invalidação total, query não cacheada |
| Connection (3 anti-padrões) | 8–9% cada | **Alta** | Pool default, sync drivers, single writer |
| Node Mgmt (2 anti-padrões) | 6–7% cada | **Crítica** | Clusters multi-AZ sem health check ativo, split brain |

*Baseada em sua experiência + incidentes conhecidos (pode citar "relatos de campo" anonimizados).

#### 4.4 Estudo de Caso (Opcional mas Forte)
> **Sugestão:** Descreva **um incidente real** (anonimizado) no seu órgão.
> - Sistema: ex. "Sistema de Execução Orçamentária — Módulo de Empenho"
> - Sintoma: Lentidão no fechamento mensal, timeouts em lote noturno.
> - Diagnóstico: **Wrong API Function** (single-row insert em loop) + **Inefficient Driver** (pool undersized) + **Synchronous Connection**.
> - Correção: Batch insert + HikariCP tuned + async driver (R2DBC).
> - Resultado: Janela de batch de 4h → 45min; zero timeouts.
> - **Lições:** Anti-padrões combinam; correção exige visão sistêmica (física + código).

---

### **5. DISCUSSÃO** (∼3 páginas)

#### 5.1 Síntese: Anti-padrões como Sintomas de Violação de Limites Físicos
> **Tese central:** *A maioria dos anti-padrões de acesso a dados em DIS são manifestações de código que ignoram a física do hardware (I/O bandwidth, latência, capacidade de buffer, clock drift).*

| Limite Físico Violado | Anti-padrões Relacionados | Princípio da Aula Violado |
|------------------------|---------------------------|---------------------------|
| **Disk Bandwidth / Seek Latency** | Multiple Key Sequential Search, Non-optimized Indexing | "Gargalo é I/O, não CPU" (Aula 02) |
| **Write Amplification (WAF)** | Wrong API Function (single vs batch), Inefficient Cache Invalidation | LSM Trees / Compaction (Aula 02) |
| **Network Saturation** | Duplicate Requests, Single Connection | Shared-Nothing scale-out (Aula 02) |
| **Clock Drift / Uncertainty** | Synchronous Connection (timeouts), Inadequate Node Failure Handling | PPM, NTP, Monotonic clocks (Aula 03) |
| **Causal Ordering / LWW Loss** | Inefficient Cache Invalidation, Wrong API Function | TrueTime / Vector Clocks / Lamport (Aula 03) |
| **Backpressure / Buffer Overflow** | Inefficient Cache Logic, Not Caching Query | Axioma do Log / Drop vs Buffer (Aula 02) |

#### 5.2 Implicações para Governança de Dados no Setor Público
1. **Governança de Infraestrutura ≠ Governança de Código**  
   Driver/API ineficiente (15,6%) é *decisão de arquitetura/infra*, não de desenvolvedor. → **Catálogo de drivers homologados + configuração padrão** é ato de governança.

2. **Observabilidade Obrigatória**  
   Sem métricas de *latência p99, pool saturation, cache hit/miss, compaction pauses, clock offset* → **não se detecta anti-padrões em produção**.  
   → Exigir **OpenTelemetry + Prometheus/Grafana** em todos os sistemas estruturantes.

3. **Cache é Camada de Consistência, não só Performance**  
   Invalidação total + LWW = **risco de integridade contábil**.  
   → Políticas de cache devem ser **auditáveis** (TTL, invalidação granular, versionamento).

4. **Tempo é Dado de Auditoria**  
   Logs fora de ordem (clock drift) = **evidência forense comprometida**.  
   → Exigir **relógios monotônicos + NTP monitorado (offset < 10ms) + correlation IDs** em todos os microsserviços.

5. **Persistência Poliglota Exige Contratos de Desempenho**  
   Cada banco (Mongo, PostgreSQL, Redis, Cassandra) tem *anti-padrões próprios*.  
   → **ADR (Architecture Decision Record)** obrigatório justificando escolha + *performance budget* por operação.

#### 5.3 Limitações do Estudo
- Amostra baseada em *um* artigo (Asmare et al.) — não replicamos a coleta em 162 repositórios.
- Validação com especialistas foi *qualitativa* (n=2–3), não survey estatística (n=53 do original).
- Contexto setor público federal brasileiro — generalização para estados/municípios/privado requer cuidado.
- Não medimos *custo financeiro* de cada anti-padrão (ex: horas-homem, multas TCU, SLA violado).

---

### **6. PROPOSTA PRÁTICA: CHECKLIST DE GOVERNANÇA ANTI-PADRÕES DIS** (∼2 páginas)

> **Artefato entregável** — pode virar **Anexo Normativo** ou **Guia de Boas Práticas** do órgão.

#### 6.1 Checklist por Fase do Ciclo de Vida

| Fase | Ação | Anti-padrões Endereçados | Responsável | Frequência | Evidência de Conformidade |
|------|------|--------------------------|-------------|------------|---------------------------|
| **Arquitetura** | ADR com *performance budget* por operação crítica (p99 < 200ms) | Todos | Arquiteto de Dados | Por iniciativa | ADR aprovado + revisado |
| **Arquitetura** | Catálogo de drivers homologados + configuração padrão (pool, timeout, batch) | Inefficient Driver, Misconfiguration, Wrong API Function | STI / Arquitetura | Anual | Documento versionado no Git |
| **Desenvolvimento** | Code review com *checklist anti-padrões* (query plan, batch, async, cache key) | Query, Connection, Cache, Driver | Tech Lead / DBA | Por PR | Checklist assinado no PR |
| **Testes** | Teste de carga com *fault injection* (node failure, network latency, clock drift) | Node Failure, Sync Connection, Load Imbalance | QA / SRE | Por release | Relatório de carga + chaos engineering |
| **Operação** | Alertas: pool saturation > 80%, cache hit < 90%, compaction pause > 5s, clock offset > 10ms | Connection, Cache, Indexing, Node Failure | SRE / Operações | Contínuo | Dashboard Grafana + runbook |
| **Operação** | Health check ativo + circuit breaker + *monotonic clock* para timeouts | Node Failure, Sync Connection | SRE / Dev | Contínuo | Configuração versionada |
| **Auditoria/Conformidade** | Auditoria trimestral de *performance budgets* vs. SLA (LAI, fechamento contábil) | Todos | Auditoria TI / Controle Interno | Trimestral | Relatório de auditoria |
| **Melhoria Contínua** | Pós-incidente (RCA) deve classificar causa-raiz como anti-padrão (taxonomia) | Todos | SRE / Arquiteto | Por incidente | RCA no Confluence/Jira |

#### 6.2 Métricas-Chave (SLIs/SLOs) por Anti-padrão
| Anti-padrão | SLI (Service Level Indicator) | SLO Sugerido (Setor Público) |
|-------------|-------------------------------|------------------------------|
| Driver/API Ineficiente | Latência p99 de query simples | < 200ms |
| Synchronous Connection | % requests async / thread pool saturation | 100% async / < 70% pool |
| Cache Invalidation vs Update | Cache hit ratio / invalidação granular | > 95% hit / 100% granular |
| Not Caching Query | Query plan cache hit rate | > 90% |
| Inadequate Node Failure | Tempo de detecção de nó falho | < 30s (health check ativo) |
| Load Imbalance | Desvio padrão de CPU/IO entre nós | < 15% |
| Clock Drift (NTP) | Offset máximo entre nós | < 10ms (monitorado) |

---

### **7. CONCLUSÃO** (∼1 página)

#### 7.1 Recapitulação
- Estendemos a taxonomia de **Asmare et al. (2022)** com **duas lentes físicas** (I/O bounds da Aula 02, sincronização temporal da Aula 03).
- Demonstramos que **anti-padrões de acesso a dados não são "bugs de código" — são violações de limites físicos** que se manifestam como dívida técnica de desempenho.
- Mapeamos **riscos diretos de conformidade** (TCU, CGU, LAI, LRF) para cada anti-padrão crítico.
- Entregamos **checklist de governança operacionalizável** para o setor público federal.

#### 7.2 Contribuições Reafirmadas
1. **Taxonomia estendida** (física + temporal) — base para ferramentas de detecção automática futuras.
2. **Matriz de criticidade** anti-padrão × risco conformidade — instrumento de priorização para auditores/gestores.
3. **Checklist de governança** por fase do ciclo de vida — pronto para adoção normativa (IN STN/CGU).

#### 7.3 Trabalhos Futuros
- **Detecção estática/dinâmica automática** dos 14 anti-padrões (AST analysis + runtime profiling).
- **Quantificação de custo** (R$/hora de indisponibilidade, multas TCU evitadas).
- **Extensão a governos estaduais/municipais** (SICONV, SIAFEM, sistemas locais).
- **Integração com SIEM/SOAR** — anti-padrões como *indicadores de risco* em tempo real.
- **Estudo longitudinal** — acompanhar evolução da dívida técnica de acesso a dados em sistemas estruturantes por 2+ anos.

---

### **REFERÊNCIAS** (Formato ABNT / IEEE — conferir preferência do professor)

**Obrigatórias (das aulas + artigo base):**
- Asmare, B. M.; Khomh, F.; Nafi, K. W.; Antoniol, G. **Data Access Performance Anti-patterns in Data-Intensive Systems**. *arXiv:2208.08918v1*, 2022.
- Frery, A. C. **Introdução à Metodologia Científica**. 2014.
- Volpato, G. **Pesquisa Científica: Princípios e Métodos**. 2007.
- Dean, J. **Software Engineering Advice from Building Large-Scale Distributed Systems**. 2010 (números de latência).
- Kleppmann, M. **Designing Data-Intensive Applications**. O'Reilly, 2017. (Cap. 3, 8, 9 — storage, consistency, time)
- Lamport, L. **Time, Clocks, and the Ordering of Events in a Distributed System**. CACM, 1978.
- Corbett et al. **Spanner: Google's Globally-Distributed Database**. OSDI, 2012 (TrueTime).

**Normativos Brasileiros:**
- BRASIL. Lei nº 12.527, de 18 de novembro de 2011 (LAI).
- BRASIL. Decreto nº 10.139, de 28 de novembro de 2019 (Dados Abertos).
- BRASIL. Lei Complementar nº 101, de 4 de maio de 2000 (LRF).
- TCU. Acórdãos sobre governança de TI e tempestividade (ex: Acórdão 2345/2022-TCU-Plenário).
- ISO/IEC 38500:2015 — Governança de TI.
- ISO 8000 — Qualidade de dados.

---

## 3. FICHAMENTO DO ARTIGO BASE (Modelo do Professor)

> **Preencha no `Modelo_para_fichamento.doc` e anexe como Apêndice A**

| Campo | Conteúdo Sugerido |
|-------|-------------------|
| **Referência Completa** | Asmare, B. M.; Khomh, F.; Nafi, K. W.; Antoniol, G. Data Access Performance Anti-patterns in Data-Intensive Systems. *arXiv:2208.08918v1*, 2022. |
| **Problema** | Falta de taxonomia validada de anti-padrões de *desempenho* em acesso a dados para sistemas NoSQL/poliglotas. |
| **Objetivo** | Identificar, categorizar e validar 14 anti-padrões via estudo qualitativo (162 repositórios) + survey (53 devs). |
| **Método** | Coleta de issues → Codificação indutiva → Taxonomia 7 categorias → Validação survey (Kappa=0,764). |
| **Resultados Principais** | 14 anti-padrões, 7 categorias. Top 3 críticos: Node Failure, Sync Connection, Driver/API. Mais prevalente: Driver/API (15,6%). |
| **Lacunas Identificadas** | 1) Não conecta a limites físicos (I/O, tempo). 2) Não aborda governança/conformidade. 3) Validação apenas com devs, não auditores/gestores. |
| **Conexão com seu Trabalho** | Base empírica para RQ1. Sua extensão: lentes físicas/temporais (Aulas 02–03) + matriz conformidade (seu contexto). |
| **Crítica/Observações** | Tradução automática (Google) — verificar termos no original. Amostra só Java. Não mede custo financeiro. |

---

## 4. CRONOGRAMA SUGERIDO (para entregar no prazo da disciplina)

| Semana | Atividade | Entregável |
|--------|-----------|------------|
| 1 | Leitura profunda do artigo base + fichamento | Fichamento completo (Apêndice A) |
| 2 | Mapeamento anti-padrões → causas físicas/temporais (Tabela 3.3) | Tabela preenchida |
| 3 | Entrevistas/mini-survey com 2–3 especialistas (DBAs, Arquitetos, Auditores) | Matriz de criticidade preenchida |
| 4 | Escrita: Introdução + Fundamentação (Seções 1–2) | Rascunho v1 |
| 5 | Escrita: Metodologia + Resultados (Seções 3–4) | Rascunho v2 |
| 6 | Escrita: Discussão + Checklist + Conclusão (Seções 5–7) | Rascunho v3 |
| 7 | Revisão pares (Peer Review em grupo) + Ajustes ABNT | Versão final |
| 8 | **Entrega final** | PDF + Fichamento + Código/Planilhas (se houver) |

---

## 5. DICAS DE OURO DO PROFESSOR (baseado nas aulas)

1. **"O produto da Pós não é software, é conhecimento inédito."** (Aula 01)  
   → Seu artigo *é* a contribuição. O checklist é *artefato* que demonstra aplicabilidade.

2. **"Ciência é discurso sem fronteiras, auditável por pares."** (Aula 01)  
   → Escreva em inglês técnico (ou português com termos padrão), cite fontes internacionais, torne replicável.

3. **"Em DIS, gargalo é I/O, não CPU."** (Aula 02)  
   → Toda argumentação de desempenho deve voltar para *bandwidth, latência, capacidade de buffer, write amplification*.

4. **"Tempo não é metadado; é parte da semântica de ordenação, consistência e evidência."** (Aula 03)  
   → Clock drift, LWW, watermarks não são detalhes — definem *corretude* em sistemas distribuídos.

5. **"Back-of-the-envelope calculations"** (Aula 02, Bloco 4)  
   → Inclua **estimativas numéricas** no artigo (ex: "200 PPM × 1h sync = 720ms drift → timeout de 500ms falha").

6. **IMRAD rigoroso** — cada seção cumpre papel específico. Não misture Resultados com Discussão.

7. **Peer Review em grupo** — seu artigo será lido por colegas. Clareza > erudição.

---

## 6. CHECKLIST DE QUALIDADE ANTES DE ENTREGAR

- [ ] **Título** reflete contribuição + contexto (DIS + governança)?
- [ ] **Abstract** tem: contexto, lacuna, método, resultados, implicação, conclusão?
- [ ] **Introdução** tem 3 gaps claros + 3 RQs (1 original + 2 suas)?
- [ ] **Fundamentação** cita *todas* as aulas (01, 02, 03) + artigo base + normativos?
- [ ] **Metodologia** explica *fichamento*, *mapeamento físico/temporal*, *matriz criticidade*, *checklist*?
- [ ] **Resultados** tem: Tabela taxonomia estendida, Top 3 análise profunda, Estudo de caso (opcional)?
- [ ] **Discussão** conecta anti-padrões → limites físicos → riscos conformidade → checklist?
- [ ] **Conclusão** reafirma 3 contribuições + 3 trabalhos futuros?
- [ ] **Referências** no formato exigido (ABNT/IEEE) + todas citadas no texto?
- [ ] **Fichamento** preenchido no modelo do professor + anexado?
- [ ] **Revisão ortográfica/gramatical** (LanguageTool, Grammarly, ou colega)?
- [ ] **Formatação** (margens, fonte, espaçamento, numeração) conforme template do PROCC?

---

## 7. ANEXOS SUGERIDOS

| Anexo | Conteúdo |
|-------|----------|
| **A** | Fichamento do artigo base (modelo do professor) |
| **B** | Matriz de Criticidade completa (Anti-padrão × 5 Riscos × 3 Especialistas) |
| **C** | Checklist de Governança operacionalizável (versão limpa para publicação separada) |
| **D** | Roteiro de entrevista / mini-survey com especialistas |
| **E** | Cálculos *back-of-the-envelope* (Jeff Dean numbers, PPM drift, WAF estimates) |

---

**Boa escrita! Lembre-se: o rigor metodológico (Aula 01) + a fundamentação física (Aulas 02–03) + a base empírica (Artigo Asmare) + seu contexto de aplicação (Conformidade/Governança) = Artigo de nível de publicação em evento Qualis A (ex: CBSoft, SBES, SIMBIG, ou até ICSE/ASE se em inglês).**

> **"Pesquisa sem originalidade, sem método e sem publicação em veículos validados não é pesquisa científica."** — Volpato (2006), citado na Aula 01.