import matplotlib.pyplot as plt
from statistics import mean


# Dados de maior erro
x = [0.5, 1, 1.5, 4.6, 15] # Altura (m)
y = [15.023, 13.149, 12.087, 15.557, 13.157] # Aceleração gravitacional (m/s²)
y_err = [2.17, 2.17, 2.17, 2.17, 2.17]  # Incertezas associadas à gravidade

# Plota os dados de maior erro
plt.errorbar(
    x, y, yerr=y_err,
    fmt='o',  # Formato do marcador
    markerfacecolor='black',  # Cor interna do marcador
    markeredgecolor='black',  # Cor da borda do marcador
    ecolor='black',            # Cor das barras de erro
    capsize=3                 # Tamanho das extremidades das barras de erro
)

# Plota em destaque a melhor aproximação para a aceleração gravitacional
best_approx_x = [0.56775]
best_approx_y = [9.54]
best_approx_err = [2.17]
plt.errorbar(
    best_approx_x, best_approx_y, yerr=best_approx_err,
    fmt='o',    # Formato do marcador
    markerfacecolor='red',  # Cor interna do marcador
    markeredgecolor='red',  # Cor da borda do marcador
    ecolor='black', # Cor das barras de erro
    capsize=3,  # Tamanho das extremidades das barras de erro
    label='Melhor aproximação'  #Legenda
    )

#Plota em destaque o ponto com média global de altura e aceleração gravitacional
h_global_mean = [mean([0.5, 0.56775, 1, 1.5, 4.6, 15])]
g_global_mean = [mean([15.023, 9.54, 13.149, 12.087, 15.557, 13.157])]
global_err = [2.17]
plt.errorbar(
    h_global_mean, g_global_mean, yerr=global_err,
    fmt='o',    # Formato do marcador
    markerfacecolor='blue', # Cor interna do marcador
    markeredgecolor='blue', # Cor da borda do marcador
    ecolor='black', # Cor das barras de erro
    capsize=3,  # Tamanho das extremidades das barras de erro
    label='Média global'    # Legenda
    )

# Configurações do gráfico
plt.xlabel('Altura (m)')
plt.ylabel('Aceleração Gravitacional (m/s²)')
plt.title('Medidas e Incertezas na Relação Altura x Aceleração Gravitacional')
plt.legend()
plt.grid(True)
plt.show()
