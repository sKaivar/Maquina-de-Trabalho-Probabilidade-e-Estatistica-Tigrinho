import statistics
from collections import Counter

from modelo import (
    APOSTA, ROLO, TABELA_BASE, TABELA_MAIS_10,
    categoria, chance_premio, criar_gerador, distribuicao_teorica,
    esperanca_lucro, lucro, premio, rtp_teorico, sortear_rodada,
)


def gerar_sequencia(semente, n):
    rng = criar_gerador(semente)
    return [sortear_rodada(rng) for _ in range(n)]


def resumo(rodadas, tabela=TABELA_BASE):
    premios = [premio(r, tabela) for r in rodadas]
    lucros = [p - APOSTA for p in premios]
    n = len(rodadas)
    premiadas = [p for p in premios if p > 0]
    return {
        "N": n,
        "lucro_medio": sum(lucros) / n,
        "rtp_observado": sum(premios) / (n * APOSTA),
        "proporcao_premiadas": len(premiadas) / n,
        "desvio_padrao_lucro": statistics.stdev(lucros),
        "premio_medio_por_rodada": sum(premios) / n,
        "premio_medio_se_premiada": (sum(premiadas) / len(premiadas)) if premiadas else None,
    }


def experimento_1(rodadas):
    contagem = Counter(categoria(r) for r in rodadas)
    n = len(rodadas)
    tabela = []
    for nome, _, x, prob in distribuicao_teorica(TABELA_BASE):
        c = contagem.get(nome, 0)
        tabela.append({
            "resultado": nome,
            "lucro": float(x),
            "probabilidade_teorica": float(prob),
            "contagem": c,
            "frequencia_relativa": c / n,
        })
    assert sum(linha["contagem"] for linha in tabela) == n
    return {"tabela": tabela, "resumo": resumo(rodadas)}


def medias_acumuladas(rodadas, tabela=TABELA_BASE):
    soma = 0
    medias = []
    for i, r in enumerate(rodadas, start=1):
        soma += lucro(r, tabela)
        medias.append(soma / i)
    return medias


def experimento_2(sequencias, marcos=(100, 1000, 10000), n_conferencia=10):
    trajetorias = {s: medias_acumuladas(rodadas) for s, rodadas in sequencias.items()}
    tabela = [
        {"semente": s, **{f"apos_{m}": trajetorias[s][m - 1] for m in marcos}}
        for s in sequencias
    ]
    original = sequencias[2026][:n_conferencia]
    repetida = gerar_sequencia(2026, n_conferencia)
    conferencia = [
        {
            "rodada": i + 1,
            "paradas_original": a.paradas,
            "paradas_repetida": b.paradas,
            "igual": a.paradas == b.paradas,
        }
        for i, (a, b) in enumerate(zip(original, repetida))
    ]
    reproduzida = all(linha["igual"] for linha in conferencia)
    return {
        "tabela": tabela,
        "trajetorias": trajetorias,
        "conferencia": conferencia,
        "reproduzida": reproduzida,
        "esperanca": float(esperanca_lucro()),
    }


def experimento_3(semente=42, participantes=100, saldo_inicial=100, max_rodadas=500):
    rng = criar_gerador(semente)
    registros = []
    trajetorias = []
    for pid in range(1, participantes + 1):
        saldo = saldo_inicial
        trajetoria = [saldo]
        rodadas = 0
        while rodadas < max_rodadas and saldo >= APOSTA:
            saldo += lucro(sortear_rodada(rng))
            rodadas += 1
            trajetoria.append(saldo)
        if saldo > saldo_inicial:
            situacao = "ganho"
        elif saldo == saldo_inicial:
            situacao = "empate"
        else:
            situacao = "perda"
        registros.append({
            "participante": pid,
            "saldo_final": saldo,
            "rodadas": rodadas,
            "esgotou": saldo < APOSTA,
            "situacao": situacao,
        })
        trajetorias.append(trajetoria)
    contagem = Counter(r["situacao"] for r in registros)
    finais = [r["saldo_final"] for r in registros]
    esgotados = sum(r["esgotou"] for r in registros)
    assert sum(contagem.values()) == participantes
    assert esgotados <= contagem["perda"]
    resumo_e3 = {
        "proporcao_ganho": contagem["ganho"] / participantes,
        "proporcao_empate": contagem["empate"] / participantes,
        "proporcao_perda": contagem["perda"] / participantes,
        "proporcao_esgotamento": esgotados / participantes,
        "media_saldo_final": statistics.mean(finais),
        "mediana_saldo_final": statistics.median(finais),
        "media_rodadas": statistics.mean(r["rodadas"] for r in registros),
    }
    return {"registros": registros, "trajetorias": trajetorias, "resumo": resumo_e3,
            "max_rodadas": max_rodadas, "saldo_inicial": saldo_inicial}


def experimento_4(rodadas):
    grupos = {"após prêmio": [0, 0], "após perda": [0, 0]}
    for anterior, seguinte in zip(rodadas, rodadas[1:]):
        chave = "após prêmio" if anterior.premiada else "após perda"
        grupos[chave][0] += 1
        grupos[chave][1] += int(seguinte.premiada)
    total_pares = sum(g[0] for g in grupos.values())
    assert total_pares == len(rodadas) - 1
    tabela = [
        {
            "resultado_anterior": chave,
            "total_pares": pares,
            "premios_na_seguinte": premios,
            "proporcao": (premios / pares) if pares else "não estimável",
        }
        for chave, (pares, premios) in grupos.items()
    ]
    return {"tabela": tabela, "referencia": float(chance_premio()), "total_pares": total_pares}


def experimento_5(rodadas):
    configuracoes = {"Base": TABELA_BASE, "Prêmios +10%": TABELA_MAIS_10}
    tabela = []
    for nome, pagamentos in configuracoes.items():
        r = resumo(rodadas, pagamentos)
        tabela.append({
            "configuracao": nome,
            "probabilidade_premio": float(chance_premio()),
            "frequencia_premio": r["proporcao_premiadas"],
            "premio_medio_por_rodada": r["premio_medio_por_rodada"],
            "premio_medio_se_premiada": r["premio_medio_se_premiada"],
            "lucro_medio": r["lucro_medio"],
            "lucro_esperado": float(esperanca_lucro(pagamentos)),
            "rtp_teorico": float(rtp_teorico(pagamentos)),
            "rtp_observado": r["rtp_observado"],
        })
    return {"tabela": tabela}


def executar_todos(n=10000, sementes=(10, 2026, 123456)):
    sequencias = {s: gerar_sequencia(s, n) for s in sementes}
    base = sequencias[2026]
    return {
        "n": n,
        "rodadas_2026": base,
        "e1": experimento_1(base),
        "e2": experimento_2(sequencias),
        "e3": experimento_3(),
        "e4": experimento_4(base),
        "e5": experimento_5(base),
    }
