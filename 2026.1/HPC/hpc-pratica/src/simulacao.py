"""
simulacao.py — Simulação de Difusão por Caminhada Aleatória 2D
==============================================================
Executa a simulação tanto em CPU (NumPy) quanto em GPU (PyTorch),
gera figuras comparativas e registra logs estruturados.

Uso:
    python simulacao.py [--device cpu|gpu|auto] [--config PATH]

Exemplo:
    python simulacao.py --device auto --config configs/config.yaml
"""

import argparse
import logging
import os
import time
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import yaml

# ─────────────────────────────────────────────────────────────────────────────
# Configuração de Logging
# ─────────────────────────────────────────────────────────────────────────────

def configurar_logging(log_dir: str, job_id: str = "local") -> logging.Logger:
    """
    Configura o sistema de logging com saída simultânea para arquivo e terminal.
    
    Em HPC, o log é a principal ferramenta de diagnóstico — não há acesso
    interativo durante a execução. Um bom log permite reconstruir exatamente
    o que aconteceu, quando, e com quais parâmetros.
    """
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"run_{job_id}.log")

    # Formato: data/hora | nível | mensagem
    fmt = "%(asctime)s | %(levelname)-8s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        datefmt=datefmt,
        handlers=[
            logging.FileHandler(log_file, mode="w", encoding="utf-8"),
            logging.StreamHandler(stream=sys.stdout),   # também imprime no terminal / SLURM .out
        ],
    )
    return logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Implementação CPU — NumPy
# ─────────────────────────────────────────────────────────────────────────────

def simular_cpu(n_particles: int, n_steps: int, step_size: float,
                seed: int | None) -> tuple[np.ndarray, np.ndarray]:
    """
    Simula a caminhada aleatória 2D de N partículas usando NumPy (CPU).

    Algoritmo:
        1. Sorteia passos aleatórios em x e y: cada passo é ±step_size.
        2. Acumula os passos para obter as posições ao longo do tempo.
        3. Computa o MSD = média de (Δx² + Δy²) sobre todas as partículas.

    Parâmetros
    ----------
    n_particles : int
        Número de partículas independentes.
    n_steps : int
        Número de passos de tempo.
    step_size : float
        Amplitude de cada passo.
    seed : int | None
        Semente para o gerador de números aleatórios.

    Retorna
    -------
    positions : ndarray, shape (n_steps+1, n_particles, 2)
        Posições (x, y) de cada partícula em cada instante de tempo.
    msd : ndarray, shape (n_steps+1,)
        Deslocamento quadrático médio em cada instante.
    """
    rng = np.random.default_rng(seed)

    # Passos aleatórios: shape (n_steps, n_particles, 2)
    # Cada passo é +step_size ou -step_size com probabilidade 1/2
    passos = rng.choice([-step_size, +step_size],
                        size=(n_steps, n_particles, 2))

    # Posições: acumulação dos passos ao longo do eixo do tempo (eixo 0)
    # positions[0] = origem (0, 0) para todas as partículas
    positions = np.zeros((n_steps + 1, n_particles, 2), dtype=np.float32)
    np.cumsum(passos, axis=0, out=positions[1:])

    # MSD: média sobre partículas de (x² + y²) para cada instante t
    msd = np.mean(positions[:, :, 0] ** 2 + positions[:, :, 1] ** 2, axis=1)

    return positions, msd


# ─────────────────────────────────────────────────────────────────────────────
# Implementação GPU — PyTorch
# ─────────────────────────────────────────────────────────────────────────────

def simular_gpu(n_particles: int, n_steps: int, step_size: float,
                seed: int | None, device: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Simula a caminhada aleatória 2D de N partículas usando PyTorch (CPU ou GPU).

    A lógica é idêntica à versão NumPy, mas operando sobre tensores PyTorch.
    Quando device='cuda', os tensores são alocados na VRAM da GPU e todas as
    operações são executadas nos milhares de CUDA cores em paralelo.

    Parâmetros
    ----------
    device : str
        'cpu' para CPU via PyTorch, 'cuda' para GPU NVIDIA.
    """
    import torch  # importação adiada — evita erro se PyTorch não estiver instalado

    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError(
            "GPU solicitada, mas nenhum dispositivo CUDA foi encontrado. "
            "Verifique se o job foi submetido com --gres=gpu:1."
        )

    torch.manual_seed(seed if seed is not None else 0)
    dev = torch.device(device)

    # Passos aleatórios no dispositivo alvo
    # bernoulli(0.5): gera 0 ou 1 → converte para -1 ou +1
    passos = (torch.bernoulli(
        torch.full((n_steps, n_particles, 2), 0.5, device=dev)
    ) * 2 - 1) * step_size  # shape: (n_steps, n_particles, 2)

    # Acumulação dos passos → posições
    # torch.cumsum é equivalente ao np.cumsum
    positions_torch = torch.zeros(
        (n_steps + 1, n_particles, 2), dtype=torch.float32, device=dev
    )
    torch.cumsum(passos, dim=0, out=positions_torch[1:])

    # MSD
    msd_torch = torch.mean(
        positions_torch[:, :, 0] ** 2 + positions_torch[:, :, 1] ** 2,
        dim=1
    )

    # Transfere de volta para CPU/RAM para salvar e plotar
    # (tensores na GPU não podem ser diretamente convertidos para NumPy)
    positions = positions_torch.cpu().numpy()
    msd = msd_torch.cpu().numpy()

    return positions, msd


# ─────────────────────────────────────────────────────────────────────────────
# Análise Física: Ajuste Linear do MSD
# ─────────────────────────────────────────────────────────────────────────────

def estimar_coeficiente_difusao(msd: np.ndarray, step_size: float) -> dict:
    """
    Estima o coeficiente de difusão D a partir do ajuste linear do MSD.

    Pela lei de Einstein: MSD(t) = 2 * d * D * t  (d=2 dimensões)
    Portanto:  D = slope / (2 * d) = slope / 4

    O valor teórico esperado é: D_teorico = step_size² / 2
    (derivado diretamente da definição da caminhada aleatória simples).
    """
    t = np.arange(len(msd), dtype=float)

    # Regressão linear: MSD = slope * t + intercept
    slope, intercept, r_value, p_value, std_err = stats.linregress(t, msd)

    D_estimado = slope / 4.0           # 2 * d = 2 * 2 = 4
    D_teorico = step_size ** 2 / 2.0   # valor analítico exato

    return {
        "D_estimado": D_estimado,
        "D_teorico": D_teorico,
        "slope": slope,
        "intercept": intercept,
        "R2": r_value ** 2,
        "erro_relativo_pct": abs(D_estimado - D_teorico) / D_teorico * 100,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Visualização
# ─────────────────────────────────────────────────────────────────────────────

def plotar_resultados(positions: np.ndarray, msd: np.ndarray,
                      analise: dict, config: dict,
                      device_label: str, output_dir: str) -> None:
    """
    Gera uma figura com três painéis:
      - Esquerdo: trajetórias individuais de partículas selecionadas
      - Centro: MSD observado vs. ajuste linear (lei de Einstein)
      - Direito: distribuição das posições finais (deve ser Gaussiana)
    """
    os.makedirs(output_dir, exist_ok=True)

    n_traj = min(config["n_trajectories_to_plot"], positions.shape[1])
    t = np.arange(len(msd))

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        f"Simulação de Difusão 2D — {device_label}\n"
        f"N = {positions.shape[1]:,} partículas | T = {len(msd)-1} passos",
        fontsize=13, fontweight="bold"
    )

    # ── Painel 1: Trajetórias ─────────────────────────────────────────────
    ax = axes[0]
    cmap = plt.get_cmap("viridis")
    for i in range(n_traj):
        cor = cmap(i / n_traj)
        ax.plot(positions[:, i, 0], positions[:, i, 1],
                alpha=0.4, linewidth=0.6, color=cor)
        ax.scatter(*positions[-1, i, :], s=12, color=cor, zorder=5)

    ax.scatter(0, 0, s=80, color="red", zorder=10, label="Origem")
    ax.set_title("Trajetórias Individuais", fontsize=11)
    ax.set_xlabel("x (u.a.)")
    ax.set_ylabel("y (u.a.)")
    ax.legend(fontsize=9)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

    # ── Painel 2: MSD vs. Tempo ───────────────────────────────────────────
    ax = axes[1]
    slope = analise["slope"]
    intercept = analise["intercept"]

    ax.plot(t, msd, "o", markersize=2, alpha=0.6, color="steelblue",
            label="MSD simulado")
    ax.plot(t, slope * t + intercept, "-", color="tomato", linewidth=2,
            label=f"Ajuste linear\n$D_{{est}}$ = {analise['D_estimado']:.4f}\n"
                  f"$D_{{teo}}$ = {analise['D_teorico']:.4f}\n"
                  f"$R^2$ = {analise['R2']:.5f}")

    ax.set_title("Deslocamento Quadrático Médio", fontsize=11)
    ax.set_xlabel("Tempo (passos)")
    ax.set_ylabel("MSD (u.a.²)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Painel 3: Distribuição das Posições Finais ────────────────────────
    ax = axes[2]
    x_final = positions[-1, :, 0]
    y_final = positions[-1, :, 1]

    # Histograma 2D das posições finais
    h = ax.hist2d(x_final, y_final, bins=60, cmap="Blues")
    fig.colorbar(h[3], ax=ax, label="Contagem")

    # Sobreposição da Gaussiana teórica (contornos)
    sigma_teo = np.sqrt(2 * analise["D_teorico"] * (len(msd) - 1))
    theta = np.linspace(0, 2 * np.pi, 200)
    for k in [1, 2, 3]:
        ax.plot(k * sigma_teo * np.cos(theta),
                k * sigma_teo * np.sin(theta),
                "--", color="red", linewidth=1.2,
                label=f"{k}σ teórico" if k == 1 else f"_{k}σ")
    ax.legend(fontsize=9)
    ax.set_title("Distribuição das Posições Finais\n(deve ser Gaussiana!)", fontsize=11)
    ax.set_xlabel("x (u.a.)")
    ax.set_ylabel("y (u.a.)")
    ax.set_aspect("equal")

    plt.tight_layout()

    fname = os.path.join(output_dir, f"diffusion_{device_label.lower()}.png")
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close()

    return fname


# ─────────────────────────────────────────────────────────────────────────────
# Ponto de Entrada Principal
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Simulação de Difusão 2D no HPC")
    parser.add_argument(
        "--device", choices=["cpu", "gpu", "auto"], default="auto",
        help="Dispositivo de execução. 'auto' detecta automaticamente a GPU."
    )
    parser.add_argument(
        "--config", default="configs/config.yaml",
        help="Caminho para o arquivo de configuração YAML."
    )
    args = parser.parse_args()

    # ── Carrega configuração ──────────────────────────────────────────────
    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    # ID do job SLURM (disponível como variável de ambiente quando rodando no cluster)
    job_id = os.environ.get("SLURM_JOB_ID", "local")

    log = configurar_logging(cfg["log_dir"], job_id)

    # ── Informações de ambiente ───────────────────────────────────────────
    log.info("=" * 60)
    log.info("INÍCIO DA EXECUÇÃO — Simulação de Difusão 2D")
    log.info("=" * 60)
    log.info(f"Job ID (SLURM): {job_id}")
    log.info(f"Dispositivo solicitado: {args.device}")
    log.info(f"Configuração: {args.config}")
    log.info(f"Parâmetros: N={cfg['n_particles']:,} | T={cfg['n_steps']} | seed={cfg['seed']}")

    # ── Detecta dispositivo ───────────────────────────────────────────────
    try:
        import torch
        torch_disponivel = True
    except ImportError:
        torch_disponivel = False
        log.warning("PyTorch não encontrado. Apenas CPU (NumPy) disponível.")

    if args.device == "auto":
        if torch_disponivel:
            import torch
            usar_gpu = torch.cuda.is_available()
        else:
            usar_gpu = False
    else:
        usar_gpu = (args.device == "gpu")

    device_torch = "cuda" if usar_gpu else "cpu"
    device_label = "GPU" if usar_gpu else "CPU"

    if usar_gpu:
        import torch
        gpu_nome = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
        log.info(f"GPU detectada: {gpu_nome} ({gpu_mem:.1f} GiB VRAM)")
    else:
        log.info("Executando em CPU.")

    # ── Executa Simulação ─────────────────────────────────────────────────
    log.info("Iniciando simulação...")
    t0 = time.perf_counter()

    if usar_gpu and torch_disponivel:
        log.info("Backend: PyTorch (CUDA)")
        positions, msd = simular_gpu(
            n_particles=cfg["n_particles"],
            n_steps=cfg["n_steps"],
            step_size=cfg["step_size"],
            seed=cfg["seed"],
            device=device_torch,
        )
    else:
        log.info("Backend: NumPy (CPU)")
        positions, msd = simular_cpu(
            n_particles=cfg["n_particles"],
            n_steps=cfg["n_steps"],
            step_size=cfg["step_size"],
            seed=cfg["seed"],
        )

    t_sim = time.perf_counter() - t0
    log.info(f"Simulação concluída em {t_sim:.3f} s")
    log.info(f"Memória dos dados: {positions.nbytes / 1024**2:.1f} MiB")

    # ── Análise Física ────────────────────────────────────────────────────
    log.info("Calculando coeficiente de difusão (ajuste linear do MSD)...")
    analise = estimar_coeficiente_difusao(msd, cfg["step_size"])

    log.info(f"  D estimado  = {analise['D_estimado']:.6f}")
    log.info(f"  D teórico   = {analise['D_teorico']:.6f}")
    log.info(f"  Erro relativo: {analise['erro_relativo_pct']:.3f}%")
    log.info(f"  R² do ajuste: {analise['R2']:.6f}")

    if analise["R2"] < 0.999:
        log.warning("R² < 0.999. Considere aumentar n_particles para melhor estatística.")

    # ── Visualização ──────────────────────────────────────────────────────
    log.info("Gerando figuras...")
    fname = plotar_resultados(
        positions=positions,
        msd=msd,
        analise=analise,
        config=cfg,
        device_label=device_label,
        output_dir=cfg["output_dir"],
    )
    log.info(f"Figura salva em: {fname}")

    # ── Resumo Final ──────────────────────────────────────────────────────
    log.info("=" * 60)
    log.info("RESUMO DA EXECUÇÃO")
    log.info("=" * 60)
    log.info(f"  Dispositivo       : {device_label}")
    log.info(f"  N partículas      : {cfg['n_particles']:,}")
    log.info(f"  Passos de tempo   : {cfg['n_steps']}")
    log.info(f"  Tempo de execução : {t_sim:.3f} s")
    log.info(f"  D estimado        : {analise['D_estimado']:.6f}")
    log.info(f"  D teórico         : {analise['D_teorico']:.6f}")
    log.info(f"  Erro relativo     : {analise['erro_relativo_pct']:.3f}%")
    log.info("=" * 60)
    log.info("Execução finalizada com sucesso.")


if __name__ == "__main__":
    main()
