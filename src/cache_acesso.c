#define _POSIX_C_SOURCE 199309L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

volatile double sink = 0.0;

double *criar_matriz(int n) {
    double *matriz = malloc((size_t)n * n * sizeof(double));

    if (matriz == NULL) {
        fprintf(stderr, "Erro ao alocar matriz %dx%d\n", n, n);
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

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s <tamanho> <linha|coluna>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    char *modo = argv[2];

    double *matriz = criar_matriz(n);
    double soma = 0.0;

    if (strcmp(modo, "linha") == 0) {
        soma = somar_por_linha(matriz, n);
    } else if (strcmp(modo, "coluna") == 0) {
        soma = somar_por_coluna(matriz, n);
    } else {
        fprintf(stderr, "Modo invalido. Use linha ou coluna.\n");
        free(matriz);
        return 1;
    }

    sink = soma;

    printf("tamanho=%d modo=%s soma=%.2f\n", n, modo, soma);

    free(matriz);

    return 0;
}