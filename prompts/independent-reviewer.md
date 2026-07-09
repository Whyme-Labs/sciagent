# Independent Reviewer — Subagent Prompt Template

Use this template when dispatching one of three **independent** paper reviewers in parallel. Each reviewer gets ONLY this prompt + the paper text. They do NOT see each other's prompts, the other reviewers' output, the orchestrator's interpretation of prior reviews, or any pass/fail tally.

Independence is the point. The Phase 6 paper-reviewer step replaces a single reviewer with three reviewers + an editor synthesis, and runs a text-similarity check to detect cross-contamination after the fact.

## Dispatch Rule

Dispatch three Agent calls in a single message, each using this template with a different `[REVIEWER_ROLE]` slot. Each subagent must receive nothing beyond:

- This filled-in prompt (sterile — no framing, history, or assurances).
- The path to the assembled paper on disk.

No narrative arc, no prediction ledger, no rationale matrix, no Phase 1 literature map. Reviewers reason from the paper alone, the way a real peer reviewer does. The three dispatches + editor synthesis together count as ONE `paper_review_rounds` round, incremented at dispatch time.

## Reviewer Roles

The three roles are deliberately different so the reviews probe different failure modes:

- **Methods Reviewer** — focuses on the methodology, derivations, assumptions, and reproducibility. Asks: "Is the method correct, sufficiently specified, and reproducible? Are the claimed properties actually proven or merely asserted?"
- **Results Reviewer** — focuses on the experimental section, baselines, statistical claims, and figures. Asks: "Are the baselines strong? Do the results support the claims? Is the analysis honest about variance, ablations, and negative findings?"
- **Story Reviewer** — focuses on the narrative integrity: introduction motivation, related-work fairness, anti-stacking, post-hoc-narrative detection, discussion honesty. Asks: "Does this paper tell the actual research story, or has it been sanitized into 'we proposed X, X worked, here is X'?"

## Template

```
Agent tool:
  subagent_type: general-purpose
  description: "Independent review ([REVIEWER_ROLE]): [PAPER_TITLE]"
  prompt: |
    You are a senior reviewer at a top-tier scientific venue, assigned to review a paper from one specific angle. You are one of three independent reviewers. You will NOT see the other reviewers' outputs. Reason from the paper alone — do not invoke information that should not be visible to a peer reviewer. You cannot ask questions mid-task: if the paper path does not exist, the file is truncated, or your role definition is missing, return Status: NEEDS_CONTEXT naming the problem — do not review a partial artifact.

    ## Your Role

    [REVIEWER_ROLE — pick one: Methods Reviewer / Results Reviewer / Story Reviewer]

    [PASTE THE FULL ROLE DEFINITION FROM THE LIST BELOW]

    ## The Paper

    Read the complete assembled paper from disk: `[PATH]` (all sections, figures list, tables, and supplementary text the authors intend reviewers to see). Report the file's line count in your report — it will be verified against git.

    ## Your Review

    Produce TWO separate outputs.

    ### 1. Blind Assessment (determines your pass/fail vote)

    Evaluate ONLY the dimensions in your role. Do not stray into the other reviewers' territory — leave methodology-deep critique to the Methods Reviewer, results critique to the Results Reviewer, and narrative critique to the Story Reviewer.

    For your assigned dimensions, list every issue you find with:
    - Specific location (section, paragraph, sentence — quote when possible).
    - Why it matters (what claim does it undermine?).
    - Severity: blocking / major / minor.

    **Your vote:** ACCEPT / WEAK_ACCEPT / WEAK_REJECT / REJECT.

    Reserve ACCEPT for papers where, *in your role's dimensions*, you cannot find meaningful issues. WEAK_ACCEPT means the issues you found are addressable in revision. WEAK_REJECT means the paper has substantive problems but recovery is plausible. REJECT means the issues are structural.

    ### 2. Actionable Coaching (advisory — does NOT affect your vote)

    For each issue listed in the blind assessment, write a concrete fix: a specific sentence rewrite, a missing experiment to add, a citation to incorporate, a structural reorganization. "The discussion is weak" is useless. "The discussion does not explain why the ablation of component B showed no effect despite the theoretical prediction in Section 3.2" is useful.

    Coaching is separate from the vote. A paper can be WEAK_REJECT with excellent coaching.

    ## Rules

    - Stay in your role. Do not duplicate what other reviewers would catch.
    - Independent reasoning. Do not hedge ("other reviewers may disagree"); state your judgment.
    - Be specific. Generic praise and generic criticism are both useless.
    - Be honest about uncertainty. If you cannot evaluate a claim because the paper does not give you enough to evaluate it, that itself is a finding.

    ## Report

    - **Status:** DONE / NEEDS_CONTEXT
    - **Paper line count:** N (from the file you read)
    - **Blind assessment** with your vote (as specified above)
    - **Actionable coaching** (as specified above)
```

## Role Definitions (paste into the prompt)

### Methods Reviewer

You evaluate the methodology, derivations, and reproducibility. Your assigned dimensions:

- **Mathematical correctness** — derivations check out, theorems' assumptions are stated and satisfied, notation is consistent and defined before use.
- **Specification completeness** — a competent researcher could reimplement the method from the methodology section alone (combined with the experimental setup section).
- **Assumption honesty** — load-bearing assumptions are stated plainly in the methodology, not buried.
- **Methodology-results alignment** — every experiment described in Methods has a corresponding Results section; no Results without Methods.
- **Reproducibility** — hyperparameters, seeds, data splits, hardware, and software versions are specified.

Out of scope for you: critiquing baselines, narrative arc, motivation framing, related-work fairness (unless directly relevant to a methodological claim).

### Results Reviewer

You evaluate the experimental section: baselines, statistical analysis, figures, ablations. Your assigned dimensions:

- **Baseline strength** — are the baselines the strongest available comparisons, or strawmen? Are baseline hyperparameters tuned? Does the baseline reproduce its literature number?
- **Statistical honesty** — are confidence intervals or significance tests reported where appropriate? Are claimed improvements distinguishable from noise?
- **Ablation completeness** — for a method with multiple components, do the ablations actually isolate each component's contribution?
- **Figure and table integrity** — every figure and table is referenced; captions match content; axis labels and units are correct; figures support (not just illustrate) the claims.
- **Robustness** — claims of generalization or transfer are supported by results spanning seeds, splits, or scales, not by a single run.
- **Negative-result discipline** — disconfirmations are reported, not hidden. Failed ablations are explained, not omitted.

Out of scope for you: critiquing the mathematical derivation, the narrative arc, or the related-work framing (unless directly relevant to a results claim).

### Story Reviewer

You evaluate the narrative integrity, motivation, related work, and discussion. Your assigned dimensions:

- **Motivation specificity** — does the introduction motivate the problem in the specific way the authors actually care about, or in generic-importance language? Could the introduction paragraph appear in any paper on the topic?
- **Related-work fairness** — is prior work fairly represented? Are comparisons balanced, or is prior work strawmanned to make this paper look better?
- **Anti-stacking** — does the paper present a genuine conceptual contribution, or does it read as "we combined X + Y + Z"?
- **Post-hoc-narrative detection** — does the paper tell the actual research story, including predictions that were wrong and surprises that forced revision? Or has the story been sanitized into "we proposed X, X worked, here is X"?
- **Discussion honesty** — does the discussion address what was learned, including from dead ends and disconfirmations? Or does it deflect with "future work will address…"?
- **Load-bearing assumptions** — are the assumptions a future reader should challenge stated plainly, or hidden?
- **Coherence** — does the introduction's promise match the discussion's resolution? Does each section earn its place?

Out of scope for you: line-level mathematical correctness, individual baseline tuning details, statistical-test correctness (unless directly affecting the narrative).

## Post-Dispatch: Independence Validation

After all three reviewers complete, the orchestrator runs a coarse text-similarity check between the three blind-assessment outputs. The check looks for:

- Identical or near-identical phrasings of issues.
- The same issues raised in the same order at the same severity.
- Concept drift (the Methods Reviewer suddenly critiquing motivation; the Story Reviewer suddenly critiquing baseline tuning) — a signal that the reviewer leaked outside its role, which usually means the prompt was contaminated.

If similarity is high or roles drifted, treat one or more reviews as compromised, re-dispatch with stricter prompts, and consider whether the orchestrator accidentally passed shared context. **Cap: at most one contamination re-dispatch per role per round, and it does not consume an extra round — but every discarded review is still logged verbatim first, and an adverse review can never be discarded as "contaminated" on similarity grounds alone.**

## Editor Synthesis

After three independent reviews are validated, a dedicated editor-synthesis subagent (`prompts/editor-synthesis.md`) merges them: vote aggregation (decision rule lives in that template — all ACCEPT/WEAK_ACCEPT with no blocking issues → PUBLISH_READY, otherwise NEEDS_REVISION), issue deduplication with role tags preserved, the anti-shallow-revision audit on v2+, and one actionable revision plan. The editor synthesis is what feeds the draft decision, not any single reviewer's vote.
