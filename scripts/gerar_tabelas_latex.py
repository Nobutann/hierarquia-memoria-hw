import pandas as pd
from pathlib import Path

OUTPUT = Path("paper/tabelas_latex.tex")

def fmt(valor):
    return f"{valor:.2f}".replace(".", ",")

def tabela_acesso():
    df = pd.read_csv("data/comparacao_coluna_linha.csv")

    pivot = df.pivot(index="tamanho", columns="otimizacao", values="razao_coluna_linha")
    pivot = pivot[["O0", "O2", "O3"]]

    linhas = []
    linhas.append("\\begin{table}[ht]")
    linhas.append("\\centering")
    linhas.append("\\caption{Razão entre o tempo médio do acesso por coluna e por linha.}")
    linhas.append("\\label{tab:razao-coluna-linha}")
    linhas.append("\\begin{tabular}{rrrr}")
    linhas.append("\\hline")
    linhas.append("Tamanho & \\texttt{-O0} & \\texttt{-O2} & \\texttt{-O3} \\\\")
    linhas.append("\\hline")

    for tamanho, row in pivot.iterrows():
        linhas.append(
            f"{tamanho}x{tamanho} & {fmt(row['O0'])}x & {fmt(row['O2'])}x & {fmt(row['O3'])}x \\\\"
        )

    linhas.append("\\hline")
    linhas.append("\\end{tabular}")
    linhas.append("\\end{table}")

    return "\n".join(linhas)

def tabela_multiplicacao():
    df = pd.read_csv("data/comparacao_multiplicacao.csv")

    pivot = df.pivot(index="tamanho", columns="otimizacao", values="speedup_blocos")
    pivot = pivot[["O0", "O2", "O3"]]

    linhas = []
    linhas.append("\\begin{table}[ht]")
    linhas.append("\\centering")
    linhas.append("\\caption{Speedup da multiplicação com blocagem em relação à multiplicação tradicional.}")
    linhas.append("\\label{tab:speedup-blocagem}")
    linhas.append("\\begin{tabular}{rrrr}")
    linhas.append("\\hline")
    linhas.append("Tamanho & \\texttt{-O0} & \\texttt{-O2} & \\texttt{-O3} \\\\")
    linhas.append("\\hline")

    for tamanho, row in pivot.iterrows():
        linhas.append(
            f"{tamanho}x{tamanho} & {fmt(row['O0'])}x & {fmt(row['O2'])}x & {fmt(row['O3'])}x \\\\"
        )

    linhas.append("\\hline")
    linhas.append("\\end{tabular}")
    linhas.append("\\end{table}")

    return "\n".join(linhas)

def tabela_cachegrind():
    linhas = []
    linhas.append("\\begin{table}[ht]")
    linhas.append("\\centering")
    linhas.append("\\caption{Resultados de Cachegrind para casos representativos.}")
    linhas.append("\\label{tab:cachegrind}")
    linhas.append("\\begin{tabular}{lrrr}")
    linhas.append("\\hline")
    linhas.append("Caso & D refs & D1 misses & D1 miss rate \\\\")
    linhas.append("\\hline")
    linhas.append("Acesso por linha 2048x2048 & 6.337.458 & 1.050.490 & 16,6\\% \\\\")
    linhas.append("Acesso por coluna 2048x2048 & 6.337.465 & 4.720.505 & 74,5\\% \\\\")
    linhas.append("Multiplicação tradicional 512x512 & 269.334.520 & 134.942.113 & 50,1\\% \\\\")
    linhas.append("Multiplicação com blocagem 512x512 & 408.043.318 & 22.423.747 & 5,5\\% \\\\")
    linhas.append("\\hline")
    linhas.append("\\end{tabular}")
    linhas.append("\\end{table}")

    return "\n".join(linhas)

conteudo = "\n\n".join([
    tabela_acesso(),
    tabela_multiplicacao(),
    tabela_cachegrind()
])

OUTPUT.write_text(conteudo, encoding="utf-8")

print(f"Tabelas LaTeX salvas em {OUTPUT}")