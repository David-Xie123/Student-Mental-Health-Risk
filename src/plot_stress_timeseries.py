#!/usr/bin/env python3
"""
Self-reported stress across the semester, by participant.

All 32 participants (P3/12/14 already excluded — questionnaire-only). Shared
x-axis (whole study, so panels line up in calendar time) and shared y-axis
(0-100) so between-person level differences stay visible alongside each
person's own day-to-day swing -- the ICC = 0.389 result made visible.
Sorted by each participant's mean stress, same order as people.png.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

OUT = "C:/Users/david/Documents/Research/Student-Mental-Health-Risk/data"
FIG = "C:/Users/david/Documents/Research/Student-Mental-Health-Risk/figures"
os.makedirs(FIG, exist_ok=True)

INK = "#3f4b57"; MUTED = "#8a97a3"; GRID = "#c9d2da"
STRESS = "#c8384b"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white", "font.size": 10,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": MUTED,
    "xtick.color": INK, "ytick.color": INK, "axes.titlecolor": INK,
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 170,
})

d = pd.read_csv(f"{OUT}/combined_health_data.csv", parse_dates=["date"],
                usecols=["subject", "date", "stress"])
# d["date"] = d.t_local.dt.normalize()
d = d.sort_values(["subject", "date"])

mu = d.groupby("subject").stress.mean()
order = list(mu.sort_values().index)
xmin, xmax = d.date.min(), d.date.max()

ncol = 5
nrow = int(np.ceil(len(order) / ncol))
fig, axs = plt.subplots(nrow, ncol, figsize=(3.15 * ncol, 2.05 * nrow),
                        sharex=True, sharey=True)
axs = np.atleast_2d(axs)
for i, s in enumerate(order):
    ax = axs[i // ncol, i % ncol]
    g = d[d.subject == s]
    ax.plot(g.date, g.stress, "-o", color=STRESS, lw=1, ms=2.4,
            alpha=.85, zorder=3)
    ax.axhline(g.stress.mean(), color=MUTED, lw=.9, ls="--", zorder=2)
    ax.set_ylim(-3, 103)
    ax.set_xlim(xmin, xmax)
    ax.set_title(f"P{int(s)}   n={len(g)}   mean {g.stress.mean():.0f}",
                 fontsize=8.6, pad=3)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.tick_params(labelsize=7.5)
    ax.grid(True, color=GRID, alpha=.45, lw=.6)
    ax.set_axisbelow(True)
for j in range(len(order), nrow * ncol):
    axs[j // ncol, j % ncol].axis("off")
for c in range(ncol):
    col_axes = [i for i in range(len(order)) if i % ncol == c]
    if col_axes:
        last = max(col_axes)
        axs[last // ncol, c].tick_params(labelbottom=True, labelsize=7.5)
for rr in range(nrow):
    axs[rr, 0].set_ylabel("stress (0-100)", fontsize=8.5)

fig.suptitle("Self-reported stress across the semester, by participant -- "
             f"{len(order)} participants, sorted by mean", fontsize=13.5, y=1.012)
fig.text(.5, -.012,
         "Shared 0-100 y-axis: between-participant level differences (mean "
         f"{mu.min():.0f} to {mu.max():.0f}) sit alongside each person's own "
         "day-to-day swing -- ICC(stress) = 0.389, so about 39% of the total\n"
         "variance is who the person is, not what day it is. Dashed line is "
         "each participant's own mean.",
         ha="center", fontsize=9, color=MUTED)
fig.tight_layout()
fig.savefig(f"{FIG}/stress_timeseries_by_participant.png",
            bbox_inches="tight", dpi=155)
print("wrote stress_timeseries_by_participant.png")
print(f"{len(order)} participants, mean stress range "
      f"{mu.min():.1f} to {mu.max():.1f}")
