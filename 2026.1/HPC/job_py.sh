#!/bin/bash
#SBATCH --job-name=nome_job
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --nodelist=work1
#SBATCH --time=DD-HH:MM:SS
#SBATCH --output=logs/saida_%j.out
#SBATCH --error=logs/erro_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=usuarioXXX@ilum.cnpem.br

# ---- Preparacao do ambiente ----
mkdir -p logs
source ~/.bashrc
conda activate meu_env

# ---- Execucao ----
python script.py --argumentos