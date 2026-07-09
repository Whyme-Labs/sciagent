# SciAgent

A Claude Code skill for autonomous scientific research — from idea to publication-quality paper.

## What It Does

SciAgent encodes a complete scientific research methodology that Claude follows. Give it a research idea — or just an inspiration — and it will:

0. **Ideate** (inspiration entry) — survey the topic landscape, gather SOTA numbers and active benchmarks, scout a reproducible baseline to innovate on, and propose concrete candidate ideas for you to pick from
1. **Review literature** — search multiple sources in parallel, verify citations, build a gap analysis
2. **Form hypotheses** — with mathematical justification and cited prior work, gated by independent theory review
3. **Validate with PoC** — run quick probes before committing to full experiments
4. **Run experiments** — baseline reproduction first, adversarial code review before results are believed, then adaptive plans with ablations, tuned-baseline parity, and multi-seed robustness
5. **Analyze & iterate** — statistical analysis with effect sizes, budgeted iteration, evidence-based pivots, and an explicit publish decision (contribution paper / conclusive negative result / internal report)
6. **Write the paper** — story-first narrative (tension → gap → insight → evidence → resolution), full academic structure, deterministically verified for consistency and citation faithfulness, then reviewer-gated

Every experiment is gated by scientific reasoning. No blind hyperparameter tweaking.

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
├── section-writer.md           # One paper section per dispatch
└── paper-reviewer.md           # Top-venue publication-readiness review
```

Phase files are loaded just-in-time when the loop enters that phase — the always-loaded core stays small.

## Installation

### Personal Skill (available across all projects)

```bash
# Clone the repo
git clone https://github.com/Whyme-Labs/sciagent.git

# Symlink or copy into Claude Code's skill discovery directory
ln -s "$(pwd)/sciagent" ~/.claude/skills/sciagent
```

Claude Code auto-discovers skills from `~/.claude/skills/`. Once installed, invoke with `/sciagent` or Claude will auto-trigger it when your request matches the skill description.

### Project Skill (available only in one project)

```bash
# From your project root
mkdir -p .claude/skills
ln -s /path/to/sciagent .claude/skills/sciagent
```

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

- **Theory before experiments** — mathematical justification required, independently reviewed
- **Reframe, don't stack** — every hypothesis must make a testable prediction that a plain combination of techniques would not
- **Extrapolate and engineer** — question structures the field assumes necessary (what property do they actually provide?), and treat composition as engineering: every component justified against a measured bottleneck, ablated, and claimed only through its end-to-end impact
- **Simplicity over cleverness** — prefer elegant solutions
- **Everything documented** — full audit trail, negative results included
- **Honest science** — evidence-gated progress; nothing is "done" on self-assessment
- **Reproducibility** — environment, seeds, and exact commands recorded

## License

MIT
