# Alinhamento: disciplina, artigo, repositório do professor e sua linha de pesquisa

---

## 1. O mapa dos atores

Você tem, neste momento, quatro peças que se encaixam de forma incomum. Vale explicitar o
encaixe antes de escolher qualquer coisa.

| Peça | O que é | Por que importa |
| --- | --- | --- |
| **A disciplina** | Tópicos Avançados em ES e SI — PROCC/UFS, Prof. Dr. Fabio Gomes Rocha | Ensina DIS, microsserviços, incerteza temporal, SIEM, e trata **MSR** e **estudo de caso industrial** como métodos de primeira classe |
| **O artigo do fichamento** | Muse et al., *Data-access performance anti-patterns*, EMSE 2024 | É um **exemplar de MSR** + survey, com funil de mineração auditável e taxonomia |
| **O repositório do professor** | `gomesrocha/br-financial-ai` | É **dados financeiros públicos brasileiros** (CVM/B3) — transparência e contabilidade, exatamente o seu interesse |
| **Seu interesse** | Governança de dados no setor público, transparência, contabilidade | Coincide com o domínio do repositório e com o objeto do artigo (acesso a dados) |

**A convergência:** o artigo lhe dá um **método** (mineração de repositórios + codificação
aberta + taxonomia + survey); o professor lhe dá um **objeto empírico** (dados financeiros
públicos brasileiros); a disciplina lhe dá o **enquadramento teórico** (DIS, persistência
poliglota, incerteza temporal, ameaças à validade). Falta você escolher o recorte.

---

## 2. Como a disciplina avalia — e como cada peça se encaixa

| Componente | Peso | O que exige | Sua peça |
| --- | --- | --- | --- |
| **Fichamento individual** | 10% | Artigo atribuído, modelo oficial, apresentação oral 10–15 min | Documentos `04` e `05` |
| **Artigo em grupo** | 60% | IEEE/ACM, 6–8 p., 2–3 alunos, **"incentivado a conexão com a proposta de dissertação no PROCC"** | É aqui que a linha de pesquisa entra |
| **Peer review** | 30% | Revisão cega de 2 artigos de colegas, parecer com *Accept/Minor/Major/Reject* | Você já terá praticado isso lendo as ameaças à validade do artigo |

**Leitura estratégica:** o professor **explicitamente convida** a ligar o artigo de 60% à
dissertação. Isso significa que o trabalho em grupo não é um exercício descartável — é o
embrião da sua dissertação. Escolha o tema pensando nos próximos dois anos, não no
semestre.

---

## 3. Três linhas de pesquisa possíveis (com grau de risco)

### 🥇 Opção A — Antipadrões de acesso a dados em sistemas de transparência pública

**Pergunta:** *Quais antipadrões de acesso a dados são prevalentes em sistemas de código
aberto de transparência e dados abertos governamentais, e quais têm impacto sobre
auditabilidade e não apenas sobre desempenho?*

- **Método:** replicação estendida do artigo — MSR (GitHub API, filtro de qualidade, query
  por palavras-chave, codificação aberta até saturação, *card sorting*) + survey com
  desenvolvedores de govtech.
- **Dados:** repositórios de portais de transparência, dados abertos, orçamento público,
  prestação de contas.
- **Contribuição:** o catálogo existente foi construído sobre NoSQL comercial. Você o
  **transfere para o domínio público**, onde o custo do antipadrão não é só lentidão — é
  **perda de rastreabilidade**. Esse deslocamento de "desempenho" para "auditabilidade" é
  a contribuição original.
- **Por que funciona:** replicação com extensão de domínio é o formato de primeiro estudo
  mais defensável que existe. O método está pronto; o objeto é novo.
- **Risco:** pode ser difícil encontrar repositórios brasileiros com volume de issues
  suficiente. *Mitigação:* ampliar para governos de outros países lusófonos ou para
  sistemas de dados abertos em geral.

### 🥈 Opção B — Incerteza temporal como métrica de qualidade de dados contábeis públicos

**Pergunta:** *Como medir e publicar "incerteza temporal" como métrica de qualidade de
dados em registros contábeis e orçamentários públicos?*

- **Método:** engenharia empírica — experimento controlado com instrumentação de
  *timestamps* (event / ingestion / processing time), medição de drift e de seus efeitos na
  ordenação causal de registros.
- **Dados:** registros de execução orçamentária, empenhos, pagamentos, publicações de
  diários oficiais.
- **Contribuição:** transformar incerteza temporal de problema operacional em **métrica
  publicável de qualidade de dado** — com definição, forma de cálculo e limiares.
- **Por que funciona:** **o professor formulou essa pergunta literalmente**, no Slide 35 da
  Aula 3, como ponto para pesquisa: *"Como medir e publicar 'incerteza temporal' como
  métrica de qualidade de dados?"*. Responder uma pergunta aberta que o próprio professor
  propôs é o caminho mais curto para o interesse dele.
- **Risco:** exige instrumentação e um conjunto de dados real. Mais trabalho de
  infraestrutura que a Opção A.

### 🥉 Opção C — Governança de IA sobre dados financeiros públicos: o caso `br-financial-ai`

**Pergunta:** *Como garantir auditabilidade e rastreabilidade de evidência em sistemas de
IA que operam sobre dados contábeis públicos?*

- **Método:** **estudo de caso industrial** (um dos quatro métodos que o professor ensina
  na Aula 1) sobre o próprio repositório dele, combinado com a aplicação do catálogo de
  antipadrões à sua camada de acesso a dados.
- **Contribuição:** o repositório já implementa uma fronteira rígida entre cálculo
  determinístico e interpretação por LLM, com validação de identidade de evidência e
  *gates* de alucinação. Isso é um **arcabouço de governança pronto para ser formalizado**
  — e você pode medir onde ele falha sob escala.
- **Por que funciona:** você contribui para o software do professor **e** produz pesquisa
  sobre ele. O alinhamento é total.
- **Risco:** estudar o repositório do próprio professor exige pedir licença explícita.
  A boa notícia é que ele indicou o repositório a você — o convite provavelmente já está
  feito.

---

## 4. Recomendação

**Combine A e C.** A Opção A dá o método e a contribuição generalizável; a Opção C dá o
objeto rico, o acesso privilegiado e o vínculo direto com o trabalho do professor:

> **Título de trabalho:** *Antipadrões de acesso a dados e auditabilidade em sistemas de
> dados financeiros públicos: um estudo de mineração de repositórios com estudo de caso.*

Estrutura do artigo de 6–8 páginas:

1. **Introdução (Hook + Gap)** — sistemas de transparência pública tratam dados que
   precisam ser auditáveis; o catálogo de antipadrões de acesso a dados foi construído
   sobre NoSQL comercial e nunca foi examinado sob a ótica da auditabilidade.
2. **Trabalhos relacionados** — Shao et al. (2020), Muse et al. (2024), Kleppmann (2017),
   e literatura de governança de dados públicos.
3. **Método** — MSR (funil replicado do artigo) + estudo de caso em `br-financial-ai`.
4. **Resultados** — taxonomia adaptada ao domínio público + achados do estudo de caso
   (ex.: ausência de paginação, ingestão sequencial, camada vetorial provisionada e ociosa
   — todos já evidenciados).
5. **Ameaças à validade** — a estrutura da Aula 1, Slide 34.
6. **Conclusão e trabalho futuro** — caminho para a dissertação.

**Por que isso impressiona o orientador:** você não chega com "quero estudar dados". Você
chega com um método que ele ensinou, aplicado a um objeto que ele construiu, produzindo uma
contribuição que responde a uma pergunta que ele formulou. E os dois primeiros PRs
(correção da documentação de avaliação e CI) já terão mostrado que você lê os artefatos com
atenção.

---

## 5. Como as aulas se conectam ao seu tema

Não deixe as conexões implícitas — nomeie-as em sala:

| Conteúdo da aula | Conexão com governança/transparência/contabilidade |
| --- | --- |
| **Aula 1 — pilares de Kleppmann** | Confiabilidade, escalabilidade e manutenibilidade são, em dados públicos, requisitos de **prestação de contas**, não de performance |
| **Aula 1 — persistência poliglota** | Portais de transparência combinam relacional, documentos e busca; cada escolha carrega custo oculto de manutenção |
| **Aula 1 — MSR** | É o método do seu artigo e o método da sua proposta |
| **Aula 1 — estudo de caso industrial** | É o método da Opção C, aplicado ao repositório do professor |
| **Aula 1 — threats to validity** | Em dados públicos, validade externa vira **representatividade**: o recorte exclui entes pequenos? |
| **Aula 3 — LWW e perda silenciosa** | Em registro contábil, "maior timestamp vence" pode **apagar um lançamento** sem gerar exceção — é perda de evidência fiscal |
| **Aula 3 — event/ingestion/processing time** | Um mesmo empenho tem três marcas temporais distintas; confundir as três inviabiliza auditoria |
| **Aula 3 — watermarks** | Em janelas de agregação orçamentária, evento "do futuro" por clock adiantado empurra lançamento legítimo para atrasado |
| **Aula 3 — pergunta aberta sobre métrica de incerteza temporal** | É literalmente a Opção B |

---

## 6. Perguntas para levar ao professor

Faça poucas e boas. Estas quatro sinalizam direção:

1. "Entre **antipadrões de acesso a dados em sistemas de transparência** e **incerteza
   temporal como métrica de qualidade**, qual tem mais aderência à linha de pesquisa que o
   senhor coordena?"
2. "Posso usar o `br-financial-ai` como estudo de caso? Vi que ele tem uma fronteira
   determinístico/IA bem definida e um harness de avaliação com *gates* de alucinação —
   acho que rende um estudo de caso sobre auditabilidade."
3. "O artigo de 60% pode ser a base do meu projeto de dissertação, ou o senhor prefere que
   eu trate como um exercício separado?"
4. "Há restrição de rate limit na CVM/B3 que eu deva considerar ao escalar a coleta?"

A pergunta 2 é a mais importante: ela mostra que você **leu o código dele**, não só o
README — e o repositório foi ele quem indicou.

---

## 7. Resumo em uma frase

> Você tem um método de pesquisa (MSR, ensinado em aula), um objeto empírico (dados
> financeiros públicos brasileiros, no repositório do professor) e um interesse declarado
> (governança, transparência, contabilidade) — e eles apontam para o mesmo lugar. O
> trabalho é transformar "antipadrão de desempenho" em "antipadrão de auditabilidade".
