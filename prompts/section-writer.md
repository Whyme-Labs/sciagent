# Section Writer — Subagent Prompt Template

Fill in all `[PLACEHOLDER]` fields before dispatching. Model: session default (writing from structured inputs). Dispatch independent sections in parallel; each writes its own file.

```
Agent tool:
  subagent_type: general-purpose
  description: "Write section: [SECTION_NAME]"
  prompt: |
    You are writing one section of a scientific research paper. You cannot ask questions mid-task: if the source material below is insufficient for this section, return Status: NEEDS_CONTEXT naming what is missing. Never fill gaps with invented content.

    ## Objective

    Write the **[SECTION_NAME]** section, to `paper/sections/[NN]-[SECTION_NAME].md`.

    ## Narrative Arc (THE SPINE — read this first)

    [PASTE THE FULL CONTENTS OF paper/narrative-arc.md — the 3-5 sentence story (tension → gap → insight (the named concept) → evidence → resolution) plus the journey: why this matters, why this approach and not alternatives, predictions and disconfirmations, load-bearing assumptions, what was tried and discarded]

    Your section must advance this arc — a reader should know, by the end of your section, why it was necessary for the story. Use the concept's name consistently. Serve the narrative, never contradict or sanitize it: the reader will read this paper for motivation and journey, not just method.

    ## Writing Rationale Matrix Rows (YOUR EXECUTION PLAN — constraints, not suggestions)

    [PASTE THE TABLE SLICE FROM paper/writing-rationale-matrix.md THAT COVERS THIS SECTION — every row that applies to a unit you will write]

    Each row tells you, for one manuscript unit: the planned function, which Idea-DNA component it serves, which exemplar pattern it transfers, which venue norm applies, the evidence anchor, the operation (REWRITE / SPLIT / MERGE / DELETE / MOVE / ADD / KEEP), and the Final Text Check the finished prose must satisfy.

    Your output must satisfy every row's Final Text Check. If a row says the paragraph reports a confidence interval, the paragraph reports a confidence interval. You are not free to drop, merge, or reorder rows — flag the issue and stop.

    ## Motivation Surface Map Cues (the sentences and headings you are NOT free to change)

    [PASTE THE ROWS FROM paper/motivation-surface-map.md FOR THIS SECTION — typically the section heading(s), opening sentence(s), closing sentence(s), and figure callouts.]

    These are the reader touchpoints the orchestrator has already committed to. Use the planned wording verbatim where it is concrete; respect the strategy where it is abstract.

    ## Claim-to-Source Rows (the evidential warrant for your claims)

    [PASTE THE ROWS FROM paper/claim-to-source.md THAT FALL IN THIS SECTION — claim, type, evidence, support grade, fact/interpretation/inference label]

    Two rules bind you here:
    - **Narrow the sentence to the source.** A `partial` support grade means the source supports LESS than the natural sentence — write the narrower sentence. A `background` grade motivates but never substantiates: no mechanism, method, or quantitative claim may rest on it.
    - **Match the hedge to the label.** `fact` states; `author-interpretation` attributes ("X et al. interpret this as…"); `our-inference` hedges ("we conjecture", "one interpretation is"). Results, interpretations, inferences, and recommendations each carry their own evidence strength — never flatten them into one confident register.

    ## Exemplar Move Tables (from Phase 1 decision archaeology)

    [PASTE THE MOVE-TABLE ROWS FROM THE DECISION-ARCHAEOLOGY LOG ENTRY THAT COVER THIS SECTION'S JOB]

    For each paragraph you write, the rationale matrix row points to a specific exemplar pattern. Use the move (the rhetorical job), not the exemplar's specific words. Treat the exemplar as a structural template, not a phrase bank.

    ## Paper Outline (for context)

    [PASTE THE FULL OUTLINE — title, all section headings, one-line description of each]

    ## Source Material

    [PASTE THE RELEVANT RESEARCH LOG CONTENT. Mapping:
    - Related Work: the literature-review entry (plus the Phase 6 fresh-pass additions)
    - Methodology: the CURRENT hypothesis entry (the latest superseding iteration file)
    - Experimental Setup: research-log/000-setup.md + experiments/configs/environment.md
    - Results: the analysis tables file + figures list
    - Discussion: the Phase 5 analysis + the prediction-ledger excerpt (predicted vs actual, signals) + ALWAYS the full tried_and_failed array and every results.tsv row, all statuses (failure evidence is never trimmed)
    - Introduction: PROBLEM.md + idea DNA + key findings summary
    - Conclusion: complete research journey summary
    If a source file exceeds ~3,000 words, the orchestrator pastes only the parts relevant to this section.]

    ## Known pitfalls in this project

    [PASTE ONLY THE PROMOTED learnings ENTRIES (recurrences >= 2) FROM state.json, EACH AS "lesson — apply when: <apply_when>", OR "None yet."]

    ## Boundaries

    - Write ONLY this section. Do not draft other sections or restructure the outline.
    - Every claim must be supported by a citation or experimental evidence present in the source material. If it isn't in the source material, it doesn't go in the section.
    - Cite papers as [Author et al., Year] using ONLY references that appear in the source material — never add citations from your own knowledge; they cannot be verified against the project's citation database.
    - **Connective-tissue rule:** when you link two facts ("X implies Y", "this explains why…", "consistent with…"), the LINK itself needs support: a source asserting it, our own experimental evidence, or explicit hedging as interpretation ("we conjecture", "one interpretation is"). Never present an inferred connection with the same confidence as a cited fact — unverifiable links between true facts are the signature failure of automated scientific writing.

    ## Style Guidelines

    - Academic tone, third person ("we propose", "the results show")
    - Precise: specific numbers, never "significant improvement" without the number
    - Honest: limitations stated plainly, no overselling
    - **Overclaim lexicon** — these words are banned unless literally earned: `prove` (unless a theorem is proved), `conclusively`, `unprecedented`, `best`, `superior`, `first`, `novel`, `paradigm`. Write `show/suggest`, `to our knowledge`, `stronger on [benchmark]` instead. Never upgrade an association into a causal verb; "significant" is a statistical statement, never a synonym for large or important
    - Figure references in your text must be interpretable from the legend alone — if your sentence relies on a mapping (color, marker, n) the legend doesn't carry, flag it
    - Notation defined on first use
    - **Resist the post-hoc narrative.** Do NOT rewrite the story so the conclusion looks inevitable. If the narrative arc says we predicted X and observed ¬X, the paper should reflect that — most explicitly in the Discussion, but the Introduction's framing must also be consistent with the actual journey.

    ## Section-Specific Instructions

    [CHOOSE THE BLOCK FOR SECTION_NAME:]

    **Related Work:** Organize by technique family, not chronologically. Per family: what's been tried, what works, what doesn't. Position our work: "Unlike [X] which…, we…". Be fair — no strawmanning.

    **Methodology:** Start with problem formulation (mathematical notation). Present the approach step by step. State all assumptions explicitly. Include proofs/derivations if they fit (otherwise note "see supplementary"). The reader should understand exactly what was done and why.

    **Experimental Setup:** Hardware, software and library versions; dataset source, size, splits, preprocessing; evaluation protocol with metric definitions; all hyperparameters with justification for non-obvious choices. A reader must be able to replicate from this section alone.

    **Results:** Clear tables; reference every figure by number ("as shown in Figure 1"); statistical significance where available; baseline comparisons with specific numbers; ablation results showing component contributions. Include negative results honestly labeled.

    **Discussion:** This section is where the journey lives — do NOT write a sanitized post-hoc narrative; use the narrative arc directly. **Predictions vs. reality** — pull from the prediction ledger: where were we right, wrong, surprised, and what did the gaps teach us about the model of the problem? **Disconfirmations as primary outputs** — every meaningful `disconfirm` or `partial` signal is candidate material; a disconfirmation with a clean explanation is more valuable than a confirmation we cannot fully explain. **Load-bearing assumptions** surfaced plainly as what a future reader should challenge. Connect to the theoretical justification — where evidence supported it and where it diverged. Limitations honest and specific, not boilerplate. Future work from what was actually learned, including dead ends.

    **Introduction:** Motivate the problem with the fire, not generic importance — why does this matter in the specific way it mattered to us (from the narrative arc)? Briefly surface **why this approach and not the alternatives** — the substantive decision, not just "we propose X." State the gap (drawing on the Phase 1 decision archaeology). Describe the approach (1 paragraph). Numbered contributions. Outline of the paper.

    **Abstract:** 150-300 words. Problem → approach → key result → significance. Include the most important metric number.

    **Conclusion:** Summarize contributions (brief, not an abstract repeat); practical implications; acknowledge what was tried and discarded (briefly), so readers can extract the substantive research, not just the polished claim; future work from actual findings (including dead ends), no generic filler.

    ## Report (your return message — keep under ~1,000 tokens; do NOT paste the section text)

    - **Status:** DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
    - **File written:** paper/sections/[NN]-[SECTION_NAME].md
    - **Word count:** N
    - **References used:** list of [Author, Year] citations included
    - **Figures referenced:** list of figure numbers/filenames
    - **Rationale-matrix row coverage:** per row in your slice: ✓ satisfied / ✗ unsatisfied with the reason. Any ✗ → status DONE_WITH_CONCERNS or BLOCKED
    - **Final Text Check verification:** for each row's check, quote the sentence(s) in your draft that satisfy it. If a check cannot be satisfied with the provided source material, surface it — do not invent evidence
    - **Flags:** any place where source material was thin and the text is correspondingly cautious
```
