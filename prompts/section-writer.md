# Section Writer — Subagent Prompt Template

Use this template when dispatching a section writer subagent. Fill in all `[PLACEHOLDER]` fields before dispatching.

```
Agent tool:
  subagent_type: general-purpose
  model: sonnet
  description: "Write section: [SECTION_NAME]"
  prompt: |
    You are writing one section of a scientific research paper.

    ## Section to Write

    **[SECTION_NAME]**

    ## Narrative Arc (THE SPINE — read this first)

    [PASTE THE FULL CONTENTS OF paper/narrative-arc.md — covers: the fire / why this matters, why this approach and not alternatives, the journey including predictions and disconfirmations, load-bearing assumptions, what was tried and discarded]

    Your section must serve this narrative arc, not contradict or sanitize it. The reader will read this paper for motivation and journey, not just method — so write the version they would *want* to extract.

    ## Paper Outline (for context)

    [PASTE THE FULL PAPER OUTLINE — title, all section headings, brief description of each]

    ## Source Material

    [PASTE THE RELEVANT RESEARCH LOG CONTENT FOR THIS SECTION. Examples:
    - For Related Work: paste research-log/001-literature-review.md
    - For Methodology: paste research-log/002-hypothesis.md
    - For Experimental Setup: paste research-log/000-setup.md + experiments/configs/environment.md
    - For Results: paste the results analyzer output + figures list
    - For Discussion: paste the analysis from Phase 5
    - For Introduction: paste the idea DNA + key findings summary
    - For Conclusion: paste the complete research journey summary]

    ## Style Guidelines

    - Academic tone, third person ("we propose", "the results show")
    - Cite papers as [Author et al., Year] — use the exact references from the source material
    - Be precise: use specific numbers, not "significant improvement"
    - Be honest: state limitations plainly, do not oversell
    - Notation must be defined on first use
    - Every claim must be supported by a citation or experimental evidence from the source material
    - **Resist the post-hoc narrative.** Do NOT rewrite the story so the conclusion looks inevitable. If the narrative arc says we predicted X and observed ¬X, the paper should reflect that — most explicitly in the Discussion, but the Introduction's framing should also be consistent with the actual journey.

    ## Section-Specific Instructions

    [CHOOSE THE APPROPRIATE BLOCK BASED ON SECTION_NAME:]

    **If Related Work:**
    - Organize by technique family, not chronologically
    - For each family: what's been tried, what works, what doesn't
    - Position our work: "Unlike [X] which..., we..."
    - Be fair — do not strawman prior work to make ours look better

    **If Methodology:**
    - Start with problem formulation (mathematical notation)
    - Present the approach step by step
    - State all assumptions explicitly
    - Include proofs or derivations if they fit (otherwise note "see supplementary")
    - The reader should understand exactly what you did and why

    **If Experimental Setup:**
    - Hardware, software versions, library versions — everything needed to reproduce
    - Dataset description: source, size, splits, preprocessing
    - Evaluation protocol: metric definitions, how computed, what constitutes success
    - Hyperparameters: all of them, with justification for non-obvious choices
    - The goal: a reader should be able to replicate from this section alone

    **If Results:**
    - Present results tables with clear formatting
    - Reference all figures by number ("as shown in Figure 1")
    - Report statistical significance where available
    - Compare against baselines with specific numbers
    - Present ablation results to show component contributions

    **If Discussion:**
    - This section is where the journey lives — do NOT write a sanitized post-hoc narrative. Use the narrative arc directly.
    - **Predictions vs. reality** — pull from the prediction ledger excerpt: where were we right, where were we wrong, where were we surprised? What did the gaps teach us about the model of the problem?
    - **Disconfirmations as primary outputs** — every meaningful `disconfirm` or `partial` signal in the source material is candidate material. A disconfirmation we have a clean explanation for is more valuable than a confirmation we cannot fully explain.
    - **Load-bearing assumptions** — surface them plainly as the assumptions a future reader should challenge.
    - **Connect to theoretical justification** — where the empirical evidence supported the theory, and where it diverged.
    - **State limitations honestly and specifically** — not boilerplate.
    - **Future work** — based on what we actually learned (including from dead ends), not generic filler.

    **If Introduction:**
    - **Motivate the problem with the fire, not generic importance** — why does this matter in the specific way it mattered to us? Pull from the narrative arc.
    - **Why this approach and not the alternatives** — briefly surface the substantive decision, not just "we propose X."
    - State the gap (what's missing in current approaches, drawing on the decision-archaeology from Phase 1)
    - Describe our approach (1 paragraph)
    - List numbered contributions
    - Outline the rest of the paper

    **If Abstract:**
    - 150-300 words
    - Structure: problem → approach → key result → significance
    - Include the most important metric number

    **If Conclusion:**
    - Summarize contributions (brief, not a repeat of the abstract)
    - State practical implications
    - Acknowledge what was tried and discarded (briefly), so readers can extract the substantive research, not just the polished claim
    - Future work based on actual findings (including from dead ends), not generic filler

    ## Report

    - **Status:** DONE
    - **Section text:** (the full section text in Markdown)
    - **References used:** (list of [Author, Year] citations included)
    - **Figures referenced:** (list of figure numbers/filenames referenced)
```
