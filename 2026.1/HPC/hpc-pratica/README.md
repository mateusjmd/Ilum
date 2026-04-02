# Atividade Prática — HPC Heisenberg
### Simulação de Difusão por Random Walk

O presente repositório destina-se ao versionamento da atividade de demonstração para o uso do *cluster* HPC Heisenberg, enquanto extensão do material principal disponível em: [**Guia HPC Heisenberg**](https://github.com/mateusjmd/Ilum/blob/main/2026.1/HPC/Guia%20HPC%20Heisenberg.pdf).

---

## Contexto Interdisciplinar

A simulação implementada é um **Random Walk 2D**: $N$ partículas se movem aleatoriamente no plano, um passo por unidade de tempo. A grandeza central observada é o **Deslocamento Quadrático Médio** (MSD, *Mean Squared Displacement*), definido como:

$$
\boxed{
\mathrm{MSD}(t) = \langle |r(t) - r(\theta)|^2 \rangle = 2 \cdot d \cdot D \cdot t
}
$$

Sendo que:
- `d = 2`: Dimensões
- `D`: Coeficiente de difusão
- `t`: Tempo

Esta prática é centrada em um fenômeno amplamente presente em diferentes campos de estudo:

| Área                 | Fenômeno                                                     |
|----------------------|--------------------------------------------------------------|
| **Física**           | Movimento Browniano                                          |
| **Biologia**         | Migração celular/Difusão de proteínas em membranas lipídicas |
| **Química**          | Transporte molecular em soluções/Reações por difusão         |
| **Matemática**       | Processos estocásticos                                       |
| **Ciência de Dados** | Método de Monte Carlo/Simulação estocástica                  |
| **Humanidades**      | Difusão de informação/Dispersão de populações/Economia       |

---

## Estrutura do Repositório

```
heisenberg-pratica/
├── README.md               ← Este arquivo
├── environment.yml         ← Definição do ambiente Conda
├── .gitignore
│
├── configs/
│   └── config.yaml         ← Parâmetros da simulação
│
├── src/
│   ├── simulacao.py        ← Simulação: CPU (NumPy) e GPU (PyTorch)
│   └── benchmark.py        ← Comparação de desempenho CPU vs. GPU
│
├── jobs/
│   ├── job_cpu.sh          ← Script SLURM para execução em CPU
│   ├── job_gpu.sh          ← Script SLURM para execução em GPU
│   └── job_notebook.sh     ← Script SLURM para Jupyter Notebook
│
├── notebooks/
│   └── atividade.ipynb     ← Notebook guiado com toda a atividade
│
├── logs/                   ← Saídas geradas pelo SLURM (criado automaticamente)
└── results/                ← Figuras e dados gerados (criado automaticamente)
```

---

## Pré-requisitos

- Acesso ao *cluster* HPC Heisenberg (ver [**Guia HPC Heisenberg**](https://github.com/mateusjmd/Ilum/blob/main/2026.1/HPC/Guia%20HPC%20Heisenberg.pdf))
- Conhecimento básico de terminal Linux
- Python 3.10+ (provido pelo Conda no *cluster*)

---

## Quickstart — Passo a Passo

Para uma experiência mais gráfica e interativa, adote o passo 4. Por outro lado, se desejar uma experiência mais robusta e familiar à operação cotidiana com JOBs de maior complexidade, prossiga com os passos 5 e 6.

### Passo 1: Acesso ao *cluster*

```bash
ssh usuarioXXX@heisenberg.cnpem.br
```

> **📌 Observação:** Se estiver fora da rede do CNPEM, conecte-se primeiro à VPN (FortiClient → CNPEM-SSL).

---

### Passo 2: Clonagem do repositório

```bash
cd ~/work
git clone https://github.com/mateusjmd/Ilum/tree/main/2026.1/HPC/hpc-pratica
cd hpc-pratica
```

---

### Passo 3: Criação e ativação do ambiente Conda

```bash
conda env create -f environment.yml
conda activate hpc-pratica
```

> **📌 Observação:** Este passo pode levar alguns minutos na primeira vez.

---

### Passo 4: Explorção do Jupyter Notebook

Submeta um job para iniciar o Jupyter Notebook em um nó de processamento:

```bash
mkdir -p logs
sbatch jobs/job_notebook.sh
```

Aguarde o job iniciar e obtenha o link de acesso:

```bash
cd logs
tail -f saida_notebook_JOBID.out
```

Pressione a tecla CTRL e clique com o botão esquerdo do mouse no link com a seguinte estrutura: `http://172.XX.XX.XX:8888/tree...`.

---

### Passo 5: Execução da simulação em CPU


```bash
sbatch jobs/job_cpu.sh
```

Acompanhe a execução em tempo real:

```bash
watch -n 1 squeue -u $USER
tail -f logs/saida_cpu_JOBID.out
```

---

### Passo 6: Execução da simulação em GPU

```bash
sbatch jobs/job_gpu.sh
```

Monitore o uso da GPU durante a execução:

```bash
watch -n 1 nvidia-smi
```

---

### Passo 7: Comparação dos resultados

Após ambos os jobs terminarem, verifique os resultados gerados:

```bash
ls results/
```

Os arquivos gerados incluem:
- `diffusion_cpu.png` — trajetórias e MSD na CPU
- `diffusion_gpu.png` — trajetórias e MSD na GPU
- `benchmark_comparison.png` — gráfico de speedup CPU vs. GPU

---

## Personalização

Edite `configs/config.yaml` para modificar os parâmetros antes de submeter:

```yaml
# Aumente n_particles para ver a GPU realmente brilhar
n_particles: 100000

# Aumente n_steps para trajetórias mais longas
n_steps: 500
```

---

## 🆘 Problemas Comuns

| Problema | Solução |
|---|---|
| `ModuleNotFoundError` | Verifique se o ambiente está ativado: `conda activate hpc-pratica` |
| Job preso em PENDING | Tente `--partition=cpu` ou reduza `--mem` |
| `CUDA device not available` | Certifique-se de usar `job_gpu.sh` com `--gres=gpu:1` |
| Kernel morto no Jupyter | Reduza `n_particles` no `config.yaml` |
| Log vazio | Verifique se o diretório `logs/` existe: `mkdir -p logs` |

> Para outros problemas, consulte a **Seção 10 (Erros Comuns e Debugging)** do [**Guia HPC Heisenberg**](https://github.com/mateusjmd/Ilum/blob/main/2026.1/HPC/Guia%20HPC%20Heisenberg.pdf).
