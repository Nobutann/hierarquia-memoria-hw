import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("data/resultados_completo.csv")
RESUMO_PATH = Path("data/resumo_linha_coluna.csv")
PLOTS_DIR = Path("plots")

PLOTS_DIR.mkdir(exist_ok=True)

# Lê os dados
df = pd.read_csv(DATA_PATH)

# Remove as primeiras repetições para reduzir efeito de aquecimento
df_filtrado = df[df["repeticao"] > 5].copy()

# Gera resumo estatístico
resumo = (
    df_filtrado
    .groupby(["tamanho", "otimizacao", "tipo_acesso"])["tempo_ms"]
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

# Gera um gráfico para cada nível de otimização
for opt in sorted(df_filtrado["otimizacao"].unique()):
    dados_opt = resumo[resumo["otimizacao"] == opt]

    linha = dados_opt[dados_opt["tipo_acesso"] == "linha"]
    coluna = dados_opt[dados_opt["tipo_acesso"] == "coluna"]

    plt.figure(figsize=(8, 5))

    plt.plot(
        linha["tamanho"],
        linha["media_ms"],
        marker="o",
        label="Acesso por linha"
    )

    plt.plot(
        coluna["tamanho"],
        coluna["media_ms"],
        marker="o",
        label="Acesso por coluna"
    )

    plt.title(f"Tempo médio por padrão de acesso - {opt}")
    plt.xlabel("Tamanho da matriz")
    plt.ylabel("Tempo médio (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = PLOTS_DIR / f"grafico_linha_coluna_{opt}.png"
    plt.savefig(output_path, dpi=300)
    plt.savefig(PLOTS_DIR / f"grafico_linha_coluna_{opt}.pdf")
    plt.close()

    print("Gráfico salvo em:", output_path)

# Gera tabela comparando coluna/linha
pivot = resumo.pivot_table(
    index=["tamanho", "otimizacao"],
    columns="tipo_acesso",
    values="media_ms"
).reset_index()

pivot["razao_coluna_linha"] = pivot["coluna"] / pivot["linha"]

pivot.to_csv("data/comparacao_coluna_linha.csv", index=False)

print("Comparação salva em: data/comparacao_coluna_linha.csv")
print(pivot)