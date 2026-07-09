# Phase 0: Research Setup

Goal: convert the research idea into tracked state, a configured workspace, and fixed budgets — so every later phase runs on structure, not memory.

**If arriving from Phase 0a (inspiration entry):** the idea DNA comes from the chosen candidate (refine it with the user, don't re-derive it), the workspace skeleton and `state.json` already exist (complete them, don't recreate), and step 3's quick scan is skipped — the ideation sweep already validated the space and seeded `research-log/lit/`.

## Steps

1. **Formulate the problem — write `PROBLEM.md`** (before anything else; from Phase 0a, refine the chosen candidate's problem sketch with the user):
   - **Core question** — one sentence. If it takes three, the problem isn't formulated yet.
   - **Who has this problem and why it matters** — the concrete pain, not "the field lacks…"
   - **Why current approaches fall short** — provisional now, firmed up in Phase 1
   - **What success looks like** — measurable, and beyond the metric: what would change if this worked?
   - **Non-goals** — what this project explicitly does not attempt
   - **Proxy caveat** — "[metric] on [benchmark] is our proxy for [the real thing]; improving the metric without the real thing is failure."

   Read it back to the user and get agreement — **quote their approval verbatim in the log**. This file is the contract the whole project is checked against; it only changes via the Invalidation procedure in SKILL.md.

2. **Decompose the research idea into DNA components** (recorded in `state.json`; the DNA's problem is the core question from `PROBLEM.md`):
   - **Problem**, **Assumption** (`explicit` or `inferred`), **Novelty claim** (a *verification claim* for reproduction projects)
   - **Project type** — `empirical | theoretical | dataset | reproduction | analysis` (see SKILL.md's Entry Triage table). Confirm with the user: this selects which gate variants apply for the rest of the project.
   - **Domain**, **success criteria** (specific metrics and thresholds, stored as `success_criteria`), **scope constraints** (stored as `constraints`).

3. **Quick literature scan** (3-5 papers, budget-fixed; skip if Phase 0a ran) to validate the idea isn't trivially solved or fundamentally flawed. Detect which literature sources are available in this session; the user may add or restrict sources.

4. **Ask the user** (one batch of questions, then stop asking):
   - Where to run experiments (local specs, or remote — SSH details, cloud provider)
   - Budget constraints (time, money, API calls) and any overrides to the SKILL.md Budgets table
   - Research intensity: **Light** / **Medium** / **Deep**
   - Preferred paper output format: DOCX (default) / LaTeX / Markdown
   - **Target venue** (or "undecided" — then default to the domain's top venue for norm purposes). Recorded as `target_venue` in `state.json`; its conventions are captured from the exemplars during Phase 1 decision archaeology and drive the Venue Norm column of the Phase 6 rationale matrix and the AI-disclosure check.
   - **Data governance:** what datasets will be used, under what licenses; any personal/human-subjects data (if yes: stop — user must confirm approvals exist); for LLM-based work, is the benchmark plausibly contaminated in the models used?
   - **Checkpoint defaults (optional):** pre-recorded decisions if the user is unavailable ("if I don't respond in N days, proceed with your recommendation") — stored in `state.json`.
   Record all answers; compute answers become the paper's Experimental Setup section.

5. **Set up the workspace:**
   - Initialize git repo (or use existing — check `git status --porcelain` first; never absorb existing uncommitted work)
   - Create the directory structure (see SKILL.md)
   - Create/complete `state.json` per the SKILL.md schema: `phase`, `cycle: 1`, `iteration: 1`, `entry_mode`, `project_type`, idea DNA, the three counted budgets with defaults + approved overrides, empty `tasks`/`parked_candidates`/`tried_and_failed`/`learnings`, `gates: {}`
   - Create `research-log/progress.md` containing only its header line
   - Create `results.tsv` with the prediction-ledger header: `run_id	metric	predicted_value	predicted_direction	confidence	metric_value	signal	memory_gb	runtime_s	status	description` (one row per run × metric; for `theoretical` projects this is instead the claims ledger: `claim_id	statement	status	log`)
   - Document the environment in `experiments/configs/environment.md`: OS, hardware, GPU model + VRAM, Python version, key library versions, CUDA/driver versions
   - Record dataset/code provenance and licenses in `experiments/configs/data-governance.md`

6. **Define the evaluation contract** in `experiments/configs/evaluation-contract.md` (empirical/dataset/reproduction projects; theoretical projects instead define the proof-verification standard):
   - What is mutable (model code, hyperparameters, training logic)
   - What is read-only, **enumerated as exact file paths/globs** — evaluation harness, data loading, metrics, splits — so the Phase 4 check is a mechanical `git diff --stat <range> -- <globs>`
   - Primary metric and exactly how it is computed; **the pre-specified primary comparison** (which two numbers decide the headline claim)
   - **Data discipline tiers:** tuning signal / validation / **locked test set, run exactly once at conclusion**
   - **Seed policy:** the evaluation seed (frozen) and the pre-registered training-seed set (default {41, 42, 43}); **N ≥ 3 seeds for the baseline, the core comparison, and anything paper-bound** — single-seed runs are exploratory only
   - **Baseline reproduction tolerance:** default = the published value falls within the CI of our N-seed reproduction, or within 2% relative. Any looser tolerance requires a citation to a source reporting that reproduction range AND the user's approval (quoted). For systems work: the comparison is the baseline's public code re-run on OUR hardware, not the paper's absolute numbers.
   - **Tuning-parity budget:** whatever hyperparameter search our method receives across iterations (count it — it's the iteration history), the strongest baseline receives equivalently before conclusions are drawn
   - **Benchmarks:** the primary benchmark plus generalization benchmarks per intensity (Medium: +1, Deep: +2)
   - Immutable constants (sequence length, dataset, eval protocol)

7. **Read the contract back to the user and get approval** (quoted verbatim — the tolerance, seed policy, and test-set discipline are the project's constitution and must not be self-served).

8. **Seed the task queue** in `state.json` with the Phase 1 tasks.

## Gate (record evidence in `state.json.gates["0"]` and the log's Gate Check)

- [ ] `PROBLEM.md` written; user approval quoted verbatim
- [ ] Idea DNA + `project_type` recorded in `state.json`
- [ ] Success criteria with specific metrics and thresholds
- [ ] Compute environment documented (`experiments/configs/environment.md`)
- [ ] Data governance recorded: licenses, PII/human-subjects assessment, contamination consideration, dual-use one-liner
- [ ] Evaluation contract written (tiers, seeds, tolerance, parity, globs) and user approval quoted verbatim
- [ ] Intensity, output format, and budgets recorded in `state.json`
- [ ] `results.tsv` and `progress.md` initialized
- [ ] Workspace committed to git

## Outputs

- Research log: `research-log/000-setup.md` (all setup decisions + Gate Check + Problem alignment)
- Commit: `research: initialize workspace for [topic]` — or, when arriving from Phase 0a (workspace already exists): `research: setup complete — [topic]`
