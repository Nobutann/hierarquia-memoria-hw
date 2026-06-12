#include <stdio.h>
#include <stdlib.h>
#include <string.h>

volatile double sink = 0.0;

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
        for (int kk = 0; kk < n; kk += bloco) {
            for (int jj = 0; jj < n; jj += bloco) {

                int i_max = min_int(ii + bloco, n);
                int k_max = min_int(kk + bloco, n);
                int j_max = min_int(jj + bloco, n);

                for (int i = ii; i < i_max; i++) {
                    for (int k = kk; k < k_max; k++) {
                        double a_ik = a[i * n + k];

                        for (int j = jj; j < j_max; j++) {
                            c[i * n + j] += a_ik * b[k * n + j];
                        }
                    }
                }
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Uso: %s <tamanho> <normal|blocos> <bloco>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    char *modo = argv[2];
    int bloco = atoi(argv[3]);

    double *a = criar_matriz(n);
    double *b = criar_matriz(n);
    double *c = criar_matriz(n);

    inicializar_matriz(a, n);
    inicializar_matriz(b, n);
    zerar_matriz(c, n);

    if (strcmp(modo, "normal") == 0) {
        multiplicar_normal(a, b, c, n);
    } else if (strcmp(modo, "blocos") == 0) {
        multiplicar_blocos(a, b, c, n, bloco);
    } else {
        fprintf(stderr, "Modo invalido. Use normal ou blocos.\n");
        free(a);
        free(b);
        free(c);
        return 1;
    }

    double soma = checksum(c, n);
    sink = soma;

    printf("tamanho=%d modo=%s bloco=%d checksum=%.2f\n", n, modo, bloco, soma);

    free(a);
    free(b);
    free(c);

    return 0;
}