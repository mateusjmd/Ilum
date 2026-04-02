#!/bin/bash
# =============================================================================
# job_notebook.sh — Script SLURM para iniciar Jupyter Notebook no cluster
# =============================================================================
# Submissão: sbatch jobs/job_notebook.sh
#
# Após submetido, aguarde o job iniciar e execute:
#   cd logs
#   tail -f saida_notebook_JOBID.out
#
# Copie o link que aparecer no formato:
#   http://172.XX.XX.XX:8888/?token=...
# e abra no seu navegador.
#
# IMPORTANTE: Cancele o job quando terminar!
#   scancel JOBID
# =============================================================================

# ---------- Recursos solicitados ao SLURM ------------------------------------
#SBATCH --job-name=jupyter_difusao
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --nodelist=work1
#SBATCH --time=00-04:00:00           # 4 horas — cancele antes se terminar!
#SBATCH --output=logs/saida_notebook_%j.out
#SBATCH --mail-type=BEGIN,FAIL
#SBATCH --mail-user=usuarioXXX@ilum.cnpem.br   # ← substitua pelo seu e-mail

# ---------- Preparação do ambiente -------------------------------------------
mkdir -p logs

source ~/.bashrc
conda activate hpc-pratica
module load cuda/12.2

# ---------- Log de contexto --------------------------------------------------
echo "=================================================="
echo " JUPYTER NOTEBOOK NO CLUSTER — JOB $SLURM_JOB_ID"
echo "=================================================="
echo " Nó : $SLURM_NODELIST"
echo " Início: $(date)"
echo "=================================================="
echo ""
echo " INSTRUÇÕES:"
echo " 1) Aguarde aparecer o link abaixo"
echo " 2) Copie o link http://172.XX.XX.XX:8888/..."
echo " 3) Cole no seu navegador"
echo " 4) Quando terminar: scancel $SLURM_JOB_ID"
echo ""
echo "=================================================="

# ---------- Obtém o IP interno do nó -----------------------------------------
# O IP interno do cluster começa com 172. Extraímos ele dinamicamente.
IPADDRESS=$(ip addr | grep 172 | awk 'NR==1{print $2}' | sed 's!/23!!g' | sed 's!/0!!g')
echo "IP do nó: $IPADDRESS"
echo ""

# ---------- Inicia o Jupyter Notebook ----------------------------------------
jupyter notebook \
    --ip=$IPADDRESS \
    --no-browser \
    --NotebookApp.token='' \
    --NotebookApp.password=''

# Nota: --token='' desabilita autenticação para uso interno.
# Nunca faça isso em ambientes públicos!
