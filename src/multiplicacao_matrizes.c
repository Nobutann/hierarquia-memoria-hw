#define _POSIX_C_SOURCE 199309L

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef OPT_LEVEL
#define OPT_LEVEL "unknown"
#endif

volatile double sink = 0.0;

double now_seconds() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int min_int(int a, int b) {
    return a < b ? a : b;
}

double *criar_matriz(int n) {
    double *matriz = malloc((size_t)n * n * sizeof(double));

    if (matriz == NULL) {
        fprintf(stderr, "Erro ao alocar matriz %dx%d\n", n, n);
        exit(1);
    }

    return matriz;
}

void inicializar_matriz(double *matriz, int n) {
    for (int i = 0; i < n * n; i++) {
        matriz[i] = (double)((i % 100) + 1);
    }
}

void zerar_matriz(double *matriz, int n) {
    for (int i = 0; i < n * n; i++) {
        matriz[i] = 0.0;
    }
}

double checksum(double *matriz, int n) {
    double soma = 0.0;

    for (int i = 0; i < n * n; i++) {
        soma += matriz[i];
    }

    return soma;
}

void multiplicar_normal(double *a, double *b, double *c, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double soma = 0.0;

            for (int k = 0; k < n; k++) {
                soma += a[i * n + k] * b[k * n + j];
            }

            c[i * n + j] = soma;
        }
    }
}

void multiplicar_blocos(double *a, double *b, double *c, int n, int bloco) {
    for (int ii = 0; ii < n; ii += bloco) {
        for (int jj = 0; jj < n; jj += bloco) {
            for (int kk = 0; kk < n; kk += bloco) {

                int i_max = min_int(ii + bloco, n);
                int j_max = min_int(jj + bloco, n);
                int k_max = min_int(kk + bloco, n);

                for (int i = ii; i < i_max; i++) {
                    for (int j = jj; j < j_max; j++) {
                        double soma = c[i * n + j];

                        for (int k = kk; k < k_max; k++) {
                            soma += a[i * n + k] * b[k * n + j];
                        }

                        c[i * n + j] = soma;
                    }
                }
            }
        }
    }
}

void executar_teste(int n, int repeticoes, int bloco) {
    double *a = criar_matriz(n);
    double *b = criar_matriz(n);
    double *c = criar_matriz(n);

    inicializar_matriz(a, n);
    inicializar_matriz(b, n);

    for (int r = 1; r <= repeticoes; r++) {
        zerar_matriz(c, n);

        double inicio = now_seconds();
        multiplicar_normal(a, b, c, n);
        double fim = now_seconds();

        double soma_normal = checksum(c, n);
        sink = soma_normal;

        printf("multiplicacao,%d,%s,normal,0,%d,%.6f,%.2f\n",
               n, OPT_LEVEL, r, (fim - inicio) * 1000.0, soma_normal);

        zerar_matriz(c, n);

        inicio = now_seconds();
        multiplicar_blocos(a, b, c, n, bloco);
        fim = now_seconds();

        double soma_blocos = checksum(c, n);
        sink = soma_blocos;

        printf("multiplicacao,%d,%s,blocos,%d,%d,%.6f,%.2f\n",
               n, OPT_LEVEL, bloco, r, (fim - inicio) * 1000.0, soma_blocos);
    }

    free(a);
    free(b);
    free(c);
}

int main() {
    int tamanhos[] = {128, 256, 512};
    int quantidade_tamanhos = sizeof(tamanhos) / sizeof(tamanhos[0]);

    int repeticoes = 10;
    int bloco = 32;

    printf("experimento,tamanho,otimizacao,algoritmo,bloco,repeticao,tempo_ms,checksum\n");

    for (int i = 0; i < quantidade_tamanhos; i++) {
        executar_teste(tamanhos[i], repeticoes, bloco);
    }

    return 0;
}