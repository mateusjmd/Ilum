# Difração de LASER

Esse diretório destina-se aos códigos desenvolvidos durante a prática de laboratório cujo objetivo era efetuar uma estimativa do diâmetro de dois fios de cabelo a partir da difração de um LASER em seu entorno, utilizando da variação de distância entre um anteparo e a amostra de cabelo.

O script `grafico.py` realiza a visualização dos diferentes comprimentos da onda difratada associados à mudança da distância entre o anteparo e o fio de cabelo.

O arquivo `regressao_linear.py` contém as estimativas das duas amostras de fio de cabelo utilizadas, a partir da variação observada em cada caso, usando o modelo de regressão linear do [`scikit-learn`](https://scikit-learn.org/stable/), a fim de compará-las com as medidas obtidas utilizando microscopia óptica.