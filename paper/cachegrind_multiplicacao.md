# Resultados preliminares com Cachegrind - multiplicação de matrizes

Foram realizadas medições com a ferramenta Cachegrind para comparar o comportamento de cache entre a multiplicação de matrizes tradicional e a multiplicação com blocagem. O experimento utilizou matrizes 512x512, compilação com `-O2` e tamanho de bloco igual a 32.

Na multiplicação tradicional, foram registradas 269.334.520 referências a dados (`D refs`) e 134.942.113 falhas na cache L1 de dados (`D1 misses`), com taxa de falha de 50,1%. Já na multiplicação com blocagem, foram registradas 408.043.318 referências a dados e 22.423.747 falhas na cache L1 de dados, com taxa de falha de 5,5%.

Embora a versão com blocagem tenha apresentado maior número total de referências a dados, ela reduziu significativamente a quantidade de falhas na cache L1. A redução foi de aproximadamente 6,02 vezes em relação à multiplicação tradicional. Esse resultado indica que a blocagem melhorou a localidade de referência, reduzindo a frequência com que os dados precisaram ser buscados fora da cache L1.

Os resultados do Cachegrind reforçam os resultados de tempo de execução obtidos anteriormente. Para matrizes 512x512, a versão com blocagem apresentou speedup de 5,39x com `-O2` e 11,20x com `-O3`. Assim, a análise sugere que a reorganização do algoritmo em blocos contribuiu para melhor aproveitamento da hierarquia de memória e para redução do tempo de execução.
