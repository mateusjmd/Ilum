# Espalhamento Rayleigh

## Introdução 

Esse diretório destina-se aos versionamento dos códigos desenvolvidos durante a prática de laboratório cujo objetivo era verificar o [Espalhamento Rayleigh](http://demonstracoes.fisica.ufmg.br/artigos/ver/107/18.-Espalhamento-da-luz) por meio da criação de um sistema coloidal, dada a adição de gotas de leite em um recipiente com água. A partir dessa experiência, utilizando um sensor RGB em um sistema com Arduino, observa-se o alto grau de dispersão da luz vermelha nesses sistemas, tal como ocorre na atmosfera, explicando o fato do céu ser azul.

### Espalhamentos & Espalhamento Rayleigh

`[Inserir a fundamentação teórica]`

## Tecnologias Utilizadas

As principais tecnologias utilizadas foram:
- Python
- Arduino
- Bibliotecas

## Códigos & Demais Arquivos

O script `grafico.py` realiza a visualização da variação da intensidade das luzes vermelha, verde e azul, com a adição de gotas de leite ao sistema, bem como apresenta a visualização dos mesmos dados normalizados.

O arquivo `medidas_gotas.txt` contém os dados obtidos do sensor RGB utilizado no Arduino, por meio da conexão serial, registrando o número total de gotas de leite adicionadas ao sistema e a intensidade, no sistema RGB, das luzes vermelha, verde e azul.
