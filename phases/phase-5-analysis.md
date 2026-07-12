# Phase 5: Analysis & Iteration

Goal: statistically honest analysis, then a budgeted, evidence-based decision — iterate, pivot, or conclude, and if concluding, an explicit publish decision. The budgets decide when to stop; you decide what the evidence means.

## Steps

1. **Dispatch results analyzer subagent.** Use `prompts/results-analyzer.md`. The analyzer reads `results.tsv` from disk (and reports its row count — VERIFY against `wc -l results.tsv`), excludes `status=crash`, `status=discard`, and `status=exploratory` rows from all rankings and statistics, opens with the **statistical declaration block** (`reference/statistical-rigor.md`: independent unit, n, comparison family, correction), computes effect sizes, writes tables to `research-log/[NNN]-analysis-iter-[X]-tables.md` and figures (to the `reference/figure-spec.md` house spec) to `paper/figures/`, and returns a summary.

2. **VERIFY the analyzer's output:** figures exist on disk at the reported paths and pass the figure QA contract (`reference/figure-spec.md` §7 — SVG+PNG+source-csv present, editable text, legend carries n/error-type/test); headline numbers match `results.tsv`; no crashed/discarded/exploratory run appears in any ranking; row count matches; **the declaration block is present and its `n_units` matches the seed rows actually in the ledger** — an analysis whose n counts anything other than independent units (seeds/folds) is rejected, not corrected in place. **Recompute the statistical claim attached to the headline comparison yourself** (not one of your choosing — THE headline one) and paste the recomputation as evidence. Run the `reference/statistical-rigor.md` final checklist; any P0 item failing (pseudoreplication, undeclared family, significance-difference-as-difference inference, unpaired test on a paired design) blocks this phase's gate.

3. **Deep analysis — answer each question explicitly (all seven required to conclude):**
   - **Did it work?** Does the pre-specified primary comparison meet the success threshold, at N ≥ 3 seeds, with the effect size in units of seed variance?
   - **Why did it work (or not)?** Does the empirical evidence support the Phase 2 justification?
   - **What contributed most?** Which components mattered in ablations? Did the distinguishing prediction hold?
   - **How robust is it?** Consistent across seeds, splits, scales, generalization benchmarks? **Where does it fail?** — error analysis on concrete failure cases is required, not just aggregate numbers.
   - **What was surprising?** Read the prediction ledger's `signal` column: every `disconfirm` and `partial` is primary material — where were the predictions wrong, and what does each gap teach about the model of the problem? Any `null` signals mean wasted runs — fix the design pattern. (A surprise may trigger a targeted literature query — 1 searcher, ≤ 5 papers, verified as usual.)
   - **How does it compare to literature?** Position against Phase 1 baselines — including the TUNED baseline, at matched compute.
   - **Does it solve the problem?** Re-read `PROBLEM.md`. The metric is a proxy — does this result advance the core question at the stated scope, or only the proxy? If only the proxy, say so plainly; that changes the path decision and the paper's claims.

4. **Freshness check (each iteration):** one narrow searcher query on the exact claim — has competing work appeared since Phase 1? New competing work → escalate as a potential pivot/invalidation trigger.

5. **Search diagnosis (mechanical — SKILL.md: Search Diagnosis and Strategy Escalation).** Compute from `results.tsv` and `search_log`, and record the tables in the analysis log. Project-type substitutions: non-empirical types compute the ledger-derived rows only where a prediction ledger exists; for `theoretical` projects a proof-targeting entry counts as `kind: metric` and "`best_state` improvement" means a claims-ledger claim moving to proved or disproved.
   - **`kind` audit first** — reclassify before computing anything: an iteration whose `results.tsv` rows include a primary-metric row predicted to beat the baseline, or that updated `best_state`, is `kind: metric` regardless of its label; log any reclassification.
   - Keep / discard / crash / exploratory counts, this iteration and cumulative; the keep-rate trend.
   - **Null-signal count** — from the ledger's `signal` column; each null is a design failure (the design fix is step 3's job; the count belongs in this table).
   - **Calibration table** — confirm rate by stated `confidence` tier (high/medium/low). A `high` tier confirming below ~50% means the predictions are mis-calibrated — say so in the log and distrust the next round of confidence labels accordingly.
   - **Per-dimension table** — for each `varies` value in `search_log` with `kind: metric`: iterations spent, `best_state` improvements produced.
   - Fill this iteration's `outcome` in `search_log`: `improved | no_gain | refuted | inconclusive`.
   - **Verdict: healthy or stalled.** Healthy = `best_state` improved within the work of the last 2 `kind: metric` entries; stalled = it didn't (fewer than 2 such entries = healthy by default). Record the verdict. A stalled verdict activates the escalation check in Path A. The response to any diagnosis is binary — nothing (healthy) or a structural move (stalled); never process tweaks.

6. **Check the budgets** (mechanical — read them from `state.json`, don't reason about whether they apply):
   - `research_iterations.spent >= limit` → conclude (remember: ANY re-entry into Phases 1-4, iterate or pivot, consumes an iteration)
   - Diminishing returns: last 2 *metric-targeting* iterations (= `kind: metric` in `search_log`, post-audit) improved the primary metric by < 1% relative (in seed-std-dev units where available) → recommend conclude. Understanding-iterations (`kind: understanding` — error analysis, rival-explanation elimination) don't count against this — they improve the paper, not the metric.
   - Validation-overfitting check: gains on the tuning signal not reflected on the validation tier → you are optimizing the proxy; flag it.

7. **Decide the path:**
   - **Path A: Iterate** — promising results with a clear evidence-based next step. State what you'll try AND why, citing this analysis — and how the next step serves `PROBLEM.md`'s core question, not just the metric. An iteration that only chases the proxy is drift; flag it instead of taking it. Two additional mechanical checks:
     - **Escalation check (stalled verdict only):** if the last 2 `kind: metric` entries in `search_log` share the same `varies` dimension (the escalation trigger), the next `kind: metric` hypothesis MUST target a dimension not yet present among `search_log`'s `kind: metric` entries (a `parked_candidate` attacking a fresh dimension counts; a sub-slice of the stalled dimension does not; a genuine `kind: understanding` iteration on the stalled dimension remains legal, subject to the `kind` audit). Write the constraint — the stalled dimension and the full used-dimension list — into the enqueued Phase 2 task description; Phase 2 gates on it and the theory reviewer verifies it. If no untouched dimension is plausible, Path A is off the table; argue B or C instead. A stalled verdict without the same-dimension trigger imposes no dimension constraint. Note a fired trigger implies the diminishing-returns rule fired too (step 6) — the recommendation at the checkpoint stays conclude, with the fresh-dimension iteration presented as the alternative.
     - **Rubric when alternatives exist:** if more than one candidate next step is on the table (including retryable `implementation_defeated` entries and `parked_candidates`), apply the Candidate Critique Rubric (SKILL.md): failure mode, implementation trap, evidence check, and score per candidate; select citing the scores; log one-line rejection reasons.

     Then increment `iteration`, enqueue Phase 2 tasks, loop back to Phase 2.
   - **Path B: Pivot** — hypothesis disproved but evidence reveals a new direction. Document what was learned; append the old direction to `tried_and_failed` (honest `failure_class`); propose the new direction with justification. Consumes an iteration. Requires user approval (quoted). Loop to Phase 1 or 2. If `PROBLEM.md` itself is invalidated, use the Invalidation procedure from SKILL.md instead.
   - **Path C: Conclude** — success criteria met, diminishing returns, or budget exhausted. Then:
     1. **Run the locked test set — exactly once** (empirical projects). Log it as an irreversible event in `state.json` with command + output. These become the paper's headline numbers; validation numbers become tuning history.
     2. **Publish decision** — present three outcomes to the user, and **argue against publishing first** (steelman the no-paper option; every upstream pressure argues for it):
        - (a) **Contribution paper** — the evidence supports the claims at venue standards.
        - (b) **Negative-result / lessons paper** — only if the negative result is statistically conclusive (well-powered, tuned baselines, seeds); an underpowered null is not a publishable negative result.
        - (c) **Internal technical report** — valuable learning, insufficient evidence for either paper type. No submission.
     3. On (a) or (b) with user approval (quoted): proceed to Phase 6. On (c): write the report from the research logs.
     4. **Enqueue the cycle retrospective** (SKILL.md — Skill Retrospective): on (a)/(b) it runs as the final task after Phase 6 delivery; on (c) it runs immediately after the internal report. The cycle does not close without it.

8. **Checkpoint with user** — present the analysis, the search-diagnosis verdict and calibration table, budget status (iterations/compute/time remaining), retryable `implementation_defeated` entries from `tried_and_failed` (as options), and your recommended path. Wait for approval (quoted).

## Gate (record evidence in `state.json.gates["5"]`)

- [ ] All seven analysis questions answered explicitly (including error analysis and problem alignment)
- [ ] Analyzer output verified (figures exist and pass the figure QA contract, numbers match, row count matches, exclusions respected)
- [ ] Statistical declaration block present (independent unit, n, comparison family, correction) and the `reference/statistical-rigor.md` checklist passed — no P0 item open
- [ ] Headline statistical claim recomputed by the orchestrator (evidence: the recomputation)
- [ ] Freshness check done
- [ ] Search diagnosis recorded: `kind` audit done, null-signal count, calibration table, per-dimension table, `search_log` outcome filled, healthy/stalled verdict
- [ ] Budget check performed and recorded
- [ ] If the escalation trigger fired (stalled + last 2 metric entries on one dimension) and Path A was taken: the enqueued Phase 2 task carries the constraint and names the fresh `varies` dimension
- [ ] If alternatives were compared: rubric scores and rejection reasons logged (Candidate Critique Rubric)
- [ ] If concluding: test set run exactly once (logged), publish decision made with the no-publish option steelmanned, retrospective task enqueued
- [ ] If concluding via path (c): retrospective written and presented — evidence: the retrospective log path + the message presenting the proposals to the user
- [ ] User approved the path decision (quoted verbatim)

## Outputs

- Research log: `research-log/[NNN]-analysis-iter-[X].md` — results table, statistical tests, figure list, seven answers, path decision and rationale, Gate Check
- Commit: `research: analysis iter [X] — [iterate/pivot/conclude], [headline finding]`
