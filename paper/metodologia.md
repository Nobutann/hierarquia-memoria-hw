# Metodologia

Este trabalho foi conduzido por meio de uma abordagem experimental, com o objetivo de avaliar o impacto da hierarquia de memória e das otimizações de compilador no desempenho de algoritmos matriciais implementados em linguagem C.

## Ambiente experimental

Os experimentos foram executados em um computador com arquitetura x86_64, equipado com processador 13th Gen Intel(R) Core(TM) i5-13420H. O processador possui 8 núcleos físicos e 12 CPUs lógicas, com frequência máxima de 4,6 GHz. A hierarquia de cache informada pelo sistema inclui 320 KiB de cache L1 de dados, 384 KiB de cache L1 de instruções, 7 MiB de cache L2 e 12 MiB de cache L3.

O ambiente utilizou sistema operacional Linux, kernel 7.0.11-arch1-1, com aproximadamente 7,5 GiB de memória RAM disponível no sistema. Os programas foram compilados com GCC 16.1.1, utilizando os níveis de otimização `-O0`, `-O2` e `-O3`. A análise estatística dos resultados foi realizada com Python 3.14.5, e as medições relacionadas ao comportamento de cache foram feitas com Valgrind/Cachegrind 3.25.1.

## Experimento 1: padrão de acesso à memória

O primeiro grupo de experimentos avaliou o impacto do padrão de acesso à memória em operações de soma sobre matrizes. Foram comparados dois padrões: acesso por linha e acesso por coluna.

No acesso por linha, os elementos da matriz são percorridos de forma sequencial dentro de cada linha. No acesso por coluna, a ordem dos laços é invertida, fazendo com que elementos de linhas diferentes sejam acessados sucessivamente. Como matrizes em C são armazenadas em ordem contígua por linha, espera-se que o acesso por linha explore melhor a localidade espacial.

Foram utilizadas matrizes de tamanhos 512x512, 1024x1024, 2048x2048 e 4096x4096. Cada configuração foi executada 30 vezes para cada nível de otimização do compilador (`-O0`, `-O2` e `-O3`). Na etapa de análise, as 5 primeiras repetições foram descartadas com o objetivo de reduzir efeitos iniciais de aquecimento e variações transitórias do ambiente de execução.

O tempo de execução foi medido no próprio programa, utilizando uma função baseada em `clock_gettime` com `CLOCK_MONOTONIC`. Os resultados foram armazenados em arquivos CSV contendo o tamanho da matriz, o nível de otimização, o tipo de acesso, a repetição, o tempo em milissegundos e a soma calculada.

## Experimento 2: multiplicação de matrizes

O segundo grupo de experimentos avaliou o desempenho da multiplicação de matrizes em duas versões: uma implementação tradicional e uma implementação com blocagem.

A implementação tradicional utiliza três laços aninhados para calcular cada elemento da matriz resultante. Já a versão com blocagem divide o processamento em blocos menores, com o objetivo de favorecer a reutilização de dados enquanto eles ainda estão em níveis mais rápidos da hierarquia de memória.

Foram utilizadas matrizes de tamanhos 128x128, 256x256 e 512x512. Cada configuração foi executada 10 vezes para cada nível de otimização do compilador (`-O0`, `-O2` e `-O3`). Na etapa de análise, as 2 primeiras repetições foram descartadas. A versão com blocagem utilizou tamanho de bloco igual a 32.

Assim como no primeiro experimento, o tempo de execução foi medido com `clock_gettime` e os resultados foram armazenados em arquivos CSV. Para validar que as versões calculavam o mesmo resultado, foi utilizado um valor de verificação baseado na soma dos elementos da matriz resultante, denominado `checksum`.

## Análise estatística dos resultados

Os dados coletados foram analisados com scripts em Python, utilizando as bibliotecas Pandas e Matplotlib. Para cada configuração experimental, foram calculadas métricas estatísticas como média, mediana, desvio padrão, valor mínimo, valor máximo e quantidade de medições consideradas.

No experimento de acesso à memória, foi calculada a razão entre o tempo médio do acesso por coluna e o tempo médio do acesso por linha. Essa razão indica quantas vezes o acesso por coluna foi mais lento do que o acesso por linha.

No experimento de multiplicação de matrizes, foi calculado o speedup da versão com blocagem em relação à versão tradicional. O speedup foi obtido pela razão entre o tempo médio da multiplicação tradicional e o tempo médio da multiplicação com blocagem.

## Análise com Cachegrind

Além da medição de tempo de execução, foram realizadas análises com a ferramenta Cachegrind, do Valgrind, com o objetivo de observar o comportamento da cache nos algoritmos avaliados.

Para o primeiro experimento, foram comparados os acessos por linha e por coluna em uma matriz 2048x2048, utilizando compilação com `-O2`. Para o segundo experimento, foram comparadas a multiplicação tradicional e a multiplicação com blocagem em matrizes 512x512, também com compilação `-O2` e tamanho de bloco igual a 32.

As métricas observadas incluíram referências a dados (`D refs`), falhas na cache L1 de dados (`D1 misses`) e falhas na última cache de dados (`LLd misses`). Essas informações foram utilizadas para relacionar os tempos de execução observados com o comportamento da hierarquia de memória.

## Organização dos artefatos

O repositório do projeto foi organizado em pastas específicas para código-fonte, dados, gráficos, scripts de análise e rascunhos do artigo. Os códigos em C foram armazenados em `src/`, os dados coletados em `data/`, os gráficos gerados em `plots/`, os scripts de análise em `scripts/` e os rascunhos textuais em `paper/`.

Essa organização permite a reprodução dos experimentos e facilita a conexão entre implementação, coleta de dados, análise estatística e escrita científica.
