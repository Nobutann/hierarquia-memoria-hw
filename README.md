# Avaliação experimental do impacto da hierarquia de memória e das otimizações de compilador no desempenho de algoritmos matriciais em C

## Problema

Algoritmos matriciais podem apresentar desempenhos diferentes não apenas pela quantidade de operações realizadas, mas também pela forma como acessam os dados na memória. Em arquiteturas modernas, a hierarquia de memória e o comportamento da cache influenciam diretamente o tempo de execução dos programas.

## Pergunta de pesquisa

Como a hierarquia de memória e os níveis de otimização do compilador influenciam o desempenho de algoritmos matriciais implementados em C?

## Hipótese

Algoritmos que exploram melhor a localidade de referência tendem a apresentar melhor desempenho, especialmente quando combinados com otimizações de compilador.

## Objetivo geral

Avaliar experimentalmente o impacto da hierarquia de memória e das otimizações de compilador no desempenho de algoritmos matriciais implementados em C.

## Objetivos específicos

1. Implementar algoritmos matriciais em C com diferentes padrões de acesso à memória.
2. Comparar o desempenho de acessos por linha e por coluna.
3. Avaliar o impacto de diferentes tamanhos de matriz.
4. Comparar versões compiladas com diferentes níveis de otimização, como `-O0`, `-O2` e `-O3`.
5. Analisar os resultados com base nos conceitos de cache, localidade de referência e hierarquia de memória.