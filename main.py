import argparse

from rich import box
from rich.console import Console
from rich.table import Table

import ui
from experimentos import executar_todos
from exportacao import exportar_tudo
from modelo import AVISO


def _tabela(titulo, linhas, formatos=None):
    formatos = formatos or {}
    t = Table(title=titulo, box=box.ASCII, header_style="bold")
    for campo in linhas[0]:
        t.add_column(campo, justify="right")
    for linha in linhas:
        celulas = []
        for campo, valor in linha.items():
            if isinstance(valor, float):
                celulas.append(format(valor, formatos.get(campo, ".4f")))
            else:
                celulas.append(str(valor))
        t.add_row(*celulas)
    return t


def _pares(dicionario):
    return [{"medida": k, "valor": v} for k, v in dicionario.items()]


def rodar_experimentos(console, pasta="resultados"):
    console.print(f"[bold]{AVISO}[/bold]")
    resultados = executar_todos()
    destino = exportar_tudo(resultados, pasta)
    console.print(_tabela("E1 - Frequências (semente 2026, N = 10.000)", resultados["e1"]["tabela"]))
    console.print(_tabela("E1 - Resumo", _pares(resultados["e1"]["resumo"])))
    console.print(_tabela("E2 - Médias acumuladas do lucro", resultados["e2"]["tabela"]))
    console.print(f"E2 - Dez primeiras rodadas da semente 2026 reproduzidas: "
                  f"{'SIM' if resultados['e2']['reproduzida'] else 'NÃO'}")
    console.print(_tabela("E3 - Saldo limitado (semente 42)", _pares(resultados["e3"]["resumo"])))
    console.print(_tabela("E4 - Probabilidade condicional (9.999 pares)", resultados["e4"]["tabela"]))
    console.print(_tabela("E5 - Comparação de tabelas de pagamento", resultados["e5"]["tabela"]))
    console.print(f"Resultados exportados em: {destino.resolve()}")
    return resultados


def principal():
    parser = argparse.ArgumentParser(description=AVISO)
    parser.add_argument("modo", nargs="?", choices=["interface", "experimentos"], default="interface")
    parser.add_argument("--saida", default="resultados", help="pasta dos CSVs e gráficos")
    parser.add_argument("--sem-cor", action="store_true", help="desativa estilos de cor e ênfase")
    args = parser.parse_args()
    console = Console(no_color=args.sem_cor, highlight=False)
    if args.modo == "experimentos":
        rodar_experimentos(console, args.saida)
    else:
        ui.executar(console, lambda c: rodar_experimentos(c, args.saida))


if __name__ == "__main__":
    principal()
