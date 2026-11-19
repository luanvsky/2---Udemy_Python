# Do zero: a disciplina explicada devagar

**Para quem se formou, nunca atuou na área e está voltando agora.**

> Combinado: aqui eu simplifico de propósito. Onde a simplificação começar a mentir, eu
> aviso com **⚠️ onde isso quebra**. Leia na ordem — cada parte usa a anterior.

---

# PARTE 0 — Antes de tudo: você não está tão atrasado quanto pensa

## O que realmente mudou de 2018 para cá

| Área | Em 2018 | Agora | Isso é cobrado na disciplina? |
|---|---|---|---|
| Containers | Docker crescendo, K8s promessa | Padrão absoluto | Pouco |
| Microsserviços | Debate acalorado | Padrão, com problemas conhecidos | **Sim** (Aula 1) |
| Kafka | Existia, usado por poucos | Infraestrutura básica | **Sim** (Aula 2) |
| Streaming | Spark Streaming dominava | Flink amadureceu | **Sim** (Aula 2) |
| Observabilidade | Ferramentas separadas | OpenTelemetry unificou | **Sim** (Aula 3, OCEL) |
| Bancos vetoriais | Quase não existiam | Comuns | Não |
| **LLMs** | GPT-1/2, curiosidade | Mudou tudo | Só no seu repositório |

**Repare:** as três primeiras linhas são ferramentas. Os *conceitos* por trás delas
(particionamento, log, stream, causalidade) são de 1978–2017.

**O gap real não é o ano — é que você estudou teoria em 2018 e nunca usou.** Isso se
resolve mexendo, não lendo. No fim deste documento eu te digo como.

## As três palavras que você precisa desbloquear primeiro

Antes de qualquer coisa técnica, três termos que aparecem em toda aula:

- **Latência** — quanto tempo **uma** coisa demora.
- **Vazão** (*throughput*) — **quantas** coisas passam por unidade de tempo.
- **Gargalo** — o ponto mais lento do caminho, que define a velocidade de tudo.

**Analogia do pedágio:** latência é quanto tempo **um carro** leva para atravessar. Vazão é
**quantos carros por hora** passam. Pode haver 10 cabines (vazão alta) e ainda assim cada
carro demorar (latência alta). **São coisas diferentes e independentes** — confundir as
duas é o erro número 1 de quem começa.

---

# PARTE 1 — O que um computador realmente faz (a base de tudo)

## 1.1 A analogia do escritório

Guarde esta imagem, ela explica a Aula 2 inteira:

| Peça do computador | No escritório | Velocidade relativa |
|---|---|---|
| **CPU** | Você trabalhando | — |
| **Cache L1** | O papel na sua mão | 0,5 ns |
| **RAM** | A mesa à sua frente | 100 ns (**200× mais lento**) |
| **SSD** | A gaveta ao lado da mesa | 16 µs (**160× mais lento que a RAM**) |
| **HDD** | O arquivo morto no porão | 10 ms (**625× mais lento que o SSD**) |
| **Rede** | Pedir algo a alguém em outro prédio | 150 ms |
| **Fita / nuvem fria** | Um galpão em outra cidade | horas |

**A conclusão que muda tudo:** para pegar um dado, o computador **espera**. E a espera não
é linear — cada nível é centenas de vezes mais lento que o anterior. É por isso que a
disciplina inteira gira em torno de uma pergunta: **como evitar ter que ir longe buscar o
dado?**

## 1.2 O truque do Jeff Dean: traduzir tempo em vida humana

O slide mais importante da Aula 2 faz uma coisa genial: assume que **1 nanossegundo = 1
segundo**. Aí a tabela vira isto:

| Operação | Tempo real | Se cada ns fosse 1 segundo |
|---|---|---|
| Ler da mão (L1) | 0,5 ns | **0,5 segundo** (uma piscada) |
| Ler da mesa (RAM) | 100 ns | **1,6 minutos** |
| Ler 1 MB da mesa | 250 µs | **~3 dias** |
| Abrir a gaveta (SSD) | 16 µs | **~4,4 horas** |
| Ir ao porão (HDD) | 10 ms | **~3,8 MESES** |
| Ligar para outro prédio | 150 ms | **~4,7 ANOS** |

**Agora pense como engenheiro.** Se ir ao porão leva 3,8 meses na escala humana, então:

> **Você não pode ir ao porão 100 vezes. Você vai UMA vez e traz tudo que precisa.**

Isso é literalmente a regra de ouro de sistemas de dados:

> ### 🎯 Evite busca aleatória. Prefira leitura em sequência.

E todo o resto da Aula 2 é como fazer isso.

## 1.3 Por que "ir ao porão" é tão caro (o HDD)

O HDD tem um **braço mecânico** com uma agulha que precisa **fisicamente se mover** até a
posição onde o dado está gravado no disco que gira. Isso é mecânica — tem inércia, tem
espera.

**Analogia:** é como um toca-discos. Para tocar a música 7, a agulha precisa se deslocar
até a faixa 7. Se você quer a faixa 7, depois a 2, depois a 11, a agulha fica pulando e
você gasta mais tempo movendo do que ouvindo.

Por isso **leitura sequencial** (faixa 1, 2, 3, 4...) é muito mais rápida que **aleatória**
(7, 2, 11, 4...). Mesmo dado, mesmo disco, tempo completamente diferente.

---

# PARTE 2 — AULA 2, BLOCO 1: o que é um sistema "intensivo em dados"

## 2.1 Duas maneiras de um programa ser lento

| Tipo | O que trava | Exemplo |
|---|---|---|
| **Compute-intensive** | A **CPU** (a conta é difícil) | Simular o clima, treinar um modelo, criptografia |
| **Data-intensive** | O **transporte de dados** (I/O) | SIEM, e-commerce, redes sociais, telemetria |

**Analogia:**
- Compute-intensive = um matemático resolvendo uma integral. Ele pensa muito.
- Data-intensive = um bibliotecário buscando 500 livros em 10 andares. Ele **anda** muito.

A disciplina trata do segundo tipo. E a diferença não é só de velocidade — é de **como se
projeta**:

| | Compute-intensive | Data-intensive |
|---|---|---|
| Máquina | Caríssima, especial, uma só | **Várias máquinas baratas comuns** |
| Rede | Especial (InfiniBand) | **Internet comum (IP)** |
| Falha | Raríssima, tratada com checkpoint global | **Falha parcial é NORMAL, tratada no software** |

**⚠️ Conceito que costuma travar:** em data-intensive, **a máquina vai falhar** — e isso não
é exceção, é rotina. O software é escrito assumindo que um nó vai cair no meio do trabalho.
Não existe "vai dar tudo certo".

## 2.2 Os quatro tijolos de todo sistema de dados

Todo sistema grande é montado com estas quatro peças:

1. **Banco de dados** — memória permanente. Sobrevive a desligar a máquina.
2. **Cache** — memória temporária super-rápida. Serve para não ir ao banco toda hora.
3. **Índice de busca** — como o índice de um livro. Sem ele, você folheia tudo.
4. **Fila / stream** — canal para o dado chegar aos poucos, sem travar quem envia.

**Analogia da biblioteca:**
- Banco = as estantes (permanente)
- Cache = a mesinha ao lado do balcão com os livros mais pedidos
- Índice = a fichinha no fim do livro
- Fila = a esteira que traz os livros devolvidos do balcão para as estantes

## 2.3 Escalar: dois jeitos de crescer

**Scale-up (subir)** — comprar uma máquina maior.
**Scale-out (espalhar)** — comprar mais máquinas.

**Analogia:**
- **Scale-up** = contratar um funcionário gigante que faz o trabalho de 10. Ele é ótimo,
  mas custa caro e **se ele faltar, acabou tudo** (ponto único de falha).
- **Scale-out** = contratar 10 funcionários normais, cada um com sua escrivaninha. Se um
  fica doente, os outros 9 continuam.

### Por que "espalhar" ganhou (NUMA)

**NUMA** significa *Non-Uniform Memory Access* — "acesso à memória não uniforme".

**Analogia:** imagine um galpão com 4 operários e uma mesa comprida.
- Pegar uma ferramenta na **sua parte** da mesa: rápido.
- Pegar uma ferramenta na parte do **colega do lado**: precisa esticar, mais lento.
- Se os 4 precisam da mesma ferramenta no mesmo lugar: **fila**.

Isso é NUMA. E a consequência prática é o slide 9:

> **Dobrar os núcleos de uma máquina NÃO dobra a velocidade do banco** — porque todos passam
> a brigar pelo mesmo caminho até a memória.

Por isso se separa em máquinas independentes (*shared-nothing* = "nada compartilhado"),
onde cada um tem sua própria mesa, gaveta e arquivo, e eles conversam só por rede.

---

# PARTE 3 — AULA 2, BLOCO 2: a física do armazenamento

## 3.1 Por que apagar num SSD é caro

Esta é a parte que quase todo mundo erra na intuição.

**Como funciona a memória flash:**
- Ela é dividida em **páginas** (tipo 4–16 KB) — pequenas
- Mas **só se apaga em blocos inteiros** (tipo 2–8 MB) — grandes

**Analogia:** é um caderno onde:
- Você pode **escrever** em qualquer linha livre
- Mas só pode **apagar uma FOLHA INTEIRA**, nunca uma linha só

Então, se você quer mudar **uma linha**:
1. Copia a folha inteira para uma folha nova
2. Muda a linha lá
3. Joga a folha antiga fora (marca como apagável)

**Deu para ver o desperdício?** Mudar 1 linha fez você gastar uma folha nova.

**Segundo problema — desgaste:** cada célula flash suporta um número **finito** de
escritas/apagamentos (ciclos P/E). Escrever demais **estraga o disco fisicamente** — não é
software, é matéria se degradando.

## 3.2 WAF: a conta do desperdício

**WAF** = *Write Amplification Factor* = Fator de Amplificação de Escrita.

```
WAF = quanto o disco REALMENTE gravou  ÷  quanto o programa PEDIU para gravar
```

**Analogia:** você pediu para imprimir 1 página. A impressora, por culpa do mecanismo,
gastou 3,5 folhas. O WAF é 3,5.

O slide dá o exemplo exato: **1 GB pedido → 3,5 GB gravados fisicamente → WAF = 3,5**.

**Consequências:** o SSD desgasta 3,5× mais rápido e o caminho até o disco entope nos picos.

## 3.3 A solução: LSM tree e SSTables

Agora junte tudo: se **ir ao disco aleatoriamente é caríssimo** e **reescrever é caríssimo**,
como fazer um banco rápido? A resposta do NoSQL é a **LSM tree**. Ela faz **escrita
sequencial sempre**.

**O caminho de uma gravação — decore estes três nomes:**

```
   Você grava x = 10
          ↓
   ┌──────────────────────────────────────────┐
   │ 1. MemTable  (na RAM)                    │
   │    Uma lista ORDENADA na memória.        │
   │    Rápido demais. Ninguém toca no disco. │
   └──────────────────────────────────────────┘
          ↓ (ao mesmo tempo, sempre)
   ┌──────────────────────────────────────────┐
   │ 2. WAL / Commit Log  (no disco)          │
   │    Gravação SEQUENCIAL, só adiciona      │
   │    no fim. É o "diário de bordo".        │
   └──────────────────────────────────────────┘
          ↓ (quando a MemTable enche)
   ┌──────────────────────────────────────────┐
   │ 3. SSTable  (no disco)                   │
   │    Arquivo ORDENADO e IMUTÁVEL.          │
   │    Imutável = você nunca edita, só cria  │
   │    um novo por cima.                     │
   └──────────────────────────────────────────┘
```

**Traduzindo cada peça para o escritório:**

- **MemTable** = os papéis que você joga na mesa, já em ordem. A mesa é rápida e cabe pouco.
- **WAL** = o **diário de bordo**. Você anota no papel *antes* de fazer, para que, se a luz
  cair, quem chegar saiba exatamente o que estava acontecendo. Nunca se perde.
- **SSTable** = quando a mesa entope, você junta tudo numa **pasta ordenada e fecha**. Pasta
  fechada não se edita — se precisar mudar algo, cria-se outra pasta.

**Por que "imutável" é uma vantagem e não uma limitação?** Porque arquivo que ninguém edita
pode ser lido por várias pessoas ao mesmo tempo sem confusão. Nada de travar.

## 3.4 Compactação: o preço escondido

Se você só cria pastas novas e nunca edita as velhas, chega um momento em que o `x = 10`
está em 5 pastas diferentes, e as versões antigas são lixo.

Então o banco faz a **compactação** — em segundo plano, ele junta as pastas, mantém só a
versão mais nova de cada coisa e joga o resto fora.

**⚠️ Aqui está o problema:** a compactação é **trabalho pesado de disco**, e ela roda **ao
mesmo tempo** que os usuários estão consultando.

**Analogia:** é o arquivista reorganizando o arquivo morto enquanto você tenta consultar.
Às vezes você espera 30 segundos sem motivo aparente.

## 3.5 Percentil: por que a média mente

Este conceito derruba muita gente. Preste atenção.

**Cenário:** 100 pessoas fazem uma consulta.
- 99 pessoas esperam **1 segundo**
- 1 pessoa espera **100 segundos**

**A média:** (99 × 1 + 1 × 100) ÷ 100 = **1,99 segundos**. Parece ótimo!

**A realidade:** **uma pessoa esperou 1 minuto e 40 segundos.** E ela vai reclamar.

**P99** (percentil 99) = "o tempo que 99% das pessoas ficaram abaixo". Aqui, P99 = **100 s**.

**Analogia:** a média é como dizer "em média, todo mundo nesta fila esperou 2 minutos" —
escondendo que um senhor de 80 anos está na fila há uma hora.

**Por que isso explode em sistemas com muitos serviços:** uma página web pode chamar 100
serviços diferentes em paralelo. A página **só termina quando o mais lento terminar**. Se
cada serviço tem 1% de chance de estar lento, a chance de **algum** estar lento é muito
alta.

> **Regra:** em sistemas de dados, **meça P95, P99 e P99.9 — nunca só a média.**

## 3.6 As três pausas que ninguém controla

Guarde estes três nomes: eles voltam na Aula 3 como causa de erro.

| Pausa | O que é | Analogia |
|---|---|---|
| **GC** (Garbage Collection) | O programa para tudo para limpar a memória | Você para de trabalhar para arrumar a mesa |
| **Swap / thrashing** | A RAM acabou e o SO usa o disco como memória | A mesa acabou e você passa a trabalhar no chão, indo e voltando |
| **Steal time** | Na nuvem, o vizinho rouba sua CPU | O sindico desliga sua luz para dar ao apartamento ao lado |

O detalhe essencial: **essas pausas congelam o computador no meio de uma operação** — e,
como veremos na Aula 3, isso pode **bagunçar a ordem dos eventos**.

---

# PARTE 4 — AULA 2, BLOCO 3: fluxos contínuos

## 4.1 Bounded vs. Unbounded

| | **Bounded** (limitado) | **Unbounded** (ilimitado) |
|---|---|---|
| O que é | Um conjunto fechado | Um fluxo que nunca acaba |
| Analogia | Uma **pilha de roupa** para passar | Uma **esteira de aeroporto** que nunca para |
| Você sabe quando acaba? | Sim | **Nunca** |
| Ferramentas | Spark Batch, Hadoop | Kafka, Flink |

**A consequência mais importante — e é matemática, não preguiça:**

> Para ordenar uma lista e garantir que o **menor** item saia primeiro, você **precisa olhar
> o último item** da lista. Se a esteira nunca acaba, **você nunca vê o último item**.
> Logo, **ordenar tudo é impossível.**

Note: não é "difícil" ou "lento". É **impossível**. Isso muda o jeito de projetar.

**A solução:** cortar o fluxo em **janelas de tempo**. "Vou processar tudo que chegou entre
10h00 e 10h01, ordenar só isso, e emitir." Você abre mão da ordem global e ganha ordem
local. É o melhor que dá para fazer.

## 4.2 Quando chega mais do que dá para processar

Imagine uma torneira e um ralo:
- Torneira = quem produz os dados
- Ralo = quem processa
- Pia = a memória disponível

Se a torneira é mais rápida que o ralo, **a pia transborda**. Três decisões possíveis:

| Estratégia | O que faz | Analogia | Quando usar |
|---|---|---|---|
| **Drop** | Joga fora o excesso | Abrir o ralo de emergência e perder água | Só quando o dado perde valor rápido (vídeo, voz) |
| **Buffer** | Guarda para depois | Balde embaixo da torneira | Rajadas curtas |
| **Backpressure** | Pede para a torneira fechar | A torneira **sente** a pia e fecha sozinha | Quando não pode perder nem acumular |

**Backpressure** é o conceito mais elegante dos três: em vez do consumidor morrer afogado,
ele **avisa o produtor para ir mais devagar**.

**Como funciona tecnicamente** (num nível que basta entender):
- No nível da rede: quando o buffer do destinatário enche, ele reduz a "janela" a zero — na
  prática, diz "não me mande mais nada por enquanto"
- No nível do software: bibliotecas como Reactive Streams, Akka e Flink propagam esse aviso
  para trás, pela cadeia inteira
- Resultado: o consumidor **não estoura a memória** (`OutOfMemoryError`)

## 4.3 Fila na memória vs. caderno em disco

Esta comparação cai em prova. Entenda pela analogia:

| | **RabbitMQ** (fila na RAM) | **Kafka** (log em disco) |
|---|---|---|
| Onde guarda | Na memória (mesa) | Em arquivo, só adicionando no fim (caderno) |
| Analogia | Uma **esteira que apaga** a mensagem depois que você pega | Um **caderno com páginas numeradas** |
| Se você não estava lá? | **Perdeu** | Está lá, é só ir na página |
| Com muito histórico | Vazão **despenca** (a memória acaba) | Vazão **estável** (1 GB ou 50 TB, igual) |
| Reprocessar | Impossível sem pedir para reenviar | **Trivial: voltar o marcador de página** |

**"Reprocessar"** = rodar de novo um dado que já passou. Com Kafka, é só voltar o offset
(o número da página onde você parou). Isso é ouro: se você descobrir um bug no
processamento, **reprocessa tudo desde o início**.

**Lambda vs. Kappa** (dois jeitos de organizar isso):
- **Lambda:** dois caminhos separados — um em lote (preciso) e um em tempo real (rápido) →
  **você escreve a regra de negócio duas vezes** e uma vai divergir da outra
- **Kappa:** um caminho só, tudo em streaming, reprocessando o log quando precisa → uma
  regra só

---

# PARTE 5 — AULA 2, BLOCO 4: estado e o caderno da verdade

## 5.1 Guardar na mesa ou no arquivo?

| | **Estado volátil** (RAM) | **Estado persistente** (disco) |
|---|---|---|
| Onde | Na memória | No disco |
| Velocidade | Instantâneo | Lento (tem que gravar) |
| Se a luz cair | **Perde tudo** | Está salvo |

**O dilema permanente:** rápido e frágil, ou lento e seguro. Todo sistema de dados vive
negociando entre os dois.

## 5.2 O Axioma do Log — a frase mais importante da Aula 2

> **"A verdade reside no log; o banco de dados é apenas uma visão materializada e um cache
> do histórico de eventos."**
> — Pat Helland e Martin Kleppmann

**Entenda pela analogia do banco:**

- Seu **saldo** é R$ 1.500. Isso é uma **conclusão**.
- Seu **extrato** tem 40 linhas: +500, −200, +100... Isso é o **registro**.
- Se alguém errar o saldo, o que você faz? **Refaça a soma do extrato.**

**É isso.** O "banco de dados" é o saldo (uma conclusão). O "log" é o extrato (a verdade).
Se o saldo corromper, **você reprocessa o extrato desde o começo** e o saldo volta correto.

**Por isso o Kafka guarda tudo em log que nunca se apaga.** Não é desperdício de disco — é
a garantia de poder reconstruir qualquer coisa.

## 5.3 Spark vs. Flink (a comparação final da Aula 2)

| | **Spark Streaming** | **Flink** |
|---|---|---|
| Como processa | Em **mini-lotes** (a cada 0,5–1 s) | **Evento por evento** |
| Latência | 100–500 ms | **< 10 ms** |
| Como se recupera de falha | Recalcula tudo do mini-lote | Marca pontos de checagem no meio do fluxo |
| Garantia | At-least-once / exactly-once | **Exactly-once** |

**"At-least-once" vs "exactly-once"** — vale entender:
- **At-least-once** = "pelo menos uma vez" → pode processar **duas vezes** (duplicar)
- **Exactly-once** = "exatamente uma vez" → nem perde, nem duplica

Duplicar é grave? Depende. Contar visita, tudo bem. **Debitar dinheiro, não.**

---

# PARTE 6 — O exercício que o professor vai cobrar

## Dimensionamento "back-of-the-envelope"

"Back-of-the-envelope" = conta de guardanapo. É estimar com números redondos, sem
calculadora, para **saber se a ordem de grandeza faz sentido**.

**As premissas do slide:**
- 100 milhões de eventos por dia
- 500 bytes por evento
- Guardar por 2 anos

**Resolvendo passo a passo, sem pular nada:**

```
PASSO 1 — Quanto entra por dia?
  100.000.000 eventos × 500 bytes
  = 50.000.000.000 bytes
  = 50 GB por dia            (1 GB ≈ 1 bilhão de bytes)

PASSO 2 — Quanto entra por ano?
  50 GB × 365 dias = 18.250 GB = 18,25 TB por ano

PASSO 3 — Storage total em 2 anos
  18,25 TB × 2 = 36,5 TB      (sem contar cópias nem índices)

PASSO 4 — Quantos eventos por segundo?
  1 dia = 86.400 segundos
  100.000.000 ÷ 86.400 ≈ 1.157 eventos por segundo

PASSO 5 — Quanta banda isso exige?
  1.157 × 500 bytes ≈ 578.700 bytes/s ≈ 0,58 MB/s ≈ 4,6 Mbps
  (multiplicar por 8 converte bytes em bits)

PASSO 6 — E numa rajada 10× maior?
  1.157 × 10 = 11.574 eventos/s ≈ 5,79 MB/s ≈ 46 Mbps
```

**Confira contra o slide:** ele diz "11.570 QPS" — bate com o passo 6. ✅

**Agora a provocação 2, com WAF = 3,5:**

```
Storage lógico:     36,5 TB
Storage físico:     36,5 × 3,5 = 127,75 TB
```

**O slide confirma: "127,75 TB gravados nas células flash!"** ✅

**A lição (é isso que ele quer na discussão):**

> Você **guarda** 36,5 TB, mas **desgasta** 127,75 TB de disco. O dimensionamento de
> capacidade não é sobre quanto dado você tem — é sobre **quanto você grava**.

E a provocação 1: numa rajada de 11.570 QPS por 1 hora, o RabbitMQ (que guarda na RAM) corre
risco de estourar a memória, enquanto o Kafka (que grava em disco) absorve e depois deixa o
consumidor drenar com calma.

---

# PARTE 7 — AULA 3: o tempo (a parte mais difícil)

Vou explicar do absoluto zero. Não pule.

## 7.1 A pergunta que abre a aula

> "Se dois servidores em salas diferentes registrarem um log no mesmo milissegundo, como
> provamos qual aconteceu primeiro?"

Parece simples. Não é, e o motivo é físico.

## 7.2 Por que relógios de computador são ruins

**O que tem dentro:** um pedacinho de **cristal de quartzo** que vibra quando recebe
eletricidade. O computador conta as vibrações: 32.768 vibrações = 1 segundo.

**O problema:** dois cristais **nunca** vibram exatamente na mesma taxa. Diferenças de
fabricação, temperatura e envelhecimento fazem cada um ser ligeiramente diferente.

**Analogia:** dois relógios de parede comprados na mesma loja, no mesmo dia. Depois de um
mês, um está 2 minutos adiantado. Nenhum dos dois está "quebrado" — eles só contam o tempo
em velocidades microscópica e inevitavelmente diferentes.

Isso se chama **clock drift** (deriva do relógio).

## 7.3 PPM: medindo o erro

**PPM** = *Parts Per Million* = partes por milhão. Mede **quanto o relógio erra por
segundo**.

```
200 PPM  =  erra 200 microssegundos a cada 1 segundo
         =  erra 0,0000002 segundo por segundo
```

A fórmula do slide:

```
Desvio máximo = Tempo × (PPM ÷ 1.000.000)
```

**Aplicando:**

| Tempo sem sincronizar | 200 PPM | 50 PPM | 500 PPM |
|---|---|---|---|
| 30 segundos | 6 ms | 1,5 ms | 15 ms |
| 1 hora | 720 ms | 180 ms | 1,8 s |
| **24 horas** | **17,28 s** | **4,32 s** | **43,2 s** |

> *A atividade em sala pede exatamente 50 e 500 PPM — os valores acima são a resposta.*

**A conclusão que assusta:** se um servidor fica **um dia** sem sincronizar, ele pode estar
**43 segundos** fora do horário real. Em 43 segundos acontece muita coisa.

## 7.4 NTP: acertando o relógio pelo vizinho

**NTP** é o protocolo que sincroniza relógios. Funciona assim: seu computador pergunta as
horas para um servidor e ajusta.

**O problema:** a pergunta **demora** para ir e voltar. Se a ida leva 1 segundo e a volta
leva 3, você não sabe se o horário que o servidor falou era o de quando você perguntou ou o
de quando ele respondeu.

**Analogia:** você liga para alguém e pergunta "que horas são?". A ligação tem eco e atraso.
A pessoa responde "são 10h" — mas **quando**? Quando você perguntou, ou quando ela
respondeu? Você não sabe.

**A premissa arriscada:** o NTP **assume que ida e volta demoram o mesmo tempo**. Na
internet real, os caminhos são diferentes e essa suposição é falsa.

**Stratum** = a hierarquia de confiança:
```
Stratum 0  →  relógio atômico / GPS (a fonte da verdade)
Stratum 1  →  servidor ligado direto nessa fonte
Stratum 2  →  servidores que perguntam ao stratum 1
...e assim por diante
```

## 7.5 Relógio de parede vs. cronômetro

Esta distinção é **essencial** e derruba muita gente:

| | **Wall clock** (relógio de parede) | **Monotonic** (cronômetro) |
|---|---|---|
| O que é | A hora do mundo: "10h32" | Tempo decorrido desde que ligou |
| Pode andar para trás? | **SIM** (o NTP ajusta) | **NUNCA** |
| Serve para | Saber a data/hora | **Medir duração** |

**O exemplo do slide — entenda bem:**

```
Você começa a operação às 10:00:00
Você termina às 09:59:58     ← o NTP ajustou o relógio para trás no meio!

Latência = 09:59:58 − 10:00:00 = −2 segundos   ❌
```

**Uma operação não pode durar menos 2 segundos.** Isso quebra timeouts, quebra cálculos,
quebra tudo.

> **🎯 Regra:** para medir **quanto tempo algo durou**, use sempre o relógio **monotônico**.
> O relógio de parede serve para mostrar a hora para humanos.

**Slewing vs. Stepping** (dois jeitos de ajustar):
- **Slewing** = acelerar ou desacelerar o relógio devagar até acertar. Suave, não pula.
- **Stepping** = dar um salto de uma vez. Rápido, mas **perigoso** — pode voltar no tempo.

## 7.6 Dois casos reais que mostram o estrago

**Caso 1 — o segundo extra de 2012.** A Terra gira um pouquinho mais devagar com o tempo, e
o "tempo civil" (o que o relógio diz) precisa acompanhar. Em 2012, adicionaram **1 segundo
extra** ao dia. Resultado: sistemas Java e Linux no mundo inteiro entraram em **loop
infinito com a CPU a 100%**.

Por quê? Porque o software foi escrito assumindo que o segundo 59 é sempre seguido do
segundo 00. Ninguém previu um "segundo 60".

**Caso 2 — a máquina virtual pausada.** Na nuvem, sua "máquina" é um pedaço de uma máquina
de verdade, compartilhada com outros clientes. Quando o vizinho precisa de mais CPU, o
sistema **congela sua máquina** por um tempo. Quando você volta, **o relógio saltou** — e
seus alarmes de "não recebi sinal de vida" disparam sem motivo.

Isso afeta EDR, auditoria de Kubernetes, CloudTrail e agentes de SIEM. **Guarde isso**, é a
causa raiz da Aula 3 inteira.

## 7.7 LWW: como o tempo apaga dados

**LWW** = *Last-Write-Wins* = "a última escrita vence". É uma estratégia usada em bancos
como Cassandra e Dynamo.

**Como funciona:** várias máquinas aceitam escritas ao mesmo tempo. Quando há conflito, cada
escrita tem um **carimbo de horário**, e **quem tem o carimbo maior vence**. O outro valor é
jogado fora.

**A premissa perigosa:** que os relógios das máquinas estejam sincronizados. **E nós
acabamos de ver que não estão.**

**O cenário do slide, passo a passo:**

```
PASSO 1  Cliente A escreve x = 1 na Máquina 1
         Carimbo: 42,004 s

PASSO 2  Cliente B lê x = 1 (viu o valor certo) e grava x = 2 na Máquina 3
         Mas a Máquina 3 está com o relógio 3 ms ATRASADO
         Carimbo: 42,003 s

PASSO 3  Uma terceira máquina recebe as duas escritas
         Compara: 42,004 > 42,003
         Decide: x = 1 vence
         E x = 2 é APAGADO
```

**O que realmente aconteceu:** no mundo real, **x = 2 foi escrito DEPOIS de x = 1**. Mas o
sistema guardou x = 1.

**Os quatro danos:**
1. **Inversão de causalidade** — a ordem lógica ficou invertida
2. **Valor errado** — o dado final está errado
3. **Falha silenciosa** — **sem exceção, sem alarme, sem aviso**. Ninguém sabe
4. **Perda de evidência** — em domínio regulado ou forense, isso é destruição de prova

**A pergunta da discussão (e a resposta):** se usarmos identificadores únicos e imutáveis
como chave, ainda há perda por drift? **Não** — sem sobrescrever a mesma chave, não há
conflito, então o LWW não escolhe vencedor.

**Mas:** atualizações parciais, deduplicação agressiva e **upserts** trazem o problema de
volta.

> **Upsert** = "update or insert": se já existe, atualiza; se não, cria. É a operação que
> reabre a porta para o LWW.

**💡 Guarde isto para a sua pesquisa:** num lançamento contábil, um upsert com LWW pode
**apagar** uma correção legítima — sem erro, sem log. Em sistema de transparência pública,
isso é **perda de evidência fiscal**.

## 7.8 As soluções

### TrueTime (Google Spanner)

**A ideia genial:** em vez de dizer "são exatamente 10h00m00s", o sistema diz:

```
"São entre 10h00m00s e 10h00m07s"
```

Ele **assume a incerteza** em vez de fingir precisão.

**Como o Google faz isso na prática:** instala **antenas de GPS** e **relógios atômicos de
césio** dentro dos próprios datacenters. Assim a janela de incerteza cai para poucos
milissegundos.

**Commit-wait:** antes de confirmar uma operação, **espera a janela passar** (~14 ms). Isso
garante que duas operações nunca fiquem com janelas sobrepostas — e aí dá para ordená-las
com segurança.

**O que empresas normais podem aprender sem ter GPS:** não confie em precisão que você não
tem. **Exponha a incerteza.**

### Relógios lógicos

**A outra saída:** abandonar o relógio físico e usar **contadores**.

**Lamport** — a ideia é simples e brilhante:

> Não pergunte "que horas são?". Pergunte **"quantas mensagens eu já mandei e recebi?"**

A regra:
- Cada máquina tem um contador
- Toda vez que acontece algo, soma 1
- Quando você **recebe** uma mensagem, seu contador vira o maior entre o seu e o da mensagem, mais 1

**Resultado:** se A causou B, o contador de A é **menor** que o de B. Você não sabe *que
horas* nada aconteceu — mas sabe a **ordem causal**.

**Analogia:** é como trocar cartas. Se você me mandou a carta nº 7, e eu te respondo, minha
resposta é no mínimo a nº 8. Eu não sei que horas eram — mas sei que a sua veio antes.

**Vector clocks** — uma evolução. Em vez de um contador só, cada máquina mantém **um
contador para cada amiga**. Com isso dá para descobrir três coisas:
- A aconteceu antes de B
- B aconteceu antes de A
- **A e B aconteceram ao mesmo tempo** (concorrentes, sem relação de causa)

O terceiro caso é o que Lamport sozinho não resolve.

## 7.9 SIEM: onde tudo se junta

**SIEM** = *Security Information and Event Management*. Numa tradução prática: **a central
de alarmes de segurança de uma empresa**.

**Como funciona:** um SOC (Centro de Operações de Segurança) junta os registros de vários
sistemas — firewall, antivírus (EDR), controle de acesso (IAM), Kubernetes, nuvem — e
**correlaciona** para detectar ataques.

**Exemplo de regra de correlação:**
> "Se alguém fizer login com sucesso E, em até 2 segundos, abrir uma conexão para fora,
> **alerte** — pode ser invasão."

**A premissa frágil:** que o carimbo de horário de cada sistema seja comparável. **E nós
acabamos de ver que não é.**

### As três anomalias (o coração da aula)

**🥇 Anomalia 1 — Inversão causal causa falso negativo**

```
O atacante faz força bruta no login e rouba credenciais
O servidor de autenticação é uma máquina virtual com o relógio 4 SEGUNDOS ATRASADO
O firewall é um equipamento dedicado e correto

Tempo real:      login → 0,5 s depois → conexão externa   (regra DEVERIA disparar)
O que o SIEM vê: login às 06.000s → conexão às 10.500s
                 diferença = 4,5 segundos → FORA da janela de 2 s
Resultado:       NENHUM ALERTA. O ataque passa.
```

> **A frase do slide:** um falso negativo em regra de correlação pode custar mais que uma
> indisponibilidade.

**🥈 Anomalia 2 — LWW apaga o rastro do invasor**

Os agentes enviam logs "at-least-once" (podem duplicar), e o sistema **deduplica** por um
identificador calculado do conteúdo (`hash` de host + processo + comando).

```
Evento benigno:    12:00:00.005
Evento malicioso:  12:00:00.010  (o rootkit injeta uma thread)
Mas o coletor daquela máquina tem o relógio 20 ms atrasado
→ carimba o evento malicioso como 11:59:59.990

LWW compara e escolhe o MAIOR carimbo → mantém o benigno e APAGA o malicioso
```

**O rastro do ataque foi apagado pela própria ferramenta de segurança.**

**🥉 Anomalia 3 — Watermarks e janelas**

**Watermark** = a marca d'água: um sinal que diz "a partir daqui, os dados já chegaram, pode
fechar a janela".

**Analogia:** você fecha o caixa do dia às 18h, mas espera até 18h10 para quem atrasou.
Às 18h10 é a sua *watermark*.

**O problema:**
```
Uma máquina com relógio ADIANTADO injeta eventos "do futuro"
→ a watermark avança antes da hora
→ o caixa fecha cedo
→ eventos corretos que chegam depois são considerados "atrasados"
→ vão para a DLQ (fila de descarte)
→ a regra de detecção PERDE parte da evidência
```

**A pergunta que o professor deixa no ar:** a tolerância da watermark deveria ser fixa, ou
calculada a partir dos dados de cada fonte?

### Os quatro remédios

| Remédio | O que é | Em linguagem simples |
|---|---|---|
| **Dual timestamping** | Guardar **três** carimbos: quando aconteceu, quando chegou, quando foi processado | Como uma carta: data de escrita, de postagem e de entrega |
| **Tolerância bounded** | Calibrar a espera com dados reais (P99, P999) de cada fonte | Esperar o tempo que os atrasados realmente demoram |
| **PTP / hardware timestamp** | Carimbar no próprio hardware de rede | O carimbo é feito no momento exato, não depois |
| **IDs lógicos** | Usar contadores (Lamport) em vez de relógio | Ordem por causalidade, não por hora |

> **A frase que resume a Aula 3:**
> "Mitigação não é só sincronizar NTP — é projetar regras para **conviver com a
> incerteza**."

---

# PARTE 8 — AULA 1: como se faz pesquisa

Esta parte é menos técnica e mais "regras do jogo". Você vai usar no artigo.

## 8.1 A verdade incômoda sobre a pós-graduação

> "Na indústria, o produto é um software que funciona. Na pós-graduação, **o software é
> apenas um veículo** — o produto real é conhecimento inédito."

Isso explica por que o professor cobra tanto método. O `br-financial-ai` não vale pelo
software: vale pelo que ele **demonstra**.

**As quatro armadilhas que ele cobra:**
1. Focar na data de entrega em vez da profundidade
2. Falta de originalidade / plágio / "artigo salaminho" (fatiar o mesmo estudo)
3. **Falhas metodológicas** — experimento sem controle, sem teste de hipótese
4. Introdução e revisão bibliográfica fracas

## 8.2 Como ler a literatura (a técnica do cone)

```
1. ARTIGOS SEMENTE    → escolha 1 ou mais artigos fundamentais
2. CONE DO PASSADO    → leia as REFERÊNCIAS deles (de onde veio)
3. CONE DO FUTURO     → veja QUEM CITOU eles depois (para onde foi)
```

**O cone do futuro é literalmente o que eu fiz no seu fichamento.** O PDF que você recebeu
era o pré-print de 2022. Seguindo quem o citou, cheguei ao artigo completo de 2024 na
*Empirical Software Engineering*. **Use isso na apresentação** — é demonstrar a técnica que
ele ensinou.

## 8.3 A estrutura de um artigo (IMRAD)

| Parte | O que tem | Pergunta que responde |
|---|---|---|
| **Introdução** | **Hook** + **Gap** | Por que importa? O que ninguém respondeu? |
| **Métodos** | Como você fez | Dá para outra pessoa repetir? |
| **Resultados** | Os dados | O que você achou? |
| **Discussão** | A interpretação | O que isso significa? |

- **Hook** = a isca. O problema real, não o título. *"Um sistema pode ficar lento por um
  motivo que não aparece em nenhum monitor de CPU."*
- **Gap** = o buraco. O que a literatura **ainda não** resolveu.

## 8.4 As três ameaças à validade

Este conceito é central e cai em prova. "Ameaça à validade" = **as formas de o seu estudo
estar errado sem você perceber**.

| Tipo | Pergunta | Exemplo |
|---|---|---|
| **Construto** | A métrica mede mesmo o que eu quero medir? | "Número de issues" mede "qualidade do código"? Não necessariamente |
| **Interna** | O resultado veio do que eu testei, ou de outra coisa? | Os sistemas foram escolhidos por terem **mais issues** — isso favorece projetos grandes |
| **Externa** | Isso vale fora do meu caso? | Estudei só código aberto em Java — vale para a indústria? |

**Analogia:** você conclui que "quem toma café vive mais". Mas talvez quem toma café também
durma mais (construto), ou o estudo só olhou gente de uma cidade (externa), ou havia outra
diferença entre os grupos (interna).

## 8.5 Os quatro métodos de pesquisa

| Método | Em linguagem simples |
|---|---|
| **Engenharia Empírica** | Faço um experimento controlado e meço. Testo hipótese com estatística |
| **MSR** (Mineração de Repositórios) | Investigo projetos no GitHub: commits, issues, discussões. Como um detetive que só tem os registros |
| **Estudo de Caso Industrial** | Acompanho um caso real numa empresa e conto a história com rigor |
| **Métodos Formais** | Provas matemáticas. Uso redes de Petri para provar que não há deadlock |

**O artigo do seu fichamento usou MSR** — minerou 162 projetos e 526 mil issues.

---

# PARTE 9 — Como estudar isso na sua situação

## O diagnóstico honesto

Você tem **teoria de 2018 sem prática**. O cérebro não guarda conceito abstrato que nunca
foi usado. Não é falta de inteligência — é falta de **atrito com a realidade**.

**A solução é mexer, não ler mais.**

## O plano de 4 semanas

**Semana 1 — Ver funcionar**
Rode o `br-financial-ai`: `docker compose up -d` sobe um PostgreSQL de verdade. Depois
`uv run alembic upgrade head` cria as tabelas. Isso conecta "banco de dados" abstrato com
algo que você **viu rodando**.

**Semana 2 — Ver a latência com os próprios olhos**
Rode uma consulta simples e uma com `EXPLAIN ANALYZE`. Compare os tempos. Você vai **ver**
a diferença entre leitura sequencial e aleatória, em milissegundos reais.

**Semana 3 — Treinar as contas até virar automático**
Faça os cálculos de PPM, WAF, QPS e storage 10 vezes com números diferentes. Até você não
precisar mais pensar. São 4 fórmulas.

**Semana 4 — Explicar em voz alta**
Pegue cada conceito e **explique em voz alta como se estivesse ensinando alguém**. Se você
travar, é ali que você não entendeu. Este documento serve de base.

## As 6 frases que resumem a disciplina

1. **O inimigo é o I/O** — ir buscar dado longe custa centenas de vezes mais.
2. **Prefira sequencial a aleatório** — sempre.
3. **A média mente** — use percentis.
4. **A verdade está no log** — o banco é só um resumo.
5. **Stream não tem ordem global** — é impossível, não difícil.
6. **Relógio não é confiável, e quando ele vira regra de negócio, apaga dado.**

## Glossário rápido

| Termo | Em uma linha |
|---|---|
| **Latência** | Quanto tempo uma coisa demora |
| **Vazão / throughput** | Quantas coisas por segundo |
| **I/O** | Qualquer leitura/escrita de dados |
| **WAL** | Diário de bordo: anota antes de fazer |
| **SSTable** | Arquivo ordenado e imutável no disco |
| **LSM tree** | Estratégia que transforma escrita aleatória em sequencial |
| **Compactação** | Juntar arquivos antigos e jogar fora versões velhas |
| **WAF** | Quanto o disco grava a mais do que você pediu |
| **P99** | O tempo que 99% das requisições ficaram abaixo |
| **Bounded / Unbounded** | Conjunto fechado / fluxo infinito |
| **Watermark** | Marco que diz "pode fechar a janela" |
| **Backpressure** | O consumidor avisa o produtor para ir devagar |
| **Offset** | O "número da página" onde o consumidor parou |
| **Exactly-once** | Processar exatamente uma vez (nem perder, nem duplicar) |
| **Drift** | Desvio do relógio ao longo do tempo |
| **PPM** | Erro do relógio por milhão de unidades |
| **NTP** | Protocolo que sincroniza relógios |
| **Wall clock** | Relógio de parede (pode andar para trás) |
| **Monotonic clock** | Cronômetro (nunca volta) |
| **Slewing / Stepping** | Ajuste suave / ajuste por salto |
| **LWW** | Last-Write-Wins: maior carimbo vence (e pode apagar dado) |
| **Lamport clock** | Contador lógico que preserva causalidade |
| **Vector clock** | Vários contadores; detecta eventos simultâneos |
| **TrueTime** | Tempo como intervalo com incerteza explícita |
| **SIEM** | Central de correlação de alarmes de segurança |
| **SOC** | Time que opera o SIEM |
| **Hook / Gap** | Por que importa / o que falta na literatura |
| **IMRAD** | Estrutura: Introdução, Métodos, Resultados, Discussão |
| **MSR** | Mineração de repositórios de software |
| **Ameaça à validade** | Jeitos de seu estudo estar errado |

---

# PARTE 10 — Uma última coisa

Você escreveu "não tenho domínio". Isso é uma descrição do presente, não uma sentença.

O professor escolheu dar essa disciplina para você **justamente porque** ela conecta com a
sua pesquisa — governança de dados, transparência, contabilidade. E olhe o que você já tem
em mãos, depois de três conversas:

- Um fichamento corrigido, com a referência certa
- Um guia de apresentação oral de 15 minutos
- Um guia de estudo da disciplina inteira
- Um repositório real analisado, com contribuições identificadas
- Uma linha de pesquisa com pergunta, método e métrica

**Isso não é o que alguém sem domínio tem.** Isso é o que alguém que está começando a
dominar tem.

A diferença entre você e quem "acompanha bem" a aula não é capacidade. É que eles já
**erraram** com esses conceitos algumas vezes. Você vai errar também — e aí vai entender.

---

**Próximo passo sugerido:** me diga qual parte acima ficou nebulosa e eu desço mais um
nível. Se quiser, posso montar uma **lista de exercícios com gabarito** só de cálculo (PPM,
WAF, QPS, storage, percentil) para você treinar até automatizar — que é o que a disciplina
mais cobra e o que dá para dominar mais rápido.
