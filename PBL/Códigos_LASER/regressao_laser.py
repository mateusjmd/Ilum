import numpy as np
import matplotlib.pyplot as plt
from statistics import stdev
from sklearn.linear_model import LinearRegression


D = [] # Distância anti-fenda - anteparo (m)
Ym = [] # Distância entre o centro e o meio da franja (mm)

file_name = ['amostra_1.txt', 'amostra_2.txt']

for name in file_name:
    # Abre os arquivos com dados e os salva
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
desvios = [[s] * len(a[0]) for s in sigma] # Desvio padrão das medidas

# Constantes
m_ordem = 1
λ_nm = 637.8
λ_m = λ_nm * 1e-9

# Guarda valores para plotar
cores = ['blue', 'red']
labels = ['Amostra 1', 'Amostra 2']

# ------------------------------ REGRESSÃO LINEAR D X Ym ------------------------------
plt.figure(figsize=(8, 5))

for i in range(2):
    X = np.array(D[i]).reshape(-1, 1)
    y = np.array(Ym[i]) / 1e3 # Conversão para mimlímetros
    
    # Regressão linear
    model = LinearRegression().fit(X, y)
    k = model.coef_[0]
    
    # Diâmetro estimado
    a_m = (m_ordem * λ_m) / k
    a_um = a_m * 1e6  # micrômetros
    
    # Exibe o resultado
    print(f'{labels[i]}:')
    print(f'  Coeficiente angular (k): {k:.6e}')
    print(f'  Diâmetro estimado do fio de cabelo: {a_um:.2f} µm\n')
    
    # Plota os pontos e reta de regressão
    plt.scatter(X, y, color=cores[i], label=f'{labels[i]}')
    plt.plot(X, model.predict(X), linestyle='-', color=cores[i], label=f'Regressão Linear - {labels[i]}')

# Configurações do gráfico
plt.title("Regressão Linear De Cada Amostra")
plt.xlabel("Distância Do Anteparo (m)")
plt.ylabel("$Y_m$ (m)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------ REGRESSÃO LINEAR D X a ------------------------------
plt.figure(figsize=(8, 5))

for i in range(2):
    x = np.array(D[i])
    y = np.array(a[i])

    # Regressão linear apenas para visualização -> Essa regressão não possui "sentido físico real"
    model = LinearRegression().fit(x.reshape(-1, 1), y)
    y_pred = model.predict(x.reshape(-1, 1))

    # Plota os pontos com a regressão
    plt.scatter(x, y, color=cores[i], label=f'{labels[i]}')
    plt.plot(x, y_pred, linestyle='-', color=cores[i], label=f'Regressão Linear - {labels[i]}')

# Configurações do gráfico
plt.title("Diâmetro Estimado da Anti-fenda x Distância Do Anteparo")
plt.xlabel("Distância Do Anteparo (m)")
plt.ylabel("Diâmetro Estimado da Anti-fenda (µm)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
