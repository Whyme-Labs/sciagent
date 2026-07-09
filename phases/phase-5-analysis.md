# Phase 5: Analysis & Iteration

Goal: statistically honest analysis, then a budgeted, evidence-based decision — iterate, pivot, or conclude, and if concluding, an explicit publish decision. The budgets decide when to stop; you decide what the evidence means.

## Steps

1. **Dispatch results analyzer subagent.** Use `prompts/results-analyzer.md`. The analyzer reads `results.tsv` from disk (and reports its row count — VERIFY against `wc -l results.tsv`), excludes `status=crash`, `status=discard`, and `status=exploratory` rows from all rankings and statistics, computes effect sizes and discloses the comparison family, writes tables to `research-log/[NNN]-analysis-iter-[X]-tables.md` and figures to `paper/figures/`, and returns a summary.

2. **VERIFY the analyzer's output:** figures exist on disk at the reported paths; headline numbers match `results.tsv`; no crashed/discarded/exploratory run appears in any ranking; row count matches. **Recompute the statistical claim attached to the headline comparison yourself** (not one of your choosing — THE headline one) and paste the recomputation as evidence.

3. **Deep analysis — answer each question explicitly (all seven required to conclude):**
   - **Did it work?** Does the pre-specified primary comparison meet the success threshold, at N ≥ 3 seeds, with the effect size in units of seed variance?
   - **Why did it work (or not)?** Does the empirical evidence support the Phase 2 justification?
   - **What contributed most?** Which components mattered in ablations? Did the distinguishing prediction hold?
   - **How robust is it?** Consistent across seeds, splits, scales, generalization benchmarks? **Where does it fail?** — error analysis on concrete failure cases is required, not just aggregate numbers.
   - **What was surprising?** Read the prediction ledger's `signal` column: every `disconfirm` and `partial` is primary material — where were the predictions wrong, and what does each gap teach about the model of the problem? Any `null` signals mean wasted runs — fix the design pattern. (A surprise may trigger a targeted literature query — 1 searcher, ≤ 5 papers, verified as usual.)
   - **How does it compare to literature?** Position against Phase 1 baselines — including the TUNED baseline, at matched compute.
   - **Does it solve the problem?** Re-read `PROBLEM.md`. The metric is a proxy — does this result advance the core question at the stated scope, or only the proxy? If only the proxy, say so plainly; that changes the path decision and the paper's claims.

4. **Freshness check (each iteration):** one narrow searcher query on the exact claim — has competing work appeared since Phase 1? New competing work → escalate as a potential pivot/invalidation trigger.

5. **Check the budgets** (mechanical — read them from `state.json`, don't reason about whether they apply):
   - `research_iterations.spent >= limit` → conclude (remember: ANY re-entry into Phases 1-4, iterate or pivot, consumes an iteration)
   - Diminishing returns: last 2 *metric-targeting* iterations improved the primary metric by < 1% relative (in seed-std-dev units where available) → recommend conclude. Understanding-iterations (error analysis, rival-explanation elimination) don't count against this — they improve the paper, not the metric.
   - Validation-overfitting check: gains on the tuning signal not reflected on the validation tier → you are optimizing the proxy; flag it.

6. **Decide the path:**
   - **Path A: Iterate** — promising results with a clear evidence-based next step. State what you'll try AND why, citing this analysis — and how the next step serves `PROBLEM.md`'s core question, not just the metric. An iteration that only chases the proxy is drift; flag it instead of taking it. Increment `iteration`, enqueue Phase 2 tasks, loop back to Phase 2.
   - **Path B: Pivot** — hypothesis disproved but evidence reveals a new direction. Document what was learned; append the old direction to `tried_and_failed` (honest `failure_class`); propose the new direction with justification. Consumes an iteration. Requires user approval (quoted). Loop to Phase 1 or 2. If `PROBLEM.md` itself is invalidated, use the Invalidation procedure from SKILL.md instead.
   - **Path C: Conclude** — success criteria met, diminishing returns, or budget exhausted. Then:
     1. **Run the locked test set — exactly once** (empirical projects). Log it as an irreversible event in `state.json` with command + output. These become the paper's headline numbers; validation numbers become tuning history.
     2. **Publish decision** — present three outcomes to the user, and **argue against publishing first** (steelman the no-paper option; every upstream pressure argues for it):
        - (a) **Contribution paper** — the evidence supports the claims at venue standards.
        - (b) **Negative-result / lessons paper** — only if the negative result is statistically conclusive (well-powered, tuned baselines, seeds); an underpowered null is not a publishable negative result.
        - (c) **Internal technical report** — valuable learning, insufficient evidence for either paper type. No submission.
     3. On (a) or (b) with user approval (quoted): proceed to Phase 6. On (c): write the report from the research logs and close the cycle.

7. **Checkpoint with user** — present the analysis, budget status (iterations/compute/time remaining), retryable `implementation_defeated` entries from `tried_and_failed` (as options), and your recommended path. Wait for approval (quoted).

## Gate (record evidence in `state.json.gates["5"]`)

- [ ] All seven analysis questions answered explicitly (including error analysis and problem alignment)
- [ ] Analyzer output verified (figures exist, numbers match, row count matches, exclusions respected)
- [ ] Headline statistical claim recomputed by the orchestrator (evidence: the recomputation)
- [ ] Freshness check done
- [ ] Budget check performed and recorded
- [ ] If concluding: test set run exactly once (logged), publish decision made with the no-publish option steelmanned
- [ ] User approved the path decision (quoted verbatim)

## Outputs

- Research log: `research-log/[NNN]-analysis-iter-[X].md` — results table, statistical tests, figure list, seven answers, path decision and rationale, Gate Check
- Commit: `research: analysis iter [X] — [iterate/pivot/conclude], [headline finding]`
