"""Assemble Section 4.5: insert tables/figures, number citations in order of appearance (IEEE), emit .md and .docx."""
import re
import subprocess
from pathlib import Path

from refs import REFS

HERE = Path(__file__).parent
text = (HERE / "section_4_5_source.md").read_text()
tables_src = (HERE / "tables.md").read_text()
tables = dict(re.findall(r"<<<(\w+)\n(.*?)\n>>>", tables_src, flags=re.S))

FIGS = {
    "FIG1": ("figures/Fig_4_5_1_degradation_pathways.png",
             "**Fig. 4.5-1.** Coupled degradation pathways in natural fibre biocomposite insulation boards: "
             "exposure agents (left), material-level processes (centre) and performance consequences (right). "
             "Moisture acts as the gating variable for biological attack, and interphase damage feeds back into "
             "higher water uptake. Mitigation levers are listed at the bottom. *Original schematic prepared for this review; "
             "placement: end of the Section 4.5 introduction.*"),
    "FIG2": ("figures/Fig_4_5_2_ageing_and_biodegradation.png",
             "**Fig. 4.5-2.** (a) Change in thermal conductivity of hemp concrete after control storage, outdoor exposure, "
             "immersion–drying and freeze–thaw ageing (bars: mean; lines: specimen range), plotted from data in {poupard2023}. "
             "(b) Degradation versus exposure time for natural fibre–biopolymer systems compiled from "
             "{slezak2023}, {palai2021}, {yetis2022}, {ni2023}, {rongor2024}, {kumar2025}, {sharma2026}, {feijoo2023}, {brdlik2022}, {feijoo2026}. "
             "Filled markers denote mass loss, and open markers denote disintegration or CO₂ evolution, which are not strictly "
             "comparable with mass loss. *Placement: panel (a) in Section 4.5.3 and panel (b) cross-referenced in Section 4.5.5.*"),
    "FIG3": ("figures/Fig_4_5_3_durability_biodegradability_window.png",
             "**Fig. 4.5-3.** Conceptual durability–biodegradability design window. A moisture-managed board retains "
             "function through the service phase and degrades only once end-of-life conditions are imposed, whereas a "
             "board in a persistently wet envelope fails prematurely. The curves are schematic and do not represent "
             "measured data. *Placement: Section 4.5.5, after the paragraph on fibre effects.*"),
}

for k, (path, cap) in FIGS.items():
    text = text.replace(f"<<{k}>>", f"![]({path}){{width=100%}}\n\n{cap}\n")
for k, body in tables.items():
    text = text.replace(f"<<{k}>>", body.strip() + "\n")

order = []


def num(m):
    key = m.group(1)
    if key not in REFS:
        raise KeyError(key)
    if key not in order:
        order.append(key)
    return f"[{order.index(key) + 1}]"


text = re.sub(r"\{([a-z0-9]+)\}(?!\})", num, text)
unused = sorted(set(REFS) - set(order))
if unused:
    print("UNUSED refs:", unused)

reflist = "\n### References\n\n" + "\n".join(
    f"[{i + 1}] {REFS[k]}\n" for i, k in enumerate(order))
out = text + reflist
(HERE / "Section_4.5_Durability_and_Biodegradation.md").write_text(out)
subprocess.run(["pandoc", "Section_4.5_Durability_and_Biodegradation.md", "-o",
                "Section_4.5_Durability_and_Biodegradation.docx", "--resource-path=."],
               cwd=HERE, check=True)
words = len(re.sub(r"\|.*\|", "", text.split("### References")[0]).split())
print(f"refs cited: {len(order)}; approx. words (excl. tables): {words}")
