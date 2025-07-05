from statistics import mean
from numpy import sqrt
from pandas import DataFrame


# Definição das funções
def aceleracao(h, t):
    """
    Calcula a aceleração gravitacional a partir da altura e do tempo de queda livre de um corpo.

    Argumentos:
    h: Altura (m)
    t: Tempo (s)
    """
    return round((2 * h) / t ** 2, 3)

def desvio(dados):
    """
    Calcula a média e o desvio padrão para os dados amostrais informados

    Argumentos
    dados: Lista ou tupla contendo os dados amostrais no formato int ou float
    """
    x_m = mean(dados) # Calcula a média
    N = len(dados) # Calcula a quantidade de amostras
    sum = 0 # Recebe o somatório

    # Realiza o somatório iterativo do quadrado da diferença entre cada dado e a média
    for x_i in dados:
        sum += (x_i - x_m)**2

    # Calcula o desvio padrão amostral
    sigma = sqrt(sum / (N - 1))

    return sigma

def incerteza(dados, desvio):
    """
    Calcula o valor da grandeza e sua incerteza, arredondando-os segundo o algarismo significativo

    Argumentos
    media: Média dos valores obtidos para a grandeza
    desvio: Desvio padrão da grandeza
    """

    media = mean(dados)

    if ('.1' in str(media) or '.2' in str(media)) or ('.1' in str(desvio) or '.2' in str(desvio)):
        # Retorna a média e incerteza com 2 algarismos significativos, caso a média ou o desvio iniciem as casas decimais com 0.1 ou 0.2
        return round(media, 2), round(desvio, 2)
    elif round(desvio, 2) == 0:
        print('ROUND(3)')
        return round(media, 3), round(desvio, 3)
    else:
        # Retorna a média e incerteza com 1 algarismo significativo, para qualquer outro caso
        return round(media, 1), round(desvio, 1)

def prop_erro(h, t, sigma_h, sigma_t):
    """
    Calcula a incerteza da gravidade, considerando a propagação de erros para as variáveis altura e tempo
    
    Argumentos
    h: Altura (m)
    t: Tempo (s)
    sigma_h: Desvio padrão da altura (m)
    sigma_t: Desvio padrão do tempo (s)
    """
    sigma_g = sqrt(((2/t**2) * sigma_h)**2 + ((4*h/t**3) * sigma_t)**2)

    return sigma_g


altura = [4.6, 4.63, 4.58, 4.6, 4.59, 4.61, 4.61, 4.59, 4.6, 4.57] # Alturas medidas em metros
media_altura = mean(altura) # Média aritmética das alturas
tempo = [0.73, 0.66, 0.60, 0.61, 0.66, 0.88, 0.88, 1, 0.98, 0.69] # Tempos medidos em segundos
media_tempo = mean(tempo) # Média aritmética dos tempos

gravidade = [] # Recebe o valor da gravidade para cada altura e tempo correspondentes
for i in zip(altura, tempo):
    gravidade.append(aceleracao(i[0], i[1]))
media_gravidade = mean(gravidade) # Média aritmética dos valores calculados para a gravidade

sigma_altura = desvio(altura) # Desvio padrão da altura
sigma_tempo = desvio(tempo) # Desvio padrão do tempo
sigma_gravidade = desvio(gravidade) # Desvio padrão da gravidade

incerteza_altura = incerteza(altura, sigma_altura) # Altura com média e incerteza ajustadas para o algarismo significativo
incerteza_tempo = incerteza(tempo, sigma_tempo) # Tempo com média e incerteza ajustadas para o algarismo significativo
incerteza_gravidade = incerteza(gravidade, sigma_gravidade) # Gravidade com média e incerteza ajustadas para o algarismo significativo

# Exibição dos resultados
resultado = {
    'Sigma_h': [sigma_altura],
    'Sigma_t': [sigma_tempo],
    'Sigma_g': [sigma_gravidade],
    'Incerteza_h': [f'{incerteza_altura[0]} ± {incerteza_altura[1]}'],
    'Incerteza_t': [f'{incerteza_tempo[0]} ± {incerteza_tempo[1]}'],
    'Incerteza_g': [f'{incerteza_gravidade[0]} ± {incerteza_gravidade[1]}'],
    'Prop_err_g': [prop_erro(media_altura, media_tempo, sigma_altura, sigma_tempo)]     
}
tabela = DataFrame(resultado)
print(tabela)
