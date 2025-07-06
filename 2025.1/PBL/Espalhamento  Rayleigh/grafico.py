import matplotlib.pyplot as plt
from desvio_padrao import desvio # Função desenvolvida por Mateus J. Mendes


def norma(dados):
    """
    Efetua a normalização dos dados informados

    Parâmetros:
    dados: lista ou array contendo os dados a serem normalizados

    Retorno:
    Lista com os respectivos dados normalizados
    """

    dados_normalizados = []

    for d in dados:
        dados_normalizados.append((d - min(dados)) / (max(dados) - min(dados)))
    
    print(dados_normalizados)

    return dados_normalizados


GT = [] # Número total de gotas adicionadas
R = [] # Todos os valores de R
G = [] # Todos os valores de G
B = [] # Todos os valores de B

file_name = ['medidas_gotas.txt'] # Arquivo com as medidas, seguindo a ordem GT,R,G,B

for name in file_name:
    with open(f'{name}', 'r') as file: # Abre o arquivo

        for line in file: # Lê linha por linha, de cima para baixo
            gt, r, g, b = list(line.strip().split(',')) # Armazena a informação de cada "coluna" em cada variável respectiva
            GT.append(float(gt)) # Armazena o valor da linha atualmente lida para a "coluna GT"
            R.append(float(r)) # Armazena o valor da linha atualmente lida para a "coluna R"
            G.append(float(g)) # Armazena o valor da linha atualmente lida para a "coluna G"
            B.append(float(b)) # Armazena o valor da linha atualmente lida para a "coluna B"

t_GT = GT[::3] # Valor de GT para cada triplicata de R, G e B
t_R = [list(R[3 * i : 3 * i + 3]) for i in range(14)]
t_G = [list(G[3 * i : 3 * i + 3]) for i in range(14)]
t_B = [list(B[3 * i : 3 * i + 3]) for i in range(14)]

m_R = [] # Médias das triplicatas de R
m_G = [] # Médias das triplicatas de G
m_B = [] # Médias das triplicatas de B

d_R = [] # Desvios das triplicatas de R
d_G = [] # Desvios das triplicatas de G
d_B = [] # Desvios das triplicatas de B


for d_r, d_g, d_b in zip(t_R, t_G, t_B):
    # Armazena as médias de cada triplicata
    m_R.append(desvio(d_r)[0])
    m_G.append(desvio(d_g)[0])
    m_B.append(desvio(d_b)[0])

    # Armazena os desvios de cada triplicata
    d_R.append(desvio(d_r)[1])
    d_G.append(desvio(d_g)[1])
    d_B.append(desvio(d_b)[1])


# Normalização dos dados de GT (eixo X), R, G e B (eixo Y)
norm_GT = norma(GT)
norm_R = norma(R)
norm_G = norma(G)
norm_B = norma(B)


for i in range(0, 14): # Plotagem ponto a ponto, com as barras de erro para R, G e B
    plt.errorbar(
        t_GT[i], m_R[i], yerr=d_R[i],
        fmt='o',    # Formato do marcador
        markerfacecolor='red',  # Cor interna do marcador
        markeredgecolor='red',  # Cor da borda do marcador
        ecolor='black', # Cor das barras de erro
        capsize=3,  # Tamanho das extremidades das barras de erro
        label='Espectro de Luz Vermelha' if i == 0 else ''  #Legenda
        )
    
    plt.errorbar(
        t_GT[i], m_G[i], yerr=d_G[i],
        fmt='o',    # Formato do marcador
        markerfacecolor='green',  # Cor interna do marcador
        markeredgecolor='green',  # Cor da borda do marcador
        ecolor='black', # Cor das barras de erro
        capsize=3,  # Tamanho das extremidades das barras de erro
        label='Espectro de Luz Verde' if i == 0 else ''  #Legenda
        )
    
    plt.errorbar(
        t_GT[i], m_B[i], yerr=d_B[i],
        fmt='o',    # Formato do marcador
        markerfacecolor='blue',  # Cor interna do marcador
        markeredgecolor='blue',  # Cor da borda do marcador
        ecolor='black', # Cor das barras de erro
        capsize=3,  # Tamanho das extremidades das barras de erro
        label='Espectro de Luz Azul' if i == 0 else ''  #Legenda
        )

# Plots dos gráficos contínuos para R, G e B
plt.plot(GT, R, '-', color='red', label='Espectro de Luz Vermelha')
plt.plot(GT, G, '-', color='green', label = 'Espectro de Luz Verde')
plt.plot(GT, B, ':', color='blue', label='Espectro de Luz Azul')


# Configuração da plotagem
plt.title('Espalhamento Rayleigh')
plt.xlabel('Número Total de Gotas (uni)')
plt.ylabel('Intensidade do Espectro (u.a.)')
plt.legend()
plt.xticks(range(0, 65, 5))
plt.yticks(range(210, 260, 5))
plt.grid(True)
plt.tight_layout()
plt.show()


# Plots das normalizações dos dados para R, G, e B
plt.plot(norm_GT, norm_R, color='red', label='Espectro de Luz Vermelha')
plt.plot(norm_GT, norm_G, '--', color='green', label='Espectro de Luz Verde')
plt.plot(norm_GT, norm_B, ':', color='blue', label='Espectro de Luz Azul')

plt.title(r'Normalização dos Dados ($\mathbb{R}^2$)')
plt.xlabel('Número Total de Gotas Normalizado (u.a.)')
plt.ylabel('Intensidade do Espectro Normalizada (u.a.)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()