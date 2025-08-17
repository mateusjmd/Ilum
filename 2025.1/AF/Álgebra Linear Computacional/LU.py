# Algoritmo de Decomposição LU com Pivoteamento Parcial

def decomp_Lu(P, L, U, b):
    """
    Calcula as soluções do sistema linear utilizando o método de decomposição LU
    
    PARÂMETROS
    
    P: Matriz de permutação

    L: Matriz triangular inferior (lower)

    U: Matriz triangular superior (upper)

    b: Vetor com os coeficientes das igualdades do sistema linear

    RETORNO

    x: Vetor contendo as soluções do sistema linear
    """

    n = len(b)

    # Multiplicação de matriz P por vetor b
    Pb = [sum(P[i][j] * b[j] for j in range(n)) for i in range(n)]


    # Resolução de Ly = Pb (Substituição Direta)
    y = [0.0] * n
    for i in range(n):
        y[i] = Pb[i] - sum(L[i][j] * y[j] for j in range(i))

    # Resolução de Ux = y (Substituição Retroativa)
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x


a = [[4, 3, -1], [2, 1, 1], [-1, 3, 4]] # Lista de listas -> Matriz com os coeficientes da matriz Anxn
b = [1, 0, 2] # Lista do vetor bnx1, contendo os valores de cada equação do sistema
n = len(a) # Ordem da matriz A -> Por ser uma matriz quadrada, seu length é igual à sua ordem
A = [linha[:] for linha in a] # Cópia da matriz dos coeficientes "a"
L = [[0] * n for _ in range(n)] # Inicializa L como uma matriz nula
U = [[0] * n for _ in range(n)] # Inicializa U como uma matriz nula
P = [[float(i == j) for j in range(n)] for i in range(n)] # Inicializa P como uma matriz identidade

for k in range(n):    
    # PIVOTEAMENTO PARCIAL LU
    indice_pivo = max(range(k, n), key=lambda i: abs(A[i][k]))

    # Verifica a singularidade da matriz A
    if A[indice_pivo][k] == 0:
        raise ZeroDivisionError('Matriz singular identificada! S.P.I ou S.I.')

    # Troca de linhas em A e P
    if indice_pivo != k:
        A[k], A[indice_pivo] = A[indice_pivo], A[k]
        P[k], P[indice_pivo] = P[indice_pivo], P[k]
        
        # Troca de linhas em L apenas até a coluna k
        if k > 0:
            L[k][:k], L[indice_pivo][:k] = L[indice_pivo][:k], L[k][:k]

    # Diagonal de L
    L[k][k] = 1.0

    # Fórmula geral dos elementos de U
    for j in range(k, n):
        U[k][j] = A[k][j] - sum(L[k][s] * U[s][j] for s in range(k))

    for i in range(k + 1, n):
        L[i][k] = (A[i][k] - sum(L[i][s] * U[s][k] for s in range(k))) / U[k][k]

print(decomp_Lu(P, L, U, b))
