# Algoritmo de Eliminação Gaussiana com Pivoteamento Parcial

a = [[4, 3, -1], [2, 1, 1], [-1, 3, 4]] # Lista de listas -> Matriz com os coeficientes da matriz Anxn
b = [1, 0, 2] # Lista do vetor bnx1, contendo os valores de cada equação do sistema
n = len(a) # Ordem da matriz A -> Por ser uma matriz quadrada, seu length é igual à sua ordem
x = [0.0 for _ in range(len(b))] # Inicializa como uma lista de zeros e passa a receber as soluções do sistema

print(x)


for k in range(n):
    # PIVOTEAMENTO PARCIAL
    pivo = abs(a[k][k])
    indice_pivo = k

    for i in range(k + 1, n):
        if abs(a[i][k]) > pivo:
            pivo = abs(a[i][k])
            indice_pivo = i
    
    if pivo == 0:
            print('Matriz singular identificada! S.P.I ou S.I.')
            exit()

    if indice_pivo != k:
        for j in range(n):
            troca = a[k][j]
            a[k][j] = a[indice_pivo][j]
            a[indice_pivo][j] = troca
        
        troca = b[k]
        b[k] = b[indice_pivo]
        b[indice_pivo] = troca

    # ELIMINAÇÃO GAUSSIANA
    for i in range(k + 1, n):
        m = a[i][k] / a[k][k]
        b[i] -= m * b[k]
        a[i][k] = 0
        
        for j in range(k + 1, n):
            a[i][j] -= m * a[k][j]

# OUTPUT
x[n - 1] = b[n - 1] / a[n - 1][n - 1] # ???

for k in range(n - 2, -1, -1):
    s= 0

    for j in range(k + 1, n):
        s += a[k][j] * x[j]
    
    x[k] = (b[k] - s) / a[k][k]

print(x)
