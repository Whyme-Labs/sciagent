# Phase 2: Hypothesis Formation

Goal: a falsifiable hypothesis with complete, claim-type-appropriate justification that survives independent theory review. This is the hard gate that makes every confirmatory experiment scientifically justified.

## Steps

1. **Formulate the hypothesis** with all components:
   - **Claim** — precise, falsifiable ("We hypothesize that X will improve Y by Z because…"). For `analysis` projects: the explanation under test plus the enumerated rival explanations. For `reproduction` projects: the original's claims and the load-bearing assumptions you will stress.
   - **Independent variables** — what you're changing
   - **Dependent variables** — what you're measuring
   - **Controls** — what stays constant
   - **Expected effect** — directional prediction, with estimated magnitude if possible
   - **The pre-specified primary comparison** — which single comparison decides the headline claim (everything else is secondary/exploratory and will be labeled as such in the paper)

2. **Name and articulate the concept.** The hypothesis operationalizes a conceptual contribution — make that contribution an explicit artifact:
   - **Name it** — a short handle (two to five words) the paper and all logs will use consistently.
   - **State it in plain language** — one paragraph a researcher outside the subfield would understand.
   - **Define it formally** — the precise mathematical or operational definition the justification builds on.
   If you cannot write the plain-language paragraph, you have a technique, not a concept — and probably a stacking problem. This named concept becomes the spine of the paper's story in Phase 6.

3. **Provide justification appropriate to the claim type** (HARD GATE — cannot be skipped, but its currency matches the claim):
   - **Theoretical claims:** derive or cite the mathematical basis. Show the chain explicitly: "From [theorem A] in [Paper X]… combined with [finding B] from [Paper Y], this implies…". State ALL assumptions.
   - **Empirical/systems claims:** mechanistic reasoning (WHY should this work, causally?) + measurement design: what will be measured, threats to validity, the confound list and how each confound is controlled. Decorative equations that don't carry the argument are a defect, not rigor — the reviewer is instructed to flag mathiness.
   - **Dataset/benchmark claims:** construct-validity argument — why does this dataset measure what it claims to measure? Coverage rationale, contamination analysis, reliability plan (inter-annotator agreement or measurement repeatability).
   - **Engineering claims:** the profile artifact (measured bottleneck numbers, from a published profile or your own PoC measurement — existing NOW, not promised for Phase 4) + per-component mechanism.
   In all cases: cited prior work, explicit assumptions, no "it might work." Demand depth of yourself before the reviewer does: reason in the right lens (a matrix as a transformation of space, a problem mapped into an easier space, error controlled rather than exact solutions chased), bind every symbol to a concrete meaning, state each assumption's validity domain, and unpack dense notation rather than skipping it — `reference/mathematical-thinking.md` is the lens catalog. Hollow math that looks rigorous is worse than honest hand-waving.

4. **Predict failure modes:** what could go wrong; under what conditions the justification breaks; what result would **disprove** the hypothesis; what would be inconclusive vs. conclusive.

5. **Define metrics:** primary metric, secondary metrics, baseline numbers to beat (from Phase 1), and concrete thresholds — what number = success, what number = failure — in units of the measured seed variance where available.

6. **Anti-stacking check** (empirical projects only; the tests from SKILL.md):
   - **Reframing/extrapolation hypothesis:** state at least one testable prediction this framing makes that a plain combination of the same components would NOT make. Write it down — it becomes an experiment in Phase 4. No differing prediction = stacking; go back to step 1.
   - **Engineering hypothesis:** all three engineering tests documented — a named bottleneck per component *with its measured number and source*, a planned per-component ablation, and a contribution claim that is the end-to-end system result under a stated constraint. Any test unmet = stacking; go back to step 1.

7. **Self-critique** (advisory — the theory reviewer is the real gate, but fix what you can first): Is it falsifiable? Is the justification sound (re-derive the math / re-walk the causal chain)? Any logical leaps? Does it still serve `PROBLEM.md`, or has it drifted?

8. **Write the full hypothesis entry** to `research-log/[NNN]-hypothesis-iter-[X].md` BEFORE dispatching review. **Once the theory review is dispatched, this entry is immutable** — post-PoC or post-data revisions are NEW entries marked "Supersedes: [previous]", never edits in place. The predicted-vs-postdicted distinction must survive in the record; the paper will disclose how many hypothesis iterations were attempted.

9. **Dispatch theory reviewer subagent** (most capable model available). Use `prompts/theory-reviewer.md`. The dispatch is **sterile** (SKILL.md Dispatch Contract): template content only, no framing or assurances. The reviewer reads the hypothesis entry **from disk** at the path you give it and reports the file's line count; VERIFY that count against `git show HEAD:<path> | wc -l`.

   **Accounting (hard rules):** increment `hypothesis_review_rounds.spent` at dispatch time, every dispatch, regardless of verdict. Log every verdict verbatim in the research log BEFORE any re-dispatch. An adverse verdict can never be declared invalid; a passing verdict without scrutiny evidence is invalid and may be re-dispatched at most once for that round.

   Handle the blind assessment:
   - **RIGOROUS** (with scrutiny evidence) — proceed to Phase 3.
   - **NEEDS_REVISION** — write a new superseding hypothesis entry using the coaching, re-dispatch. On re-review, include the previous issue list; the reviewer judges each issue RESOLVED/IMPROVED/UNCHANGED/WORSE. Budget: 2 rounds, then escalate to the user with the hypothesis and the unresolved objections.
   - **FUNDAMENTALLY_FLAWED** — record in `tried_and_failed` (`failure_class: refuted` only if the flaw is in the idea, not your write-up), rethink; consider looping to Phase 1.

## Gate (record evidence in `state.json.gates["2"]`)

- [ ] Hypothesis falsifiable, with defined variables, controls, and the pre-specified primary comparison
- [ ] Concept named, stated in plain language, and formally defined
- [ ] Claim-type-appropriate justification complete with citations (for engineering: profile artifact with numbers exists now)
- [ ] Failure modes identified
- [ ] Metrics defined with concrete thresholds
- [ ] Anti-stacking check passed: distinguishing prediction written down, OR all three engineering tests evidenced (empirical projects; N/A for other project types)
- [ ] Problem alignment: one line stating how confirming this hypothesis would answer `PROBLEM.md`'s core question
- [ ] Theory reviewer verdict RIGOROUS with evidence of scrutiny; all dispatches counted and all verdicts logged

## Outputs

- Research log: `research-log/[NNN]-hypothesis-iter-[X].md` — immutable once reviewed; revisions are new superseding entries
- Commit: `research: hypothesis — [one-line claim summary]`
