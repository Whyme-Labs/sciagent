# Phase 1: Literature Review

Goal: a literature map with verified papers, identified gaps, and exact baseline numbers — the foundation every later citation and comparison rests on.

**If Phase 0a ran:** this phase is targeted deepening, not a from-scratch survey. Keep and extend the existing `research-log/lit/*.json` database; aim queries at the chosen direction — its closest prior work, its benchmark's leaderboard, the baseline's known weaknesses — and spend the remaining paper budget there. The SOTA table from ideation carries forward; verify and sharpen it rather than rebuilding it.

## Steps

1. **Generate search queries through perspectives, not one flat list.** Adopt distinct researcher personas — at minimum: theorist (foundations, proofs, bounds), experimentalist (methods, benchmarks, reproductions), statistician (evaluation validity, significance practices), skeptical reviewer (known failure modes, negative results, critiques), practitioner (deployment constraints, real-world gaps). Generate 2-3 queries per perspective (5-15 total) covering the problem from `PROBLEM.md`, key techniques, baselines and benchmarks, and recent surveys. Different perspectives ask questions a single viewpoint never would — this is how unknown unknowns get found.

2. **Dispatch literature searcher subagents** — one per available source, in parallel. Budget: 3-5 searchers, ≤ 15 papers each; divide the intensity target across sources. Route sources by tier (`reference/citation-integrity.md` §1): authoritative APIs first, aggregators on thin coverage, scraped sources last and flagged.

   Use `prompts/literature-searcher.md`. Each searcher writes its findings to `research-log/lit/[source].json` — including its `search_record` (verbatim query, platform, date, result count per batch query; §2 of the same reference) — and returns only a summary (counts, highlights, coverage). Include the promoted `learnings` entries (`recurrences >= 2`) from `state.json`, if any.

   On the FIRST search round of a project, stage the parallelism: dispatch ONE searcher first and treat its first 2 papers as an extraction-schema pilot — check them against the JSON schema (two differently-structured papers ideally); only then dispatch the remaining searchers in parallel. A schema mismatch found now costs minutes; found at synthesis it costs the round. Later rounds dispatch fully in parallel. For `reproduction` projects and Deep intensity, fix inclusion/exclusion criteria in the log BEFORE this step (§2 of the reference).

3. **Verify before trusting (VERIFY step — mandatory):** fabricated citations are the most common failure of automated literature search — and they hide in plausible mid-tier entries, not famous papers. So the sample must not be yours to choose:
   - Select **at least 2 papers per source at random** with a logged command (e.g., `jq -r '.papers[].title' research-log/lit/arxiv.json | shuf -n 2`) — paste the command and its output as the gate evidence.
   - For each selected paper, fetch the URL and confirm title/authors match **and that at least one number in `key_results` actually appears in the paper's abstract or tables** — a real paper with hallucinated numbers poisons the SOTA table just as badly as a fake paper.
   - Additionally verify (non-random, always) every paper the hypothesis's evidence chain will lean on.
   - Mark every paper you verified `reviewed: yes` in its JSON entry (searchers always write `no`); an `extraction_confidence: low` entry that is still unreviewed never feeds the SOTA table or a baseline choice.
   - If any paper fails, discard that source's entire batch, record the failure in `learnings`, and re-dispatch that searcher (most capable available model this time).

4. **Synthesize:** deduplicate across sources, resolve conflicting relevance assessments, merge into a unified collection (keep the per-source JSON files as the citation database for Phase 6).

5. **Unused-paper sweep** (the highest-value 10 minutes of this phase): go through every high-relevance paper in the database that your emerging literature map does NOT yet use. For each: place it in the map, or write one line on why it doesn't belong. These leftovers are where rival hypotheses, disconfirming results, and adjacent methods hide — the papers you retrieved but weren't looking for. Two hard rules:
   - A high-relevance paper you can't place and can't dismiss is a signal to search deeper in its direction, not to ignore it.
   - **Novelty tripwire:** if papers resembling your intended direction keep accumulating in the unused pile, the direction is not novel — confront that now, not at review time.

6. **Decision archaeology on exemplars:** for the 2-3 papers closest to our direction (the exemplars the paper will be measured against), go beyond the searcher's extraction using `reference/deep-imitation-protocol.md`: reconstruct the decisions behind the paper (why this baseline, this benchmark, this framing; what was tried and discarded; the load-bearing assumption) and build the **Exemplar Move Tables** — the rhetorical moves each exemplar section performs, which Phase 6's rationale matrix will transfer. Also tag each exemplar's `(opportunity pattern, method paradigm, dominant operation)` per `reference/idea-taxonomy.md` — this is the venue's empirical distribution of how humans actually frame gaps and build contributions, the reference point for the Phase 0a diversity gate and the Phase 2 tripwire. Write to `research-log/[NNN]-decision-archaeology.md`.

7. **Build the literature map:**
   - **What's been tried** — grouped by technique family
   - **What works** — strongest results with specific numbers on specific benchmarks
   - **What's missing** — gaps and contradictions, with discipline on both:
     - **Contradictions:** when two papers disagree, decompose before adjudicating — check population/data, design, measurement, analysis, and time-period differences first; venue prestige is not a tiebreaker. Record the likely cause and what evidence would resolve it.
     - **Gaps:** distinguish `no study exists` / `study exists, full text inaccessible` / `studied, result not reported` — three different gaps; only the first is open territory, and claiming it requires having looked (cite the search_record queries that came up empty).
   - **Assumed-necessary structures** — what every approach keeps, what property it actually provides, and any work that questions it (extrapolation fuel: the biggest ideas replace these structures, not tune them)
   - **Measured bottlenecks** — where time/memory/cost actually goes according to published profiles (engineering fuel: components target these)
   - **Mathematical foundations** — key theorems, proofs, bounds underpinning the field
   - **Baselines to beat** — current SOTA with exact metric values

8. **Identify 2-3 research directions** from the gaps. For each: what gap it addresses, why existing work hasn't solved it, what prior evidence suggests it could work, and preliminary feasibility on our compute — plus the Candidate Critique Rubric fields (SKILL.md): most likely failure mode, hardest implementation trap, evidence check (cite the mapped papers supporting the premise), and the impact × feasibility ÷ complexity score. **Novelty must be argued by synthesis, not keyword absence** — "no paper matched this phrase" is not evidence of novelty; compare against the closest existing work explicitly.

9. **Check in with user** — present the literature map and proposed directions with your recommendation citing the rubric scores; non-recommended directions carry a one-line rejection reason in the log. Wait for the user to pick one (or suggest their own).

## Gate (record evidence in `state.json.gates["1"]`)

- [ ] Literature map documented, papers grouped by technique; contradictions decomposed, gaps typed (no-study / no-access / not-reported)
- [ ] Citation spot-checks passed (list which papers were verified)
- [ ] `search_record` present in every source's JSON (verbatim queries, platform, date, counts)
- [ ] Unused-paper sweep done — every high-relevance paper placed or dismissed with a reason
- [ ] Decision archaeology done on 2-3 exemplars, Exemplar Move Tables written
- [ ] At least one gap identified with cited evidence
- [ ] Baselines to beat identified with specific metric numbers
- [ ] Directions compared with the Candidate Critique Rubric (scores + rejection reasons logged)
- [ ] User approved a research direction

## Outputs

- Research log: `research-log/[NNN]-literature-review.md` (typically `001-` on the first pass; a pivot's targeted review gets the next unused number) — map, summaries, gaps, chosen direction, Gate Check
- Citation database: `research-log/lit/*.json` (kept for Phase 6 verification)
- Commit: `research: literature review — [N] papers surveyed, pursuing [direction]`
