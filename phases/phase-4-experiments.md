# Phase 4: Experiment Design & Execution

Goal: baseline reproduction, an adversarially code-reviewed core experiment, then ablations and robustness — one run at a time, each verified with provenance, each committed, with pruning instead of endless fixing.

Project-type note: `theoretical` projects replace this phase with proof verification per the SKILL.md table; `dataset` projects swap ablations for validity checks (inter-annotator agreement, contamination audit, baseline suite); `reproduction` projects treat the baseline block as the main event and the stress-tests as the plan.

## Steps

1. **Design the experiment plan** and enqueue each run as a task in `state.json`. **Runs come from this plan** — adding a run later requires a logged plan-amendment entry stating why (append-only, so churn is countable):
   - **Baseline run(s)** — reproduce SOTA or the closest comparison, at N ≥ 3 seeds (the contract's pre-registered seed set). MUST succeed first, within the contract's tolerance, AND: the baseline is implemented from a trusted reference (official code, or replication of a peer-reviewed result — never a casual reimplementation), and any gap to the literature number is explained in the log before proceeding. A claimed improvement over a weak baseline is not a result; it is a fiction the project will eventually be embarrassed by. If the baseline can't be reproduced, stop and debug, or escalate. **For engineering hypotheses:** the baseline run also produces the profile artifact (`experiments/baseline/profile.md` with a measured number per claimed bottleneck, produced by a logged command) — any component whose bottleneck the profile doesn't confirm gets cut from the plan before it is built.
   - **Core experiment** — implement the hypothesis. Single clean change from baseline. Same seed set.
   - **Distinguishing-prediction run** — tests the anti-stacking prediction from Phase 2, if not covered by the core run.
   - **Tuned-baseline run** — before conclusions: the strongest baseline gets the tuning-parity budget from the contract (equivalent search effort to what our method has received across iterations). "We tuned ours for five rounds against their defaults" is the #1 reviewer kill-shot.
   - **Ablation studies** — components A+B+C → A-only, B-only, C-only, A+B, A+C, B+C, A+B+C.
   - **Generalization runs** — the contract's additional benchmarks (Medium: +1, Deep: +2).
   - **Scaling analysis** — 2-3 runs at different scales, if relevant.
   - **Robustness checks** — the pre-registered training-seed set, splits, hyperparameter ranges.

   Write the plan explicitly: what each run changes, estimated time and compute.

2. **Code-review gate (before the core experiment's results may be believed):** dispatch a code reviewer (`prompts/code-reviewer.md`, most capable available model, sterile dispatch) on the baseline + core experiment code. It hunts leakage, split hygiene, metric implementation vs. the contract's definition, and train/eval separation. NEEDS_REVISION blocks the phase until fixed. This is the only gate standing between a leaky experiment and a beautiful wrong paper.

3. **Execute runs sequentially — one run per iteration of the loop protocol.** For each run, apply the Predict-Then-Run Discipline first (SKILL.md): prediction row in `results.tsv` + rationale paragraph in the log BEFORE dispatch. Then dispatch an experiment implementer (`prompts/experiment-implementer.md`) with: full spec, the prediction block, environment, evaluation contract, baseline results (once available), run/output conventions. Budgets (SKILL.md): 2 fix attempts per *change being tested* — a re-run testing the same change is a fix attempt whatever its run ID, and its task must set `parent`; 3 cumulative failed runs on one approach since the last `best_state` improvement → prune (baseline re-runs and kept-config re-runs never reset or count).

   **Long-running runs** (won't finish within a session): the implementer launches detached (`nohup <cmd> > run.log 2>&1 &` or scheduler submit) and returns DONE_WITH_CONCERNS + the job handle; the task's `evidence` records `{job_id, log_path, launched_at}` and stays `in_progress`. ORIENT checks job status before selecting new work; a successor session must NEVER re-dispatch an `in_progress` run without checking its job first. "Sequential" means no *dependent* run starts before its predecessor's metrics are verified — independent seed replicas may overlap.

4. **VERIFY each run yourself** (never trust the report alone):
   - Code exists in `experiments/[run-id]/`; run log exists; **the log's first line is the executed command**
   - Provenance plausible: log length and file mtimes consistent with the reported runtime
   - Re-extract metrics: `grep "^[a-z_]*:" experiments/[run-id]/run.log` — numbers match the subagent's report
   - Immutables untouched — mechanical check: `git diff --stat <range> -- <read-only globs from the contract>` is empty (command + output = evidence)
   - **Before any `best_state` update:** re-run the evaluation command yourself once (the eval harness is immutable and cheap); record command + output. **Too-good-to-be-true tripwire:** a result beating SOTA by more than the field-typical margin triggers a mandatory leakage re-audit (code reviewer on the diff) before it may enter `best_state`.

5. **Record + keep/prune, in this exact order** (the Keep/Prune Protocol from SKILL.md):
   1. Complete the run's prediction-ledger rows in `results.tsv` (fill `metric_value` and `signal`: confirm/partial/disconfirm/null; `NA` for crashed metrics; a `null` signal means the run produced no gradient — flag the design) and write `research-log/[NNN]-exp-[run-id].md` including a "Prediction vs. Reality" line
   2. `git add` (explicit paths) + `git commit` — always, regardless of outcome
   3. Provenance verified + eval re-run → improved: update `best_state`
   4. Regressed/crashed out of budget → `git revert` the experiment's code changes (never `git reset`), append to `tried_and_failed` with an honest `failure_class`
   5. Apply the simplicity criterion

6. **Adapt the plan after each run** (adaptation = logged plan amendment, not improvisation):
   - Baseline off-tolerance → stop, debug, or escalate. Do NOT proceed on a broken baseline.
   - Core succeeds → full ablation + generalization + scaling plan
   - Core partially succeeds → narrow ablations to the underperforming component, skip scaling
   - Core fails → stop, log with analysis and `failure_class`, fill the current `search_log` entry's `outcome` (`refuted | inconclusive`), loop back to Phase 2 (consumes a research iteration — increment `iteration` AND `research_iterations.spent`; the new hypothesis appends a new `search_log` entry)
   - **Prune rule:** 3 cumulative failures on one approach → revert to `best_state`, record, return to the plan. Never keep patching a dying branch.

7. **Checkpoint with user** after baseline + core experiment, before ablations. This blocks the *decision* on the remaining plan — while waiting you may clear verification debt and draft figures, but not start runs whose design depends on the pending decision. Generate comparison plots after each batch.

## Gate (record evidence in `state.json.gates["4"]`)

- [ ] Baseline reproduced within the contract's tolerance across the seed set (state the numbers and CI)
- [ ] Code review passed on baseline + core experiment code
- [ ] Core experiment compared against baseline on the pre-specified primary comparison, N ≥ 3 seeds
- [ ] Distinguishing prediction tested, OR all three engineering tests evidenced (per hypothesis type; N/A for non-empirical projects)
- [ ] Tuned-baseline run completed under the parity budget
- [ ] Ablations isolate which components contribute
- [ ] Generalization benchmarks run per intensity level
- [ ] Every run has `results.tsv` rows, a log entry, provenance evidence, and a commit

## Outputs

- Research log: `research-log/[NNN]-exp-[run-id].md` per run; `research-log/[NNN]-exp-summary.md` for the batch (full results table, Gate Check, Problem alignment)
- Commits: `research: exp [run-id] — [brief result]`; `research: experiment batch complete — [headline finding]`
