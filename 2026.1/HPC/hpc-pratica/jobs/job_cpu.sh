#!/bin/bash
# =============================================================================
# job_cpu.sh — Script SLURM para Simulação + Benchmark em CPU
# =============================================================================
# Submissão: sbatch jobs/job_cpu.sh
# Monitoramento: tail -f logs/saida_cpu_$SLURM_JOB_ID.out
# =============================================================================

# ---------- Recursos solicitados ao SLURM ------------------------------------
#SBATCH --job-name=difusao_cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=cpu              # fila de CPU (sem GPU)
#SBATCH --cpus-per-task=4            # 4 núcleos de CPU
#SBATCH --mem=8G                     # 8 GiB de RAM
#SBATCH --time=00-00:30:00           # tempo máximo: 30 minutos
#SBATCH --output=logs/saida_cpu_%j.out
#SBATCH --error=logs/erro_cpu_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=usuarioXXX@ilum.cnpem.br   # ← substitua pelo seu e-mail

# ---------- Preparação do ambiente -------------------------------------------

# Cria diretórios necessários antes de qualquer coisa.
# Se logs/ não existir, o SLURM não consegue criar o arquivo de saída
# e o job falha silenciosamente sem deixar rastro!
mkdir -p logs results

# Carrega o .bashrc para disponibilizar o comando 'conda'
# Sem isso, o shell do job não conhece o conda.
source ~/.bashrc

# Ativa o ambiente virtual com todas as dependências instaladas.
# Lembre-se: o Python do sistema NÃO tem numpy, matplotlib etc.
conda activate hpc-pratica

# ---------- Log de contexto de execução --------------------------------------
echo "=================================================="
echo " JOB SLURM INICIADO"
echo "=================================================="
echo " Job ID       : $SLURM_JOB_ID"
echo " Nó alocado   : $SLURM_NODELIST"
echo " CPUs alocadas: $SLURM_CPUS_PER_TASK"
echo " Memória       : $SLURM_MEM_PER_NODE MiB"
echo " Diretório     : $(pwd)"
echo " Data/hora     : $(date)"
echo "=================================================="

# Exibe informações da CPU alocada
lscpu | grep "Model name"

echo ""
echo ">> Iniciando simulação em CPU..."
echo ""

# ---------- Execução ---------------------------------------------------------

# 1) Simulação principal em CPU com geração de figuras
python src/simulacao.py --device cpu --config configs/config.yaml

echo ""
echo ">> Simulação concluída. Iniciando benchmark CPU vs. GPU..."
echo ""

# 2) Benchmark comparativo (roda apenas CPU se GPU não disponível)
python src/benchmark.py --config configs/config.yaml

echo ""
echo "=================================================="
echo " JOB FINALIZADO — $(date)"
echo "=================================================="
echo " Resultados em: results/"
echo " Logs Python em: logs/"
echo "=================================================="
