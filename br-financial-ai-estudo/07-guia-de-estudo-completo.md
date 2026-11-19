# Guia de estudo completo — Sistemas Intensivos em Dados

**PROCC/UFS · Tópicos Avançados em Engenharia de Software e Sistemas de Informação · 2026/2**
Prof. Dr. Fabio Gomes Rocha

> Feito para quem está achando a disciplina difícil. A dificuldade não é sua: o curso
> atravessa filosofia da ciência, bibliometria, arquitetura distribuída, física de
> hardware, streaming e teoria de relógios **em três aulas**. Ninguém conecta esses
> assuntos para você — este guia conecta.
>
> **Arquivos que li:** Aula 1 (Sistemas Intensivos em Dados, 40 slides), Aula 2
> (Paradigma Data-Intensive e Limites Físicos, 36 slides), Aula 3 (A Física do Tempo e
> Sincronização Distribuída, 36 slides). *Observação: o arquivo `Aula_03.1` que você
> enviou é byte-idêntico ao `Aula_03` (mesmo SHA-256) — é duplicata, não conteúdo novo.*

---

# PARTE 0 — O mapa antes do território

## Por que a disciplina parece um amontoado de assuntos

Porque ela **é** um amontoado — de propósito. O nome já diz: "Tópicos Avançados". O
objetivo não é ensinar uma tecnologia, é construir um **repertório de engenharia** para
você julgar arquiteturas.

Mas existe um fio condutor único, e ele é este:

> **Em sistemas intensivos em dados, o inimigo é o I/O e o tempo. Todo o resto é
> consequência.**

Guarde essa frase. Cada assunto do curso é uma consequência dela:

| Assunto | Como decorre do fio condutor |
| --- | --- |
| Latências físicas (Aula 2) | Explicam *por que* o I/O domina |
| Árvores LSM e WAF (Aula 2) | É a resposta do NoSQL para não fazer I/O aleatório |
| Bounded vs. Unbounded (Aula 2) | Streams existem porque o dado não para de chegar |
| Backpressure (Aula 2) | É o que impede o consumidor de morrer afogado |
| Axioma do Log (Aula 2) | É a solução para não perder estado em crash |
| Clock drift (Aula 3) | É o I/O do tempo: o relógio também "vaza" |
| LWW (Aula 3) | Quando você usa tempo como regra de negócio, o drift apaga dado |
| TrueTime e Lamport (Aula 3) | Como ordenar eventos sem confiar no relógio |
| SIEM (Aulas 2 e 3) | Onde todas essas falhas se somam e viram falso negativo |

## A estrutura real da disciplina

O curso tem **dois eixos** que se cruzam:

**Eixo A — Como pesquisar** (Aula 1): o que é ciência, bibliometria, IMRAD, ameaças à
validade, métodos empíricos, MSR. Serve para o seu **artigo de 60%** e para a
**dissertação**.

**Eixo B — Como sistemas intensivos em dados funcionam e falham** (Aulas 2 e 3): física de
I/O, streaming, estado, tempo, SIEM. Serve para o **conteúdo técnico** do seu artigo.

O erro mais comum de quem se perde é estudar os dois como se fossem disciplinas separadas.
Não são: o Eixo A diz **como provar**, o Eixo B diz **o que provar**.

---

# PARTE 1 — AULA 1: O jogo da pós-graduação

## 1.1 O que é ciência (e a mudança de chave mental)

O slide central compara três coisas:

- **Pesquisa comum** — qualquer atividade para responder a uma indagação. *Nem toda
  pesquisa é científica.*
- **Pesquisa científica** — usa rigorosamente o método científico, independente do objeto.
- **Ciência** — forma humana de construir e aceitar generalizações universais, via método
  e discurso lógico, **admitindo sua precariedade**.

**A frase que mais importa da Aula 1:**

> "Na indústria, o produto é um software funcional. Na pós-graduação, o software é apenas
> um veículo experimental — a saída real é conhecimento inédito e formação de recursos
> humanos." (Frery, 2014)

Isso explica por que o professor insiste tanto em método. O `br-financial-ai` não vale
pelo software: vale pelo que ele **demonstra**.

**As três premissas da ciência (Frery):**
1. **Discurso sem fronteiras** — o que se produz no PROCC precisa ser validado
   internacionalmente. Isso define o idioma e o formato: inglês e padrão IEEE/ACM.
2. **Generalização universal** — o objetivo é achar padrões que valham além do experimento.
3. **Aceitação da precariedade** — toda teoria vale até evidência mais forte refiná-la.

**O ciclo científico:** percepção/observação controlada → hipóteses testáveis →
verificação/validação/publicação → incorporação à malha do conhecimento.

**As quatro armadilhas que ele cobra (Slide 11):**
- *Deadline-driven research* — foco na data de submissão em vez da profundidade
- Falta de originalidade / plágio / "artigo salaminho"
- **Falhas metodológicas e amostragem** — experimento sem controle, sem teste de hipótese
- Introdução e revisão bibliográfica fracas

## 1.2 Bibliometria — como escolher onde publicar

Você não precisa decorar métricas, precisa **entender o que elas premiam**:

| Métrica | O que mede | Cuidado |
| --- | --- | --- |
| **Fator de Impacto (FI/JCR)** | Média de citações dos últimos 2 anos ÷ artigos publicados | Favorece áreas de ciclo rápido |
| **Immediacy Index** | Rapidez de citação no mesmo ano | Favorece modismo |
| **Cited Half-Life** | Anos que respondem por 50% das citações | Mostra se a área é perene |
| **Índice h (Hirsch, 2005)** | h artigos com ≥ h citações cada | Equilibra quantidade e relevância |

**Conferência vs. periódico** — a distinção que ele cobra:

| | Anais de conferência | Periódico indexado |
| --- | --- | --- |
| Objetivo | Disseminação rápida, debate de ideias iniciais | Memória perene, certificação |
| Revisão | *One-shot*, sem iteração | Múltiplas rodadas |
| Espaço | Rígido (8–10 p.) | Flexível (provas, dados detalhados) |
| Impacto | Taxa de rejeição, h-index do evento | JCR, FI, SJR |

**A técnica de revisão bibliográfica (Slide 18)** — decore, você vai usar:

```
1. ARTIGOS SEMENTE      → escolha n ≥ 1 artigos fundamentais de altíssima qualidade
2. CONE DO PASSADO      → leia as REFERÊNCIAS desses artigos (as origens)
3. CONE DO FUTURO       → veja QUEM CITOU esses artigos depois (o estado da arte)
                        → itere
```

O **cone do futuro** é literalmente o que resolvi no seu fichamento: o PDF que você recebeu
era o pré-print de 2022; seguindo quem o citou, cheguei ao artigo consolidado de 2024 na
*Empirical Software Engineering*. **Use isso na apresentação oral** — é demonstrar a
técnica que ele ensinou.

## 1.3 Os quatro métodos de pesquisa em ES

Esta tabela é o coração metodológico do curso:

| Método | Foco | Aplicação em DIS | Evidência |
| --- | --- | --- | --- |
| **Engenharia Empírica** | Experimentos controlados | Latência/vazão entre mensagerias (Kafka vs. Pulsar) | Benchmarks + teste de hipótese (t, Mann-Whitney, ANOVA) |
| **Mineração de Repositórios (MSR)** | Artefatos de código | Antipadrões arquiteturais em repositórios abertos | Métricas de código + histórico Git |
| **Estudo de Caso Industrial** | Contexto real | Migração monólito→microsserviço na NTT Data | Qualitativa/mista, lições aprendidas |
| **Métodos Formais** | Prova e verificação | Deadlock em Sagas via Redes de Petri | Provas matemáticas de correção |

**Reprodutibilidade:** pacote de replicação com dados e scripts abertos. O artigo do seu
fichamento tem um (referência [39]).

## 1.4 IMRAD e ameaças à validade

**IMRAD:** Introdução (Hook + Gap) → Metodologia → Resultados e Discussão.

- **Hook** = por que isso importa (o problema real, não o título)
- **Gap** = o que a literatura **não** resolveu

**As três ameaças à validade (Slide 34)** — você vai usar na crítica do fichamento e na
seção do seu artigo:

| Tipo | Pergunta que responde | Exemplo do seu artigo |
| --- | --- | --- |
| **Construto** | A métrica mede mesmo o conceito? | "Issue resolvida" é proxy de "antipadrão real"? |
| **Interna** | O resultado veio do tratamento ou de confusão? | Sistemas escolhidos por terem **mais issues** favorece projetos grandes |
| **Externa** | Generaliza para outros domínios? | Corpus é de código aberto; versão publicada restrita a Java |

## 1.5 Os pilares de Kleppmann

Os três pilares que organizam todo o curso:

- **Confiabilidade (Reliability)** — resiliência a falhas de hardware, rede e erro humano.
  *Fault* = desvio de um componente. *Failure* = o sistema deixa de servir.
- **Escalabilidade (Scalability)** — responder ao aumento de volume, throughput e
  complexidade de consulta.
- **Manutenibilidade** — simplicidade, operabilidade por DevOps, evolução contínua.

**Dois conceitos de escala que ele cobra:**
- **Parâmetros de carga:** defina numericamente o que é "carga" (RPS, razão leitura/escrita,
  tamanho de mensagem, acessos simultâneos).
- **Percentis, não médias:** meça **P99 e P99.9** — a média esconde a cauda.

> **Cuidado com a "média ilusória":** se 99 requisições levam 10 ms e 1 leva 10 s, a média
> é ~110 ms e parece ótima. O usuário que pegou a décima nona vai embora. É por isso que
> se mede cauda.

---

# PARTE 2 — AULA 2: O paradigma e a física

Esta é a aula mais densa de fundamentos. Quatro blocos.

## Bloco 1 — O que é um sistema intensivo em dados

**Compute-Intensive vs. Data-Intensive** — a distinção fundadora:

| Dimensão | Compute-Intensive | Data-Intensive (DIS) |
| --- | --- | --- |
| **Gargalo** | Ciclos de CPU (GPU/TPU) | **Largura de banda de disco, RAM e rede (I/O-bound)** |
| **Aplicação** | Simulação molecular, clima, criptografia, HPC | SIEM, e-commerce, redes sociais, telemetria IoT |
| **Arquitetura** | Supercomputadores, RDMA/InfiniBand | **Clusters de commodity hardware via IP padrão** |
| **Falhas** | Checkpoints síncronos globais | **Falha parcial é a norma, tratada no software** |

**A inversão mental que você precisa fazer:** em HPC, a máquina é cara e o problema é
"como usar toda a CPU". Em DIS, a máquina é barata e o problema é "como mover os dados até
a CPU sem esperar". **Você projeta em torno do I/O, não da CPU.**

**Os quatro blocos de construção de um DIS:**

1. **Bancos de dados** — persistência confiável, estado íntegro após falha
2. **Caches em memória** — atenuar leituras repetitivas no banco
3. **Índices de busca** — índices invertidos, evitar varredura total
4. **Streams e filas** — canais assíncronos desacoplados no tempo

**As três dimensões de complexidade:** Volume (TB→PB), Velocidade (ingestão perto da
saturação física), Variabilidade (o formato muda dinamicamente → esquema flexível).

**Modelos de escalabilidade — o ponto central:**

```
SCALE-UP (Shared-Memory)                SCALE-OUT (Shared-Nothing)
├─ várias CPUs + RAM num SO único       ├─ cada nó tem CPU, RAM e disco próprios
├─ limite: custo exponencial,           ├─ coordenação só por software, via rede IP
│  barramento interno, NUMA             ├─ escala horizontal ~linear
└─ SPOF (ponto único de falha)          └─ tolerância natural a falhas
```

**NUMA (Non-Uniform Memory Access)** — por que *shared-nothing* venceu:

Em placas multi-socket, acessar a RAM do processador **local** é muito mais rápido que a
do vizinho. A troca pelo barramento (QPI/UPI) gera contenção severa. Consequência prática:
**dobrar os núcleos de uma máquina não dobra a vazão do banco.** Por isso se desacopla em
nós independentes, cada um processando sua partição sem disputar barramento.

## Bloco 2 — A física das latências (a parte que explica tudo)

**A tabela de Jeff Dean** — o coração deste bloco. A coluna da direita traduz
nanossegundos para escala humana, assumindo **1 ns = 1 segundo**:

| Operação | Tempo real | Escala humana |
| --- | --- | --- |
| Cache L1 | 0,5 ns | 0,5 s (uma piscada) |
| RAM principal | 100 ns | 1,6 minutos |
| Ler 1 MB sequencial da RAM | 250 µs | ~3 dias |
| Acesso aleatório em SSD | 16 µs | ~4,4 horas |
| **Seek em HDD** | **10 ms** | **~3,8 meses** |
| Rede Califórnia↔Europa | 150 ms | ~4,7 anos |

**Como usar essa tabela para raciocinar:** se você tem 1 segundo de orçamento e cada seek
de HDD custa 3,8 meses na escala humana, então **100 seeks já estouram o orçamento**.
Enquanto isso, você pode fazer **2 milhões de acessos ao L1** no mesmo tempo.

Daí decorre a regra de ouro:

> **Evite I/O aleatório. Prefira I/O sequencial.** Quase toda decisão de arquitetura em DIS
> é uma variação disso.

**A física dos SSDs — por que apagar é caro:**

- Leituras e escritas acontecem em **páginas** (4–16 KB)
- Apagamento só acontece em **blocos inteiros** (2–8 MB)
- **Sobrescrever exige ler o bloco, modificar a página e regravar o bloco em outro lugar**
- Cada célula flash suporta um número finito de ciclos P/E (write/erase)
- A controladora faz *wear leveling* e coleta de lixo (garbage collection) internamente

**Consequência que o professor quer que você entenda:** gravar em SSD não é "sobrescrever";
é "copiar e realocar". Cargas pesadas de escrita **desgastam o hardware**.

**WAF (Write Amplification Factor):**

```
WAF = bytes gravados fisicamente ÷ bytes que o software pediu para gravar
```

Se você grava 1 GB e o dispositivo grava 3,5 GB fisicamente → **WAF = 3,5**.

Consequências: vida útil do SSD cai drasticamente e o barramento de I/O satura durante
picos de escrita.

**Árvores LSM e SSTables** — a resposta arquitetural para não fazer I/O aleatório:

```
1. MemTable (RAM)     escrita entra em estrutura ordenada na memória
                      (SkipList / Red-Black Tree) → resposta ultrarrápida
2. Commit Log (WAL)   simultaneamente, gravação SEQUENCIAL append-only em disco
                      → recuperação contra crash
3. SSTables (disco)   quando a MemTable enche, é "flushed" como arquivo
                      IMUTÁVEL e ordenado por chave
```

**Compactação e latência de cauda:**

Em segundo plano, o banco mescla SSTables antigas, descartando chaves sobrescritas e
tombstones. **Esse processo disputa banda de I/O com as consultas dos clientes.**

> **Por que P99.9 importa aqui:** o pico de compactação coincide com a sua leitura e
> produz aquela lentidão súbita e esporádica. Uma página corporativa pode disparar 100
> chamadas paralelas — e a requisição fica tão lenta quanto **o serviço mais lento**.

**Pausas não-determinísticas** (aula importantíssima para o resto do curso):
- **GC (Garbage Collection)** — pausas *stop-the-world* congelam todas as threads
- **Memory thrashing / Swap** — RAM esgotada, o SO pagina para disco, 100% do I/O só movendo blocos
- **Steal time na nuvem** — hipervisor multitenant suspende sua VM para dar CPU ao vizinho

**Guarde estas três.** Na Aula 3 elas reaparecem como **causa de inversão temporal** em SIEM.

## Bloco 3 — Velocidade: Bounded vs. Unbounded

| Característica | Bounded (Batch) | Unbounded (Streaming) |
| --- | --- | --- |
| Extensão temporal | Tamanho fixo, discreto, imutável | Infinito, contínuo, incremental |
| **Ordenação global** | Viável (sort-merge joins) | **Matematicamente impossível** |
| Processamento | Início, meio e fim definidos | Roda por meses/anos sem parar |
| Tecnologias | Spark Batch, Hadoop MapReduce, DW | Flink, Kafka Streams, Spark Streaming |

**A barreira matemática do sort (Slide 19)** — entenda este argumento, é elegante:

> Para garantir que o **menor** elemento de uma coleção ordenada seja emitido primeiro, é
> obrigatório inspecionar o **último** elemento do conjunto. Como um fluxo unbounded nunca
> atinge o fim, a ordenação total global é **indecidível**.

**Solução:** discretizar em **janelas temporais** (fixa, deslizante ou por sessão). Isso,
na Aula 3, vai reaparecer como **watermarks**.

**As três estratégias de saturação de fluxo:**

| Estratégia | O que faz | Quando usar |
| --- | --- | --- |
| **Drop** | Descarta excedente | Só quando o dado perde valor em milissegundos (VoIP, vídeo) |
| **Buffer** | Enfileira para amortecer rajadas | Rajadas curtas, consumidor recupera |
| **Backpressure** | Sinaliza o produtor a desacelerar | Quando não se pode perder nem acumular |

**Filas em RAM vs. Log-Based Streams** — a comparação mais cobrada da aula:

| Critério | RabbitMQ/AMQP (RAM) | Kafka/Pulsar (Log em disco) |
| --- | --- | --- |
| Armazenamento | Memória RAM do nó | Log append-only sequencial em disco |
| Com histórico grande | **Vazão despenca** quando a RAM esgota | **Vazão estável** (1 GB ou 50 TB) |
| Consumo | **Destrutivo** (apaga após confirmação) | **Não-destrutivo** (ponteiros/offsets) |
| Reprocessar | Inviável sem reenvio do produtor | **Trivial: rebobinar os offsets** |

**A mecânica da backpressure (Slide 22):**
- **Nível de socket:** o buffer do consumidor enche → a janela TCP fecha (`Window Size = 0`) → o SO do produtor não consegue enviar
- **Nível de software:** Reactive Streams, Akka e Flink propagam o sinal de volta pela cadeia
- **Proteção:** evita `OutOfMemoryError` no consumidor

**Lambda vs. Kappa:**
- **Lambda:** dois pipelines (Batch para precisão + Speed para tempo real) → **duplica a regra de negócio**
- **Kappa:** tudo sobre a mesma engine de stream, reprocessando logs imutáveis → uma regra só

## Bloco 4 — Estado e o Axioma do Log

**Estado volátil vs. persistente:**

| | Volátil | Persistente |
| --- | --- | --- |
| Onde | RAM local (hash tables, caches) | Disco, WAL, mídia durável |
| Vantagem | Latência em nanossegundos | Durabilidade e recuperação |
| Custo | — | Penalidade de latência de I/O em **cada** mutação |
| Risco | **Perda total em crash** | — |

**O Axioma do Log Imutável (Slide 25)** — a frase mais citável do curso:

> **"A verdade reside no Log; o banco de dados é apenas uma visão materializada e um cache
> do histórico de eventos."** (Pat Helland & Martin Kleppmann)

Consequência prática: se o banco corromper, o estado pode ser **fielmente reproduzido**
reprocessando o log desde o início. É por isso que Kafka guarda tudo em log append-only —
e por isso **reprocessar é trivial**.

**Microbatching vs. Checkpointing:**

| | Spark Streaming | Flink |
| --- | --- | --- |
| Modelo | Mini-lotes de 500 ms–1 s | Evento individual |
| Latência | 100–500 ms | **< 10 ms** |
| Tolerância a falhas | Recalcula linhagem RDD | Barreiras de checkpoint assíncronas |
| Garantia | At-least-once / exactly-once | **Exactly-once com consistência de estado** |

## O exercício de dimensionamento (Back-of-the-Envelope) — resolvido

Os slides 29–31 deixam os cálculos em branco (são animações). **Reconstruí a cadeia
completa** e conferi contra o único resultado que o slide revela (127,75 TB):

**Premissas:** 100 milhões de eventos/dia · 500 bytes por evento · retenção de 2 anos.

```
1. Ingestão diária   = 100.000.000 × 500 B = 50.000.000.000 B = 50 GB/dia
2. Ingestão anual    = 50 GB × 365                        = 18.250 GB = 18,25 TB/ano
3. Storage 2 anos    = 18,25 TB × 2                       = 36,5 TB (bruto, sem réplica/índice)
4. Vazão média (QPS) = 100.000.000 ÷ 86.400 s             ≈ 1.157 eventos/s
5. Banda média       = 1.157 × 500 B ≈ 578.700 B/s        ≈ 0,58 MB/s ≈ 4,6 Mbps
6. Rajada de 10x     = 11.574 QPS ≈ 5,79 MB/s             ≈ 46,3 Mbps
```

**Conferência:** o slide afirma "11.570 QPS" na provocação 1 — bate com o passo 6. ✓

**E a provocação 2, com WAF = 3,5:**

```
36,5 TB × 3,5 = 127,75 TB gravados fisicamente nas células flash
```

O slide confirma: **"127,75 TB gravados nas células flash!"** ✓

**Como interpretar (é isso que ele quer na discussão):** 36,5 TB de dado lógico viram
127,75 TB de desgaste físico. Em SSDs corporativos, isso consome a vida útil muito antes
do previsto. **O dimensionamento de capacidade não é sobre quanto dado você guarda, é
sobre quanto você grava.**

**Provocação 1 (RabbitMQ vs. Kafka sob rajada):** com 11.570 QPS por 1 hora, o broker em
RAM cresce e ameaça `OutOfMemoryError`; o broker append-only em disco absorve a rajada com
vazão estável e depois deixa o consumidor drenar pelo offset.

---

# PARTE 3 — AULA 3: A física do tempo

Esta é a aula mais difícil do curso, e é difícil por um motivo bom: ela exige que você
**abandone a intuição de que tempo é uma coisa só**.

## 3.1 A pergunta de abertura

> "Se dois servidores em salas diferentes registrarem um log exatamente no mesmo
> milissegundo, como provamos qual evento aconteceu primeiro?"

Ela envolve **três dimensões**: **física** (o cristal), **lógica** (a ordem causal) e
**forense** (a evidência). O curso inteiro da Aula 3 é construir a resposta.

## 3.2 Por que relógios divergem (a física)

**O oscilador de quartzo:** efeito piezoelétrico — corrente gera oscilação mecânica em
frequência estável, usada como "batida" do relógio. Frequência padrão **32.768 Hz (= 2¹⁵)**,
que facilita contagem binária. **Limitação física:** diferenças de fabricação impedem dois
cristais de vibrarem na mesma taxa.

**Fatores de drift:** variação térmica (carga muda a temperatura do rack, altera a rigidez
do cristal), envelhecimento (degradação do quartzo), ruído elétrico.

**PPM (Parts Per Million):**

```
PPM mede quantos microssegundos por segundo o relógio ganha ou perde
Desvio máximo:  Δt = T × (PPM / 1.000.000)
200 PPM = 200 μs de erro por segundo
```

**O exercício da aula, resolvido (Slide 8):**

| Intervalo | 200 PPM (aula) | 50 PPM (atividade) | 500 PPM (atividade) |
| --- | --- | --- | --- |
| 30 s | 6 ms | 1,5 ms | 15 ms |
| 1 h | 720 ms | 180 ms | 1,8 s |
| **24 h** | **17,28 s** | **4,32 s** | **43,2 s** |

*A atividade em sala pede exatamente recalcular com 50 e 500 PPM — os valores acima são a
resposta.*

**A conclusão que incomoda:** uma falha de sincronização aparentemente curta desloca a
cronologia operacional **por segundos**. Com 500 PPM e 24 h sem sincronizar, você tem
**43 segundos** de incerteza.

## 3.3 NTP e suas limitações

**Hierarquia Stratum:** 0 = GPS/relógio atômico · 1 = servidor ligado à referência ·
2+ = servidores sincronizados por rede.

O NTP aproxima o UTC por troca de mensagens UDP, mas **precisa inferir o atraso da rede** —
e a rede raramente é simétrica.

**As quatro limitações:**
- **RTT variável** — ida e volta podem seguir caminhos físicos diferentes
- **Jitter** — filas nos buffers dos roteadores introduzem ruído
- **Distância geográfica** — multirregião impõe dezenas/centenas de ms
- **Vulnerabilidades** — spoofing e amplificação NTP podem desestabilizar a base temporal

**A premissa arriscada:** o algoritmo clássico assume `d₁ ≈ d₂` (simetria). Na internet
real, a variação de rotas torna essa estimativa imprecisa.

## 3.4 Wall clock vs. monotonic clock

| | `CLOCK_REALTIME` (parede) | `CLOCK_MONOTONIC` |
| --- | --- | --- |
| Mede | Tempo desde a Época UNIX | Tempo desde um ponto arbitrário (boot) |
| Uso | Humanos e auditoria | Duração, timeout, latência |
| Risco | **NTP pode saltar para trás ou para frente** | Nunca salta para trás |

**O exemplo do slide é perfeito e vale memorizar:**

```
t_início (pedido) = 10:00:00
t_final           = 09:59:58   ← o NTP ajustou o relógio para trás
latência = t_final - t_início = -2 segundos  ❌
```

Uma latência negativa quebra timeouts e medições. **Regra: meça duração sempre com relógio
monotônico.**

**Slewing vs. Stepping:**
- **Slewing** — altera suavemente a frequência dos tiques. Gradual, **preserva
  monotonicidade**. Recomendado.
- **Stepping** — salto discreto e imediato. Rápido para acertar o horário civil, mas
  **perigoso** para lógicas de duração (usado em `CLOCK_REALTIME`).

**Dois casos reais:**
- **Leap second (2012):** UTC adicionou o segundo 61. Sistemas Java/Linux sofreram loops
  infinitos e CPUs a 100% globalmente. **A lição:** conflito crítico quando "tempo civil" e
  "tempo computacional" divergem.
- **Virtualização e pausas de VM:** relógios são emulados pelo hipervisor; migração,
  contenção de CPU e *noisy neighbors* congelam a VM. Ao despausar, **o relógio salta** e
  heartbeats viram falsos alarmes. Afeta EDR, Kubernetes audit, CloudTrail e agentes SIEM.

## 3.5 LWW — a anomalia central

**O modelo leaderless:** Cassandra/Dynamo — múltiplos nós aceitam escritas concorrentes;
cada operação recebe timestamp físico; em conflito, **o maior timestamp vence**; a premissa
perigosa é que os relógios estejam sincronizados.

**O cenário do slide (Slide 20) — siga passo a passo:**

```
PASSO 1  Cliente A escreve x = 1 em Node 1, ts = 42.004s
PASSO 2  Cliente B lê x = 1 e grava x = 2 em Node 3
         Node 3 tem clock -3ms (atrasado) → ts = 42.003s
PASSO 3  Node 2 recebe as duas escritas e escolhe o MAIOR ts
         42.004 > 42.003  →  x = 1 sobrevive, x = 2 DESAPARECE
```

**O dano:** no tempo real, x=2 ocorreu **depois** de x=1. Mas o valor final é x=1.
Ocorreu **inversão de causalidade**, sem exceção, sem alarme, sem retry — **falha
silenciosa**. Em domínio regulado ou forense, isso é **perda de evidência**.

**A pegadinha da discussão (Slide 22):** se usarmos UUIDs imutáveis como chave, ainda há
perda por drift de quartzo? **Não para inserções imutáveis** — sem sobrescrita concorrente
na mesma chave, o LWW não escolhe vencedor. **Mas** atualizações parciais, deduplicação
agressiva e upserts **reintroduzem** o problema.

> Isso é ouro para a sua linha de pesquisa: em registro contábil, um **upsert** com LWW
> pode apagar um lançamento legítimo.

## 3.6 As soluções

**TrueTime (Google Spanner)** — tempo como **intervalo de incerteza**:

```
now() → [earliest, latest]      (não um escalar ilusório)
```

- **Exposição da incerteza:** o Spanner devolve explicitamente a incerteza mensurável
- **Garantia:** o tempo real absoluto está **estritamente contido** no intervalo
- **Consistência externa:** ordem global garantida sobre uma janela delimitada
- **Hardware:** antenas GPS nos datacenters + relógios atômicos de césio como reserva,
  mantendo ε na escala de poucos milissegundos
- **Commit-wait:** espera 2ε (~14 ms) antes de commitar, para que as janelas não se
  sobreponham e os commits possam ser ordenados globalmente

**Relógios lógicos:**
- **Lamport** — substitui segundos por contadores. Se A → B, então `timestamp(A) < timestamp(B)`.
- **Vector clocks** — detectam **concorrência**: A antes de B, B antes de A, ou **incomparáveis**.

Úteis quando **causalidade importa mais que horário civil**. Podem ser combinados com
timestamps físicos para auditoria e UX.

## 3.7 SIEM — onde tudo se soma

**Por que o tempo é crítico:** um SOC reconstrói a cadeia de ataque correlacionando
Firewall, EDR, IAM, Kubernetes Audit e CloudTrail. **A premissa frágil:** que o
`@timestamp` emitido na borda represente uma linha temporal universal.

> **Mercado:** um falso negativo em regra de correlação pode custar mais que uma
> indisponibilidade.

**A fragmentação do tempo em pipelines (Slide 30)** — tabela essencial:

| Timestamp | Onde nasce | Risco |
| --- | --- | --- |
| **event time** | agente/endpoint | drift, pausa de VM, manipulação |
| **ingestion time** | Kafka/Logstash | mascara fila, buffer offline, retransmissão |
| **processing time** | OpenSearch/Flink | backpressure, locks, contenção de CPU |

> **Boa engenharia guarda os três — e explicita qual deles a regra de detecção usa.**

**As três anomalias (decore estas três, são o coração da aula):**

**Anomalia 1 — Inversão causal e evasão de detecção.**
Atacante faz força bruta no IAM e exfiltra credenciais. O DC é VM sob *noisy neighbor* com
clock atrasado em 4 s. O firewall está correto. Regra: alertar se conexão externa ocorrer
até 2 s após logon bem-sucedido.

```
Tempo real:  Δ = 0,5 s   → a regra DEVERIA disparar
Registrado:  E1 = 06.000s, E2 = 10.500s → Δ = 4,5 s → regra FALHA
RESULTADO: falso negativo, ataque não detectado
```

**Anomalia 2 — Perda forense via LWW na deduplicação.**
Agentes enviam logs at-least-once; o buffer deduplica por ID. `_id = SHA256(host + pid +
comando)` parece seguro, mas cria colisão intencional por evento lógico. O rootkit injeta
thread às 12:00:00.010, mas o coletor com **-20 ms** carimba 11:59:59.990.

```
Evento malicioso: 11:59:59.990
Evento benigno:   12:00:00.005
LWW escolhe o MAIOR timestamp → o rastro malicioso é APAGADO
```

**Anomalia 3 — Watermarks e janelas deslizantes.**
Flink/Kafka Streams usam watermarks para decidir quando a janela está completa. Nós com
clock adiantado injetam eventos "do futuro"; a watermark avança prematuramente; logs
corretos passam a chegar "atrasados" e vão para DLQ. Regras de brute force/DDoS **perdem
evidência temporal**.

**A pergunta que ele deixa (Slide 34):** *a tolerância da watermark deveria ser fixa,
estatística ou adaptativa por fonte?*

**Os quatro padrões de mitigação (Slide 35)** — a resposta de engenharia:

1. **Dual timestamping** — persistir `event.created`, `event.ingested` e `event.processed`;
   a regra escolhe explicitamente a âncora temporal
2. **Tolerância bounded** — calibrar atraso de watermarks com p99/p999 de latência e
   distribuição de drift por fonte
3. **PTP / hardware timestamp** — carimbar na NIC ou appliance quando a evidência temporal
   precisa ser probatória
4. **IDs lógicos** — sequence IDs, Lamport ou vector clocks para preservar causalidade local

> **"Mitigação não é só sincronizar NTP: é projetar regras para conviver com incerteza."**

---

# PARTE 4 — A cadeia causal única do curso

Se você entender esta corrente, entendeu a disciplina inteira:

```
Commodity hardware + rede IP
        ↓
I/O é o gargalo (latências de Jeff Dean)
        ↓
Evitar I/O aleatório → LSM trees, SSTables, WAL
        ↓
Mas compactação gera latência de cauda e disputa de I/O
        ↓
E o dado não para de chegar → Unbounded streams
        ↓
Saturação → Drop / Buffer / Backpressure
        ↓
Estado volátil perde tudo em crash → Axioma do Log: a verdade está no log
        ↓
Distribuir o log exige ordenar eventos no tempo
        ↓
Mas relógios físicos derivam (quartzo, NTP assimétrico, pausa de VM)
        ↓
Se o tempo vira regra de negócio (LWW), o drift APAGA DADO silenciosamente
        ↓
Solução: expor a incerteza (TrueTime) ou abandonar o tempo físico (Lamport)
        ↓
SIEM é onde todas essas falhas se acumulam e viram FALSO NEGATIVO
```

**A grande síntese:** a Aula 2 ensina que **o I/O é o gargalo**; a Aula 3 ensina que
**o tempo é um I/O que você não controla**. As duas aulas são o mesmo problema — confiar em
algo físico que não é confiável.

---

# PARTE 5 — Formulário (para consulta rápida)

**Latências:** L1 0,5 ns · RAM 100 ns · 1 MB seq. RAM 250 µs · SSD aleatório 16 µs ·
**HDD seek 10 ms** · rede transatlântica 150 ms

**Fórmulas:**
```
Desvio de relógio:      Δt = T × (PPM / 1.000.000)
WAF:                    bytes físicos ÷ bytes lógicos
QPS médio:              eventos_por_dia ÷ 86.400
Ingestão diária:        eventos × tamanho_do_payload
Banda:                  QPS × tamanho_do_payload
Storage:                ingestão_diária × dias_de_retenção
Storage com WAF:        storage_lógico × WAF
PPM → erro:             200 PPM = 200 μs por segundo
```

**Valores do exercício SIEM:** 100 M eventos/dia · 500 B · 2 anos → **50 GB/dia** ·
**18,25 TB/ano** · **36,5 TB** · **~1.157 QPS** · **11.574 QPS na rajada 10x** ·
**127,75 TB com WAF 3,5**

**Tabelas de decisão:**

| Situação | Escolha |
| --- | --- |
| Precisa de ordenação total do dataset | Batch (bounded) |
| Fluxo infinito | Janelas + watermarks |
| Não pode perder dado sob rajada | Backpressure ou log em disco |
| Dado perde valor em ms | Drop |
| Precisa reprocessar histórico | Log-based (Kafka), não fila RAM |
| Medir duração/latência | `CLOCK_MONOTONIC` |
| Evidência temporal probatória | PTP / hardware timestamp |
| Evitar perda silenciosa por concorrência | IDs lógicos, não LWW |

---

# PARTE 6 — Datas, entregáveis e regras (Aula 2, Slides 34)

| Item | Regra |
| --- | --- |
| **Fichamento individual** | 10% — artigo entre **16 selecionados** na plataforma |
| **Entrega e apresentação oral** | **Aula 10 — 22/10/2026** |
| **Plataforma** | https://fichamento.lovable.app |
| **Artigo em grupo** | 60% — **1 a 4 integrantes** |
| **Extensão mínima** | **7 páginas** |
| **Tema** | Obrigatoriamente ligado a sistemas intensivos em dados e microsserviços |
| **Registro** | Obrigatório na plataforma: tema, nome e e-mail de cada integrante |
| **Bônus de idioma** | Artigo em **inglês** ganha pontuação extra |
| **Bônus de publicação** | Submissão a periódico/evento (após validação) ganha pontuação extra |
| **Peer review** | 30% — revisão cega de 2 artigos de colegas |

> ⚠️ **Atenção:** a Aula 1 dizia "2 a 3 alunos" e "6 a 8 páginas"; a Aula 2 atualiza para
> **1 a 4 integrantes** e **mínimo de 7 páginas**. **Vale a Aula 2**, que é mais recente.
> Confirme com o professor se houver dúvida — regras de avaliação mudam.

---

# PARTE 7 — Como estudar (e como responder ao professor)

## O que ele realmente cobra

Olhando as três aulas, os padrões são claros:

1. **Você sabe quantificar?** Ele dá números em toda aula (PPM, WAF, QPS, P99). Respostas
   vagas não passam.
2. **Você conhece as ameaças à validade do *seu* argumento?** Ele dedica um slide inteiro.
3. **Você lê o artigo, ou só o resumo?** O fichamento tem apresentação oral justamente
   para isso.
4. **Você conecta teoria com consequência de negócio?** Todo slide técnico termina em
   impacto (falso negativo custa mais que indisponibilidade).

## Como se preparar para cada bloco

| Bloco | Como estudar |
| --- | --- |
| Latências | Decore a tabela e treine **traduzir para escala humana** — é o truque didático dele |
| LSM/WAF | Desenhe o caminho da escrita (MemTable → WAL → SSTable) de memória |
| Streaming | Compare RabbitMQ vs. Kafka em 4 eixos: armazenamento, histórico, consumo, reprocessamento |
| Tempo | Treine os cálculos de PPM — é o único item puramente aritmético |
| LWW | Reconte o cenário de x=1/x=2 com números diferentes |
| SIEM | Decore as **três anomalias** — são a aplicação de tudo |

## As provocações abertas (onde ele quer pesquisa)

Presentes nos slides, são **convites** e provavelmente virarão tema de artigo:

- Como reescrever regras SIEM para usar intervalos `[t_earliest, t_latest]` sem travar
  alertas em tempo real?
- **Como medir e publicar "incerteza temporal" como métrica de qualidade de dados?**
- Como combinar vector clocks com event time em pipelines OpenTelemetry?
- Como detectar manipulação anti-forense de relógio em endpoints comprometidos?
- Como benchmarkar impacto de drift, backpressure e late data em falsos negativos?
- A tolerância da watermark deveria ser fixa, estatística ou adaptativa por fonte?

**A segunda é a mais alinhada com você.** Governança de dados + transparência +
contabilidade + uma pergunta que o próprio professor formulou. Leve isso para a aula.

## Como conectar com a sua pesquisa

Sua linha (governança, transparência, contabilidade) **não é paralela** ao curso — ela é
uma aplicação direta dele:

| Conceito do curso | Sua tradução para dados públicos |
| --- | --- |
| LWW e perda silenciosa | Um **empenho ou lançamento contábil apagado sem exceção** = perda de evidência fiscal |
| event/ingestion/processing time | Um mesmo empenho tem três marcas temporais; confundir as três **inviabiliza a auditoria** |
| Watermarks e late data | Evento "do futuro" empurra lançamento legítimo para atrasado → **falha de prestação de contas** |
| Dual timestamping | Requisito de **auditabilidade**: a regra de negócio escolhe a âncora temporal |
| Axioma do log | Reprocessar o log reconstrói o estado — em conta pública, isso é **recomposição de trilha** |
| P99, não média | Um único ente que não consegue consultar é uma **exclusão de transparência** |
| False negativo em SIEM | Em transparência, o análogo é o **dado que não foi publicado e ninguém percebeu** |

**A frase que resume sua linha de pesquisa dentro da disciplina:**

> "Antipadrão de desempenho em sistema comercial é lentidão. O mesmo antipadrão em sistema
> de transparência pública é **perda de auditabilidade**."

---

# PARTE 8 — Resumo de uma página

- O inimigo é o **I/O**; o tempo é um I/O que você não controla.
- **Compute-intensive** otimiza CPU; **data-intensive** otimiza transferência.
- **Shared-nothing venceu** porque NUMA e barramento geram contenção e SPOF.
- **HDD seek = 10 ms** = 3,8 meses na escala humana → evite I/O aleatório.
- **LSM**: MemTable → WAL → SSTable imutável. Compactação causa **latência de cauda**.
- **WAF** = bytes físicos ÷ lógicos. Fator 3,5 = 3,5× de desgaste.
- **Unbounded não tem ordenação global** — é impossível, não é difícil.
- Saturação: **Drop** (perde), **Buffer** (acumula), **Backpressure** (desacelera).
- **Kafka (log)** guarda tudo e permite rebobinar; **RabbitMQ (RAM)** consome e esquece.
- **A verdade está no log**; o banco é cache materializado.
- Relógios derivam: **200 PPM**, 24 h sem sync = **17,28 s** de erro.
- **Wall clock pode andar para trás**; meça duração com monotonic.
- **LWW + drift = perda silenciosa de dado** — sem exceção, sem alarme.
- **TrueTime** expõe a incerteza como intervalo; **Lamport** abandona o tempo físico.
- **SIEM** é onde tudo isso vira **falso negativo**.
- Mitigação: **dual timestamping**, tolerância bounded, PTP, IDs lógicos.
- Metodologia: **Hook, Gap, IMRAD, ameaças à validade, MSR**.
- **Prazo do fichamento: 22/10/2026 (Aula 10).**
