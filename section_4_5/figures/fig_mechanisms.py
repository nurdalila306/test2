"""Figure 4.5-1: conceptual schematic of degradation pathways in natural fibre insulation boards."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 6.2)
ax.axis("off")

C_AGENT = "#dbe9f6"
C_PROC = "#f3e6cf"
C_EFF = "#f6d5d2"
EDGE = "#333333"


def box(x, y, w, h, text, fc, fs=8.5, bold=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                       fc=fc, ec=EDGE, lw=0.9)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=10,
                                 lw=0.9, color=EDGE))


ax.text(1.35, 5.95, "Exposure agents", ha="center", fontsize=10, fontweight="bold")
ax.text(5.5, 5.95, "Material-level processes", ha="center", fontsize=10, fontweight="bold")
ax.text(9.55, 5.95, "Performance consequences", ha="center", fontsize=10, fontweight="bold")

agents = [
    (4.85, "Moisture\n(RH > 80-90 %, liquid water,\ncondensation, wet-dry cycles)"),
    (3.6, "Temperature\n(heat, freeze-thaw)"),
    (2.35, "Biological agents\n(moulds, brown/white rot,\ntermites)"),
    (1.1, "UV radiation and O$_2$\n(exposed or façade use)"),
]
for y, t in agents:
    box(0.1, y, 2.5, 0.95, t, C_AGENT, fs=8)

procs = [
    (4.85, "Fibre swelling, hydroxyl-water bonding;\nhemicellulose hydrolysis"),
    (3.6, "Fibre-matrix interphase debonding,\nmicro-cracking, binder softening"),
    (2.35, "Enzymatic depolymerisation\n(hemicellulose > cellulose > lignin);\nhyphal colonisation of pores"),
    (1.1, "Lignin photo-oxidation, chromophore\nformation, surface erosion"),
]
for y, t in procs:
    box(3.6, y, 3.8, 0.95, t, C_PROC, fs=8)

effs = [
    (4.85, "Rise in thermal conductivity\n(water-filled pores)"),
    (3.6, "Thickness swelling, sagging,\nloss of IB / compressive strength"),
    (2.35, "Mass loss, odour/VOC,\nspore release, IAQ risk"),
    (1.1, "Discolouration, surface\nchalking, reduced service life"),
]
for y, t in effs:
    box(8.3, y, 2.55, 0.95, t, C_EFF, fs=8)

for y, _ in agents:
    arrow(2.62, y + 0.475, 3.58, y + 0.475)
for y, _ in procs:
    arrow(7.42, y + 0.475, 8.28, y + 0.475)

# cross-couplings: moisture enables biology and interface damage
arrow(2.62, 5.1, 3.58, 2.9)
arrow(2.62, 5.0, 3.58, 4.2)
ax.text(2.78, 3.2, "moisture\ngates\nbiology", fontsize=6.5, style="italic", ha="center")
# feedback loop: interphase damage -> more water uptake (drawn outside the box column)
ax.annotate("", xy=(7.42, 5.1), xytext=(7.42, 4.3),
            arrowprops=dict(arrowstyle="-|>", lw=0.8, ls="--", color="#7a1f1f",
                            connectionstyle="arc3,rad=0.9"))
ax.text(7.78, 4.62, "feedback", fontsize=6.5, color="#7a1f1f", ha="left", style="italic")

box(0.1, 0.1, 10.75, 0.7,
    "Mitigation levers: hydrophobisation (wax, silane, thermal modification)  |  biocides and bio-actives\n"
    "(borates, tannins, chitosan, ZnO)  |  constructive protection (vapour control, ventilated cladding)", "#e7efe1", fs=8)

plt.tight_layout()
plt.savefig("Fig_4_5_1_degradation_pathways.png", bbox_inches="tight")
print("saved")
