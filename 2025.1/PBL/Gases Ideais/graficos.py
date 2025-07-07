import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from statistics import stdev, linear_regression


#------------------------------ TRATAMENTO GERAL DOS DADOS
file_name = ['medidas.txt'] # Arquivo com os dados brutos

# Recebem os dados brutos
T = []
P = []

# Leitura dos dados brutos
for name in file_name:
    with open(f'{name}', 'r') as file:
        for line in file:
            t, p = line.strip().split(',')
            T.append(float(t))
            P.append(float(p))

# Cálculo de cada média
quintas_T = [(T[i:i+5]) for i in range(0, len(T), 5)]
quintas_P = [(P[i:i+5]) for i in range(0, len(P), 5)]

medias_T = [sum(i)/5 for i in quintas_T]
medias_P = [sum(i)/5 for i in quintas_P]

# Desvio associado à média de cada quinta
desvio_T = [stdev(i) for i in quintas_T]
desvio_P = [stdev(i) for i in quintas_P]


#------------------------------ AQUECIMENTO
T_AQ = [] # Recebe os dados brutos apenas de aquecimento (ΔT > 0)

for i in range(len(T)):
    t = T[i]
    T_AQ.append(t)
    if t == max(T):
        if i + 1 < len(T) and T[i + 1] < max(T):
            break

medias_T_AQ = [sum(i)/5 for i in [(T_AQ[i:i+5]) for i in range(0, len(T_AQ), 5)]] # Cálculo de cada média
desvio_T_AQ = [stdev(i) for i in [(T_AQ[i:i+5]) for i in range(0, len(T_AQ), 5)]] # Desvio associado à média de cada quinta no intervalo de aquecimento


#------------------------------ RESFRIAMENTO
T_RF = T[len(T_AQ):] # Recebe os dados brutos apenas de resfriamento (ΔT < 0)

medias_T_RF = [sum(i)/5 for i in [(T_RF[i:i+5]) for i in range(0, len(T_RF), 5)]] # Cálculo de cada média
desvio_T_RF = [stdev(i) for i in [(T_RF[i:i+5]) for i in range(0, len(T_RF), 5)]] # Desvio associado à média de cada quinta no intervalo de resfriamento


#------------------------------ PRESSÃO DE AQUECIMENTO
P_AQ = P[:len(T_AQ)] # Recebe os dados brutos apenas da pressão durante o aquecimento
medias_P_AQ = [sum(i)/5 for i in [(P_AQ[i:i+5]) for i in range(0, len(P_AQ), 5)]] # Cálculo de cada média
desvio_P_AQ = [stdev(i) for i in [(P_AQ[i:i+5]) for i in range(0, len(P_AQ), 5)]] # Desvio associado à média de cada quinta no intervalo de aquecimento


#------------------------------ PRESSÃO DE RESFRIAMENTO
P_RF = P[len(T_AQ):] # Recebe os dados brutos apenas da pressão no resfriamento
medias_P_RF = [sum(i)/5 for i in [(P_RF[i:i+5]) for i in range(0, len(T_RF), 5)]] # Cálculo de cada média
desvio_P_RF = [stdev(i) for i in [(P_RF[i:i+5]) for i in range(0, len(T_RF), 5)]] # Desvio associado à média de cada quinta no intervalo de resfriamento

#------------------------------ REGRESSÕES LINEARES
# Geral
slope_T,  intercept_T = linear_regression(T, P)
REG_T = [slope_T*x + intercept_T for x in T]

# Aquecimento
slope_T_AQ, intercept_T_AQ = linear_regression(T_AQ, P_AQ)
REG_AQ = [slope_T_AQ*x + intercept_T_AQ for x in T_AQ]

# Resfriamento
slope_T_RF, intercept_T_RF = linear_regression(T_RF, P_RF)
REG_RF = [slope_T_RF*x + intercept_T_RF for x in T_RF]


#------------------------------ PLOTAGENS (T X P)
# Configurações gerais das plotagens

# Ativando a notação científica no eixo x
fig, ax = plt.subplots()
formatter = ScalarFormatter(useMathText=True) # Permite usar LaTex
formatter.set_scientific(True)
formatter.set_powerlimits((-3, 3))  # Define quando usar notação científica
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
# Demais configurações
plt.xlabel("Temperatura (° C)")
plt.ylabel("Pressão (Pa)")
plt.grid(True)
plt.tight_layout()


# 1. Gráfico com TODOS os dados contínuos
ax.plot(T, P, color='black')
plt.title('Relação Geral - Temperatura x Pressão')
plt.show()

# 2. Gráfico com TODOS os dados scatter + desvio
"""
fig, ax = plt.subplots()
ax.errorbar(
    medias_T,
    medias_P,
    desvio_P,
    desvio_T,
    fmt='o',
    ms=0.5,
    color='black'
)
plt.plot(T, REG_T)
plt.title('Relação Geral - Temperatura x Pressão')
plt.show()

# 3. Gráfico AQ/REF com dados contínuos por cor
fig, ax = plt.subplots()
ax.plot(T_AQ, P_AQ, color='red', label='Aquecimento')
ax.plot(T_RF, P_RF, color='blue', label='Resfriamento')
plt.title('Relações Aquecimento/Resfriamento - Temperatura x Pressão')
plt.legend()
plt.show()
"""

# 4. Gráfico AQ/REF com dados scatter + desvio
"""
fig, ax = plt.subplots()
ax.errorbar(
    medias_T_AQ,
    medias_P_AQ,
    desvio_P_AQ,
    desvio_T_AQ,
    fmt='o',
    ms=0.5,
    color='red',
    label='Aquecimento'
)
ax.errorbar(
    medias_T_RF,
    medias_P_RF,
    desvio_P_RF,
    desvio_P_RF,
    fmt='o',
    ms=0.5,
    color='blue',
    label='Resfriamento'
)
plt.title('Relações Aquecimento/Resfriamento - Temperatura x Pressão')
plt.plot(T, REG_T, color='black', label='Regressão Linear')
plt.legend()
plt.show()

# 5. Gráfico AQ com dados contínuos
fig, ax = plt.subplots()
ax.plot(medias_T_AQ, medias_P_AQ, color='red')
plt.title('Relação de Aquecimento - Temperatura x Pressão')
plt.show()
"""

# 6. Gráfico AQ com dados scatter + desvio
"""
fig, ax = plt.subplots()
ax.errorbar(
    medias_T_AQ,
    medias_P_AQ,
    desvio_P_AQ,
    desvio_T_AQ,
    fmt='o',
    ms=0.5,
    color='red',
    label='Experimento'
)
plt.plot(T_AQ, REG_AQ, color='black', label='Regressão Linear')
plt.title('Relação de Aquecimento - Temperatura x Pressão')
plt.legend()
plt.show()
"""

# 7. Gráfico REF com dados
"""
fig, ax = plt.subplots()
ax.plot(T_RF, P_RF, color='blue')
plt.title('Relação de Resfriamento - Temperatura x Pressão')
plt.show()
"""

# 8. Gráfico REF com dados scatter + desvio
"""
fig, ax = plt.subplots()
ax.errorbar(
    medias_T_RF,
    medias_P_RF,
    desvio_P_RF,
    desvio_P_RF,
    fmt='o',
    ms=0.5,
    color='blue',
    label='Experimento'    
)
plt.plot(T_RF, REG_RF, color='black', label='Regressão Linear')
plt.title('Relação de Resfriamento - Temperatura x Pressão')
plt.legend()
plt.show()
"""
