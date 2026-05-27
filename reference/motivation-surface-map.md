# Motivation Surface Map

`paper/narrative-arc.md` captures the *story* — the fire, the journey, the load-bearing assumptions, the dead ends. The surface map captures the *places where the reader meets that story*: the title, the abstract's opening sentence, the topic sentence of each Introduction paragraph, the headings, the figure callouts, the Discussion's first and last sentences.

A paper can have a clean narrative arc and still fail to communicate it because the reader never lands on the moments where the arc surfaces. The map is built to prevent that.

## Save Location

`paper/motivation-surface-map.md` — built in Phase 6 immediately after the narrative arc and before the writing rationale matrix.

## Required Inputs

- `paper/narrative-arc.md`
- Idea DNA from `research-log/000-setup.md`
- The chosen target venue's conventions (from Phase 1 literature review)

## Schema

| Surface Element | Narrative-Arc Role | Planned Wording / Strategy | Venue Constraint | Status |
|---|---|---|---|---|

- **Surface Element** — the specific reader touchpoint (see canonical list below).
- **Narrative-Arc Role** — what piece of the arc this element should carry (the fire? the load-bearing assumption? the disconfirmation we recovered from?).
- **Planned Wording / Strategy** — either a concrete draft sentence, or a strategic rule ("opens with the specific bottleneck, not the field-level importance"). Concrete is better.
- **Venue Constraint** — anything the target venue imposes (length, anonymization, claim style, "contributions must be numbered," etc.).
- **Status** — `planned` / `drafted` / `verified-in-final-paper`.

## Canonical Surface Element List

The standard reader touchpoints to populate. Skip rows that do not apply to the paper's structure; do not invent rows that the reader will not actually see.

- Title — and subtitle if used.
- Abstract — opening sentence, contribution sentence, closing sentence.
- Introduction — paragraph-by-paragraph topic sentences (typically 4-6 rows).
- Methods — subsection headings and the opening sentence of each subsection.
- Results — subsection headings and the opening sentence of each subsection.
- Figure and table callouts in the main text — the sentence that invokes each figure/table.
- Figure and table captions — the first clause of each caption.
- Discussion — opening sentence and closing paragraph's first sentence.
- Conclusion — final sentence.

## Rules

1. **Motivation-led where it reads naturally; logic-led where it doesn't.** If a neutral heading is clearer (e.g., "Robustness under distribution shift"), use the heading for the section's logical job and put the motivation in the opening sentence. Do not force the same keyword into every heading.

2. **Make the final Introduction paragraph a promise of what the Results will prove.** The first Discussion paragraph answers that exact promise. Both rows in the map reference each other.

3. **Pull from the prediction ledger.** The arc's surprises and disconfirmations are the most valuable material. At least one surface element (typically the Discussion opening, or the abstract's contribution sentence) should reflect what was *actually* learned, including from disconfirmations — not a sanitized version.

4. **Do not pad.** A row should be added only if the reader will measurably perceive that element. A topic sentence is a touchpoint; an interior sentence of a paragraph is not.

5. **Status discipline.** A row is `verified-in-final-paper` only after the assembled paper has been checked against the planned wording. This is part of the Phase 6 story-integrity gate.

## How It Feeds the Rationale Matrix

Every surface-map row maps to one or more rows in `writing-rationale-matrix.md`. The rationale matrix is the paragraph-level execution plan; the surface map is the higher-level wording-and-headings plan. Together they specify both *what each unit does* (matrix) and *what the reader sees at the seams* (surface map).

When dispatching a section-writer subagent, pass the surface-map rows for that section as explicit constraints — these are the sentences and headings the subagent is not free to change.

## Failure Mode: Generic Surface, Specific Body

The failure this map prevents: a paper whose body sections are sharp and specific, but whose title is generic ("A Novel Approach to X"), whose abstract opens with "Recent advances in X have…", whose Introduction topic sentences could appear in any paper on the topic, and whose Discussion ends with "We believe this opens exciting avenues for future research." The body teaches a reader; the surface fails to make them want to read it.

If the surface map is full of "TODO" or vague strategy notes ("emphasize novelty"), it has not been done. A real surface map contains real sentences for the highest-leverage elements (title, abstract opening, Introduction final paragraph, Discussion opening).
