# Resultados preliminares

O primeiro experimento avaliou o impacto do padrão de acesso à memória no desempenho de operações sobre matrizes em C. Foram comparados dois padrões: acesso por linha e acesso por coluna, considerando matrizes de tamanhos 512x512, 1024x1024, 2048x2048 e 4096x4096, compiladas com os níveis de otimização -O0, -O2 e -O3.

Os resultados indicam que o acesso por coluna apresentou tempo de execução superior ao acesso por linha em todos os cenários avaliados. A diferença tornou-se mais expressiva conforme o tamanho da matriz aumentou. Para matrizes 4096x4096, o acesso por coluna foi aproximadamente 6,30 vezes mais lento com -O0, 17,89 vezes mais lento com -O2 e 17,73 vezes mais lento com -O3.

Esse comportamento sugere que o acesso por linha explora melhor a localidade espacial da memória, uma vez que os elementos consecutivos de uma linha são armazenados de forma contígua em C. Por outro lado, o acesso por coluna percorre posições mais distantes na memória, reduzindo o aproveitamento da cache e aumentando o tempo de execução.

Também foi observado que os níveis de otimização do compilador reduziram significativamente o tempo de execução do acesso por linha, especialmente para matrizes maiores. Entretanto, mesmo com otimizações, o acesso por coluna permaneceu substancialmente mais lento, indicando que otimizações de compilador não eliminam completamente os efeitos negativos de padrões de acesso desfavoráveis à hierarquia de memória.