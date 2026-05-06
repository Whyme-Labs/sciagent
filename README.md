# SciAgent

A Claude Code skill for autonomous scientific research — from idea to publication-quality paper.

## What It Does

SciAgent encodes a complete scientific research methodology that Claude follows. Give it a research idea, and it will:

1. **Review literature** — search multiple sources in parallel, build a gap analysis
2. **Form hypotheses** — with mathematical justification and cited prior work (not guessing)
3. **Validate with PoC** — run quick probes before committing to full experiments
4. **Run experiments** — adaptive plans with baselines, ablations, and robustness checks
5. **Analyze & iterate** — statistical analysis, diminishing returns detection, evidence-based pivots
6. **Write the paper** — full academic structure with supplementary materials

Every experiment is gated by scientific reasoning. No blind hyperparameter tweaking.

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

Start a conversation with Claude and describe your research idea:

```
I want to investigate whether [approach X] can improve [metric Y] on [problem Z].
```

Claude will follow the SciAgent protocol:
- Ask clarifying questions (Phase 0: Setup)
- Search for related work (Phase 1: Literature Review)
- Form and justify a hypothesis (Phase 2: Hypothesis)
- Run a quick proof-of-concept (Phase 3: PoC)
- Execute the full experiment plan (Phase 4: Experiments)
- Analyze results and decide next steps (Phase 5: Analysis)
- Write the paper (Phase 6: Paper Writing)

At each phase, Claude checks in with you at key decision points.

## Research Intensity

Set at the start of each project:

| Level | Papers | Experiments | Best For |
|-------|--------|-------------|----------|
| Light | 5-10 | Few | Quick exploration |
| Medium | 15-25 | Full plan | Solid investigation |
| Deep | 30-50 | Comprehensive | Publication-grade |

## Output

- **Research logs** — `research-log/` with one Markdown file per research event
- **Results tracking** — `results.tsv` for machine-readable experiment comparison
- **Paper** — DOCX (primary), LaTeX (optional), or Markdown (fallback)
- **Git history** — every decision, experiment, and analysis is a commit

## Project Structure

SciAgent creates this workspace for each research project:

```
your-research-project/
├── research-log/           # Scientific narrative
├── results.tsv             # Experiment metrics
├── experiments/            # Code and configs
│   ├── poc/                # Proof-of-concept
│   └── configs/            # Environment + evaluation contract
├── data/                   # Datasets
└── paper/                  # Living document + figures
```

## Thinking Frameworks

Four cross-cutting reasoning frameworks are woven throughout all phases:

- **First Principles Thinking** — decompose claims to bedrock truths (proven theorems, replicated results), strip away conventions, rebuild from fundamentals
- **Socratic Questioning** — structured probing at every user checkpoint and in reviewer subagents to surface hidden assumptions
- **Occam's Razor** — prefer the simplest hypothesis, experiment design, and explanation that accounts for the evidence
- **Research Taste & Signals** — every experiment is a gradient step: predict before running, compare after, treat disconfirmations as the strongest signal; dig beneath the surface of papers to the substantive decisions that produced them

## Key Principles

- **Theory before experiments** — mathematical justification required
- **Predict, then experiment** — every run records a numeric prediction *before* dispatch; the signal (confirm / partial / disconfirm / null) is the gradient that drives the next iteration. No prediction means no experiment, just data to retrofit a story around.
- **Anti-fragile signals** — stagnation is worse than negative results; disconfirmations sharpen the model of the problem and are treated as primary outputs
- **Strong baselines only** — improvements over weak baselines are fictional; baselines are audited for strength before being targeted
- **Research taste** — break through the surface of papers to the substantive decisions; every methodological choice survives a "why" probe
- **Read for motivation, write the whole story** — when reading others' work, extract the motivation, constraints, decisions, and load-bearing assumptions, not just the method; when writing our own paper, tell the actual story (predictions, surprises, disconfirmations, dead ends), not a sanitized post-hoc narrative
- **Reframe, don't stack** — genuine innovation, not technique combination
- **Simplicity over cleverness** — prefer elegant solutions
- **Everything documented** — full audit trail, including a prediction ledger in `results.tsv`
- **Honest science** — negative results are valuable findings

## Prediction Ledger

`results.tsv` is more than a metrics dump — it is a prediction ledger. Each row is committed *before* a run with `predicted_value`, `predicted_direction`, and `confidence`, and updated *after* with `actual_value` and `signal`. Signals (`confirm` / `partial` / `disconfirm` / `null`) are the project's gradient; null-signal runs are flagged as design failures, not noise.

## License

MIT
