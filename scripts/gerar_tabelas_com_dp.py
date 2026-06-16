import pandas as pd
from pathlib import Path

OUTPUT = Path("paper/tabelas_com_dp.tex")

def fmt(valor):
    return f"{valor:.2f}".replace(".", ",")

def cell(media, dp):
    return f"{fmt(media)} $\\pm$ {fmt(dp)}x"

df = pd.read_csv("data/resultados_completo.csv")

# Descarta as 5 primeiras repetições, como descrito na metodologia
df = df[df["repeticao"] > 5].copy()

pivot = df.pivot_table(
    index=["tamanho", "otimizacao", "repeticao"],
    columns="tipo_acesso",
    values="tempo_ms"
).reset_index()

pivot["razao_coluna_linha"] = pivot["coluna"] / pivot["linha"]

stats_acesso = (
    pivot
    .groupby(["tamanho", "otimizacao"])["razao_coluna_linha"]
    .agg(["mean", "std"])
    .reset_index()
)

stats_acesso["celula"] = stats_acesso.apply(
    lambda r: cell(r["mean"], r["std"]),
    axis=1
)

tab_acesso = stats_acesso.pivot(
    index="tamanho",
    columns="otimizacao",
    values="celula"
)

dfm = pd.read_csv("data/multiplicacao_completo.csv")

# Descarta as 2 primeiras repetições, como descrito na metodologia
dfm = dfm[dfm["repeticao"] > 2].copy()

pivot_m = dfm.pivot_table(
    index=["tamanho", "otimizacao", "repeticao"],
    columns="algoritmo",
    values="tempo_ms"
).reset_index()

pivot_m["speedup_blocos"] = pivot_m["normal"] / pivot_m["blocos"]

stats_mult = (
    pivot_m
    .groupby(["tamanho", "otimizacao"])["speedup_blocos"]
    .agg(["mean", "std"])
    .reset_index()
)

stats_mult["celula"] = stats_mult.apply(
    lambda r: cell(r["mean"], r["std"]),
    axis=1
)

tab_mult = stats_mult.pivot(
    index="tamanho",
    columns="otimizacao",
    values="celula"
)

linhas = []

linhas.append(r"\begin{table}[ht]")
linhas.append(r"\centering")
linhas.append(r"\caption{Razão entre o tempo médio do acesso por coluna e por linha, apresentada como média $\pm$ desvio padrão.}")
linhas.append(r"\label{tab:razao-coluna-linha}")
linhas.append(r"\begin{tabular}{rrrr}")
linhas.append(r"\toprule")
linhas.append(r"Tamanho & \texttt{-O0} & \texttt{-O2} & \texttt{-O3} \\")
linhas.append(r"\midrule")

for tamanho in tab_acesso.index:
    linhas.append(
        f"{tamanho}x{tamanho} & {tab_acesso.loc[tamanho, 'O0']} & {tab_acesso.loc[tamanho, 'O2']} & {tab_acesso.loc[tamanho, 'O3']} \\\\"
    )

linhas.append(r"\bottomrule")
linhas.append(r"\end{tabular}")
linhas.append(r"\end{table}")
linhas.append("")

linhas.append(r"\begin{table}[ht]")
linhas.append(r"\centering")
linhas.append(r"\caption{Speedup da multiplicação com blocagem em relação à multiplicação tradicional, apresentado como média $\pm$ desvio padrão.}")
linhas.append(r"\label{tab:speedup-blocagem}")
linhas.append(r"\begin{tabular}{rrrr}")
linhas.append(r"\toprule")
linhas.append(r"Tamanho & \texttt{-O0} & \texttt{-O2} & \texttt{-O3} \\")
linhas.append(r"\midrule")

for tamanho in tab_mult.index:
    linhas.append(
        f"{tamanho}x{tamanho} & {tab_mult.loc[tamanho, 'O0']} & {tab_mult.loc[tamanho, 'O2']} & {tab_mult.loc[tamanho, 'O3']} \\\\"
    )

linhas.append(r"\bottomrule")
linhas.append(r"\end{tabular}")
linhas.append(r"\end{table}")

OUTPUT.write_text("\n".join(linhas), encoding="utf-8")

print(f"Tabelas com desvio padrão salvas em {OUTPUT}")