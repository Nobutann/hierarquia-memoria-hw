# Resultados preliminares da multiplicação de matrizes

O segundo experimento avaliou o desempenho da multiplicação de matrizes em duas versões: uma implementação tradicional e uma implementação com blocagem. O objetivo foi observar se a reorganização do algoritmo em blocos poderia melhorar o aproveitamento da hierarquia de memória, especialmente da cache.

Foram avaliadas matrizes de tamanhos 128x128, 256x256 e 512x512, compiladas com os níveis de otimização `-O0`, `-O2` e `-O3`. Para cada configuração, foram realizadas múltiplas execuções, sendo calculado o tempo médio após a remoção das primeiras repetições, utilizadas como aquecimento.

Os resultados indicam que a versão com blocagem apresentou desempenho superior à versão normal em todos os cenários avaliados. Para matrizes 128x128, o speedup variou entre aproximadamente 1,05x e 3,49x. Para matrizes 256x256, o speedup variou entre aproximadamente 1,01x e 2,83x. Já para matrizes 512x512, os ganhos foram mais expressivos: 1,32x com `-O0`, 5,39x com `-O2` e 11,20x com `-O3`.

Esses resultados sugerem que a blocagem melhora o aproveitamento da localidade de referência ao reorganizar os acessos às matrizes em subconjuntos menores. Essa estratégia favorece a reutilização de dados em níveis mais rápidos da hierarquia de memória, reduzindo o custo associado a acessos menos eficientes.

Também foi observado que os ganhos da blocagem foram mais expressivos quando combinados com os níveis de otimização `-O2` e `-O3`. Isso indica que otimizações de compilador podem potencializar os benefícios de algoritmos estruturados de forma mais favorável à hierarquia de memória.
