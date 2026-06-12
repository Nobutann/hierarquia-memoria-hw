#define _POSIX_C_SOURCE 199309L

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <time.h>
#endif

#ifndef OPT_LEVEL
#define OPT_LEVEL "unknown"
#endif

volatile double sink = 0.0;

double now_seconds() {
#ifdef _WIN32
    static LARGE_INTEGER frequency;
    static int initialized = 0;
    LARGE_INTEGER counter;

    if (!initialized) {
        QueryPerformanceFrequency(&frequency);
        initialized = 1;
    }

    QueryPerformanceCounter(&counter);
    return (double) counter.QuadPart / (double) frequency.QuadPart;
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
#endif
}

double *criar_matriz(int n) {
    double *matriz = malloc((size_t)n * n * sizeof(double));

    if (matriz == NULL) {
        fprintf(stderr, "Erro ao alocar memoria para matriz %dx%d\n", n, n);
        exit(1);
    }

    for (int i = 0; i < n * n; i++) {
        matriz[i] = (double)(i % 100);
    }

    return matriz;
}

double somar_por_linha(double *matriz, int n) {
    double soma = 0.0;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            soma += matriz[i * n + j];
        }
    }

    return soma;
}

double somar_por_coluna(double *matriz, int n) {
    double soma = 0.0;

    for (int j = 0; j < n; j++) {
        for (int i = 0; i < n; i++) {
            soma += matriz[i * n + j];
        }
    }

    return soma;
}

void executar_teste(int n, int repeticoes) {
    double *matriz = criar_matriz(n);

    // Aquecimento: evita medir apenas efeitos iniciais de carregamento.
    sink = somar_por_linha(matriz, n);
    sink = somar_por_coluna(matriz, n);

    for (int r = 1; r <= repeticoes; r++) {
        double inicio = now_seconds();
        double soma_linha = somar_por_linha(matriz, n);
        double fim = now_seconds();

        sink = soma_linha;

        printf("linha_coluna,%d,%s,linha,%d,%.6f,%.2f\n",
               n, OPT_LEVEL, r, (fim - inicio) * 1000.0, soma_linha);

        inicio = now_seconds();
        double soma_coluna = somar_por_coluna(matriz, n);
        fim = now_seconds();

        sink = soma_coluna;

        printf("linha_coluna,%d,%s,coluna,%d,%.6f,%.2f\n",
               n, OPT_LEVEL, r, (fim - inicio) * 1000.0, soma_coluna);
    }

    free(matriz);
}

int main() {
    int tamanhos[] = {512, 1024, 2048, 4096};
    int quantidade_tamanhos = sizeof(tamanhos) / sizeof(tamanhos[0]);
    int repeticoes = 30;

    printf("experimento,tamanho,otimizacao,tipo_acesso,repeticao,tempo_ms,soma\n");

    for (int i = 0; i < quantidade_tamanhos; i++) {
        executar_teste(tamanhos[i], repeticoes);
    }

    return 0;
}