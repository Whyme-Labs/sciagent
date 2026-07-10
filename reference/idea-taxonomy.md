# Idea Taxonomy: Opportunity Patterns × Method Paradigms

A two-axis classification of research ideas, adapted from Chen, Zhao & Cohan, *Measuring the Gap Between Human and LLM Research Ideas* (arXiv:2607.01233). Used in Phase 0a (candidate diversity gate) and Phase 2 (default-template tripwire). Every candidate and every hypothesis gets classified on both axes; the classification is recorded in the log entry and verified by the theory reviewer.

## Why this exists: the measured LLM ideation bias

The paper reverse-engineered the prior work behind published papers, gave the same prior-work context to LLMs, and compared what each proposed. The gap is distributional, not qualitative — LLM ideas are individually reasonable but collapse onto one template:

| Pattern | Human papers | LLM-generated |
|---|---|---|
| Bridge Opportunity (motivation) | 12.1% | 47.1–64.2% |
| Synthesis/Unification (method) | 5.1% | 22.5–38.7% |
| "Integrate" operation | 2.35% | 34.2% |
| "Replace" operation | 9.13% | 0.92% |
| "Decouple" operation | 2.33% | 0.21% |

Human ideas hold >0.92 normalized entropy across both axes; models range 0.55–0.88. Three findings make this OUR problem specifically:

1. **More effort makes it worse, not better.** Extended reasoning *increased* bridge/synthesis concentration; full-paper context (vs. abstracts) *worsened* alignment; larger models were not better. Thinking harder about ideation does not escape the template — so the countermeasure must be mechanical (classification + diversity gate), not "be more creative."
2. **No prompt mitigation is known to work.** Neutral wording only slightly reduced the bias. This is why the gates below are checklist items, not exhortations.
3. **Humans favor targeted local interventions** — replace a component, decouple two things assumed to co-occur, formalize a fuzzy notion — while models default to wholesale connection of literatures. Our Extrapolation move (SKILL.md) is a disciplined *replace*; the bias data says it must be forced into every candidate slate, because it will not arise by default.

## Axis 1 — Opportunity Pattern (why is research needed here?)

1. **Puzzle/Contradiction** — a paradox, tradeoff, surprising failure, or conflicting evidence.
2. **Explanation Gap** — a missing causal, mechanistic, theoretical, or explanatory account.
3. **Scope Mismatch** — unrealistic assumptions, narrow regimes, unclear transferability, or boundary conditions.
4. **Evidence Gap** — missing ways to observe, measure, benchmark, audit, diagnose, validate, or compare.
5. **Bridge Opportunity** — disconnected literatures, theories, evidence streams, communities, or methods that could be connected. **← the LLM default; cap it.**
6. **Failure/Risk Gap** — brittleness, unreliability, bias, uncertainty, safety/privacy/security risk, or reproducibility concerns.
7. **Resource Bottleneck** — cost, compute, time, data access, sample scarcity, deployment friction, or scalability constraints.

## Axis 2 — Method Paradigm (how is the contribution constructed?)

1. **Synthesis/Unification** — bridges, integrates, reconciles, or unifies separate literatures, theories, mechanisms, or methods. **← the LLM default; cap it.**
2. **Relax/Extend Scope** — makes prior work function under weaker assumptions, broader scope, new regimes, or more realistic settings.
3. **Robustification** — reduces failures, brittleness, risk, uncertainty, bias, or unreliability.
4. **Formal Derivation** — introduces a formal model, theorem, bound, objective, proof, ontology, taxonomy, or explanatory formulation.
5. **Empirical Mapping** — builds or applies systematic measurement, benchmarks, diagnostics, datasets, comparative studies, or pattern analyses.
6. **Artifact/System** — builds a concrete artifact, system, platform, prototype, or deployment workflow as the central contribution.
7. **Optimization/Search** — uses optimization, search, screening, tuning, active/adaptive design, scaling, or efficiency strategies.

## The operations vocabulary (how the idea departs from prior work)

Name the single dominant operation the idea performs on the closest prior work. Human-enriched operations (generate toward these): **replace** (swap a component/assumption for a cheaper or better provider of the same function — the Extrapolation move), **decouple** (separate two things prior work treats as one), **formalize** (give a fuzzy notion a precise definition and derive consequences). LLM-default operations (allowed, but they trigger the anti-stacking tests): **integrate**, **unify**, **merge**, **adapt**, **design**.

## How to apply it

**Phase 0a — candidate diversity gate (mechanical):**
- Tag every candidate `(opportunity pattern, method paradigm, dominant operation)`.
- Across the slate: **at most ONE candidate may be Bridge Opportunity × Synthesis/Unification**, the slate must span **≥ 3 distinct opportunity patterns** (≥ 2 if only two candidates), and **≥ 1 candidate's dominant operation must be replace, decouple, or formalize**.
- A slate failing any check is regenerated targeting the missing cells — name the cell explicitly in the regeneration ("generate a Puzzle/Contradiction × Formal Derivation candidate for this topic"). Do NOT fix a failing slate by relabeling; the tag must match the candidate's actual gap-and-contribution structure.

**Phase 2 — default-template tripwire:**
- Classify the hypothesis on both axes in the hypothesis entry.
- If it lands **Bridge × Synthesis** (or its dominant operation is integrate/unify/merge), it matches the statistically most likely LLM template (~4–7× human base rate). It is not banned — real bridge papers exist — but it must additionally document why a local move (replace / decouple / formalize) on the strongest single prior work would NOT achieve the goal. The theory reviewer verifies both the classification and this justification.

**Phase 1 — decision archaeology enrichment:** when reading exemplars, tag each exemplar's (opportunity pattern, paradigm, operation) in its Exemplar Move Table — this builds the venue's empirical distribution, which is the reference the Phase 0a slate is diversified against.

The classification is a thinking tool, not a stamp: if an idea genuinely straddles two cells, record the dominant one and note the second. What is never acceptable is a slate or a hypothesis that was not classified at all — unclassified ideation defaults to the template.
