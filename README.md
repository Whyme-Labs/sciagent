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

Three cross-cutting reasoning frameworks are woven throughout all phases:

- **First Principles Thinking** — decompose claims to bedrock truths (proven theorems, replicated results), strip away conventions, rebuild from fundamentals
- **Socratic Questioning** — structured probing at every user checkpoint and in reviewer subagents to surface hidden assumptions
- **Occam's Razor** — prefer the simplest hypothesis, experiment design, and explanation that accounts for the evidence

## Key Principles

- **Theory before experiments** — mathematical justification required
- **Reframe, don't stack** — genuine innovation, not technique combination
- **Simplicity over cleverness** — prefer elegant solutions
- **Everything documented** — full audit trail
- **Honest science** — negative results are valuable findings

## License

MIT
