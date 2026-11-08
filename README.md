# Máquina Estatística — Trabalho I de Probabilidade e Estatística I

**Simulador acadêmico - somente créditos fictícios.**

IFES Campus Serra · Bacharelado em Sistemas de Informação · Prof. Fidelis Zanetti de Castro · 2026/2

## Integrantes

- Kaiva Silverio Gums (20241BSI0130)
- Matheus Morôni Arçari Barcellos (20212BSI0154)

O relatório está em `relatorio.pdf` (fonte editável: `relatorio.md`).

## Requisitos

- Python 3.10 ou superior
- Dependências: `pip install -r requirements.txt` (rich, matplotlib)

## Execução

```
python main.py                 # interface textual (menu numérico)
python main.py --sem-cor       # interface sem cor e sem ênfase visual
python main.py experimentos    # executa os cinco experimentos sem interface e exporta os resultados
python main.py experimentos --saida outra_pasta
```

A interface pede uma semente (padrão 2026) e oferece: jogar uma rodada, jogar dez rodadas, ver a distribuição teórica, executar os experimentos e sair. A variável de ambiente `NO_COLOR` também é respeitada.

## Organização

| Arquivo | Função |
|---|---|
| `modelo.py` | Rolo circular, janela, sorteio da rodada, prêmio, lucro, distribuição teórica, esperança e RTP (em frações exatas) |
| `experimentos.py` | Experimentos 1 a 5 e resumos estatísticos |
| `exportacao.py` | CSVs, gráficos (SVG e PNG) e registro do ambiente |
| `ui.py` | Interface textual com Rich |
| `main.py` | Ponto de entrada |

O sorteio (as paradas K dos três rolos) é separado do pagamento (a tabela). Por isso, o Experimento 5 aplica duas tabelas aos mesmos resultados sorteados, e os Experimentos 1, 2, 4 e 5 reutilizam uma única sequência da semente 2026.

## Gerador e reprodução

- Gerador: `random.Random` (Mersenne Twister), biblioteca padrão do Python
- Cada rodada consome três chamadas a `rng.randrange(5)`, na ordem rolo 1, rolo 2, rolo 3
- A semente é fixada uma única vez por execução: 2026 (E1, E4, E5), 10, 2026 e 123456 (E2), 42 (E3, contínua entre participantes)
- Versões efetivamente usadas: `resultados/ambiente.txt`

## Resultados

Pasta `resultados/`:

| Arquivo | Conteúdo |
|---|---|
| `e1_rodadas_semente_2026.csv` | As 10.000 rodadas brutas (paradas, linha central, prêmio, lucro) |
| `e1_frequencias.csv`, `e1_resumo.csv` | Contagens, frequências e medidas do E1 |
| `e1_teoria_vs_observacao.svg` | Gráfico de barras teoria versus observação |
| `e2_medias_acumuladas.csv`, `.svg` | Médias após 100, 1.000 e 10.000 rodadas; trajetórias |
| `e2_conferencia_reproducao.csv` | Conferência das dez primeiras rodadas da semente 2026 |
| `e3_participantes.csv`, `e3_resumo.csv` | Saldos finais, rodadas e esgotamento dos 100 participantes |
| `e3_trajetorias_cinco_primeiros.svg`, `e3_distribuicao_saldos_finais.svg` | Gráficos do E3 |
| `e4_probabilidade_condicional.csv` | Pares consecutivos após prêmio e após perda |
| `e5_comparacao_tabelas.csv` | Tabela base versus prêmios +10% |

## Uso de IA

Utilizamos o Claude (Anthropic) como apoio na revisão e reescrita do código, na geração da interface textual, na conferência de atualizações do quadro jurídico e na formatação do relatório para exportação em PDF.

O que foi conferido pelo grupo:

- pagamentos das cinco triplas e prêmio zero nas demais (`e1_rodadas_semente_2026.csv`);
- desconto da aposta no lucro (X = P − 1);
- reprodução pela semente (E2; também reexecutado em Linux, Python 3.13, com CSVs idênticos);
- totais: 10.000 contagens no E1, 100 participantes no E3 e 9.999 pares no E4, verificados também por asserções no código;
- correspondência entre os números do relatório e os arquivos de `resultados/`.
