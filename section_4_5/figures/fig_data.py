"""Figures 4.5-2 (data compiled from cited studies) and 4.5-3 (conceptual design window)."""
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({"font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b",
                     "xtick.color": "#52514e", "ytick.color": "#52514e"})
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"

# ---------------- Figure 4.5-2 ----------------
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.4), dpi=300, gridspec_kw={"width_ratios": [1, 1.35]})

# (a) Poupard et al. 2023, hemp concrete: change in thermal conductivity
labels = ["Control storage\n(4 months)", "Outdoor exposure\n(4 months)",
          "Immersion-drying\n(20 cycles)", "Freeze-thaw\n(20 cycles)"]
mean = [1.22, 9.0, 15.2, None]
lo = [-2.7, 2.7, 7.3, -5.6]
hi = [6.3, 18.3, 23.6, 12.3]
y = list(range(len(labels)))[::-1]
for yi, m, l, h in zip(y, mean, lo, hi):
    a.plot([l, h], [yi, yi], color=MUTED, lw=2, solid_capstyle="round", zorder=2)
    if m is not None:
        a.barh(yi, m, height=0.42, color=S1, zorder=3)
        a.text(max(h, m) + 0.8, yi, f"mean {m:+.1f} %", va="center", color=INK, fontsize=7.5)
    else:
        a.text(h + 0.8, yi, "range only", va="center", color=MUTED, fontsize=7.5, style="italic")
a.axvline(0, color=MUTED, lw=0.8)
a.set_yticks(y)
a.set_yticklabels(labels)
a.set_xlim(-8, 32)
a.set_xlabel("Change in thermal conductivity, Δλ (%)")
a.xaxis.grid(True, color=GRID, lw=0.6)
a.set_axisbelow(True)
a.set_title("(a) Hemp concrete under accelerated ageing", loc="left", fontsize=9, fontweight="bold")
a.text(-8, -0.95, "Bars: mean; grey lines: specimen range. Data: Poupard et al. (2023).",
       fontsize=6.8, color=MUTED)

# (b) Biodegradation kinetics across studies (mass loss unless stated)
soil = [  # (days, %, label, label offset)
    (365, 0.6, "PLA film, field soil (<0.6 %)", (8, -4)),
    (365, 4.3, "PBS film, field soil", (8, 5)),
    (90, 3.33, "Neat PLA", (-40, -4)),
    (90, 8.30, "PLA/NR + 5 % rice straw", (6, -2)),
    (90, 40.06, "PLA/TPS", (6, -2)),
    (30, 5.4, "PLA/MFLC, 45 °C", (6, -2)),
    (180, 21.40, "Astragalus/TPS/PLA", (6, -2)),
    (180, 12.0, "Sisal/PBS (~12 %)", (6, -2)),
]
outdoor = [
    (180, 90.31, "Wood-PLA + mycelium", (8, 0)),
    (180, 57.77, "Wood-PCL + mycelium", (6, -2)),
]
compost = [  # disintegration / mineralisation, not mass loss
    (45, 100, "PHBV/woodflour, compost (disintegration)", (8, 0)),
    (90, 90, "PHBV, ISO 14855-1\n(>90 % CO$_2$)", (-78, -4)),
    (548, 88, "PHBV/almond shell,\nmarine (disintegration)", (-40, -18)),
]


def plot(series, colour, marker, filled, name):
    xs = [p[0] for p in series]
    ys = [p[1] for p in series]
    b.scatter(xs, ys, s=38, marker=marker, facecolor=colour if filled else "white",
              edgecolor=colour if not filled else "white", linewidth=1.6 if not filled else 1.2,
              zorder=3, label=name)
    for x, yv, lab, off in series:
        b.annotate(lab, (x, yv), xytext=off, textcoords="offset points", fontsize=6.6, color=INK,
                   va="center")


plot(soil, S1, "o", True, "Soil burial (mass loss)")
plot(outdoor, S2, "s", True, "Outdoor, mycelium-programmed (mass loss)")
plot(compost, S3, "D", False, "Compost / marine (disintegration or CO$_2$)")
b.set_xscale("log")
b.set_xlim(20, 1200)
b.set_ylim(-4, 110)
b.set_xlabel("Exposure time (days, log scale)")
b.set_ylabel("Degradation (%)")
b.yaxis.grid(True, color=GRID, lw=0.6)
b.set_axisbelow(True)
b.set_xticks([30, 60, 90, 180, 365, 730])
b.set_xticklabels(["30", "60", "90", "180", "365", "730"])
b.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False, fontsize=7)
b.set_title("(b) Biodegradation of fibre-biopolymer systems", loc="left", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.savefig("Fig_4_5_2_ageing_and_biodegradation.png", bbox_inches="tight")
plt.close()

# ---------------- Figure 4.5-3 (conceptual) ----------------
import numpy as np

fig, ax = plt.subplots(figsize=(8, 4.2), dpi=300)
t = np.linspace(0, 60, 600)
service_end = 50
designed = np.where(t < service_end, 100 - 0.12 * t,
                    (100 - 0.12 * service_end) * np.exp(-(t - service_end) / 2.2))
unprotected = 100 * np.exp(-((t / 22) ** 2.2))
ax.axvspan(0, service_end, color="#f3f2ee", zorder=0)
ax.axvspan(service_end, 60, color="#e9f3ee", zorder=0)
ax.plot(t, designed, color=S1, lw=2, label="Moisture-managed board, triggered end of life")
ax.plot(t, unprotected, color=S2, lw=2, label="Board in poorly designed, wet envelope")
ax.axhline(70, color=MUTED, lw=0.9, ls="--")
ax.text(26, 72, "Indicative performance threshold (λ, IB, appearance)", fontsize=7, color=MUTED)
ax.text(24, 103, "Service phase: durability required", ha="center", fontsize=8, color=INK)
ax.text(55, 103, "End of life:\nbiodegradation wanted", ha="center", fontsize=8, color=INK)
ax.annotate("composting / soil trigger\n(T, moisture, microbes)", xy=(50.5, 80), xytext=(33, 45),
            fontsize=7, color=INK, arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))
ax.annotate("premature failure", xy=(21, 40), xytext=(7, 22), fontsize=7, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))
ax.set_xlim(0, 60)
ax.set_ylim(0, 112)
ax.set_xlabel("Time (years; schematic)")
ax.set_ylabel("Retained functional performance (%; schematic)")
ax.set_xticks([])
ax.legend(loc="lower left", frameon=False, fontsize=7.5)
plt.tight_layout()
plt.savefig("Fig_4_5_3_durability_biodegradability_window.png", bbox_inches="tight")
print("saved")
