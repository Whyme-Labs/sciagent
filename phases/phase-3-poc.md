# Phase 3: PoC Validation

Goal: the smallest possible experiment that tests the hypothesis's core assumptions — minutes of compute before committing hours.

## Steps

1. **Design a minimal probe** of the core assumptions. Options:
   - A toy dataset or subset (1-5% of full data)
   - A simplified version of the architecture
   - A back-of-envelope calculation implemented as code
   - A mathematical simulation checking theoretical bounds hold empirically
   - For engineering hypotheses: the profiling run that produces the bottleneck measurements (if not already sourced from literature)

   The PoC must complete in **minutes**, not hours. Define BEFORE running: what numbers/behavior = confirm vs. reject. Also write a one-paragraph **transferability argument**: why should the toy-scale result predict full scale? If the phenomenon is plausibly scale-dependent (optimization effects, emergent behavior, systems bottlenecks), say so — "inconclusive at feasible PoC scale" is then a legal outcome that escalates to the user rather than counting as a near-failure.

2. **Predict, then dispatch.** Apply the Predict-Then-Run Discipline (SKILL.md): write the prediction row into `results.tsv` (predicted value, direction, confidence) and the one-paragraph rationale into the research log BEFORE dispatching. Then dispatch the experiment implementer (`prompts/experiment-implementer.md`) with **RUN_ID = `poc`** (so all outputs land in `experiments/poc/`), including the prediction block. Fill in: the assumption being tested, expected confirm/reject outputs, environment (`experiments/configs/environment.md`), evaluation contract, run constraints (minutes), and the hypothesis context. Budget: 3 debug attempts total for the PoC.

3. **VERIFY the subagent's report:** confirm the code exists in `experiments/poc/`, the run log exists with the executed command as its first line, log length and mtimes are plausible for the reported runtime, and the reported metrics appear in it (`grep` them yourself). A subagent report alone is not evidence.

4. **Interpret results against the pre-defined confirm/reject criteria:**
   - **Confirmed** — document the evidence; proceed toward Phase 4.
   - **Partially confirmed** — write a NEW superseding hypothesis entry accounting for what you learned (never edit the reviewed entry); re-run the Phase 2 self-critique. **Substantive is defined mechanically:** any change to the claim, assumptions, justification, or success thresholds is substantive and requires re-dispatching the theory reviewer (counted against `hypothesis_review_rounds`); only a change to the expected-effect-magnitude line may skip re-review.
   - **Violated** — a valuable finding, not a failure. Document why. Add the assumption to `tried_and_failed` (choose the `failure_class` honestly: did a correctly-running probe contradict the prediction, or did we fail to probe it?) and loop back to Phase 2 with the new evidence.
   - **Inconclusive at feasible scale** — escalate to the user with the transferability argument and options; do not silently loop.

5. **Checkpoint with user** — present PoC results, your interpretation, and your recommendation: proceed / revise hypothesis / abandon direction. Wait for the go/no-go.

## Gate (record evidence in `state.json.gates["3"]`)

- [ ] PoC results support the core assumptions (or hypothesis was revised to account for findings)
- [ ] Metrics verified directly from the run log, not just the subagent report
- [ ] User approved the go/no-go decision

## Outputs

- Research log: `research-log/[NNN]-poc-[name].md` — design rationale, code location, results, interpretation, decision, Gate Check
- Commit: `research: poc — [assumption tested], result: [confirmed/revised/rejected]`
