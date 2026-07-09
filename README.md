# SciAgent

A Claude Code skill for autonomous scientific research — from idea to publication-quality paper.

## What It Does

SciAgent encodes a complete scientific research methodology that Claude follows. Give it a research idea — or just an inspiration — and it will:

0. **Ideate** (inspiration entry) — survey the topic landscape, gather SOTA numbers and active benchmarks, scout a reproducible baseline to innovate on, and propose concrete candidate ideas for you to pick from
1. **Review literature** — search multiple sources in parallel, verify citations, build a gap analysis, and run decision archaeology on exemplar papers (Exemplar Move Tables that feed Phase 6 writing)
2. **Form hypotheses** — with claim-type-appropriate justification and cited prior work, gated by independent theory review demanding mathematical depth, not decoration
3. **Validate with PoC** — run quick probes before committing to full experiments
4. **Run experiments** — baseline reproduction first, adversarial code review before results are believed, then predict-then-run adaptive plans with ablations, tuned-baseline parity, and multi-seed robustness
5. **Analyze & iterate** — statistical analysis with effect sizes, prediction-vs-reality signals, budgeted iteration, evidence-based pivots, and an explicit publish decision (contribution paper / conclusive negative result / internal report)
6. **Write the paper** — narrative arc + motivation surface map + writing rationale matrix as the execution plan; deterministic consistency and citation-faithfulness checks; three independent reviewers in parallel + editor synthesis at Deep intensity; anti-shallow-revision metrics on every revision

Every experiment is gated by scientific reasoning. No blind hyperparameter tweaking. Every paragraph of the paper is gated by a rationale-matrix row. No generic academic prose.

## Architecture: A Structured Research Loop

SciAgent v2 is engineered as a **deterministic research loop** rather than a monolithic instruction set, following current best practices for long-running agents (externalized state, fixed budgets, one task per iteration, evidence-gated progress). This makes it reliable across long sessions and across model tiers — the structure carries the process, not the model's memory.

Key mechanisms:

- **`PROBLEM.md`** — a pinned problem formulation (core question, success beyond the metric, non-goals, and the metric-proxy caveat) re-read every turn; drift-prone points (hypothesis gate, iteration decisions, paper assembly) carry explicit problem-alignment checks so the loop never optimizes the benchmark while forgetting what it was a proxy for.
- **`state.json`** — machine-checkable project state (phase, task queue, budgets, tried-and-failed ledger, gate evidence). Read at the start of every turn, updated at the end of every step. Append-only; statuses only move forward with recorded evidence.
- **The Iteration Protocol** — every working turn is ORIENT → SELECT (one task) → EXECUTE → VERIFY → RECORD → ADVANCE. Survives context compaction: the files are always enough to resume.
- **Fixed budgets** — iteration caps, debug-attempt limits, reviewer-round limits, and a diminishing-returns rule are set at Phase 0 and enforced, never renegotiated mid-run.
- **Debug-then-prune** — failing experiment branches get a bounded number of fix attempts, then the loop reverts to the best known-good state instead of patching a dying branch.
- **Deterministic verification before LLM review** — citations checked against a verified database, paper numbers checked against the results ledger, figures checked on disk — so reviewer subagents spend judgment on science, not typos.
- **Anti-rubber-stamp review gates** — reviewers must show evidence of scrutiny for a passing verdict; re-reviews judge the previous issue list item by item instead of re-grading from scratch.
- **Subagents write files, return summaries** — heavy artifacts (paper lists, code, sections, figures) go to disk; the orchestrator's context stays lean.
- **Scientific-integrity machinery** — three-tier data discipline with a locked test set run exactly once; N ≥ 3 seeds for paper-bound comparisons; baseline tuning-parity budgets; adversarial code review for leakage before results count; immutable hypothesis entries (revisions supersede, never overwrite — pre-specified vs. post-hoc survives in the record); run provenance checks so a fabricated log can't enter the ledger.
- **Project-type awareness** — empirical, theoretical, dataset, reproduction, and analysis projects get type-appropriate gates instead of being forced into the method-paper mold; justification currency matches the claim type (derivations for theory, measurement design for empirical/systems, construct validity for datasets).
- **Ethics & governance** — data licensing, PII/human-subjects, contamination, and dual-use checks at setup, plus a standing stop-and-escalate rule.

No model names are hardcoded anywhere — subagents inherit the session model by default, with capability-relative guidance (strongest available for reviewer roles, fastest for mechanical search).

## Repository Layout

```
SKILL.md                        # Core: the loop protocol, state schema, budgets, dispatch contract
phases/
├── phase-0a-ideation.md        # Inspiration → landscape, SOTA, benchmarks, candidate ideas
├── phase-0-setup.md            # Idea DNA, workspace, evaluation contract, budgets
├── phase-1-literature.md       # Literature map with citation verification
├── phase-2-hypothesis.md       # Hypothesis + math justification + theory review gate
├── phase-3-poc.md              # Minimal probe of core assumptions
├── phase-4-experiments.md      # Baseline, core, ablations, keep/prune protocol
├── phase-5-analysis.md         # Statistics, budget check, iterate/pivot/conclude
└── phase-6-paper.md            # Assembly, consistency checks, review gate, delivery
prompts/
├── literature-searcher.md      # Parallel search + structured extraction to JSON
├── theory-reviewer.md          # Skeptical claim-type-appropriate review of hypotheses
├── code-reviewer.md            # Adversarial leakage/split/metric audit of experiment code
├── experiment-implementer.md   # One run per dispatch, immutable-contract-aware
├── results-analyzer.md         # Statistics + publication-quality figures
├── section-writer.md           # One paper section per dispatch, matrix-constrained
├── paper-reviewer.md           # Single-reviewer publication-readiness review (Light/Medium)
├── independent-reviewer.md     # Three parallel independent reviewers (Deep)
└── editor-synthesis.md         # Merges the three reviews into one decision (Deep)
reference/
├── mathematical-thinking.md    # Depth lenses for the justification gate
├── thinking-frameworks.md      # First principles, Socratic, Occam, research taste
├── deep-imitation-protocol.md  # Decision archaeology for reading; closed-book redo for writing
├── motivation-surface-map.md   # Reader-touchpoint planning for Phase 6
└── writing-rationale-matrix.md # Row-per-unit execution plan for Phase 6
```

Phase files are loaded just-in-time when the loop enters that phase — the always-loaded core stays small.

## Installation

### npx (recommended)

```bash
npx skills add Whyme-Labs/sciagent
```

Or install globally (available in all projects):

```bash
npx skills add -g Whyme-Labs/sciagent
```

### Manual (git clone)

**Personal skill** (available across all projects):

```bash
git clone https://github.com/Whyme-Labs/sciagent.git
ln -s "$(pwd)/sciagent" ~/.claude/skills/sciagent
```

**Project skill** (available only in one project):

```bash
mkdir -p .claude/skills
ln -s /path/to/sciagent .claude/skills/sciagent
```

Claude Code auto-discovers skills from `~/.claude/skills/` and `.claude/skills/`.

### Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Git (for experiment tracking)
- At least one literature source configured:
  - Web search (built-in)
  - arXiv MCP server (optional)
  - Scholar Gateway MCP (optional)

## Usage

Start a conversation with Claude with either a concrete idea or just an inspiration:

```
# Concrete idea — enters at Phase 0
I want to investigate whether [approach X] can improve [metric Y] on [problem Z].

# Inspiration — enters at Phase 0a (Ideation)
I'm fascinated by [topic]. Find me something worth researching in this space.
```

From an inspiration, SciAgent first surveys the field, builds a SOTA table over the active benchmarks, identifies a reproducible baseline worth innovating on, and presents 2-4 concrete candidate ideas — you pick one, and the pipeline continues from there.

Claude follows the SciAgent loop through Phases 0-6, checking in with you at fixed decision points: candidate selection (inspiration entry), setup questions, research-direction approval, PoC go/no-go, after baseline + core experiment, path decisions (iterate/pivot/conclude), and final draft review.

## Research Intensity & Budgets

Set at Phase 0 (defaults shown; you can override them at setup, never mid-run):

| Level | Papers | Best For |
|-------|--------|----------|
| Light | 5-10 | Quick exploration |
| Medium | 15-25 | Solid investigation |
| Deep | 30-50 | Publication-grade |

| Budget | Default |
|--------|---------|
| Research iterations (any iterate OR pivot) | 5 |
| Diminishing returns | conclude when last 2 metric-targeting iterations < 1% relative improvement |
| Fix attempts per experimental change | 2 |
| Cumulative failed runs on one approach before pruning | 3 |
| Theory/paper reviewer rounds (counted at dispatch time) | 2 each, then escalate to user |
| Exploratory runs (seed hypotheses, never confirm) | 2 per iteration |

## Research Workspace Output

SciAgent creates this workspace for each research project:

```
your-research-project/
├── state.json              # Machine-checkable loop state
├── PROBLEM.md              # Pinned problem formulation — the contract all work is checked against
├── research-log/           # Scientific narrative + progress.md + lit/ citation database
├── results.tsv             # Experiment ledger (crashes recorded as NA, never 0)
├── experiments/            # Code and configs (poc/, configs/)
├── data/                   # Datasets
└── paper/                  # Living document + sections/ + figures/
```

- **Paper** — DOCX (primary), LaTeX (optional), or Markdown (fallback)
- **Git history** — every decision, experiment, and analysis is a commit (`research:` prefix)

## Key Principles

- **Rigor before confirmation** — claim-type-appropriate justification required and independently reviewed; exploratory runs may seed hypotheses, never confirm them
- **Predict, then experiment** — every run records a numeric prediction *before* dispatch; the signal (confirm / partial / disconfirm / null) is the gradient that drives the next iteration
- **Anti-fragile signals** — disconfirmations sharpen the model of the problem and are treated as primary outputs
- **Strong baselines only** — improvements over weak or untuned baselines are fictional; baselines are audited and given tuning parity before being targeted
- **Reframe, don't stack** — every hypothesis must make a testable prediction that a plain combination of techniques would not
- **Extrapolate and engineer** — question structures the field assumes necessary (what property do they actually provide?), and treat composition as engineering: every component justified against a measured bottleneck, ablated, and claimed only through its end-to-end impact
- **Mathematical depth, not decoration** — matrices as transformations of space, problems mapped into easier spaces, error controlled rather than exact solutions chased; validity domains stated, key steps re-derived, dense notation unpacked
- **Read for motivation, write the whole story** — extract the decisions and constraints behind others' papers, not just the method; tell our own actual story (predictions, surprises, dead ends), never a sanitized post-hoc narrative
- **Simplicity over cleverness** — prefer elegant solutions
- **Everything documented** — full audit trail including the prediction ledger, negative results included
- **Honest science** — evidence-gated progress; nothing is "done" on self-assessment
- **Reproducibility** — environment, seeds, and exact commands recorded

## Operating Discipline

The quality gates are not advisory. SciAgent opens with a non-negotiable **Operating Discipline** section: the predict-then-run discipline, the Strong Baseline Gate, the anti-stacking check, and the mathematical-justification gate cannot be skipped or rationalized past — only the *user* can relax them. A "Red Flags — You Are Rationalizing" table names the precise thoughts that precede a skipped gate ("I'm fairly sure how this will turn out, I'll skip the prediction"; "the baseline is close enough"; "this notation is dense, the gist is clear enough") and pairs each with the gate it betrays. When the agent catches one, it names the gate and satisfies it rather than narrating past it.

## Mathematical Thinking

The Phase 2 justification gate demands *understood* mathematics, not cited formulas. `reference/mathematical-thinking.md` supplies four lenses — high-dimensional geometric intuition (a matrix is a transformation of space), isomorphism & mapping (relocate a hard problem to where it is easy), limit thinking & error-bound control (approximate and bound the error; state every assumption's validity domain), and probability as a measure over a space (densities and divergences as geometric objects) — plus a meta-discipline: re-derive what you cite, bind every symbol to a concrete meaning, prize the proof over the result, and unpack intimidating notation rather than skipping it. The theory-reviewer subagent enforces these, refusing to pass on notation it has not unpacked or assumptions stated without their regimes.

## Thinking Frameworks

Four cross-cutting reasoning frameworks are woven throughout all phases:

- **First Principles Thinking** — decompose claims to bedrock truths (proven theorems, replicated results), strip away conventions, rebuild from fundamentals
- **Socratic Questioning** — structured probing at every user checkpoint and in reviewer subagents to surface hidden assumptions
- **Occam's Razor** — prefer the simplest hypothesis, experiment design, and explanation that accounts for the evidence
- **Research Taste & Signals** — every experiment is a gradient step: predict before running, compare after, treat disconfirmations as the strongest signal; dig beneath the surface of papers to the substantive decisions that produced them


## Prediction Ledger

`results.tsv` is more than a metrics dump — it is a prediction ledger. Each row is committed *before* a run with `predicted_value`, `predicted_direction`, and `confidence`, and updated *after* with `actual_value` and `signal`. Signals (`confirm` / `partial` / `disconfirm` / `null`) are the project's gradient; null-signal runs are flagged as design failures, not noise.

## Paper Architecture

Phase 6 produces three planning artifacts *before* any prose is written:

- **`paper/narrative-arc.md`** — the story: the fire, why this approach (and not the alternatives), the journey including predictions and disconfirmations, load-bearing assumptions, what was tried and discarded.
- **`paper/motivation-surface-map.md`** — the places where the reader meets the story: title, abstract opening, Introduction topic sentences, headings, figure callouts, Discussion opening and closing. Real draft sentences in the highest-leverage rows, not vague strategy notes.
- **`paper/writing-rationale-matrix.md`** — the row-per-manuscript-unit execution plan. Columns: Manuscript Unit | Planned Function | Idea-DNA Link | Exemplar Pattern | Venue Norm | Evidence Anchor | Operation | Final Text Check. Row 1 justifies the whole-work framework. Subsequent rows follow the chosen structure in order.

Section-writer subagents receive their slice of the matrix as a constraint, not a suggestion. They must satisfy every row's Final Text Check.

## Three Independent Reviewers + Editor Synthesis

Single reviewers correlate with their own prompts. SciAgent dispatches three reviewers **in parallel**, each from a different angle (Methods / Results / Story), each seeing only its prompt and the paper text — no narrative arc, no rationale matrix, no shared context. After all three return, an independence-validation step catches cross-contamination (identical phrasings, role drift). An editor synthesis then merges the three validated reviews into one revision decision.

## Anti-Shallow-Revision Metrics

For any revised draft (v2+), the editor synthesis compares v(N) to v(N-1) against six metrics — near-identical paragraph ratio, dominant operation in the rationale matrix, `KEEP`-row count, missing obligatory moves, unsupported new claims, numbers without source. A revision that fails any row is "patch writing" (a few sentences added or reworded, structure untouched) and must be redone closed-book using `reference/deep-imitation-protocol.md`. These metrics override the reviewer votes — a patch-writing revision is NEEDS_REVISION even with three ACCEPT votes.

## Branch-of-Origin Routing

When a reviewer flags a problem, the orchestrator routes the fix back to the phase that owns the weak artifact, not just the surface where the failure appeared. A generic Introduction is a Phase 0/6-step-1 problem (idea DNA + narrative arc), not a Phase 6 prose patch. A weak baseline is a Phase 1/4 problem, not a Results-section rewrite. Patching at the surface is faster but leaves the upstream gap — and the upstream gap will resurface in peer review.

## License

MIT
