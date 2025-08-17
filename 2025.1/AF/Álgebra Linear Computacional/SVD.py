import numpy as np
from sklearn.decomposition import TruncatedSVD

# Matriz de avaliações com valores ausentes preenchidos com 0
R = np.array([
    [5, 3, 0, 0],
    [0, 5, 4, 0],
    [2, 0, 0, 3]
])

# SVD truncado com k componentes latentes
svd = TruncatedSVD(n_components=2)
U_k = svd.fit_transform(R)
Sigma_k = svd.singular_values_
V_k = svd.components_

# Reconstrução aproximada da matriz original
R_hat = U_k @ np.diag(Sigma_k) @ V_k
print(np.round(R_hat, 2))  # valores previstos
