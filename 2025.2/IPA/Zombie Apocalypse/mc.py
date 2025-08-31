import numpy as np
import matplotlib.pyplot as plt
from random import choices, randint, random

# Parâmetros
alpha = 0.15  # probabilidade de nascimento
beta = 0.10   # probabilidade de morte
gamma = 0.50  # força zumbi (infecção por confronto)
delta = 0.60  # força humana (matar zumbi)
rho   = 0.10  # infecção pós-morte

# População inicial
N0 = 100
p0 = 0.75  # proporção inicial de humanos
pop = ['L'] * int(p0 * N0) + ['Z'] * int((1 - p0) * N0)
D = 0

# Simulação
T = 3_000  # número de turnos
L_hist, Z_hist, D_hist = [], [], []

for t in range(T):
    L = pop.count('L')
    Z = pop.count('Z')
    N = L + Z

    if L == 0 or Z == 0:
        print('L OU Z IGUAL A ZERO') # Substituir por st.error() no gui
        break

    # Etapa 1: Interação
    i1, i2 = randint(0, N - 1), randint(0, N - 1)
    if i1 != i2:
        a, b = pop[i1], pop[i2]

        if {'L', 'Z'} == {a, b}:
            if a == 'L':
                l_idx, z_idx = i1, i2
            else:
                l_idx, z_idx = i2, i1
            
            # Probabilidade de sucesso
            if random() < delta:
                pop.pop(z_idx)
            elif random() < gamma:
                pop[l_idx] = 'Z'
                D += 1
    
    # Etapa 2: Nascimento
    if L > 0 and random() < alpha:
        pop.append('L')
    
    # Etapa 3: Morte Natural
    if L > 0 and random() < beta:
        idx = choices([i for i, v in enumerate(pop) if v == 'L'])[0]

        if random() < rho:
            pop[idx] = 'Z'
        else:
            pop.pop(idx)
    
    # Armazena histórico
    L_hist.append(pop.count('L'))
    Z_hist.append(pop.count('Z'))
    D_hist.append(D)

plt.figure(figsize=(10,6))
plt.plot(L_hist, label='Humanos (L)')
plt.plot(Z_hist, label='Zumbis (Z)')
plt.plot(D_hist, label='Mortos (D)')
plt.xlabel("Tempo (turnos)")
plt.ylabel("População")
plt.title("Modelo Zumbi - Simulação Monte Carlo")
plt.legend()
plt.show()
