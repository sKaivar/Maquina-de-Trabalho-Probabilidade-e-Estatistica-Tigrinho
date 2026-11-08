#!/bin/sh
pandoc relatorio_build.md -o relatorio.pdf --pdf-engine=xelatex -H cabecalho.tex \
  -V documentclass=article -V papersize=a4 -V fontsize=11pt -V geometry:margin=2.2cm \
  -V mainfont="Latin Modern Roman" -V monofont="Latin Modern Mono" -V linestretch=1.06 \
  -V colorlinks=true -V linkcolor=black -V urlcolor=[HTML]{1F4E79} -V pagestyle=plain
