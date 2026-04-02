"""
benchmark.py — Comparação de Desempenho CPU vs. GPU
=====================================================
Executa a simulação de caminhada aleatória para diferentes valores de N
(número de partículas) e mede o tempo de execução em CPU e GPU.

Gera um gráfico de speedup (tempo_CPU / tempo_GPU) em função de N,
demonstrando quando vale a pena usar GPU.

Uso:
    python benchmark.py [--config PATH]
"""

import argparse
import logging
import os
import time
import warnings
import sys

import matplotlib.pyplot as plt
import numpy as np
import yaml

warnings.filterwarnings("ignore")


def configurar_logging(log_dir: str) -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    job_id = os.environ.get("SLURM_JOB_ID", "local")
    log_file = os.path.join(log_dir, f"benchmark_{job_id}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, mode="w", encoding="utf-8"),
            logging.StreamHandler(stream=sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def medir_tempo_cpu(n_particles: int, n_steps: int, step_size: float,
                    seed: int, repeats: int) -> float:
    """
    Mede o tempo médio da simulação em CPU (NumPy).
    Retorna a mediana dos tempos (mais robusta a outliers que a média).
    """
    tempos = []
    rng = np.random.default_rng(seed)

    for _ in range(repeats):
        t0 = time.perf_counter()
        passos = rng.choice([-step_size, step_size],
                            size=(n_steps, n_particles, 2))
        positions = np.zeros((n_steps + 1, n_particles, 2), dtype=np.float32)
        np.cumsum(passos, axis=0, out=positions[1:])
        _ = np.mean(positions[:, :, 0]**2 + positions[:, :, 1]**2, axis=1)
        tempos.append(time.perf_counter() - t0)

    return float(np.median(tempos))


def medir_tempo_gpu(n_particles: int, n_steps: int, step_size: float,
                    seed: int, repeats: int, device) -> float:
    """
    Mede o tempo médio da simulação em GPU (PyTorch/CUDA).

    Nota: usamos torch.cuda.synchronize() antes e depois da medição.
    Isso é FUNDAMENTAL em benchmarks de GPU: operações CUDA são assíncronas
    — sem synchronize(), o temporizador captura apenas o tempo de submissão
    das operações, não o tempo real de execução.
    """
    import torch

    tempos = []
    torch.manual_seed(seed)

    # Warm-up: a primeira execução na GPU inclui o tempo de compilação JIT.
    # Descartamos ela para uma medição justa.
    _ = torch.bernoulli(torch.full((10, 100, 2), 0.5, device=device))
    torch.cuda.synchronize()

    for _ in range(repeats):
        torch.cuda.synchronize()   # ← garante que operações anteriores terminaram
        t0 = time.perf_counter()

        passos = (torch.bernoulli(
            torch.full((n_steps, n_particles, 2), 0.5, device=device)
        ) * 2 - 1) * step_size

        positions = torch.zeros(
            (n_steps + 1, n_particles, 2), dtype=torch.float32, device=device
        )
        torch.cumsum(passos, dim=0, out=positions[1:])
        _ = torch.mean(
            positions[:, :, 0]**2 + positions[:, :, 1]**2, dim=1
        )

        torch.cuda.synchronize()   # ← aguarda TUDO terminar antes de parar o timer
        tempos.append(time.perf_counter() - t0)

    return float(np.median(tempos))


def plotar_benchmark(resultados: dict, output_dir: str) -> str:
    """
    Gera figura com dois painéis:
      - Esquerdo: tempo de execução CPU vs. GPU em função de N
      - Direito: speedup (tempo_CPU / tempo_GPU) em função de N

    O gráfico de speedup é a visualização mais intuitiva:
    speedup > 1 → GPU mais rápida
    speedup < 1 → CPU mais rápida (para N pequeno)
    """
    os.makedirs(output_dir, exist_ok=True)

    N_vals = resultados["N"]
    t_cpu = resultados["tempo_cpu"]
    t_gpu = resultados.get("tempo_gpu")

    fig, axes = plt.subplots(1, 2 if t_gpu else 1, figsize=(14 if t_gpu else 7, 5))
    if t_gpu is None:
        axes = [axes]

    fig.suptitle("Benchmark: CPU vs. GPU — Simulação de Difusão 2D",
                 fontsize=13, fontweight="bold")

    # ── Painel 1: Tempo absoluto ──────────────────────────────────────────
    ax = axes[0]
    ax.loglog(N_vals, t_cpu, "o-", color="steelblue", linewidth=2,
              markersize=8, label="CPU (NumPy)")
    if t_gpu:
        ax.loglog(N_vals, t_gpu, "s-", color="tomato", linewidth=2,
                  markersize=8, label="GPU (PyTorch/CUDA)")

    ax.set_title("Tempo de Execução", fontsize=11)
    ax.set_xlabel("Número de Partículas (N)")
    ax.set_ylabel("Tempo mediano (s)")
    ax.legend(fontsize=10)
    ax.grid(True, which="both", alpha=0.3)

    # Linha de referência O(N) para guia visual
    n_ref = np.array([N_vals[0], N_vals[-1]], dtype=float)
    t_ref = t_cpu[0] * n_ref / N_vals[0]
    ax.loglog(n_ref, t_ref, "--", color="gray", linewidth=1, label="O(N) referência")
    ax.legend(fontsize=9)

    # ── Painel 2: Speedup ─────────────────────────────────────────────────
    if t_gpu and len(axes) > 1:
        ax2 = axes[1]
        speedup = [tc / tg for tc, tg in zip(t_cpu, t_gpu)]

        cores = ["tomato" if s < 1 else "seagreen" for s in speedup]
        ax2.bar(range(len(N_vals)), speedup, color=cores, edgecolor="black",
                linewidth=0.7)
        ax2.axhline(y=1, color="black", linestyle="--", linewidth=1.5,
                    label="Speedup = 1 (empate)")
        ax2.set_xticks(range(len(N_vals)))
        ax2.set_xticklabels([f"{n:,}" for n in N_vals], rotation=30, ha="right")
        ax2.set_title("Speedup  (tempo_CPU / tempo_GPU)", fontsize=11)
        ax2.set_xlabel("Número de Partículas (N)")
        ax2.set_ylabel("Speedup")
        ax2.legend(fontsize=9)
        ax2.grid(True, axis="y", alpha=0.3)

        # Anota os valores
        for i, s in enumerate(speedup):
            cor_txt = "white" if s > 1.5 else "black"
            ax2.text(i, s / 2, f"{s:.1f}×", ha="center", va="center",
                     fontsize=9, fontweight="bold", color=cor_txt)

    plt.tight_layout()
    fname = os.path.join(output_dir, "benchmark_comparison.png")
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close()
    return fname


def main():
    parser = argparse.ArgumentParser(description="Benchmark CPU vs GPU")
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    log = configurar_logging(cfg["log_dir"])

    log.info("=" * 60)
    log.info("BENCHMARK — CPU vs. GPU")
    log.info("=" * 60)

    # ── Detecta GPU ───────────────────────────────────────────────────────
    try:
        import torch
        gpu_disponivel = torch.cuda.is_available()
        if gpu_disponivel:
            log.info(f"GPU: {torch.cuda.get_device_name(0)}")
            device = torch.device("cuda")
        else:
            log.warning("GPU não disponível. Benchmark apenas em CPU.")
    except ImportError:
        gpu_disponivel = False
        log.warning("PyTorch não instalado. Benchmark apenas em CPU.")

    N_vals = cfg["benchmark_sizes"]
    repeats = cfg["benchmark_repeats"]
    n_steps = cfg["n_steps"]
    step_size = cfg["step_size"]
    seed = cfg["seed"] if cfg["seed"] is not None else 0

    log.info(f"Tamanhos de N: {N_vals}")
    log.info(f"Repetições por tamanho: {repeats}")
    log.info(f"Passos de tempo (T): {n_steps}")

    resultados = {"N": N_vals, "tempo_cpu": [], "tempo_gpu": [] if gpu_disponivel else None}

    # ── Benchmark CPU ─────────────────────────────────────────────────────
    log.info("\n--- Benchmark CPU (NumPy) ---")
    for n in N_vals:
        t = medir_tempo_cpu(n, n_steps, step_size, seed, repeats)
        resultados["tempo_cpu"].append(t)
        log.info(f"  N = {n:>8,} | tempo = {t:.4f} s")

    # ── Benchmark GPU ─────────────────────────────────────────────────────
    if gpu_disponivel:
        log.info("\n--- Benchmark GPU (PyTorch/CUDA) ---")
        for n in N_vals:
            try:
                t = medir_tempo_gpu(n, n_steps, step_size, seed, repeats, device)
                resultados["tempo_gpu"].append(t)
                speedup = resultados["tempo_cpu"][N_vals.index(n)] / t
                log.info(f"  N = {n:>8,} | tempo = {t:.4f} s | speedup = {speedup:.1f}×")
            except RuntimeError as e:
                log.error(f"  N = {n:>8,} | ERRO: {e}")
                resultados["tempo_gpu"].append(None)

    # ── Gera figura ───────────────────────────────────────────────────────
    log.info("\nGerando figura de benchmark...")
    fname = plotar_benchmark(resultados, cfg["output_dir"])
    log.info(f"Figura salva em: {fname}")

    # ── Tabela resumo ─────────────────────────────────────────────────────
    log.info("\n" + "=" * 60)
    log.info("TABELA RESUMO")
    log.info("=" * 60)
    header = f"{'N':>10} | {'CPU (s)':>10} | {'GPU (s)':>10} | {'Speedup':>10}"
    log.info(header)
    log.info("-" * len(header))
    for i, n in enumerate(N_vals):
        tc = resultados["tempo_cpu"][i]
        if resultados["tempo_gpu"] and resultados["tempo_gpu"][i] is not None:
            tg = resultados["tempo_gpu"][i]
            sp = tc / tg
            log.info(f"{n:>10,} | {tc:>10.4f} | {tg:>10.4f} | {sp:>9.1f}×")
        else:
            log.info(f"{n:>10,} | {tc:>10.4f} | {'N/A':>10} | {'N/A':>10}")

    log.info("Benchmark finalizado com sucesso.")


if __name__ == "__main__":
    main()
