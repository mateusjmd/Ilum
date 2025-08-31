import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parâmetros do modelo
alpha = 0.15 # Taxa de nascimento
beta = 0.10 # Taxa de morte natural
gamma = 0.005 # Taxa de infecção por encontros
delta = 0.006 # Taxa de destruição de zumbis
rho = 0.1 # Fração de mortos naturalmente que viram zumbis

def modelo_zumbi(t, y):
    """
    Resolve as equações diferenciais do modelo populacional

    Parâmetros:
        t: Tempo
        y: Sequência contendo a população humana, população de zumbis e a população de mortos

    Retorna:
        Lista contendo a solução da equação diferencial para L, Z e D, respectivamente
    """

    L, Z, D = y

    dLdt = ((alpha - beta) * L) - (gamma * L * Z)
    dZdt = (rho * beta * L) + ((gamma - delta) * L * Z)
    dDdt = (1 - rho) * beta * L + delta * L * Z

    return [dLdt, dZdt, dDdt]


L0 = 70
Z0 = 20
D0 = 0

t_span = (0, 1000)
t_eval = np.linspace(*t_span, 1000)
sol = solve_ivp(modelo_zumbi, t_span, [L0, Z0, D0], t_eval=t_eval)

plt.figure(figsize=(10, 6))
plt.plot(sol.t, sol.y[0], label='Humanos (L)')
plt.plot(sol.t, sol.y[1], label='Zumbis (Z)')
#plt.plot(sol.t, sol.y[2], label='Mortos (D)')
plt.title("Dinâmica Populacional - Modelo Zumbi")
plt.xlabel("Tempo")
plt.ylabel("População")
plt.legend()
plt.show()
