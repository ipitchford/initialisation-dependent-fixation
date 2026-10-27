"""Recreate the two figures of the consensus manuscript.

No image generation or stochastic simulation is used. Finite-population points
are read from the recorded deterministic solves; curves use the proved formulas.
"""
from pathlib import Path
import csv
import os
import tempfile
os.environ.setdefault("MPLCONFIGDIR", tempfile.mkdtemp(prefix="mpl_cache_"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
PLUM = "#67445E"
COPPER = "#B16642"
MOSS = "#526950"
INK = "#292F2B"
GREY = "#8A8D85"
CREAM = "#F3EEE5"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.titlesize": 10, "axes.labelsize": 9,
    "axes.labelcolor": INK, "text.color": INK,
    "axes.edgecolor": GREY, "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "grid.color": "#DFE1DC", "grid.linewidth": 0.6,
    "legend.frameon": False, "pdf.fonttype": 42,
})


def save(fig, stem):
    fig.savefig(OUT / (stem + ".pdf"), bbox_inches="tight")
    fig.savefig(OUT / (stem + ".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.25), constrained_layout=True)
t = np.linspace(0, 1.8, 400)
fresh_rate = 3 + np.exp(-4 * t)
ax[0].plot(t, fresh_rate, color=PLUM, lw=2.2, label="Fresh residents")
ax[0].plot(t, np.full_like(t, 3), color=MOSS, ls="--", lw=1.7,
           label="Equilibrium residents")
ax[0].fill_between(t, 3, fresh_rate, color=PLUM, alpha=0.10)
ax[0].set(xlabel="Time (A update rate = 1)", ylabel="Resident mean update rate",
          title="A  The early environment differs", ylim=(2.9, 4.12))
ax[0].legend(loc="upper right", fontsize=8)
ax[0].grid(axis="y")

with (ROOT / "consensus/evidence/finite_n_values.csv").open() as f:
    rows = [r for r in csv.DictReader(f) if r["case"] == "rates_2_6"]
rows.sort(key=lambda r: int(r["N"]))
ns = [int(r["N"]) for r in rows]
fresh = [float(r["fresh_fixation"]) for r in rows]
stationary = [float(r["stationary_fixation"]) for r in rows]
c = 0.70203205392821271153
ax[1].plot(ns, fresh, "o-", color=PLUM, markersize=3.8, lw=1.5,
           label="Fresh initialisation")
ax[1].plot(ns, stationary, "s--", color=MOSS, markersize=3.5, lw=1.4,
           label="Equilibrium initialisation")
ax[1].axhline(c, color=PLUM, ls=":", lw=1.2)
ax[1].axhline(2 / 3, color=MOSS, ls=":", lw=1.2)
ax[1].annotate("Limit 0.702032…", (200, c), (-4, 5),
               textcoords="offset points", ha="right", color=PLUM, fontsize=8)
ax[1].annotate("Limit 2/3", (200, 2/3), (-4, -13),
               textcoords="offset points", ha="right", color=MOSS, fontsize=8)
ax[1].set(xscale="log", xlabel="Population size N (log scale)",
          ylabel="Single-founder fixation probability",
          title="B  Different large-population limits", ylim=(0.64, 0.777))
ax[1].set_xticks([2, 5, 10, 25, 50, 100, 200],
                 ["2", "5", "10", "25", "50", "100", "200"])
ax[1].legend(loc="upper right", fontsize=7.7)
ax[1].grid(axis="y")
save(fig, "consensus_initialisation")

fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.25), constrained_layout=True)
t = np.linspace(0.001, 7.0, 800)
stat = t / (1 + t)
envelope = t / (t + np.exp(-t))
gap = envelope - stat
star = 1.718911513458379
maximum = 0.273355434321515
ax[0].plot(t, envelope, color=PLUM, lw=2.1, label="Supremum over fresh laws")
ax[0].plot(t, stat, color=MOSS, lw=1.8, ls="--", label="Equilibrium prediction")
ax[0].fill_between(t, stat, envelope, color=COPPER, alpha=0.13)
ax[0].set(xlabel=r"Harmonic-mean ratio minus one, $\xi=\lambda/a-1$",
          ylabel="Single-founder fixation probability", ylim=(0, 1.04),
          title="A  The sharp asymptotic envelope")
ax[0].legend(loc="lower right", fontsize=8)
ax[0].grid(axis="y")
ax[1].plot(t, 100 * gap, color=COPPER, lw=2.2)
ax[1].scatter([star], [100 * maximum], color=PLUM, zorder=5, s=28)
ax[1].annotate("Supremum, not attained:\n27.3355… points\n" + r"at $\xi_*=1.71891\ldots$",
               xy=(star, 100*maximum), xytext=(3.1, 29.0),
               fontsize=8, ha="left", va="center",
               arrowprops={"arrowstyle": "-", "color": GREY, "lw": 0.8})
ax[1].set(xlabel=r"Harmonic-mean ratio minus one, $\xi=\lambda/a-1$",
          ylabel="Underestimate (percentage points)", ylim=(0, 32),
          title="B  Largest possible stationary error")
ax[1].grid(axis="y")
save(fig, "consensus_error_envelope")

print("Created two mathematical figures as vector PDF and PNG.")
