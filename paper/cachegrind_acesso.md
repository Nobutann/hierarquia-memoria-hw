# Resultados preliminares com Cachegrind - acesso por linha e coluna

Foram realizadas medições com a ferramenta Cachegrind para comparar o comportamento de cache entre o acesso por linha e o acesso por coluna em uma matriz 2048x2048. O programa foi compilado com o nível de otimização `-O2`.

Os resultados indicaram que ambos os modos apresentaram quantidade semelhante de referências a dados (`D refs`), com aproximadamente 6,33 milhões de acessos. No entanto, a quantidade de falhas na cache L1 de dados (`D1 misses`) foi significativamente maior no acesso por coluna.

No acesso por linha, foram registradas 1.050.490 falhas na cache L1 de dados, com taxa de falha de 16,6%. Já no acesso por coluna, foram registradas 4.720.505 falhas, com taxa de falha de 74,5%. Dessa forma, o acesso por coluna apresentou aproximadamente 4,49 vezes mais falhas de cache L1 do que o acesso por linha.

Ao observar apenas as falhas associadas a leituras, a diferença é ainda mais expressiva. O acesso por linha apresentou 525.764 falhas de leitura, enquanto o acesso por coluna apresentou 4.195.779 falhas de leitura, valor aproximadamente 7,98 vezes maior.

Esses resultados reforçam a hipótese de que o padrão de acesso à memória influencia diretamente o desempenho de algoritmos matriciais. Como matrizes em C são armazenadas em ordem contígua por linha, o acesso sequencial por linha explora melhor a localidade espacial. Por outro lado, o acesso por coluna percorre posições mais distantes na memória, aumentando a taxa de falhas de cache e, consequentemente, o custo de acesso aos dados.
