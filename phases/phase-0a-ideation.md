# Phase 0a: Ideation (optional — inspiration entry only)

Goal: turn a vague inspiration ("something about efficient long-context attention", "I find X fascinating") into 2-4 concrete, evidence-backed candidate research ideas — each with a benchmark, SOTA numbers, and a reproducible baseline already identified — so the user picks a direction grounded in the actual state of the field, not a guess.

Skip this phase entirely when the user arrives with a concrete idea (Entry Triage in SKILL.md).

## Steps

1. **Bootstrap the workspace skeleton** (so state tracking starts from the very first turn): init git, create the directory structure, create a minimal `state.json` with `"phase": "0a"`, `"entry_mode": "inspiration"`, and the inspiration recorded verbatim. Commit: `research: initialize workspace for [topic]`.

2. **Clarify the inspiration with the user** (one short batch, not an interrogation): What about this topic excites them? Any domain preference? Rough compute reality (laptop / single GPU / cluster)? Any direction they explicitly do NOT want? Record answers in `state.json`.

3. **Exploratory literature sweep** — dispatch literature searchers (`prompts/literature-searcher.md`, inspiration-brief variant) with broad topic queries. Budget: 2-3 searchers, ≤ 10 papers each. Target mix: recent surveys, the most-cited recent work, and papers that report benchmark tables. Spot-check citations exactly as in Phase 1 (2 per source minimum).

4. **Build the topic landscape** from the verified results:
   - **Subareas and open problems** — what the field itself says is unsolved (from surveys' future-work and limitations sections)
   - **Active benchmarks** — which datasets/tasks the community actually evaluates on right now
   - **SOTA table** — per benchmark: current best method, exact metric value, paper, year
   - **Baseline candidates** — for each benchmark: a strong, *reproducible* baseline — public code available, compute cost within the user's budget, published numbers to verify reproduction against. A brilliant direction with no runnable baseline is not actionable.

5. **Generate 2-4 candidate research ideas.** For each candidate:
   - **Problem formulation sketch** — the core question in one sentence, who has this problem, and a draft proxy caveat ("[metric] on [benchmark] would be our proxy for [the real thing]")
   - **Provisional idea DNA** — problem, assumption (labeled `inferred`), novelty claim
   - **The gap it exploits** — with cited evidence from the sweep
   - **Benchmark + baseline** — which benchmark it would be evaluated on, which baseline it would innovate on, the SOTA number to beat
   - **Sketch of the distinguishing prediction** — what this idea predicts that existing approaches don't (the anti-stacking test starts here, not at Phase 2)
   - **Taxonomy tag** — `(opportunity pattern, method paradigm, dominant operation)` per `reference/idea-taxonomy.md`. The tag must match the candidate's actual gap-and-contribution structure, not be chosen to satisfy the gate below.
   - **Feasibility** — honest compute estimate vs. the user's budget
   - **Risk/impact** — what makes it publishable if it works; what kills it

   Candidates must be genuinely distinct directions, not variations of one idea. Aim for a mix of idea moves (see Idea Moves in SKILL.md): at least one **extrapolation** candidate (questions a structure the field assumes necessary — name the structure, the property it provides, and the cheaper mechanism that could provide it) alongside **reframing** or **engineering** candidates (engineering candidates must name the measured bottleneck each component would attack). Discard any candidate whose novelty rests on "no paper matched this keyword" — novelty is argued by comparison to the closest existing work.

   **Slate diversity gate (mechanical — LLM ideation collapses onto bridge/synthesis templates at 4–7× the human rate, and more thinking makes it worse; see `reference/idea-taxonomy.md`):** across the slate, at most ONE candidate may be Bridge Opportunity × Synthesis/Unification; the slate spans ≥ 3 distinct opportunity patterns (≥ 2 if only two candidates); and ≥ 1 candidate's dominant operation is **replace**, **decouple**, or **formalize**. A failing slate is regenerated targeting the missing cells by name — never fixed by relabeling.

6. **Present to user and wait.** Show the landscape summary, the SOTA table, and the candidates side by side with your recommendation and why. The user picks one (or redirects — that's cheap at this stage; another ideation round costs one sweep, not a research project). Budget: 2 ideation rounds total; after that, ask the user to narrow the topic themselves.

7. **Hand off to Phase 0:** write the chosen candidate's DNA into `state.json`, set `"phase": "0"` (phase is always a string). Phase 0 turns the candidate's problem formulation sketch into the full `PROBLEM.md` with the user. Phase 0 then skips its quick scan (the sweep already validated the space), and Phase 1 runs as targeted deepening on the chosen direction rather than a from-scratch survey.

## Gate (record evidence in `state.json.gates["0a"]`)

- [ ] Topic landscape documented with citation spot-checks passed
- [ ] SOTA table with exact numbers per active benchmark
- [ ] At least 2 candidate ideas, each with benchmark + reproducible baseline + provisional DNA + distinguishing-prediction sketch + taxonomy tag
- [ ] Slate diversity gate passed: ≤ 1 Bridge×Synthesis candidate, ≥ 3 distinct opportunity patterns (≥ 2 if two candidates), ≥ 1 replace/decouple/formalize candidate
- [ ] User selected a candidate

## Outputs

- Research log: `research-log/000a-ideation.md` — landscape, SOTA table, all candidates (including rejected ones — they document the road not taken), user's choice, Gate Check
- Citation database seeded: `research-log/lit/*.json`
- Commit: `research: ideation — [N] candidates from [topic], pursuing [chosen idea]`
