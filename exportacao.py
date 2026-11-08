import csv
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from modelo import ROLO, premio, lucro

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Liberation Serif", "Times New Roman", "serif"],
    "font.size": 10,
    "axes.facecolor": SUPERFICIE,
    "figure.facecolor": SUPERFICIE,
    "axes.edgecolor": TINTA_SECUNDARIA,
    "axes.labelcolor": TINTA,
    "xtick.color": TINTA_SECUNDARIA,
    "ytick.color": TINTA_SECUNDARIA,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e4e3df",
    "grid.linewidth": 0.6,
    "legend.frameon": False,
    "svg.fonttype": "path",
})


def _csv(caminho, linhas, campos=None):
    campos = campos or list(linhas[0].keys())
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(linhas)


def _salvar(fig, pasta, nome):
    for ext in ("svg", "png"):
        fig.savefig(pasta / f"{nome}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)


def _versao(pacote):
    try:
        return version(pacote)
    except PackageNotFoundError:
        return "não instalado"


def registrar_ambiente(pasta):
    linhas = [
        f"Python: {sys.version.split()[0]} ({platform.python_implementation()})",
        f"Sistema: {platform.platform()}",
        "Gerador: random.Random (Mersenne Twister MT19937), biblioteca padrão",
        "Sorteio da parada: rng.randrange(5), três chamadas por rodada, ordem rolo 1, 2, 3",
        f"rich: {_versao('rich')}",
        f"matplotlib: {_versao('matplotlib')}",
    ]
    (pasta / "ambiente.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")


def exportar_rodadas(pasta, rodadas):
    linhas = []
    for i, r in enumerate(rodadas, start=1):
        linhas.append({
            "rodada": i,
            "k1": r.paradas[0], "k2": r.paradas[1], "k3": r.paradas[2],
            "linha_central": "-".join(r.central),
            "premio": premio(r),
            "lucro": lucro(r),
        })
    _csv(pasta / "e1_rodadas_semente_2026.csv", linhas)


def exportar_e1(pasta, e1):
    _csv(pasta / "e1_frequencias.csv", e1["tabela"])
    _csv(pasta / "e1_resumo.csv", [{"medida": k, "valor": v} for k, v in e1["resumo"].items()])

    tabela = e1["tabela"]
    rotulos = [f"{linha['lucro']:g}" for linha in tabela]
    teorica = [linha["probabilidade_teorica"] for linha in tabela]
    observada = [linha["frequencia_relativa"] for linha in tabela]
    x = range(len(tabela))
    largura = 0.38

    fig, ax = plt.subplots(figsize=(7, 4))
    b1 = ax.bar([i - largura / 2 - 0.01 for i in x], teorica, largura, color=SERIES[0], label="Probabilidade teórica")
    b2 = ax.bar([i + largura / 2 + 0.01 for i in x], observada, largura, color=SERIES[1], label="Frequência relativa observada")
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 2)
    ax.set_xticks(list(x), rotulos)
    ax.set_xlabel("Lucro X por rodada (créditos)")
    ax.set_ylabel("Proporção (escala logarítmica)")
    for barras in (b1, b2):
        for barra in barras:
            altura = barra.get_height()
            ax.annotate(f"{altura:.4f}".replace(".", ","), (barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 2), textcoords="offset points", ha="center", va="bottom",
                        fontsize=7, color=TINTA_SECUNDARIA, rotation=90)
    ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.12))
    ax.grid(axis="x", visible=False)
    _salvar(fig, pasta, "e1_teoria_vs_observacao")


def exportar_e2(pasta, e2):
    _csv(pasta / "e2_medias_acumuladas.csv", e2["tabela"])
    _csv(pasta / "e2_conferencia_reproducao.csv", [
        {**linha, "paradas_original": " ".join(map(str, linha["paradas_original"])),
         "paradas_repetida": " ".join(map(str, linha["paradas_repetida"]))}
        for linha in e2["conferencia"]
    ])

    fig, ax = plt.subplots(figsize=(7, 4))
    for cor, (semente, medias) in zip(SERIES, e2["trajetorias"].items()):
        ax.plot(range(1, len(medias) + 1), medias, color=cor, linewidth=1.4, label=f"Semente {semente}")
    ax.axhline(e2["esperanca"], color=TINTA, linewidth=1.2, linestyle="--", label="E[X] = −0,16")
    ax.set_xscale("log")
    ax.set_ylim(-1.05, 2.0)
    ax.set_xlabel("Número de rodadas n (escala logarítmica)")
    ax.set_ylabel("Lucro médio acumulado (créditos)")
    ax.legend(loc="upper right")
    _salvar(fig, pasta, "e2_medias_acumuladas")


def exportar_e3(pasta, e3):
    _csv(pasta / "e3_participantes.csv", e3["registros"])
    _csv(pasta / "e3_resumo.csv", [{"medida": k, "valor": v} for k, v in e3["resumo"].items()])

    fig, ax = plt.subplots(figsize=(7, 4))
    estilos = ["-", "--", "-.", ":", (0, (5, 1, 1, 1))]
    for i, trajetoria in enumerate(e3["trajetorias"][:5]):
        completa = trajetoria + [trajetoria[-1]] * (e3["max_rodadas"] + 1 - len(trajetoria))
        ax.plot(range(len(completa)), completa, color=SERIES[i], linestyle=estilos[i],
                linewidth=1.4, label=f"Participante {i + 1}")
    ax.axhline(e3["saldo_inicial"], color=TINTA_SECUNDARIA, linewidth=0.9, linestyle=":")
    ax.set_xlabel("Rodada")
    ax.set_ylabel("Saldo (créditos)")
    ax.set_xlim(0, e3["max_rodadas"])
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper center", ncol=5, bbox_to_anchor=(0.5, -0.16), fontsize=8)
    _salvar(fig, pasta, "e3_trajetorias_cinco_primeiros")

    finais = [r["saldo_final"] for r in e3["registros"]]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.hist(finais, bins=20, color=SERIES[0], edgecolor=SUPERFICIE, linewidth=2)
    ax.axvline(e3["resumo"]["media_saldo_final"], color=TINTA, linestyle="--", linewidth=1.2,
               label=f"Média = {e3['resumo']['media_saldo_final']:.2f}".replace(".", ","))
    ax.axvline(e3["resumo"]["mediana_saldo_final"], color=SERIES[1], linestyle="-", linewidth=1.6,
               label=f"Mediana = {e3['resumo']['mediana_saldo_final']:.1f}".replace(".", ","))
    ax.set_xlabel("Saldo final (créditos)")
    ax.set_ylabel("Número de participantes")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    _salvar(fig, pasta, "e3_distribuicao_saldos_finais")


def exportar_e4(pasta, e4):
    _csv(pasta / "e4_probabilidade_condicional.csv", e4["tabela"])


def exportar_e5(pasta, e5):
    _csv(pasta / "e5_comparacao_tabelas.csv", e5["tabela"])


def exportar_tudo(resultados, pasta="resultados"):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    registrar_ambiente(pasta)
    exportar_rodadas(pasta, resultados["rodadas_2026"])
    exportar_e1(pasta, resultados["e1"])
    exportar_e2(pasta, resultados["e2"])
    exportar_e3(pasta, resultados["e3"])
    exportar_e4(pasta, resultados["e4"])
    exportar_e5(pasta, resultados["e5"])
    return pasta
