---
title: Máquina Estatística — Relatório
disciplina: Probabilidade e Estatística I
professor: Fidelis Zanetti de Castro
semestre: 2026/2
---

# Máquina Estatística: probabilidade, apostas e pensamento crítico

<div style="text-align:center;">Kaiva Silverio Gums (20241BSI0130) · Matheus Morôni Arçari Barcellos (20212BSI0154)</div>

<div style="text-align:center; font-size:0.9em;">Instituto Federal do Espírito Santo — Campus Serra · Bacharelado em Sistemas de Informação<br>Probabilidade e Estatística I — Trabalho I — 2026/2 · Prof. Fidelis Zanetti de Castro</div>

---

## 1 Contexto e objetivos

As apostas de quota fixa on-line, entre elas as máquinas de rolos digitais popularizadas como "jogo do tigrinho", tornaram-se no Brasil um tema simultaneamente econômico, sanitário e jurídico. A Lei 14.790/2023 integrou essa modalidade ao marco regulatório [6]; em 25 de setembro de 2026, a Medida Provisória 1.394/2026 proibiu sua exploração, oferta, intermediação e publicidade, preservadas as demais modalidades lotéricas autorizadas em lei [7, 8]. A União ajuizou ação contra 17 plataformas, com pedido de reparação por danos morais coletivos e cobrança de despesas do SUS [9]. A medida foi imediatamente contestada no Supremo Tribunal Federal por associações do setor [10, 18], e a Advocacia-Geral da União pediu sua manutenção [19]. Até 2 de novembro de 2026, não se registrava decisão cautelar: o relator, ministro Luiz Fux, convocou audiência pública para 3 de novembro no âmbito da ADI 8.027, ajuizada pela Associação Nacional de Jogos e Loterias [20, 21]. A MP seguia em tramitação no Congresso, sujeita ao prazo constitucional de vigência de 60 dias, prorrogável por igual período (CF, art. 62, § 3º). Esse quadro é, portanto, provisório; distinguimos ao longo do texto norma publicada, alegação de parte e decisão judicial.

O trabalho responde à pergunta: *como ganhos ocasionais podem coexistir com uma perda esperada para o jogador, e o que essa diferença nos ajuda a compreender sobre as apostas na sociedade?* Para isso, implementamos em Python uma máquina didática de regras públicas, calculamos sua distribuição de resultados e executamos cinco experimentos de simulação. A simulação demonstra propriedades de um **modelo**; ela não mede prevalência de transtornos nem o impacto nacional das apostas, que exigem as fontes documentais discutidas na Seção 4.

## 2 Modelo e conceitos

### 2.1 Sorteio, janela e independência

Cada rolo possui a sequência circular $\mathcal{R} = (A, B, C, D, E)$, nas posições 0 a 4. Em cada rolo sorteia-se uma parada $K$ uniforme em $\{0,1,2,3,4\}$; a coluna exibe $\mathcal{R}_K$ no topo, $\mathcal{R}_{(K+1) \bmod 5}$ no centro e $\mathcal{R}_{(K+2) \bmod 5}$ na base. Apenas a linha central é avaliada, e só paga quando seus três símbolos são iguais. A aposta é de 1 crédito fictício.

**Por que cada símbolo é equiprovável no centro.** A aplicação $K \mapsto (K+1) \bmod 5$ é uma bijeção do conjunto $\{0,\dots,4\}$ nele mesmo — uma rotação do ciclo —; como cada posição do rolo contém um símbolo distinto, cada símbolo corresponde a exatamente um valor de $K$. Logo, $\Pr(\text{centro} = s) = \Pr(K = k_s) = 1/5$ para todo símbolo $s$.

**Por que podemos multiplicar entre rolos, mas não dentro de uma coluna.** As três paradas $K_1, K_2, K_3$ são sorteadas por chamadas distintas do gerador, sem que uma dependa da outra; as células centrais, funções de paradas independentes, são independentes entre si. Já as três células de uma mesma coluna são funções do *mesmo* $K$: conhecido o centro, o topo e a base ficam determinados. Por exemplo, $\Pr(\text{topo}=A,\ \text{centro}=B) = 1/5$, enquanto o produto das marginais seria $1/25$ — a fatoração falha.

### 2.2 Espaço amostral, variável aleatória e distribuição

O espaço amostral relevante é o das triplas centrais, com $5^3 = 125$ resultados equiprováveis, cada um com probabilidade $(1/5)^3 = 1/125$. As cinco triplas premiadas (A–A–A, …, E–E–E) são eventos disjuntos; o evento "sem prêmio" reúne as outras 120 triplas.

Distinguimos duas variáveis aleatórias, ambas funções do mesmo resultado $\omega$: o **prêmio bruto** $P = g(\omega)$, dado pela tabela de pagamentos, e o **lucro líquido** $X = P - 1$. A distinção é estrutural no código: o sorteio produz $\omega$ (as três paradas), e a tabela é a função $g$ aplicada a ele — o que permite, no Experimento 5, trocar $g$ mantendo $\omega$ fixo.

**Tabela 1.** Distribuição do prêmio e do lucro no modelo-base.

| Linha central | $P$ | $X$ | Probabilidade |
|---|---:|---:|---:|
| A–A–A | 5 | 4 | 1/125 |
| B–B–B | 10 | 9 | 1/125 |
| C–C–C | 15 | 14 | 1/125 |
| D–D–D | 25 | 24 | 1/125 |
| E–E–E | 50 | 49 | 1/125 |
| Qualquer outra tripla | 0 | −1 | 120/125 |

### 2.3 Esperança, RTP e dispersão

A chance de prêmio é $5/125 = 4\%$. A esperança pondera cada valor pela probabilidade — uma média ponderada sobre a partição do espaço amostral, com a mesma estrutura da probabilidade total:

$$\mathbb{E}[P] = \frac{5+10+15+25+50}{125} = 0{,}84, \qquad \mathbb{E}[X] = \mathbb{E}[P] - 1 = -0{,}16.$$

A segunda igualdade usa a linearidade da esperança. O **RTP** (retorno ao jogador) é $\mathbb{E}[P]/\text{aposta} = 84\%$, e a vantagem esperada do operador é $16\%$ do volume apostado [15]. As duas grandezas medem coisas diferentes: a chance de prêmio (4%) responde "com que frequência algo é pago"; o RTP (84%) responde "quanto, em média, retorna de cada crédito apostado". Um RTP de 84% não é 84% de chance de ganhar, nem promessa de devolução de 84% do depósito em uma sessão [17]: é uma média sobre todo o volume apostado, inclusive créditos reapostados.

Para a dispersão, $\mathbb{E}[P^2] = (25+100+225+625+2500)/125 = 27{,}8$, de modo que

$$\operatorname{Var}(X) = \operatorname{Var}(P) = 27{,}8 - 0{,}84^2 = 27{,}0944, \qquad \sigma_X \approx 5{,}205 \text{ créditos.}$$

O desvio-padrão é cerca de 33 vezes maior, em módulo, que a esperança: em poucas rodadas, o resultado individual é dominado pela variabilidade, não pela média. Esse contraste é o núcleo matemático da resposta à pergunta do trabalho. Para $n$ rodadas fixas, a soma dos lucros tem esperança $-0{,}16\,n$ e desvio-padrão $5{,}205\sqrt{n}$; a média, portanto, tem erro-padrão $5{,}205/\sqrt{n}$.

### 2.4 Implementação

O simulador foi escrito em Python, com núcleo (`modelo.py`, `experimentos.py`) separado da exportação e da interface textual (`ui.py`, com a biblioteca Rich). Usamos `random.Random` (Mersenne Twister) da biblioteca padrão [16], com a semente fixada uma única vez por execução. Cada rodada consome três chamadas a `randrange(5)`, na ordem rolo 1, 2, 3. As probabilidades e esperanças teóricas são calculadas em frações exatas (`fractions.Fraction`). O ambiente está registrado em `resultados/ambiente.txt`; as instruções, no README.

## 3 Cinco experimentos

**Condições comuns.** Aposta de 1 crédito; tabela-base, salvo no E5. A sequência de 10.000 rodadas da semente 2026 foi gerada uma única vez e reutilizada nos Experimentos 1, 2, 4 e 5. Nenhum resultado foi descartado ou selecionado.

### 3.1 Experimento 1 — As frequências acompanham as probabilidades?

**Procedimento.** 10.000 rodadas, semente 2026, sem saldo ou regra de parada. Contagem dos seis resultados da Tabela 1 e cálculo do lucro médio, do RTP observado, da proporção de rodadas premiadas e do desvio-padrão amostral do lucro (divisor $N-1$).

**Tabela 2.** Frequências observadas no E1 ($N = 10.000$; as contagens somam 10.000).

| Resultado | Lucro $X$ | Prob. teórica | Contagem | Freq. relativa |
|---|---:|---:|---:|---:|
| A–A–A | 4 | 0,0080 | 77 | 0,0077 |
| B–B–B | 9 | 0,0080 | 88 | 0,0088 |
| C–C–C | 14 | 0,0080 | 78 | 0,0078 |
| D–D–D | 24 | 0,0080 | 88 | 0,0088 |
| E–E–E | 49 | 0,0080 | 81 | 0,0081 |
| Outra | −1 | 0,9600 | 9.588 | 0,9588 |

**Tabela 3.** Medidas-resumo do E1.

| Medida | Observado | Referência teórica |
|---|---:|---:|
| Lucro médio $\bar X$ (créditos) | −0,1315 | −0,16 |
| RTP observado | 86,85% | 84% |
| Proporção de rodadas premiadas | 4,12% | 4% |
| Desvio-padrão amostral $s$ (créditos) | 5,275 | 5,205 |

![[e1_teoria_vs_observacao.svg]]

*Figura 1. Probabilidade teórica e frequência relativa observada de cada valor do lucro (escala logarítmica no eixo vertical, para tornar visíveis as probabilidades de 0,8% ao lado de 96%). Fonte: elaboração própria, semente 2026.*

**Interpretação.** Cada frequência relativa oscila em torno de sua probabilidade: as contagens das triplas premiadas variam de 77 a 88, em torno do valor esperado de 80, e a categoria "outra" fica em 95,88% contra 96%. Não há razão para coincidência exata, porque a frequência é ela mesma uma variável aleatória. O lucro médio (−0,1315) difere da esperança (−0,16) em 0,0285 crédito; com erro-padrão $5{,}205/\sqrt{10.000} \approx 0{,}052$, a diferença equivale a cerca de 0,55 erro-padrão — variação amostral comum, que não autoriza alterar dados nem regras. A proporção de rodadas premiadas (4,12%) e o RTP observado (86,85%) são números distintos: o primeiro conta *quantas vezes* houve pagamento; o segundo soma *quanto* foi pago. A média descreve o centro (perde-se, em média, cerca de 0,13 crédito por rodada nesta amostra); o desvio-padrão de 5,3 créditos descreve uma dispersão muito superior à aposta, produzida por poucos prêmios grandes em meio a perdas unitárias.

### 3.2 Experimento 2 — O que muda quando aumentamos a amostra?

**Procedimento.** Três sequências de 10.000 rodadas, com sementes 10, 2026 e 123456; registro da média acumulada do lucro após 100, 1.000 e 10.000 rodadas. Conferência da reprodução: a semente 2026 foi reexecutada no mesmo ambiente, e as dez primeiras rodadas (paradas $K_1, K_2, K_3$) coincidiram integralmente com a sequência original (`e2_conferencia_reproducao.csv`). Em outra máquina (Windows, Python 3.12), a execução reproduziu os mesmos números; numa terceira conferência, em Linux com Python 3.13, os nove arquivos CSV resultaram idênticos, byte a byte, aos entregues.

**Tabela 4.** Média acumulada do lucro (créditos). Esperança: −0,16.

| Semente | após 100 | após 1.000 | após 10.000 |
|---|---:|---:|---:|
| 10 | −0,700 | −0,055 | −0,096 |
| 2026 | +0,200 | −0,220 | −0,1315 |
| 123456 | +0,200 | −0,070 | −0,2215 |
| *Erro-padrão teórico* | *0,52* | *0,165* | *0,052* |

![[e2_medias_acumuladas.svg]]

*Figura 2. Trajetórias da média acumulada do lucro nas três sementes, com a referência $\mathbb{E}[X] = -0{,}16$ (tracejado). Eixo horizontal em escala logarítmica; o eixo vertical foi limitado a 2,0 crédito, o que corta os valores iniciais da semente 123456. Fonte: elaboração própria.*

**Interpretação.** Após 100 rodadas, duas das três sequências apresentavam média *positiva* (+0,20): um jogador que parasse ali teria lucro. Com 10.000 rodadas, as três médias se aproximam de −0,16, e a distância entre elas diminui de 0,90 para 0,13 crédito — compatível com o erro-padrão, que decresce na proporção $1/\sqrt{n}$. Esse é o conteúdo da Lei dos Grandes Números sob as hipóteses do modelo (rodadas independentes e identicamente distribuídas, com esperança finita): a média tende à esperança. A lei não exige aproximação monotônica — a semente 10, por exemplo, passa de −0,055 (1.000 rodadas) para −0,096 (10.000) — nem promete erro máximo em um número fixo de rodadas; a semente 123456 termina mais distante de −0,16 que as outras.

Uma sequência inicial favorável não altera as rodadas seguintes: a média se aproxima da esperança não porque perdas futuras "compensem" ganhos passados, mas porque o peso relativo das primeiras rodadas se dilui à medida que $n$ cresce. Aumentar a amostra melhora o conhecimento sobre a média; não transforma uma aposta de esperança negativa em fonte de renda.

### 3.3 Experimento 3 — O que acontece com um saldo limitado?

**Procedimento.** 100 participantes virtuais, cada um com saldo inicial de 100 créditos e aposta de 1. A sessão termina ao completar 500 rodadas ou quando o saldo fica abaixo de 1 (esgotamento). O saldo evolui por $B_{t+1} = B_t + X_{t+1}$, sem reposição. O gerador foi iniciado com semente 42 uma única vez, e a sequência continuou entre participantes.

**Tabela 5.** Resultados finais dos 100 participantes.

| Medida | Valor |
|---|---:|
| Ganho ($B_f > 100$) | 23% |
| Empate ($B_f = 100$) | 2% |
| Perda ($B_f < 100$) | 75% |
| — dos quais com esgotamento ($B_f < 1$) | 67% do total |
| Média do saldo final | 52,1 créditos |
| Mediana do saldo final | 0 crédito |
| Média de rodadas jogadas | 339,9 |

![[e3_trajetorias_cinco_primeiros.svg]]

*Figura 3. Trajetórias de saldo dos cinco primeiros participantes, na ordem da simulação (sem seleção por resultado). Após o esgotamento, o saldo é mantido constante; a linha pontilhada marca o saldo inicial. Fonte: elaboração própria, semente 42.*

![[e3_distribuicao_saldos_finais.svg]]

*Figura 4. Distribuição dos saldos finais dos 100 participantes, com média e mediana. Fonte: elaboração própria, semente 42.*

**Interpretação.** Em um jogo desfavorável, 23 dos 100 participantes terminaram com ganho — alguns com mais do que o triplo do saldo inicial. Isso é possível porque a dispersão por rodada (5,2 créditos) é grande frente à perda esperada (0,16): em 500 rodadas, a perda esperada acumulada (80 créditos) é da mesma ordem que o desvio-padrão da soma ($5{,}205\sqrt{500} \approx 116$). Ao mesmo tempo, 67 participantes esgotaram o saldo, e outros 8 terminaram com perda sem esgotá-lo.

A comparação entre média (52,1) e mediana (0) é o achado central: a mediana mostra que o participante "típico" perdeu tudo, enquanto a média é sustentada pelos poucos vencedores com saldos altos. Um relato isolado de sucesso descreve a cauda direita dessa distribuição e omite a massa de casos à esquerda — exatamente os que não costumam ser divulgados.

A referência $100 - 500 \times 0{,}16 = 20$ não se aplica, porque a duração da sessão varia: quem esgota o saldo para antes de 500 rodadas, e sua perda fica limitada a 100. A referência adequada usa o número esperado de rodadas efetivamente jogadas. Como a regra de parada depende apenas de resultados já observados e a sessão tem no máximo 500 rodadas, a identidade de Wald fornece $\mathbb{E}[B_f] = 100 - 0{,}16\,\mathbb{E}[T]$, em que $T$ é o número de rodadas jogadas. Com a estimativa $\bar T = 339{,}9$, obtém-se cerca de 45,6 créditos, próximo da média observada de 52,1 (com apenas 100 participantes e alta dispersão, a diferença é esperável). A taxa de esgotamento descreve **este modelo, este saldo e este horizonte**; não é estimativa da situação de famílias brasileiras.

### 3.4 Experimento 4 — Depois de perder, aumenta a chance de ganhar?

**Procedimento.** Reutilização das 10.000 rodadas do E1. Os 9.999 pares consecutivos foram separados conforme a primeira rodada do par tenha ou não sido premiada; em cada grupo, contou-se quantas vezes a rodada seguinte foi premiada. Definindo $G_i = \{P_i > 0\}$, a referência do modelo é

$$\Pr(G_{i+1} \mid G_i) = \Pr(G_{i+1} \mid G_i^c) = \Pr(G_{i+1}) = 4\%.$$

**Tabela 6.** Proporção de prêmios na rodada seguinte, por resultado anterior (412 + 9.587 = 9.999 pares).

| Resultado anterior | Total de pares | Prêmios na seguinte | Proporção | Erro-padrão aprox. |
|---|---:|---:|---:|---:|
| Após prêmio | 412 | 17 | 4,13% | 0,97 p.p. |
| Após perda | 9.587 | 395 | 4,12% | 0,20 p.p. |

**Interpretação.** As duas proporções são praticamente iguais, e ambas próximas de 4%. A máquina não passa a "dever" um prêmio após perdas: as paradas de cada rodada são sorteadas de novo, sem memória do resultado anterior, de modo que a probabilidade condicional coincide com a incondicional — é o que significa independência. A falácia do jogador consiste em esperar compensação imediata entre resultados independentes.

A coincidência quase exata nesta amostra é, em parte, acaso: o grupo "após prêmio" tem apenas 412 pares, e seu erro-padrão aproximado, $\sqrt{0{,}04 \times 0{,}96/412} \approx 0{,}97$ ponto percentual, é cerca de cinco vezes o do outro grupo. Com outra semente, uma diferença de um ou dois pontos percentuais entre os grupos seria compatível com o modelo e, sozinha, não indicaria mudança das regras. O cálculo de Bayes, quando as probabilidades são conhecidas, dá a resposta exata; a frequência condicional a estima, com incerteza que depende do denominador.

### 3.5 Experimento 5 — Prêmios maiores tornam o jogo favorável?

**Procedimento.** Duas tabelas de pagamento — a base e a de prêmios 10% maiores (5,5; 11; 16,5; 27,5; 55) — aplicadas aos *mesmos* 10.000 resultados do E1, sem novo sorteio. Mantidos os símbolos, suas probabilidades e a aposta de 1 crédito.

**Tabela 7.** Comparação das tabelas de pagamento sobre a mesma sequência.

| Medida | Base | Prêmios +10% |
|---|---:|---:|
| Probabilidade de prêmio | 4% | 4% |
| Frequência de prêmio observada | 4,12% | 4,12% |
| Prêmio médio por rodada (créditos) | 0,8685 | 0,9554 |
| Prêmio médio por rodada premiada (créditos) | 21,08 | 23,19 |
| Lucro médio observado (créditos) | −0,1315 | −0,0447 |
| Lucro esperado (créditos) | −0,160 | −0,076 |
| RTP teórico | 84,0% | 92,4% |
| RTP observado | 86,85% | 95,54% |

**Interpretação.** A frequência de prêmio é idêntica nas duas configurações, porque o sorteio é o mesmo: mudou a função $g$, não o resultado $\omega$. Pela linearidade da esperança, multiplicar todos os prêmios por 1,10 multiplica $\mathbb{E}[P]$ por 1,10: $\text{RTP}_{+10\%} = 1{,}10 \times 0{,}84 = 92{,}4\%$ e $\mathbb{E}[X_{+10\%}] = 0{,}924 - 1 = -0{,}076$. O mesmo fator aparece nos dados observados ($1{,}10 \times 86{,}85\% = 95{,}54\%$), já que cada prêmio da amostra foi multiplicado por 1,10. O jogo melhora para o jogador, mas continua desfavorável: só seria neutro com prêmios multiplicados por $1/0{,}84 \approx 1{,}19$, isto é, cerca de 19% maiores.

Três afirmações devem ser separadas: **pagar mais** (aumentar os valores da tabela, que eleva o RTP sem alterar a chance de prêmio); **pagar com maior frequência** (alterar as probabilidades, o que muda a chance de prêmio e pode ou não alterar o RTP); e **produzir lucro esperado positivo** (RTP acima de 100%). Prêmios maiores, sozinhos, não implicam a terceira.

## 4 Discussão crítica

### 4.1 Mecanismo e percepção

A pergunta do trabalho tem uma resposta matemática precisa no modelo: ganhos ocasionais e perda esperada coexistem porque a esperança (−0,16 por rodada) é pequena diante do desvio-padrão (5,2 por rodada). A perda é uma propriedade da *distribuição*; o ganho é um *acontecimento*, visível e memorável. O E2 mostra que, em 100 rodadas, duas de três sequências exibiam lucro; o E3 mostra que 23% dos participantes terminaram ganhando, enquanto a mediana do saldo final foi zero. Quem observa apenas os vencedores — por relato pessoal, publicidade ou redes sociais — vê a cauda direita da distribuição e nada vê da massa de esgotados. A animação dos rolos agrava esse descompasso: ela mostra a rodada, não a distribuição.

### 4.2 Renda e saúde

A simulação fornece o mecanismo; os efeitos sobre pessoas reais vêm de estudos com pessoas reais, e mantemos as duas coisas separadas. A Organização Mundial da Saúde associa os danos das apostas a sofrimento financeiro, comprometimento de despesas essenciais, problemas de saúde mental e conflitos familiares, inclusive para quem não aposta e sem diagnóstico de transtorno; máquinas eletrônicas e jogos de cassino estão entre os produtos de maior risco [1]. A Comissão da *The Lancet Public Health* estimou em 15,8% (IC 10,7%–21,6%) a proporção de jogo problemático ou transtorno do jogo **entre adultos que usaram cassino ou rolos on-line** [2] — o denominador é essa subpopulação, não a população adulta, e a estimativa reúne estudos de vários países. No Brasil, o LENAD III aplicou a escala PGSI a uma subamostra de 4.914 participantes de um levantamento com amostragem probabilística [3]; trata-se de rastreamento populacional, não de diagnóstico individual.

Quanto à renda, Baker e colaboradores encontraram, em famílias dos Estados Unidos, redução de poupança e maior pressão sobre o crédito após a expansão das apostas esportivas legais, sobretudo entre famílias com restrições financeiras [4]. O mecanismo do E3 ajuda a entender por que isso importa: com orçamento limitado e apostas repetidas, o esgotamento torna-se o resultado típico, e o recurso perdido pode ser o destinado a despesas essenciais. Mas a transferência é limitada: o estudo trata de apostas esportivas, em outro país, e nossa simulação trata de um modelo com 100 participantes virtuais. Uma rodada perdida não é um diagnóstico, e a taxa de esgotamento do E3 não estima nada sobre famílias brasileiras.

Os números agregados brasileiros também medem coisas diferentes e não podem ser somados. A estimativa preliminar do Banco Central de R\$ 18–21 bilhões mensais em 2024 refere-se a transferências brutas via Pix às empresas identificadas, não à perda líquida dos apostadores [11]. Os R\$ 17,4 bilhões do primeiro semestre de 2025, citados pelo TCU, são a receita bruta de jogos do mercado autorizado — valores apostados menos prêmios pagos [12]. Os R\$ 38,8 bilhões anuais do IEPS são uma estimativa de custos sociais que inclui valoração de perdas de saúde, construída com parâmetros de uma revisão britânica e conversão por paridade de poder de compra; não é despesa efetivamente paga pelo SUS, e o próprio dossiê aponta componentes estimados, lacunas de mensuração e associações que não estabelecem causalidade [13, 14]. Em termos do nosso modelo: a receita bruta corresponde à vantagem do operador acumulada sobre o volume apostado, enquanto as transferências via Pix se aproximam de depósitos, que incluem créditos depois reapostados ou sacados.

### 4.3 Políticas e interesses

**Um argumento favorável à restrição.** A defesa da MP 1.394/2026 enfatiza proteção da saúde, da renda familiar e de pessoas vulneráveis [8]. Em manifestação ao STF, a AGU sustentou que a União pode reavaliar uma política pública quando a prática revela riscos, citou o uso de plataformas por organizações criminosas para lavagem de dinheiro e mencionou estimativas de impacto sobre o consumo e a inadimplência das famílias [19]. A parte sanitária do argumento tem apoio em evidência de pesquisa ([1], [2], [3]), embora não haja, nas fontes consultadas, estimativa causal específica para os rolos digitais no Brasil.

**Um argumento crítico à proibição.** As associações do setor (ANJL, IBJR, Anseja) alegam insegurança jurídica, prejuízo a investimentos feitos sob o marco de 2023 e falta de urgência para a medida provisória; pedem a suspensão da MP ou, subsidiariamente, um prazo de transição [10, 18]. Há também um argumento mais forte, independente dos interesses comerciais: a capacidade do Estado de impedir a oferta clandestina. O TCU já havia identificado, em maio de 2026, falhas de coordenação e limitações no monitoramento de operadores ilegais [12]. Se a proibição desloca apostadores para plataformas sem controle algum, parte da proteção pretendida pode se perder.

**Avaliação.** Os argumentos não têm o mesmo peso de evidência. Os danos à saúde e à renda são documentados por pesquisa revisada e por levantamento populacional, com as ressalvas de denominador e de contexto acima. As alegações de insegurança jurídica e de prejuízo econômico são pedidos de partes interessadas — legítimos, mas ainda não julgados. A objeção da fiscalização é a mais consistente do lado crítico, porque se apoia em constatação de órgão de controle; ela não apaga os danos, mas indica que o efeito real da proibição depende de implementação. A autonomia individual também merece consideração: o E3 mostra, porém, que a decisão de apostar é tomada diante de uma distribuição que o jogador não vê, o que torna a informação sobre o produto parte da própria condição de autonomia.

### 4.4 Responsabilidade profissional

Como futuros profissionais de Sistemas de Informação, notamos que muitas decisões que afetam a compreensão do usuário são de projeto de software. A animação, os sons e a ênfase visual nas vitórias tornam o acontecimento saliente e a distribuição invisível. A forma de comunicar o risco também importa: Newall e colaboradores observaram que a mesma informação, apresentada como retorno ao jogador ou como vantagem da casa, é percebida de modo diferente [5] — "84% de retorno" soa favorável; "a casa retém 16% de tudo o que é apostado" descreve o mesmo número sob outra luz. Isso não demonstra que um aviso isolado elimine danos, mas mostra que escolhas de interface não são neutras.

No nosso simulador, procuramos aplicar o princípio inverso: o aviso de créditos fictícios aparece na abertura; a tela das regras exibe a distribuição, a chance de prêmio, a esperança e o RTP lado a lado; as rodadas mostram as paradas sorteadas e o lucro, não apenas o prêmio; e a informação não depende de cor (marcadores textuais como "[ PRÊMIO ]" e ">>" indicam o resultado e a linha avaliada). A conclusão educativa que propomos é esta: ganhar algumas vezes não contradiz perder em expectativa, e um relato de vitória não é evidência sobre a distribuição. Ela não promete ganho a ninguém nem culpa as pessoas afetadas, que tomam decisões diante de produtos desenhados para tornar a perda pouco visível.

### 4.5 Limites da análise

Os resultados descrevem um modelo didático com RTP de 84%, sem pretensão de representar produto comercial; não fizemos engenharia reversa de nenhum jogo. As simulações dependem do gerador pseudoaleatório e de sementes fixas, e outras sementes produziriam números diferentes, compatíveis com as mesmas conclusões. O E3 usa apenas 100 participantes. Os dados sobre saúde e renda vêm de estudos com populações, períodos e modalidades distintos dos rolos digitais no Brasil de 2026. O quadro jurídico é provisório na data deste relatório.

## 5 Conclusão

No modelo estudado, a chance de prêmio é 4%, o RTP é 84% e o lucro esperado é −0,16 crédito por rodada, com desvio-padrão de 5,2. Os experimentos confirmaram essas propriedades: as frequências acompanham as probabilidades (E1), as médias convergem para a esperança sem obrigação de compensar perdas (E2), perder não aumenta a chance de ganhar (E4), e prêmios 10% maiores elevam o RTP para 92,4% sem tornar o jogo favorável (E5). O E3 sintetiza a resposta à pergunta do trabalho: 23% dos participantes ganharam, mas a mediana do saldo final foi zero. Ganhos ocasionais são reais, frequentes o bastante para gerar relatos de sucesso, e raros o bastante para que a perda seja o resultado típico. Essa distância entre o acontecimento visível e a propriedade da distribuição ajuda a entender por que as apostas são tema de saúde pública e de política, e por que comunicar sua matemática é também uma responsabilidade de quem projeta sistemas.

<div style="page-break-after: always;"></div>

## Referências

[1] WORLD HEALTH ORGANIZATION. *Gambling*. 2 dez. 2024.

[2] WARDLE, H. et al. The Lancet Public Health Commission on gambling. *The Lancet Public Health*, v. 9, p. e950–e994, 2024. DOI: 10.1016/S2468-2667(24)00167-1.

[3] UNIVERSIDADE FEDERAL DE SÃO PAULO; UNIAD. *Caderno Temático LENAD III: jogos de aposta na população brasileira*. Resultados 2023. 2025.

[4] BAKER, S. R.; BALTHROP, J.; JOHNSON, M. J.; KOTTER, J. D.; PISCIOTTA, K. *Gambling Away Stability: Sports Betting's Impact on Vulnerable Households*. NBER Working Paper 33108, nov. 2024. DOI: 10.3386/w33108.

[5] NEWALL, P. W. S.; WALASEK, L.; LUDVIG, E. A. Equivalent gambling warning labels are perceived differently. *Addiction*, v. 115, n. 9, p. 1762–1767, 2020. DOI: 10.1111/add.14954.

[6] BRASIL. Lei 14.790, de 29 de dezembro de 2023.

[7] BRASIL. Congresso Nacional. Medida Provisória 1.394/2026. Publicada em 25 set. 2026.

[8] BRASIL. Ministério da Saúde. Presidente Lula assina Medida Provisória que proíbe as bets no Brasil. 25 set. 2026.

[9] RICHTER, A. Governo cobra na Justiça gastos do SUS com tratamento de apostadores. *Agência Brasil*, 28 set. 2026.

[10] PONTES, F. Associações de jogos acionam STF contra MP que proibiu apostas online. *Agência Brasil*, 28 set. 2026.

[11] BANCO CENTRAL DO BRASIL. *Análise técnica sobre o mercado de apostas online no Brasil e o perfil dos apostadores*. Estudo Especial 119/2024; Nota Técnica 513/2024, set. 2024.

[12] TRIBUNAL DE CONTAS DA UNIÃO. Tribunal analisa enfrentamento a casas de apostas ilegais. 19 maio 2026. Acórdão 1296/2026 — Plenário.

[13] ROSA, D. et al. *A saúde dos brasileiros em jogo: análise político-econômica da regulamentação de apostas online e seus impactos para a saúde da população brasileira*. IEPS; FPSM; Umane, dez. 2025.

[14] OFFICE FOR HEALTH IMPROVEMENT AND DISPARITIES; PUBLIC HEALTH ENGLAND. *Gambling-related harms: evidence review*. 2021; atualização de custos em 11 jan. 2023.

[15] ILLOWSKY, B.; DEAN, S. *Introductory Statistics 2e*. Houston: OpenStax, 2023.

[16] PYTHON SOFTWARE FOUNDATION. *random — Generate pseudo-random numbers*. Documentação do Python 3.

[17] GAMBLING COMMISSION. *Return to player: how much gaming machines payout*. 16 jun. 2021.

[18] SUPREMO TRIBUNAL FEDERAL. Associações questionam no STF medida provisória que proíbe bets. *Notícias STF*, 28 set. 2026. Disponível em: https://noticias.stf.jus.br/postsnoticias/associacoes-questionam-no-stf-medida-provisoria-que-proibe-bets/.

[19] CONGRESSO EM FOCO. AGU pede que STF mantenha proibição de bets determinada por Lula. 6 out. 2026. Disponível em: https://www.congressoemfoco.com.br/noticia/123027/agu-pede-que-stf-mantenha-proibicao-de-bets-determinada-por-lula.

[20] BNLDATA. MP das apostas pode caducar no Congresso ou ser suspensa por Fux no STF. 12 out. 2026. Disponível em: https://bnldata.com.br/mp-das-apostas-pode-caducar-no-congresso-ou-ser-suspensa-por-fux-no-stf/.

[21] MIGALHAS. Fux marca audiência das bets para dia 3; entidades pedem participação. 31 out. 2026. Disponível em: https://www.migalhas.com.br/quentes/467651/fux-marca-audiencia-das-bets-para-dia-3-entidades-pedem-participacao.

**Gênero das fontes.** Pesquisa e revisão: [2], [3], [4], [5], [13], [14]. Documentos institucionais e normativos: [1], [6], [7], [8], [11], [12], [17]. Notícias e registros de posições no debate: [9], [10], [18], [19], [20], [21]. As referências de 2024 e 2025 documentam seus respectivos períodos. Data de consulta das fontes on-line de 2026: 2 nov. 2026.

## Transparência e uso de IA

Utilizamos o Claude (Anthropic) como apoio na revisão e reescrita do código, na geração da interface textual, na conferência de atualizações do quadro jurídico e na formatação do relatório para exportação em PDF. As contas, os resultados e as afirmações do texto foram conferidos pelo grupo
