# E-mail para o orientador — rascunho

**Para:** Prof. Dr. Fábio Gomes Rocha
**Assunto:** Disciplina Engenharia de Software Experimental — proposta de estudo e possível vínculo com a dissertação

---

Prezado Prof. Fábio,

Escrevo para apresentar o que estou desenvolvendo na disciplina **PROCC0094 — Engenharia de Software Experimental** (Prof. Methanias Colaço Júnior) e ouvir sua avaliação sobre um possível vínculo com a dissertação.

**O tema.** Mineração de defeitos em relatórios XBRL: uma análise empírica de padrões de erro em diferentes jurisdições. O XBRL é o padrão global de relatório financeiro legível por máquina, usado por SEC (EUA), ESMA (UE) e Companies House (Reino Unido). Erros de validação são frequentes e afetam qualidade e comparabilidade do dado.

**O enquadramento.** Trato a instância XBRL como **artefato de software** e o defeito de validação como **defeito de software**. O objeto é o artefato; o foco é medir, classificar e comparar, não avaliar o mérito contábil.

**A meta experimental.** Caracterizar os defeitos de validação — classe e frequência — propondo uma taxonomia com confiabilidade medida e um pipeline reprodutível.

**A decisão técnica que destrava o estudo.** A medição não depende de os reguladores publicarem relatórios de validação. Uso o **Arelle**, processador XBRL de código aberto certificado pela XBRL International, que já distribui os conjuntos de regras das jurisdições (EFM/SEC, ESEF/UE, HMRC/Reino Unido). Assim eu baixo a instância pública, valido localmente e qualquer terceiro reproduz. Verifiquei os conjuntos de regras na versão 2.45.3 instalada.

**Como pretendo validar.** Quatro frentes, nesta ordem: determinismo do instrumento; concordância entre dois codificadores com κ de Cohen para a taxonomia; triangulação entre jurisdições com a mesma ferramenta; e reprodutibilidade aberta (scripts, versões e critérios publicados). O piloto tem fases com critério de decisão declarado **antes** de ver os dados.

**Duas delimitações que quero registrar desde já.** Primeiro, só observo instâncias **já aceitas** pelos reguladores — meço conformidade residual, não a qualidade dos relatórios. Segundo, **jurisdição não é qualidade**: cada regulador tem um conjunto de regras diferente, e comparar direto seria comparar os instrumentos. O estudo é observacional, não experimento controlado.

**Sobre a dissertação.** Vejo dois caminhos e gostaria da sua leitura:

1. **Como capítulo empírico.** O estudo se sustenta sozinho como capítulo de análise de defeitos em artefatos de dados regulados, com o pipeline reprodutível como contribuição prática.
2. **Como estudo piloto.** Se a taxonomia se mostrar confiável, ela vira instrumento para um estudo maior, com mais jurisdições e série histórica — o que daria corpo a uma dissertação.

**O que preciso decidir com você:** se o escopo deve permanecer em uma jurisdição (SEC, um trimestre) para caber no semestre, e se há interesse em estender depois para o eixo entre jurisdições.

Posso enviar a proposta completa e os slides da apresentação, se ajudar.

Agradeço a atenção e fico à disposição para conversarmos.

Cordialmente,
**Victor Cesar Santos de Melo**
Mestrado em Ciência da Computação — PROCC/UFS
