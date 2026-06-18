# SciAgent

A Claude Code skill for autonomous scientific research — from idea to publication-quality paper.

## What It Does

SciAgent encodes a complete scientific research methodology that Claude follows. Give it a research idea, and it will:

1. **Review literature** — search multiple sources in parallel, build a gap analysis, populate Exemplar Move Tables that feed Phase 6 writing
2. **Form hypotheses** — with mathematical justification and cited prior work (not guessing)
3. **Validate with PoC** — run quick probes before committing to full experiments
4. **Run experiments** — adaptive plans with baselines, ablations, and robustness checks
5. **Analyze & iterate** — statistical analysis, diminishing returns detection, evidence-based pivots
6. **Write the paper** — narrative arc + motivation surface map + writing rationale matrix as the execution plan; three independent reviewers in parallel + editor synthesis; anti-shallow-revision metrics on every iteration

Every experiment is gated by scientific reasoning. No blind hyperparameter tweaking. Every paragraph of the paper is gated by a rationale-matrix row. No generic academic prose.

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

## Key Principles

- **Theory before experiments** — mathematical justification required
- **Predict, then experiment** — every run records a numeric prediction *before* dispatch; the signal (confirm / partial / disconfirm / null) is the gradient that drives the next iteration. No prediction means no experiment, just data to retrofit a story around.
- **Anti-fragile signals** — stagnation is worse than negative results; disconfirmations sharpen the model of the problem and are treated as primary outputs
- **Strong baselines only** — improvements over weak baselines are fictional; baselines are audited for strength before being targeted
- **Research taste** — break through the surface of papers to the substantive decisions; every methodological choice survives a "why" probe
- **Read for motivation, write the whole story** — when reading others' work, extract the motivation, constraints, decisions, and load-bearing assumptions, not just the method; when writing our own paper, tell the actual story (predictions, surprises, disconfirmations, dead ends), not a sanitized post-hoc narrative
- **Reframe, don't stack** — genuine innovation, not technique combination
- **Simplicity over cleverness** — prefer elegant solutions
- **Mathematical depth, not decoration** — the justification gate demands *understood* mathematics (matrices as transformations of space, hard problems mapped into easier spaces, error controlled rather than exact solutions chased, probability as a measure over a space), with the validity domain of every assumption stated, key steps re-derived from scratch, and dense notation unpacked rather than skipped
- **Everything documented** — full audit trail, including a prediction ledger in `results.tsv`
- **Honest science** — negative results are valuable findings

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
