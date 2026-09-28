#!/usr/bin/env python3
"""'Person differences' caterpillar plot (from make_figs.py), with each
participant's mean night HRV RMSSD overlaid on a second axis — same
x-order (sorted by mean stress) as the original figure in the report.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "/sessions/pensive-trusting-maxwell/mnt/outputs"
FIG = "/sessions/pensive-trusting-maxwell/mnt/student_mental_health/analysis/figures"

INK = "#3f4b57"; MUTED = "#8a97a3"; GRID = "#c9d2da"
BLUE = "#3b82f6"; AMBER = "#f59e0b"; ROSE = "#f43f5e"; TEAL = "#14b8a6"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white", "font.size": 10,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": MUTED,
    "xtick.color": INK, "ytick.color": INK, "axes.titlecolor": INK,
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 170,
})

df = pd.read_csv(f"{OUT}/ssaqs_analysis_table.csv")

g = df.groupby("subject")["stress"]
order = g.mean().sort_values().index
x = np.arange(len(order))
lo = df.groupby("subject")["stress"].quantile(.25).loc[order].values
hi = df.groupby("subject")["stress"].quantile(.75).loc[order].values
mu = g.mean().loc[order].values
mua = df.groupby("subject")["anxiety"].mean().loc[order].values
rmssd = df.groupby("subject")["hrv_rmssd_night"].mean().reindex(order)

fig, ax = plt.subplots(figsize=(10.5, 4.0))
ax.vlines(x, lo, hi, color=BLUE, alpha=.4, lw=5, zorder=2)
ax.plot(x, mu, "o", color=BLUE, ms=4.5, label="stress mean (IQR bar)", zorder=3)
ax.plot(x, mua, "^", color=AMBER, ms=4.5, label="anxiety mean", zorder=3)
ax.axhline(df.stress.mean(), color=ROSE, lw=1.2, ls="--",
           label="cohort mean stress", zorder=1)
ax.set_xticks(x); ax.set_xticklabels(order, fontsize=7.5)
ax.set_xlabel("participant (sorted by mean stress)")
ax.set_ylabel("0–100")
ax.set_ylim(0, 100)

ax2 = ax.twinx()
mask = rmssd.notna()
ax2.plot(x[mask.values], rmssd[mask].values, "s-", color=TEAL, ms=5, lw=1.4,
         alpha=.9, label="mean night RMSSD (right)", zorder=4)
ax2.set_ylabel("mean night RMSSD (ms)", color=TEAL)
ax2.tick_params(axis="y", colors=TEAL)
ax2.spines["top"].set_visible(False)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.5, ncol=2, loc="upper left")

r, p = None, None
paired = pd.DataFrame({"stress": mu, "rmssd": rmssd.values})
paired = paired.dropna()
r = np.corrcoef(paired.stress, paired.rmssd)[0, 1]
ax.set_title("Person differences dominate: mean stress ranges "
             f"{mu.min():.0f} → {mu.max():.0f}, mean night RMSSD "
             f"{np.nanmin(rmssd.values):.0f}→{np.nanmax(rmssd.values):.0f} ms "
             f"across the same participants\n"
             f"between-person r(mean stress, mean RMSSD) = {r:+.2f}, "
             f"n = {len(paired)}", fontsize=10.5)
ax.grid(True, axis="y", color=GRID, alpha=.45, lw=.7); ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(f"{FIG}/people_with_rmssd.png", bbox_inches="tight", dpi=170)
print("wrote people_with_rmssd.png")
print(f"between-person r(mean stress, mean RMSSD) = {r:+.3f}, n={len(paired)}")
print(f"RMSSD missing for: {list(rmssd[~mask].index)}")
