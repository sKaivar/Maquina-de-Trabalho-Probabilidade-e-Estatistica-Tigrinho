"""Converte o relatorio.md (sintaxe Obsidian) em Markdown para pandoc/xelatex."""
import re
import sys
from pathlib import Path

origem, destino = Path(sys.argv[1]), Path(sys.argv[2])
texto = origem.read_text(encoding="utf-8")

# 1. Remove o frontmatter YAML.
texto = re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.S)

# 2. Substitui título, autores e cabeçalho HTML por um bloco LaTeX.
titulo = r"""
```{=latex}
\begin{center}
{\LARGE\bfseries Máquina Estatística: probabilidade, apostas e pensamento crítico\par}
\vspace{0.8em}
{\large Kaiva Silverio Gums (20241BSI0130)\\ Matheus Morôni Arçari Barcellos (20212BSI0154)\par}
\vspace{0.5em}
{\small Instituto Federal do Espírito Santo — Campus Serra · Bacharelado em Sistemas de Informação\\
Probabilidade e Estatística I — Trabalho I — 2026/2 · Prof. Fidelis Zanetti de Castro\par}
\end{center}
\vspace{0.4em}\hrule\vspace{1em}
```
"""
texto = re.sub(r"\A\s*# .*?\n\n---\n", lambda m: titulo, texto, flags=re.S)

# 3. Figuras: ![[arquivo.svg]] + parágrafo de legenda em itálico -> figura com legenda.
def figura(m):
    nome = Path(m.group(1)).stem
    legenda = m.group(2).strip()
    legenda = re.sub(r"^(Figura \d+\.)", r"**\1**", legenda)
    return f"![{legenda}](figs/{nome}.pdf){{width=76%}}\n"

texto, n = re.subn(r"!\[\[([^\]]+\.svg)\]\]\n\n\*(Figura .+?)\*\n", figura, texto)
assert n == 4, n

# 4. Quebra de página antes das referências.
texto = texto.replace('<div style="page-break-after: always;"></div>', "\\newpage")

# 5. Mantém o rótulo da tabela junto da tabela.
texto = re.sub(r"\n(\*\*Tabela \d+\.\*\*.*\n)", r"\n\\needspace{11\\baselineskip}\n\n\1", texto)

assert "<div" not in texto and "![[" not in texto

# 6. Hifenização pt-BR: insere hífens discricionários (U+00AD) via pyphen, pois o
#    TeX local não traz os padrões portugueses. Matemática, código, URLs, caminhos
#    de imagem e o bloco LaTeX bruto ficam intactos.
import pyphen

SHY = "­"
dic = pyphen.Pyphen(lang="pt_BR", left=2, right=3)
protegido = re.compile(r"(\$\$.*?\$\$|\$[^$]+\$|`[^`]*`|https?://\S+|\]\([^)]*\)|\{[^}]*\}|\\[A-Za-z]+)")
palavra = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]{7,}")


def hifenizar_trecho(trecho):
    return palavra.sub(lambda m: dic.inserted(m.group(0), hyphen=SHY), trecho)


saida, em_bloco = [], False
for linha in texto.split("\n"):
    if linha.startswith("```"):
        em_bloco = not em_bloco
        saida.append(linha)
        continue
    if em_bloco or linha.startswith("$$"):
        saida.append(linha)
        continue
    partes = protegido.split(linha)
    saida.append("".join(p if i % 2 else hifenizar_trecho(p) for i, p in enumerate(partes)))
texto = "\n".join(saida)
destino.write_text(texto, encoding="utf-8")
print("ok", destino)
