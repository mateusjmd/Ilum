#!/bin/bash
# =============================================================================
# job_gpu.sh — Script SLURM para Simulação + Benchmark em GPU
# =============================================================================
# Submissão: sbatch jobs/job_gpu.sh
# Monitoramento: tail -f logs/saida_gpu_$SLURM_JOB_ID.out
#                watch -n 1 nvidia-smi
# =============================================================================

# ---------- Recursos solicitados ao SLURM ------------------------------------
#SBATCH --job-name=difusao_gpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=gpu              # OBRIGATÓRIO: fila de GPU
#SBATCH --gres=gpu:1                 # OBRIGATÓRIO: solicita 1 GPU
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G                    # GPU jobs geralmente precisam de mais RAM
#SBATCH --nodelist=work1             # work1 tem Tesla T4 (boa para inferência/ciência)
                                     # Alternativas: work4, work5, work6 (RTX 4090)
#SBATCH --time=00-00:30:00
#SBATCH --output=logs/saida_gpu_%j.out
#SBATCH --error=logs/erro_gpu_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=usuarioXXX@ilum.cnpem.br   # ← substitua pelo seu e-mail

# ---------- Preparação do ambiente -------------------------------------------
mkdir -p logs results

source ~/.bashrc
conda activate hpc-pratica

# Carrega o módulo CUDA do cluster (necessário para usar a GPU)
module load cuda/12.2

# ---------- Log de contexto de execução --------------------------------------
echo "=================================================="
echo " JOB SLURM (GPU) INICIADO"
echo "=================================================="
echo " Job ID        : $SLURM_JOB_ID"
echo " Nó alocado    : $SLURM_NODELIST"
echo " CPUs alocadas : $SLURM_CPUS_PER_TASK"
echo " GPUs alocadas : $SLURM_GPUS_ON_NODE"
echo " Diretório     : $(pwd)"
echo " Data/hora     : $(date)"
echo "=================================================="

# Status da GPU alocada — verifique o nome e VRAM disponível
echo ""
echo ">> Status da GPU:"
nvidia-smi
echo ""

# Versão do CUDA disponível
nvcc --version
echo ""

echo ">> Iniciando simulação em GPU..."
echo ""

# ---------- Execução ---------------------------------------------------------

# 1) Simulação principal na GPU com geração de figuras
python src/simulacao.py --device gpu --config configs/config.yaml

echo ""
echo ">> Simulação concluída. Iniciando benchmark comparativo CPU vs. GPU..."
echo ""

# 2) Benchmark comparativo (mede tempo em ambos os dispositivos)
python src/benchmark.py --config configs/config.yaml

echo ""
echo "=================================================="
echo " STATUS FINAL DA GPU:"
nvidia-smi --query-gpu=name,temperature.gpu,memory.used,memory.total \
           --format=csv,noheader
echo ""
echo " JOB FINALIZADO — $(date)"
echo "=================================================="
echo " Resultados em: results/"
echo " Logs Python em: logs/"
echo "=================================================="
