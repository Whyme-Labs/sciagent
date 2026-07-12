# Publication Figure Specification

The house style for every figure that may reach the paper. Consumed by the results-analyzer dispatch (Phase 5) and by the Phase 6 figure QA. The point of a fixed spec is that figure quality becomes machine-checkable: a figure passes the QA table below or it is redone — no taste debates. Adapted from Nature-standard figure practice.

## 1. Mandatory rcParams

Every plotting script starts with exactly this block (matplotlib):

```python
import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",   # text stays TEXT in the SVG — editable in Illustrator/Inkscape
    "pdf.fonttype": 42,       # TrueType, not Type 3 — required by most journals
    "axes.spines.top": False,
    "axes.spines.right": False,
})
```

Never `svg.fonttype: "path"` — it converts labels to outlines and destroys editability, which journals and co-authors both need.

## 2. Layout laws

- Top and right spines off, always (set globally above).
- Legends frameless (`frameon=False`). No gridlines unless the figure is unreadable without them (then light, dashed, behind the data).
- **Tighten y-limits to the data range.** Values spanning 80–95 are not plotted on 0–100; the wasted axis hides the effect the figure exists to show. (Bar charts of ratio quantities may still need a zero baseline — say so in the log if you keep one.)
- When the methods are identified in a legend, do not also spell them on the x-axis — one encoding per fact.
- Multi-axis / many-panel figures with a shared legend: give the legend its own dedicated slot (a legend-only subplot or figure-level legend), never duplicated per panel.
- End with `fig.tight_layout(pad=2)` and `plt.close(fig)` (no dangling figures across runs).

## 3. Size discipline

Design at final print size — text that is legible when the figure is scaled down was sized wrong, not saved by luck:

- Single-column width ≈ **89 mm** (3.5 in); double-column ≈ **183 mm** (7.2 in). Set `figsize` from these.
- Body, tick, and legend text: **5–7 pt at final size**.
- Panel letters: **bold lowercase** (`a`, `b`, `c`), top-left of each panel, ~8 pt.

## 4. Export policy

- **SVG is the primary artifact** (vector, editable text). PNG at **dpi=300** (600 for dense bar panels) is the secondary/preview artifact. Save both, same basename, to `paper/figures/`.
- The data behind each figure is written alongside it as `paper/figures/<name>.source.csv` (or `.tsv`) — the per-figure source-data file the data-availability audit (Phase 6/7) checks for.

## 5. Multi-panel design — anti-redundancy

Rule: **each panel answers a unique scientific question; covering a panel must leave an unrecoverable gap.** If removing a panel loses nothing, remove it.

A well-formed multi-panel figure typically progresses **Overview → Deviation → Relationship**: what the landscape looks like, where the interesting departure is, and what explains it.

Redundancy traps (each is a delete-one-panel signal):

| Trap | Example |
|---|---|
| Two absolute views of the same quantity | bar chart of accuracy + table of the same accuracies |
| A subset re-plotted next to its parent | full curve + zoomed inset that adds no new comparison |
| Two rankings of the same ordering | sorted bars + a leaderboard table |

## 6. Figure legend skeleton

Every caption follows this fixed skeleton — self-contained, so the figure is interpretable without the body text:

```
Fig. N | Bold noun-phrase title stating the finding. a, Telegraphic present-tense
description of panel a. b, … Statistics: n = <independent units, and what the unit is>,
error bars show <s.d. | s.e.m. | 95% CI>, <test name>, p = <exact value>.
Source data are provided as a Source Data file.
```

- Tense rule: visual facts in present tense ("accuracy increases with depth"); how the data was obtained in past tense ("models were trained for 100k steps").
- Self-containment rule: every color/shape/linestyle mapping, the n, and the key numbers live in the legend, not only in the body text.
- Legend ≤ ~300 words.

## 7. Figure QA contract

Run this table for every figure before it is accepted (Phase 5 VERIFY for analyzer output; Phase 6 deterministic checks for the assembled paper). A row fails → the figure is redone, not excused.

| Check | Pass condition |
|---|---|
| Formats | `.svg` + `.png` exist, same basename, in `paper/figures/` |
| Editable text | SVG contains `<text` elements (`grep -l "<text" <fig>.svg`) — not paths |
| Source data | `<name>.source.csv` exists and reproduces the plotted values |
| Spines/grid | no top/right spines; no default grid |
| Axis honesty | y-limits fit the data range; axes labeled with units |
| Size | figsize matches a journal column width; text ≥ 5 pt at that size |
| Panel letters | bold lowercase, consistent placement (multi-panel only) |
| Panel uniqueness | each panel states, in one line in the log, the question only it answers |
| Legend | follows the §6 skeleton: n + unit, error-bar type, test, exact p (where a comparison is shown) |
| Statistics minimum | any panel showing a comparison has its n, variability measure, and test recoverable from the legend |
| Integrity | no cropping/contrast/pseudo-color manipulation that changes what the data shows; any image reuse across figures is declared |
