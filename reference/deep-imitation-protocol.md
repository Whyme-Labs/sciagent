# Deep Imitation Protocol

Use this reference when (a) doing decision archaeology in Phase 1 on the most relevant prior papers, or (b) writing/rewriting sections in Phase 6. It exists to prevent two failure modes:

1. **Shallow reading** — extracting only the method from a paper and missing the decisions that produced it.
2. **Shallow writing** — patching a draft by adding one sentence here and rewording another there, leaving the structure untouched.

The two failure modes are mirror images. The same three-table discipline solves both.

## What "Learning From Papers" Means

Learning is not copying phrases and not loosely "sounding academic." It is extracting reusable writing and reasoning decisions:

| Layer | What to learn from each exemplar | Where it lands in our project |
|---|---|---|
| Argument architecture | how the paper moves from field problem to contribution | narrative-arc.md |
| Section rhythm | paragraph count, paragraph jobs, length distribution | writing-rationale-matrix.md |
| Claim calibration | how strongly claims are stated given evidence | per-row "Final Text Check" |
| Evidence placement | where numbers, figures, citations, and caveats appear | per-row "Evidence Anchor" |
| Sentence architecture | sentence roles and slots, not copied sentences | section-writer prompt cues |
| Reader contract | what the paper assumes, explains, and omits | motivation-surface-map.md |

If a section is written without anchoring to these layers, the result is generic academic prose. The three tables below force the anchoring to be explicit.

## Three-Table Method

For each section that matters (typically Introduction, Methodology, Results, Discussion), build three tables.

### Table 1 — Exemplar Move Table

Filled in Phase 1 alongside decision archaeology. One table per section job, drawing from the 2-3 exemplar papers selected in the Phase 1 decision-archaeology step.

```markdown
| Exemplar | Paragraph | Move | Evidence Type | Opening Function | Closing Function | Notes on why this move worked |
|---|---|---|---|---|---|---|
```

A "move" is the rhetorical job of the paragraph — e.g., "establish field-level stakes," "narrow to the specific bottleneck," "preview the testable promise," "name the load-bearing assumption." Use exact quotations only inside the Notes column. Convert quotes to abstract patterns before reusing.

### Table 2 — Our Draft Move Table

Filled in Phase 6 once a first pass exists. Mark every paragraph honestly:

```markdown
| Draft Paragraph | Current Move | Evidence Present | Problem | Keepable Content |
|---|---|---|---|---|
```

Problem categories — pick the most accurate one, not the least embarrassing:

- `wrong-move` — paragraph is doing a different job than the spine requires here.
- `move-missing` — the spine needs a move here that no paragraph performs.
- `multi-move` — two or more moves stuffed into one paragraph; reader cannot follow.
- `unsupported-claim` — assertion without evidence or citation.
- `weak-transition` — paragraph does not earn its place after the previous one.
- `wrong-level` — too coarse or too fine for the section's audience.
- `off-style` — register or claim strength does not match the target venue.
- `off-thread` — paragraph is correct in isolation but does not serve the narrative arc.

### Table 3 — Target Section Blueprint

The merger of Tables 1 and 2 into a paragraph-level plan. This is the input to the section-writer subagent.

```markdown
| Target Paragraph | Move | Source Evidence | Exemplar Pattern | Target Length | Operation |
|---|---|---|---|---|---|
```

Allowed operations:

- `REWRITE` — old content is retained as evidence, but prose and structure are regenerated from notes.
- `SPLIT` — one overpacked draft paragraph becomes multiple target paragraphs.
- `MERGE` — several weak paragraphs become one stronger paragraph.
- `DELETE` — unsupported, off-thread, or duplicative content is removed.
- `MOVE` — content moves to a better section.
- `ADD` — new connective or explanatory text generated from existing evidence.
- `KEEP` — paragraph is retained nearly as-is. Must include an explicit justification.

`KEEP` should be rare in any iteration that claims to be substantive. `ADD` should be secondary. If the matrix is dominated by `ADD` and `KEEP`, the writing pass is a patch, not a revision — see the failure pattern below.

## Closed-Book Rewrite

For each section being substantively rewritten (typical in Phase 6 v1 → v2 revisions, or after a paper-reviewer NEEDS_REVISION):

1. Read the original section and extract facts, claims, citations, figure references, and numbers into notes.
2. Read the Exemplar Move Table and Target Section Blueprint.
3. Stop looking at the original prose.
4. Draft the new section from notes and blueprint.
5. Reopen the original only to verify that claims, numbers, citations, and figure references are preserved.

This prevents the common failure mode where the model simply edits one sentence, adds one sentence, and leaves the rest untouched — the "patch writing" failure pattern below.

## Anti-Shallow-Revision Metrics (Hard Gate for Iterated Drafts)

Applied when comparing draft v(N) to v(N-1) for any section the paper-reviewer flagged for substantive revision. A revision must satisfy:

| Metric | Threshold | Why |
|---|---|---|
| Near-identical paragraph ratio | below 35% | Detects untouched bulk |
| Dominant operation in matrix | not `ADD` | A real revision changes structure, not just adds prose |
| `KEEP` rows | below 25% (unless user requested polish only) | Same reason |
| Missing obligatory moves | 0 | Spine integrity |
| Unsupported new claims | 0 | No claims introduced without evidence |
| Numbers without source | 0 | Every number traces to a run, a table, or a citation |

A revision that fails any row is "patch writing" and must be redone closed-book. These metrics are not universal quality measures — they catch the specific failure of treating a deep revision as a surface edit.

## Failure Pattern: Patch Writing

Patch writing looks like this:

- "This paragraph is adequate; minor polish only" repeated across the matrix.
- Most operations are `ADD` or `KEEP`.
- A new subsection appears, but the weak sections that triggered the revision are untouched.
- Exemplar papers appear in the references but not in Table 1.
- No Table 3 blueprint exists — the section was rewritten directly.
- The paper-reviewer's specific NEEDS_REVISION items appear addressed sentence-by-sentence but the underlying structural problem persists.

When patch writing is detected: discard the patch, redo Tables 1-3, and apply the closed-book method.

## Decision Archaeology Inputs (Phase 1 Use)

When this protocol is used during literature review rather than writing, only Table 1 is built. For each of the 2-3 exemplar papers, the table is filled with:

- The paragraph-level moves the authors used in the section job you are studying.
- The Notes column captures *why* those moves worked given the authors' constraints — this is the "why did the authors arrive here" probe that taste depends on.
- A one-line taxonomy tag per exemplar — `(opportunity pattern, method paradigm, dominant operation)` per `reference/idea-taxonomy.md` — recording how the humans at this venue actually framed the gap and built the contribution.

The output of Phase-1 deep imitation is a populated Table 1 per section job, stored under `research-log/[NNN]-decision-archaeology.md` (next unused sequence number). It feeds directly into the Phase 6 Target Section Blueprint without re-derivation.
