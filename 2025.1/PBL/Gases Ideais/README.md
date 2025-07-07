# Gases Ideais

## Introdução 

Esse diretório destina-se ao versionamento dos códigos desenvolvidos durante a prática de laboratório cujo objetivo era verificar o comportamento termodinâmico dos gases atmosféricos em um sistema fechado submetido a aquecimento constante. A partir dessa experiência, utilizando um sensor BMP 280 em um sistema com Arduino, observa-se um processo termodinâmico irreversível, que respeita a [**Segunda Lei da Termodinâmica**7](), demonstrando que o ar atmosférico não pode ser rigorosamente tratado como um Gás Ideal.

### Termodinâmica dos Gases Ideais

`[Inserir a fundamentação teórica]`

## Tecnologias Utilizadas

As principais tecnologias utilizadas foram:
- Python
- Arduino
- Bibliotecas

## Códigos & Demais Arquivos

`codigo_bmp.ino`: Script em C++ utilizado no Arduino para o funcionamento do sensor BMP 280

`conexao_serial.py`: Script em Python para a captura dos dados transferidos via porta serial do Arduino para o computador

`graficos.py`: Visualizações diversas dos dados obtidos, incluindo regressões lineares que adequam-se às previsões teóricas para o comportamento termodinâmico de gases ideais

`medidas.txt`: Dados registrados pelo script `conexao_serial.py`

## Execução

`[Inserir a instruções para o uso dos códigos]`

