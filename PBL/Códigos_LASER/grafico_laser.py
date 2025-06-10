import pandas as pd
import matplotlib.pyplot as plt
from statistics import stdev

D = []# Distância anti-fenda - anteparo (m)
Ym = []# Distância entre o centro e o meio da franja (mm)

file_name = ['amostra_1.txt', 'amostra_2.txt']

for name in file_name:
    with open(f'{name}', 'r') as file:
        d_anteparo = []
        d_franja = []

        for line in file:
            d, ym = line.strip().split(',')
            d_anteparo.append(float(d))
            d_franja.append(float(ym))
        
        D.append(d_anteparo)
        Ym.append(d_franja)
        del d_anteparo, d_franja

m = 1 # Número do mínimo
λ = 637.8 # Comprimento de onda do LASER (nm)
a = [] # Diâmetro do fio de cabelo (antifenda) (µm)
for i in range(len(D)):
    diametros = []
    for d, ym in zip(D[i], Ym[i]):
        diametros.append((m*d*λ) / ym)
    a.append(diametros)

sigma = [stdev(diametro) for diametro in a]
desvios = [[s] * len(a[0]) for s in sigma]

# PLOTAGENS

# D x Ym
color = ['blue', 'red']

for i in range(len(D)):
    plt.plot(D[i], Ym[i], color=color[i], label=f'Amostra {i+1}')
plt.title('Variação da distância entre o centro e franja ($Y_m$) em função da distância anteparo-anti-fenda ($D$)')
plt.xlabel('Distância anteparo-anti-fenda $D$ (m)')
plt.ylabel('Distância do centro à franja $Y_m$ (mm)')
plt.grid(True)
plt.legend()
plt.show()

# D x a - Scatter & STDEV
color = ['blue', 'red']

for i in range(len(D)):
    plt.errorbar(D[i], Ym[i], yerr=desvios[i],
                fmt='o',
                label=f'Amostra {i + 1}',
                markerfacecolor=color[i],  # Cor interna do marcador
                markeredgecolor='black',  # Cor da borda do marcador
                ecolor='black',            # Cor das barras de erro
                capsize=3)             # Tamanho das extremidades das barras de erro)
plt.grid(True)
plt.title('Variação do diâmetro da anti-fenda ($a$) em função da distância anteparo-anti-fenda ($D$)')
plt.xlabel('Distância anteparo-anti-fenda $D$ (m)')
plt.ylabel('Diâmetro da anti-fenda $a$ (μm)')
plt.legend()
plt.show()
