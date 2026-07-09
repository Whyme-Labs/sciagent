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

    ## The Paper's Story

    [PASTE THE 3-5 SENTENCE NARRATIVE ARC FROM PHASE 6 STEP 1: tension → gap → insight (the named concept) → evidence → resolution]

    Your section must advance this arc — a reader should know, by the end of your section, why it was necessary for the story. Use the concept's name consistently.

    ## Paper Outline (for context)

    [PASTE THE FULL OUTLINE — title, all section headings, one-line description of each]

    ## Source Material

    [PASTE THE RELEVANT RESEARCH LOG CONTENT. Mapping:
    - Related Work: the literature-review entry (plus the Phase 6 fresh-pass additions)
    - Methodology: the CURRENT hypothesis entry (the latest superseding iteration file)
    - Experimental Setup: research-log/000-setup.md + experiments/configs/environment.md
    - Results: the analysis tables file + figures list
    - Discussion: the Phase 5 analysis + ALWAYS the full tried_and_failed array and every results.tsv row, all statuses (failure evidence is never trimmed)
    - Introduction: PROBLEM.md + idea DNA + key findings summary
    - Conclusion: complete research journey summary
    If a source file exceeds ~3,000 words, the orchestrator pastes only the parts relevant to this section.]

    ## Boundaries

    - Write ONLY this section. Do not draft other sections or restructure the outline.
    - Every claim must be supported by a citation or experimental evidence present in the source material. If it isn't in the source material, it doesn't go in the section.
    - Cite papers as [Author et al., Year] using ONLY references that appear in the source material — never add citations from your own knowledge; they cannot be verified against the project's citation database.
    - **Connective-tissue rule:** when you link two facts ("X implies Y", "this explains why…", "consistent with…"), the LINK itself needs support: a source asserting it, our own experimental evidence, or explicit hedging as interpretation ("we conjecture", "one interpretation is"). Never present an inferred connection with the same confidence as a cited fact — unverifiable links between true facts are the signature failure of automated scientific writing.

    ## Style Guidelines

    - Academic tone, third person ("we propose", "the results show")
    - Precise: specific numbers, never "significant improvement" without the number
    - Honest: limitations stated plainly, no overselling
    - Notation defined on first use

    ## Section-Specific Instructions

    [CHOOSE THE BLOCK FOR SECTION_NAME:]

    **Related Work:** Organize by technique family, not chronologically. Per family: what's been tried, what works, what doesn't. Position our work: "Unlike [X] which…, we…". Be fair — no strawmanning.

    **Methodology:** Start with problem formulation (mathematical notation). Present the approach step by step. State all assumptions explicitly. Include proofs/derivations if they fit (otherwise note "see supplementary"). The reader should understand exactly what was done and why.

    **Experimental Setup:** Hardware, software and library versions; dataset source, size, splits, preprocessing; evaluation protocol with metric definitions; all hyperparameters with justification for non-obvious choices. A reader must be able to replicate from this section alone.

    **Results:** Clear tables; reference every figure by number ("as shown in Figure 1"); statistical significance where available; baseline comparisons with specific numbers; ablation results showing component contributions. Include negative results honestly labeled.

    **Discussion:** Interpret results — why did things work or not? Connect back to the theoretical justification. Limitations honest and specific. Unexpected findings and what they might mean. Future work grounded in what was actually learned.

    **Introduction:** Motivate the problem; state the gap; describe the approach (1 paragraph); numbered contributions; outline of the paper.

    **Abstract:** 150-300 words. Problem → approach → key result → significance. Include the most important metric number.

    **Conclusion:** Summarize contributions (brief, not an abstract repeat); practical implications; future work from actual findings, no generic filler.

    ## Report (your return message — keep under ~1,000 tokens; do NOT paste the section text)

    - **Status:** DONE / NEEDS_CONTEXT
    - **File written:** paper/sections/[NN]-[SECTION_NAME].md
    - **Word count:** N
    - **References used:** list of [Author, Year] citations included
    - **Figures referenced:** list of figure numbers/filenames
    - **Flags:** any place where source material was thin and the text is correspondingly cautious
```
