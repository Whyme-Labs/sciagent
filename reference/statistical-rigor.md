# Statistical Rigor Rules

The statistical errors an autonomous experiment loop is most prone to, ranked by severity, with the declarations that prevent them. Consumed by the results-analyzer dispatch and the Phase 5 VERIFY step; the reviewer prompts carry the same checks from the reading side. sciagent already enforces effect sizes and N ≥ 3 seeds — these rules govern *what counts as N* and *which comparisons the p-values survive*.

## The declaration block (Phase 5, before any statistic is trusted)

Every analysis log entry declares, once, at the top:

```
independent_unit:   <what one independent observation IS — e.g., "one training run (seed)">
n_units:            <count of independent units per condition — seeds/folds, NOT eval batches or forward passes>
comparison_family:  <total number of baseline comparisons performed in this analysis>
correction:         <none — single pre-specified primary | Holm/Bonferroni/BH across the family>
```

An analysis without this block does not pass the Phase 5 gate. The pre-specified primary comparison (from the evaluation contract) needs no correction; every secondary comparison is judged against the declared family.

## P0 — errors that invalidate the conclusion (blocking)

1. **Pseudoreplication.** The default n is the **independent experimental unit**. Model runs from different seeds are independent units; eval-set examples, batches, checkpoints of one run, and technical replicates are NOT — treating them as n inflates significance arbitrarily. If per-example statistics are used (e.g., paired bootstrap over test examples), say so explicitly and treat runs and examples as different levels — never mix them into one n.
2. **Uncorrected multiple comparisons.** Define the comparison family BEFORE computing p-values. Ablations, secondary metrics, and generalization benchmarks are all family members. A "significant" secondary finding that would not survive correction across the declared family is reported as exploratory, not as a finding.
3. **The interaction error.** *A difference in significance is not evidence of a significant difference.* "Our method improves significantly on benchmark A (p<.05) but the baseline doesn't (p=.2)" says nothing about A-vs-baseline — test the interaction or compare the effect sizes with their intervals directly.
4. **Analysis-unit mismatch.** Paired/nested designs (same seeds across methods, same splits) analyzed with independent-sample tests (or vice versa). Same-seed comparisons are paired — use the paired test; it is also more powerful.

## P1 — errors that overstate the evidence (major)

5. **Significance-only conclusions.** Every paper-bound comparison reports effect size + interval + exact p + n; "p < 0.05" alone is not a result. "Significant" is never used to mean important, large, or causal.
6. **Undefined error bars.** Every interval names what it is — s.d., s.e.m., or 95% CI — and over what units (seeds? folds?). s.e.m. bars on n=3 that *look* tight are the classic false-confidence figure.
7. **Silent variance shopping.** The seed set is the pre-registered one from the evaluation contract; dropping a "bad seed" from the statistics is fabrication unless the run is `crash` with a logged cause.

## P2 — reporting hygiene (minor)

8. Exact p-values (not `p < 0.05` ladders) down to p < 0.001; test names with their assumptions ("Welch's t-test, unequal variance"); one-sided tests only if pre-specified in the contract.
9. Per-panel n in every figure legend (see `reference/figure-spec.md` §6).

## Final checklist (analyzer output + Phase 5 VERIFY)

- [ ] Declaration block present and consistent with `results.tsv` (n_units matches the seed rows actually present)
- [ ] No statistic anywhere uses a non-independent unit as n
- [ ] Family declared; every secondary comparison labeled exploratory or corrected
- [ ] No claim of the form "significant here, not there, therefore different" without an interaction test
- [ ] Paired designs use paired tests
- [ ] Every comparison: effect size + interval (named) + exact p + n
