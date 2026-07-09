# Writing Rationale Matrix

The matrix is the **execution plan** for Phase 6 writing, not a post-hoc summary. It is built before any section-writer subagent is dispatched. Every manuscript unit — paragraph, equation, figure caption, table, heading — gets a row.

A shallow matrix is a failure. If most rows say "improve clarity" or "polish wording," stop and redo the blueprint stage (Phase 1 decision archaeology, Phase 6 narrative arc, three-table method). The matrix is what prevents the polished sections from collapsing into generic prose.

## Save Location

`paper/writing-rationale-matrix.md` — alongside `paper/narrative-arc.md` and `paper/motivation-surface-map.md`.

## Required Inputs

Before building the matrix, all of these must exist:

- `paper/narrative-arc.md` (Phase 6 step 1)
- `paper/motivation-surface-map.md` (Phase 6 step 3b)
- the `research-log/[NNN]-decision-archaeology.md` entry with the Exemplar Move Tables (Phase 1)
- Idea DNA from `state.json` (and `PROBLEM.md` for the core question)
- `results.tsv` prediction ledger (for Discussion/Results evidence anchors)
- For rewrites only: the previous draft's section text

## Schema

| Row ID | Manuscript Unit | Planned Function | Idea-DNA Link | Exemplar Pattern (from decision archaeology) | Venue Norm | Evidence Anchor | Operation | Final Text Check |
|---|---|---|---|---|---|---|---|---|

Column definitions:

- **Row ID** — `intro-p1`, `methods-eq3`, `results-fig2-caption`, etc. Stable identifier.
- **Manuscript Unit** — the smallest useful writing unit (one paragraph, one equation block with surrounding prose, one caption, one heading + opening sentence).
- **Planned Function** — the rhetorical move this unit performs. Pulled from the narrative arc. Examples: "establish field stakes," "name the load-bearing assumption," "test Intro promise P2," "compare to baseline B on metric M," "resolve disconfirmation D1 from `results.tsv`."
- **Idea-DNA Link** — which component of the Phase 0 Idea DNA this unit serves (Problem / Assumption / Novelty claim). If a unit serves none, it should probably be deleted.
- **Exemplar Pattern** — the specific Table-1 row from Phase 1 decision archaeology that this unit transfers from. Cite by exemplar paper + paragraph. If no exemplar pattern applies, justify why this is genuinely new ground.
- **Venue Norm** — the target-venue convention this unit respects (e.g., "NeurIPS Intro: numbered contributions in final paragraph," "JMLR Methods: theorem-proof blocks with explicit assumption lists").
- **Evidence Anchor** — for any unit making a factual claim: the specific source. Examples: `results.tsv:exp-04`, `[Vaswani et al., 2017] Sec 3.2`, `experiments/configs/environment.md`, `paper/figures/ablation.pdf`. Units without an evidence anchor must be either pure transition prose or flagged for deletion.
- **Operation** — one of `REWRITE`, `SPLIT`, `MERGE`, `DELETE`, `MOVE`, `ADD`, `KEEP` (see deep-imitation-protocol). For a v1 draft, the default is `REWRITE` (writing from notes). For v2+ revisions, the operation distribution must satisfy the anti-shallow-revision metrics.
- **Final Text Check** — the specific assertion the finished prose must satisfy to count as done. Examples: "uses the named concept's term from paper/narrative-arc.md," "reports CI alongside point estimate," "does not claim transfer beyond domains tested in exp-04/05/06."

## The First Row Is Special

Row 1 (`whole-paper`) is not a paragraph row. It justifies the whole-work framework: why this controlling structure (the narrative arc) is the right one for this paper. Required content:

- Why this controlling structure (not the obvious alternatives — IMRaD, problem-method-results, theorem-driven)?
- Which exemplar paper's overall arc most informs it?
- How does the arc follow the confirmed idea DNA?
- Which result/finding is the structural pivot — the thing the arc bends around?
- How will the assembled paper be checked against this arc? (Story integrity check, Phase 6 quality gate.)

Subsequent rows follow the target document in order.

## Scene Flexibility

The matrix is flexible by paper scene. Force-fitting all papers into IMRaD is a known failure.

- A typical ML paper: abstract, introduction, related work, methodology, experimental setup, results, discussion, conclusion.
- A theory paper: abstract, introduction, preliminaries, main result(s) with proofs, discussion of consequences, conclusion.
- A systems paper: abstract, introduction, motivation, design, implementation, evaluation, related work, conclusion.
- A position paper or survey: distinct structure entirely.

The first row chooses the structure. The remaining rows split the chosen structure into the smallest useful units for *that* structure.

## What Each Row Must Demonstrate

A row is "deep" when its cells together demonstrate:

1. The unit advances or narrows the Idea DNA.
2. The unit transfers a specific structural pattern from a real exemplar (or justifies departing from convention).
3. The unit fits a target-venue norm.
4. The unit is anchored in concrete evidence — a specific run, a specific citation, a specific figure.
5. The unit either fixes a known failure in the previous draft or creates a front/back echo in the narrative arc.
6. The operation is honest — if the previous version of this paragraph was 90% reusable, it is `KEEP`; if the function changed, it is `REWRITE`.

A row that says only "polish prose" or "improve clarity" fails this bar. So does a row whose Exemplar Pattern column is blank for a paragraph that performs a non-trivial rhetorical move.

## Anti-Stacking at the Writing Layer

The Phase 2 anti-stacking rule applies to hypotheses. The matrix extends it to writing: a Methodology section that reads "we combined X with Y and added Z" but has no row articulating the conceptual reframing has stacked at the prose layer even if the hypothesis was a genuine reframing. The matrix is where this is caught — by forcing each Methodology row to declare which component of the novelty claim it serves and why.

## Dispatch Rule

When the matrix is complete, section-writer subagents receive:

- The rows for their section (full table slice).
- The narrative arc.
- The motivation surface map cues for their section.
- The Exemplar Move Tables for their section.
- The relevant research log content.

They do NOT receive freedom to invent structure. The matrix is the spec; their job is to produce prose that satisfies each row's Final Text Check.

## Failure Mode: Post-Hoc Matrix

A matrix written *after* the sections is worthless — it becomes a description of what happened, not a constraint on what should happen. If the matrix and sections are built in the wrong order, treat the sections as a draft, write the matrix from the narrative arc (not from the draft), then redo the sections closed-book against the matrix.
