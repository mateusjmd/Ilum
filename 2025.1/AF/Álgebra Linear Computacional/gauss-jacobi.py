# Algoritmo Iterativo de Gauss-Jacobi com Erro Relativo

"""
A = [
    [15, -1,  0,  0,  0,  2,  0,  0,  1,  0],
    [-1, 16, -2,  0,  0,  0,  3,  0,  0,  1],
    [ 0, -2, 17, -3,  0,  0,  0,  4,  0,  0],
    [ 0,  0, -3, 18, -4,  0,  0,  0,  5,  0],
    [ 0,  0,  0, -4, 19, -5,  0,  0,  0,  6],
    [ 2,  0,  0,  0, -5, 20, -6,  0,  0,  0],
    [ 0,  3,  0,  0,  0, -6, 21, -7,  0,  0],
    [ 0,  0,  4,  0,  0,  0, -7, 22, -8,  0],
    [ 1,  0,  0,  5,  0,  0,  0, -8, 23, -9],
    [ 0,  1,  0,  0,  6,  0,  0,  0, -9, 24]
]
X = [0 for _ in range(10)]
b = [15, 23, 14, -6, 19, 24, 31, 12, -5, 21]
E = 1e-3
"""

A = [[10, 1, 2], [1, 5, 1], [2, 3, 10]]
X = [3, 2, 5] # Vetor contendo as soluções arbitrárias iniciais
b = [1, 2, -1] # Vetor contendo as igualdades das equações do sistema linear
E = 1e-7 # Tolerância 
n = len(A)

# Validação da matriz A
for i in range(n):
    # Verifica a presença de elementos nulos na diagonal principal
    if A[i][i] == 0:
            raise ValueError(f'Elemento nulo na diagonal principal: a[{i + 1}][{i + 1}]')

    # Critério das Linhas
    a_k = sum(abs(A[i][j]) for j in range(n) if i != j) / abs(A[i][i])

    if a_k > 1:
        raise ValueError(f'Critério das Linhas não satisfeito. Erro na linha: {i}')

x_0 = X.copy()
x_1 = [] # Novo vetor provisório a ser avaliado pelo critério de parada
while True:
    for i in range(n):
        x_i = 1/A[i][i] * (b[i] - sum(A[i][j] * x_0[j] for j in range(n) if i != j)) # Cálculo de cada x_i, já isolado
        x_1.append(x_i)

    # Critério de parada
    x_diff = [abs(x_1[_] - x_0[_]) for _ in range(n)] # Vetor diferença
    
    # Erro relativo / O uso de 1e-10 evita divisões próximas de zero
    Er = max(abs(x_1[i] - x_0[i]) / max(abs(x_1[i]), 1e-10) for i in range(n))
    # Er = max(x_diff) -> Erro absoluto

    if Er > E:
        x_0 = x_1.copy() # Substitui para usar x_1 como o x_0 da próxima iteração
        x_1.clear() # Limpa os elementos do vetor
    else:
        break # Sai do loop


# Exibição das soluções estimadas
solucoes = x_0.copy()

print('_' * 10)
print('SOLUÇÕES ESTIMADAS')
for pos, solucao in enumerate(solucoes):
    print(f'X{pos + 1} = {solucao:.6f}')


# Verificação dos resultados
print('_' * 10)
print('Verificação das equações com as soluções estimadas')
for i in range(n):
    linha = ''
    resultado = 0
    for j in range(n):
        a = A[i][j]
        x = solucoes[j]
        resultado += a * x
        linha += f'{a}*({x:.5f})'
        if j < n - 1:
            linha += ' + '
    linha += f' ≈ {resultado:.5f}'
    print(linha)
