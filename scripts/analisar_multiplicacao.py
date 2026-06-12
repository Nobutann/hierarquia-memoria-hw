import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("data/multiplicacao_completo.csv")
RESUMO_PATH = Path("data/resumo_multiplicacao.csv")
COMPARACAO_PATH = Path("data/comparacao_multiplicacao.csv")
PLOTS_DIR = Path("plots")

PLOTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Remove as 2 primeiras repetições para reduzir efeito de aquecimento
df_filtrado = df[df["repeticao"] > 2].copy()

resumo = (
    df_filtrado
    .groupby(["tamanho", "otimizacao", "algoritmo"])["tempo_ms"]
    .agg(["mean", "median", "std", "min", "max", "count"])
    .reset_index()
)

resumo = resumo.rename(columns={
    "mean": "media_ms",
    "median": "mediana_ms",
    "std": "desvio_padrao_ms",
    "min": "minimo_ms",
    "max": "maximo_ms",
    "count": "quantidade_medicoes"
})

resumo.to_csv(RESUMO_PATH, index=False)

print("Resumo salvo em:", RESUMO_PATH)
print(resumo)

pivot = resumo.pivot_table(
    index=["tamanho", "otimizacao"],
    columns="algoritmo",
    values="media_ms"
).reset_index()

pivot["speedup_blocos"] = pivot["normal"] / pivot["blocos"]

pivot.to_csv(COMPARACAO_PATH, index=False)

print("Comparação salva em:", COMPARACAO_PATH)
print(pivot)

for opt in sorted(df_filtrado["otimizacao"].unique()):
    dados_opt = resumo[resumo["otimizacao"] == opt]

    normal = dados_opt[dados_opt["algoritmo"] == "normal"]
    blocos = dados_opt[dados_opt["algoritmo"] == "blocos"]

    plt.figure(figsize=(8, 5))

    plt.plot(
        normal["tamanho"],
        normal["media_ms"],
        marker="o",
        label="Multiplicação normal"
    )

    plt.plot(
        blocos["tamanho"],
        blocos["media_ms"],
        marker="o",
        label="Multiplicação com blocagem"
    )

    plt.title(f"Multiplicação de matrizes - {opt}")
    plt.xlabel("Tamanho da matriz")
    plt.ylabel("Tempo médio (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = PLOTS_DIR / f"grafico_multiplicacao_{opt}.png"
    plt.savefig(output_path, dpi=300)
    plt.savefig(PLOTS_DIR / f"grafico_multiplicacao_{opt}.pdf")
    plt.close()

    print("Gráfico salvo em:", output_path)