from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from modelo import (
    AVISO, TABELA_BASE, chance_premio, criar_gerador, distribuicao_teorica,
    esperanca_lucro, lucro, premio, rtp_teorico, sortear_rodada,
)

CAIXA = box.ASCII


def tabuleiro(rodada):
    t = Table(box=CAIXA, show_header=True, header_style="bold", padding=(0, 2))
    t.add_column("", justify="right")
    for i in range(1, 4):
        t.add_column(f"Rolo {i}", justify="center")
    t.add_column("", justify="left")
    colunas = rodada.colunas
    nomes = ("topo", "CENTRO", "base")
    for linha in range(3):
        celulas = [colunas[c][linha] for c in range(3)]
        if linha == 1:
            t.add_row(">>", *[Text(s, style="bold reverse") for s in celulas], "<< linha paga")
        else:
            t.add_row("", *celulas, Text(nomes[linha], style="italic"))
    return t


def painel_rodada(rodada, numero, saldo):
    p = premio(rodada)
    x = lucro(rodada)
    if p > 0:
        veredito = Text(f"[ PRÊMIO ] tripla {'-'.join(rodada.central)}: recebe {p} créditos", style="bold")
    else:
        veredito = Text("[ SEM PRÊMIO ] linha central sem três símbolos iguais", style="bold")
    detalhe = Text(
        f"Paradas K = {rodada.paradas}   |   prêmio P = {p}   |   lucro X = {x:+}   |   saldo = {saldo}"
    )
    return Panel(Group(tabuleiro(rodada), veredito, detalhe), title=f"Rodada {numero}",
                 box=CAIXA, title_align="left", expand=False)


def painel_regras():
    t = Table(box=CAIXA, title="Distribuição teórica (modelo-base)", header_style="bold")
    t.add_column("Linha central")
    t.add_column("P", justify="right")
    t.add_column("X", justify="right")
    t.add_column("Probabilidade", justify="right")
    for nome, p, x, prob in distribuicao_teorica(TABELA_BASE):
        t.add_row(nome, f"{float(p):g}", f"{float(x):g}", f"{prob} ({float(prob):.2%})")
    rodape = Text(
        f"Chance de prêmio = {chance_premio()} = {float(chance_premio()):.0%}   |   "
        f"E[X] = {float(esperanca_lucro()):+.2f}   |   RTP = {float(rtp_teorico()):.0%}"
    )
    return Panel(Group(t, rodape), box=CAIXA, expand=False)


def menu(console):
    t = Table(box=CAIXA, show_header=False)
    t.add_column(justify="right", style="bold")
    t.add_column()
    for chave, texto in (("1", "Jogar uma rodada"), ("2", "Jogar dez rodadas"),
                         ("3", "Ver regras e distribuição teórica"),
                         ("4", "Executar os cinco experimentos e exportar resultados"),
                         ("0", "Sair")):
        t.add_row(f"[{chave}]", texto)
    console.print(t)
    return Prompt.ask("Escolha", choices=["1", "2", "3", "4", "0"], default="1", console=console)


def executar(console=None, executar_experimentos=None):
    console = console or Console()
    console.print(Panel(Text(AVISO, justify="center", style="bold"), box=box.DOUBLE_EDGE))
    semente = IntPrompt.ask("Semente desta sessão", default=2026, console=console)
    rng = criar_gerador(semente)
    saldo = 100
    numero = 0
    console.print(Text(f"Saldo inicial fictício: {saldo} créditos. Aposta fixa: 1 crédito."))
    while True:
        escolha = menu(console)
        if escolha == "0":
            console.print(Text(f"Sessão encerrada após {numero} rodadas. Saldo final: {saldo}."))
            break
        if escolha == "3":
            console.print(painel_regras())
            continue
        if escolha == "4":
            if executar_experimentos:
                executar_experimentos(console)
            continue
        quantidade = 1 if escolha == "1" else 10
        for _ in range(quantidade):
            if saldo < 1:
                console.print(Text("[ SALDO ESGOTADO ] saldo abaixo de 1 crédito.", style="bold"))
                break
            rodada = sortear_rodada(rng)
            numero += 1
            saldo += lucro(rodada)
            console.print(painel_rodada(rodada, numero, saldo))
