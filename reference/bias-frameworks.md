# Bias Frameworks and Review Stress Gates

Design-typed validity machinery, adapted from the evidence-synthesis tradition (RoB 2, ROBINS-I, TRIPOD, QUADAS lineage). sciagent's reviewers are strong on ML-venue failure modes; this file adds (a) the rule that the bias framework must match the study design, (b) a fixed enumeration of the bias surface so threats-to-validity lists stop being freeform, and (c) the claim-downgrade route for limitations that cannot be fixed. Consumed by the Phase 2 threats-to-validity step and by the reviewer templates (theory-reviewer, paper-reviewer, independent-reviewer) — reviewer dispatches stay sterile, so each template carries its relevant checklist inline; a reviewer is never pointed at this file.

## 1. Choose the framework by design — never mix tools

A reporting checklist (did they say what they did?) is not a bias tool (does what they did threaten the conclusion?). Assess bias with the framework matching the design, at the **outcome/claim level** — never one score for a whole paper:

| Design | Bias framing | Core questions |
|---|---|---|
| Randomized / controlled experiment (incl. seeded ML runs with random assignment of conditions) | RoB 2-style, per outcome | randomization actually random? deviations from the planned protocol? missing outcomes correlated with condition? outcome measurement blind to condition? selective reporting? |
| Non-randomized comparison (observational data, found experiments, post-hoc cohorts) | ROBINS-I-style + target-trial framing | what randomized experiment is this imitating? confounding? selection into the sample? classification of the "intervention"? |
| Prediction / ML model claims | TRIPOD-style staging | which stage is claimed — development, internal validation, **external validation**, impact? Claims must not exceed the stage actually performed |
| Diagnostic / measurement claims | QUADAS-style | index test independent of the reference standard? threshold chosen before or after seeing results? use-context matching the claim? |

Project-type mapping: `empirical` runs are usually row 1 (assignment of conditions is under our control — the evaluation contract is the protocol); `analysis` and `reproduction` projects frequently need rows 2–3; `dataset` projects need row 4 thinking for their construct-validity gate.

## 2. The fixed bias surface

Every threats-to-validity list (Phase 2 hypothesis entry; reviewer checks) walks this enumeration explicitly — each item gets one line: *how it could operate here*, or *why it can't*:

1. **Selection** — how units entered the sample (datasets chosen, examples filtered, runs kept)
2. **Confounding** — a third variable driving both "method" and "outcome" (compute budget, tuning effort, data freshness)
3. **Allocation / assignment** — how conditions were assigned to units (seed sets, hardware, orderings)
4. **Deviation from protocol** — what was actually run vs. what the contract pre-specified
5. **Missing data** — dropped runs, failed seeds, filtered examples — and whether the missingness correlates with condition
6. **Measurement** — the metric implementation, its failure modes, who/what computes it (leakage lives here)
7. **Analysis flexibility** — forking paths: the comparisons, exclusions, and transforms that were choices
8. **Selective reporting** — which of the results that exist made it into the claim

## 3. ML-specific stress gates (Results-reviewer ammunition)

- **Leakage & split independence** — train/eval contamination; non-independent splits (temporal, spatial, entity overlap: same user/molecule/repo on both sides); preprocessing fit on the full dataset.
- **Out-of-domain claims** — generalization claims tested only in-domain; rare-event/imbalance effects reported as aggregate accuracy.
- **Baseline fairness under matched constraints** — baselines current, tuned with equivalent budget, evaluated under the same compute/latency/data constraints as the method.
- **Operating envelope** — where the method was actually evaluated (scales, datasets, conditions) vs. the breadth of the claim; autonomy/robustness claims must not exceed proof-of-concept evidence.

## 4. Principles (each kills a common rationalization)

- **Missing reporting ≠ method not done** — but it caps evaluability: the review says "cannot be assessed," never assumes the best.
- **Statistical significance cannot cure design bias.** A biased comparison at p < 0.001 is a precisely-estimated biased comparison.
- **Large n cannot fix systematic measurement error** — it makes the wrong answer more confident.
- **Adjustment variables need causal or substantive justification** — chosen by univariate p-values is itself a bias.

## 5. The claim-downgrade route

Two rules that change what "fix" means, for reviewers and for Branch-of-Origin routing:

1. **An unfixable design limitation lowers the conclusion's strength — it is not "future work."** When the flaw cannot be fixed within budget (the data doesn't exist, the confound can't be isolated, the external validation can't be run), the correct revision is **narrowing the claim** to what the design supports: scope it ("on in-domain data…", "at the scales tested…"), weaken the verb (demonstrates → suggests), or drop the claim. Wrapping the limitation in more citations or a limitations-section mention while the abstract keeps the strong claim is the failure mode.
2. **Every critique states its conclusion impact.** A review issue must say how it would change the conclusion or the decision if unaddressed ("if the splits share entities, the headline gain may be memorization — the central claim is unsupported"). An issue that changes nothing is a comment, not a finding — reviewers label those as coaching, not blockers.
