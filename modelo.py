import random
from dataclasses import dataclass
from fractions import Fraction

ROLO = ("A", "B", "C", "D", "E")
APOSTA = 1
AVISO = "Simulador acadêmico - somente créditos fictícios"

TABELA_BASE = {"A": 5, "B": 10, "C": 15, "D": 25, "E": 50}
TABELA_MAIS_10 = {"A": 5.5, "B": 11, "C": 16.5, "D": 27.5, "E": 55}


def janela(k):
    n = len(ROLO)
    return (ROLO[k % n], ROLO[(k + 1) % n], ROLO[(k + 2) % n])


@dataclass(frozen=True)
class Rodada:
    paradas: tuple

    @property
    def colunas(self):
        return tuple(janela(k) for k in self.paradas)

    @property
    def central(self):
        return tuple(coluna[1] for coluna in self.colunas)

    @property
    def premiada(self):
        return len(set(self.central)) == 1


def criar_gerador(semente):
    return random.Random(semente)


def sortear_rodada(rng):
    k1 = rng.randrange(len(ROLO))
    k2 = rng.randrange(len(ROLO))
    k3 = rng.randrange(len(ROLO))
    return Rodada((k1, k2, k3))


def premio(rodada, tabela=TABELA_BASE):
    if rodada.premiada:
        return tabela[rodada.central[0]]
    return 0


def lucro(rodada, tabela=TABELA_BASE):
    return premio(rodada, tabela) - APOSTA


def categoria(rodada):
    if rodada.premiada:
        return "–".join(rodada.central)
    return "Outra"


def distribuicao_teorica(tabela=TABELA_BASE):
    n = len(ROLO)
    p_tripla = Fraction(1, n ** 3)
    linhas = []
    for simbolo in ROLO:
        p = Fraction(str(tabela[simbolo]))
        linhas.append(("–".join([simbolo] * 3), p, p - APOSTA, p_tripla))
    p_outra = 1 - n * p_tripla
    linhas.append(("Outra", Fraction(0), Fraction(-APOSTA), p_outra))
    return linhas


def esperanca_premio(tabela=TABELA_BASE):
    return sum(p * prob for _, p, _, prob in distribuicao_teorica(tabela))


def esperanca_lucro(tabela=TABELA_BASE):
    return esperanca_premio(tabela) - APOSTA


def rtp_teorico(tabela=TABELA_BASE):
    return esperanca_premio(tabela) / APOSTA


def chance_premio():
    return Fraction(len(ROLO), len(ROLO) ** 3)
