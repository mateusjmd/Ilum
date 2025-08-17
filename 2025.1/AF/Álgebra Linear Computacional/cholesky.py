# Algoritmo da Decomposição de Cholesky
# A = G * Gt -> O algoritmo produz a matriz G

from math import sqrt
import numpy as np

# A = np.array([[16, -4, 12, -4], [-4, 2, -1, 1], [12, -1, 14, -2], [-4, 1, -2, 83]]) # Matriz dos coeficientes
A = np.array([[4, 2, -2],
              [2, 10, 4],
              [-2, 4, 9]], dtype=float)
n = len(A) # Ordem da matriz A
# x_real = np.array([1, 2, 3, 4]) # Inserir o conjunto solução real para testes do algoritmo
# b = A @ x_real
x = np.zeros(n) # Recebe as soluções do sistema linear
b = np.array([2, 6, 7], dtype=float) # Vetor com as igualdades iniciais do sistema linear
G = np.zeros((n, n)) # Matriz obtida da decomposição de Cholesky
y = np.zeros(n) # Vetor intermediário entre a substituição regressiva e a progressiva

# DECOMPOSIÇÃO DE CHOLESKY
for k in range(n):
    s = 0

    for j in range(k):
        s += G[k][j] ** 2
    
    r = A[k][k] - s

    G[k][k] = sqrt(r)

    for i in range(k + 1, n):
        s = 0

        for j in range(k):
            s += G[i][j] * G[k][j]
        
        G[i][k] = (A[i][k] - s) / G[k][k]

# SOLUÇÃO DO SISTEMA LINEAR
# G * y = b (Substituição Progressiva)
for i in range(n):
    s = sum(G[i][j] * y[j] for j in range(i))
    y[i] = (b[i] - s) / G[i][i]

# G.T * x = y (Substituição Regressiva)
for i in reversed(range(n)):
    s = sum(G.T[i][j] * x[j] for j in range(i + 1, n))
    x[i] = (y[i] -s) / G.T[i][i]

print("Solução estimada x =", x)
# print("Solução real x     =", x_real)