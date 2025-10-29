# Tratamento e Visualização de Dados - Raman

Este repositório contém os *scripts* utilizados para o pré-processamento, tratamento e visualização de espectros Raman.

As rotinas foram implementadas em Python (3.12.7) dentro de um ambiente *Jupyter Notebook*, com foco na limpeza, normalização, correção de linha de base (*baseline*) e análise gráfica dos dados espectroscópicos.

> ### Como Usar
Para executar o código, substitua o caminho dos arquivos no parâmetro `file_path` (único caminho) ou `file_paths` (sequência de caminhos) pelas localizações correspondentes aos seus dados de espectroscopia Raman.

Exemplo:
```python
raman_plot(
           file_path='C://Users/...',
           sample_name='NOME_DA_AMOSTRA',
           method='max')
```

Então, o espectro é exibido automaticamente em duas versões: uma estática (Matplotlib) e outra interativa (Plotly).

> ### Tecnologias Utilizadas
As principais bibliotecas empregadas foram:

| Biblioteca     | Versão | Função Principal                                |
| -------------- | ------ | ----------------------------------------------- |
| **Pandas**     | 2.3.1  | Manipulação e organização de dados              |
| **NumPy**      | 2.3.2  | Operações numéricas e vetoriais                 |
| **SciPy**      | 1.15.3 | Correção de linha de base e funções matemáticas |
| **Matplotlib** | 3.10.3 | Visualização estática dos espectros             |
| **Plotly**     | 6.2.0  | Visualizações interativas e comparativas        |

# Referências

A função de correção de linha de base baseia-se em:

    EILERS, P. H. C.; BOELENS, H. F. M. Baseline correction with asymmetric least squares smoothing. Leiden University Medical Centre Report, 2005.

# Como Citar
MENDES, Mateus de Jesus. Raman_plot.ipynb: Tratamento e Visualização de Dados - Raman. [recurso eletrônico]. Campinas: Ilum – Escola de Ciência, 2025. Disponível em: https://github.com/mateusjmd/Ilum/tree/main/2025.2/LA1/Raman. Acesso em: 29 out. 2025.