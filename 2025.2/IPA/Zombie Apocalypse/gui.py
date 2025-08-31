import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from tqdm import tqdm

st.set_page_config(page_title='Simulador de Apocalipse Zumbi', layout='wide')

st.title('🧟 Simulador de Apocalipse Zumbi 🧟')
#st.markdown('Explore como a população humana, zumbi e de mortos evolui ao longo do tempo com parâmetros ajustáveis.')

# Sidebar com os parâmetros
with st.sidebar:
    st.header('Parâmetros do Modelo')

    L0 = st.number_input('Humanos iniciais ($L_0$)', min_value=0, value=70)
    Z0 = st.number_input('Zumbis iniciais ($Z_0$)', min_value=0, value=20)
    D0 = st.number_input('Mortos iniciais ($D_0$)', min_value=0, value=0)

    alpha = st.slider('Taxa de nascimento (α)', 0.0, 1.0, 0.15, step=0.01)
    beta = st.slider('Taxa de morte natural (β)', 0.0, 1.0, 0.10, step=0.01)
    gamma = st.slider('Taxa de infecção (γ)', 0.0, 1.0, 0.005, step=0.001, format='%0.3f')
    delta = st.slider('Taxa de destruição de zumbis (δ)', 0.0, 1.0, 0.006, step=0.001, format='%0.3f')
    rho = st.slider('Fração de mortos que viram zumbi (ρ)', 0.0, 1.0, 0.1, step=0.05)

    tempo_max = st.sidebar.slider('Tempo total da simulação', 100, 2000, 1000, step=100)

    st.header('Curvas Exibidas')
    mostrar_L = st.checkbox('Humanos', value=True)
    mostrar_Z = st.checkbox('Zumbis', value=True)
    mostrar_D = st.checkbox('Mortos', value=True)

t_eval = np.linspace(0, tempo_max, 1000)

# Modelo usando solve_ivp (ordem dos argumentos: t, y)
def modelo_zumbi(t, y):
    L, Z, D = y
    dLdt = ((alpha - beta) * L) - (gamma * L * Z)
    dZdt = (rho * beta * L) + ((gamma - delta) * L * Z)
    dDdt = (1 - rho) * beta * L + delta * L * Z
    return [dLdt, dZdt, dDdt]

# Resolve as EDO's
sol = solve_ivp(
    modelo_zumbi,
    t_span=(0, tempo_max),
    y0=[L0, Z0, D0],
    t_eval=t_eval,
    method='RK45'
)
L, Z, D = sol.y

# Cálculo e exibição do número básico de reprodução
R0_basic = gamma / delta
st.write(f'Número básico de reprodução ($R_0$): {R0_basic:.2f}')

# Infecção passiva
infec_passiva = rho * beta* L0
st.write(f'Infecção passiva inicial: {infec_passiva:.2f}')

if R0_basic > 1:
    st.warning("⚠️ Os zumbis têm vantagem no confronto direto!")
else:
    st.success("✅ Os humanos têm vantagem no confronto direto.")

if infec_passiva > 1:
    st.info("☠️ Cuidado: a infecção passiva ainda pode manter a ameaça zumbi.")

# Verifica se a solução foi bem-sucedida
if sol.success:
    fig, ax = plt.subplots(figsize=(14, 8))
    if mostrar_L:
        ax.plot(sol.t, L, label='Humanos (L)', color='tab:blue')
    if mostrar_Z:
        ax.plot(sol.t, Z, label='Zumbis (Z)', color='tab:red')
    if mostrar_D:
        ax.plot(sol.t, D, label='Mortos (D)', color='tab:gray')

    ax.set_xlabel('Tempo')
    ax.set_ylabel('População')
    ax.set_title('Dinâmica Populacional - Modelo Zumbi')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
else:
    st.error('Erro na simulação. Tente ajustar os parâmetros.')

# Encontra o dia e o valor correspondentes ao pico de infecções
pico = t_eval[np.argmax(Z)]
max_infeccoes = np.max(Z)

# Exibe os resultados dos picos
st.subheader('Pico da Epidemia (Máximo de Infectados)')
st.markdown(f"""
- **Dia do pico**: {int(pico)}  
- **Número máximo de infectados simultâneos**: {int(max_infeccoes)}  
""")

# Valores finais de cada variável
st.subheader('Distribuição final das populações')
col1, col2, col3, = st.columns(3)

total_final = L[-1] + Z[-1] + D[-1]

with col1:
    st.metric('Susceptíveis finais (S)', value=f'{int(L[-1])}', delta=f'{int(L[-1] - L0)}')
    st.metric('% Susceptíveis', value=f'{(L[-1]/total_final)*100:.2f}%')

with col2:
    st.metric('Infectados finais (I)', value=f'{int(Z[-1])}', delta=f'{int(Z[-1] - Z0)}')
    st.metric('% Infectados', value=f'{(Z[-1]/total_final)*100:.2f}%')

with col3:
    st.metric('Mortos finais (D)', value=f'{int(D[-1])}', delta=f'{int(D[-1] - D0)}')
    st.metric('% Mortos', value=f'{(D[-1]/total_final)*100:.2f}%')

############################################


# Parâmetros fixos
beta = 0.2
gamma = 0.6
rho   = 0.1

# Condições iniciais
L0 = 0.5
Z0 = 0.25
D0 = 0.0

# Tempo de simulação
t_span = (0, 100)
t_eval = np.linspace(*t_span, 1000)

# Malha de parâmetros
alphas = np.linspace(0.05, 0.25, 50)
deltas = np.linspace(0.1, 1.0, 50)

resultados = np.zeros((len(alphas), len(deltas)))

# Função do modelo
def modelo_zumbi(t, y, alpha, beta, gamma, delta, rho):
    L, Z, D = y
    dLdt = (alpha - beta) * L - gamma * L * Z
    dZdt = rho * beta * L + (gamma - delta) * L * Z
    dDdt = (1 - rho) * beta * L + delta * L * Z
    return [dLdt, dZdt, dDdt]

# Loop sobre a malha de parâmetros
for i, alpha in tqdm(enumerate(alphas), total=len(alphas)):
    for j, delta in enumerate(deltas):
        sol = solve_ivp(
            modelo_zumbi,
            t_span,
            [L0, Z0, D0],
            t_eval=t_eval,
            args=(alpha, beta, gamma, delta, rho)
        )
        L_final = sol.y[0, -1]
        Z_final = sol.y[1, -1]
        if L_final + Z_final > 0:
            indicador = (L_final - Z_final) / (L_final + Z_final)
        else:
            indicador = -1  # tudo morreu
        resultados[i, j] = indicador


# Supondo que 'resultados' seja uma matriz 2D, e 'deltas' e 'alphas' sejam arrays 1D
fig, ax = plt.subplots(figsize=(10, 6))  # Corrigido aqui

# Usa imshow para mostrar uma matriz com mapa de cores
im = ax.imshow(resultados, origin='lower', aspect='auto',
               extent=[deltas[0], deltas[-1], alphas[0], alphas[-1]],
               cmap='seismic', vmin=-1, vmax=1)

# Adiciona colorbar com rótulo
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('(L - Z) / (L + Z)')

# Configurações de rótulo e título
ax.set_xlabel('δ (Força dos humanos)')
ax.set_ylabel('α (Taxa de nascimento)')
ax.set_title('Espaço de parâmetros (Modelo Contínuo)')
ax.grid(False)

# Renderiza no Streamlit
st.pyplot(fig)
