# Thinking Frameworks

Four cross-cutting reasoning frameworks applied throughout the research process. These are not phases — they are lenses applied within existing phases to sharpen scientific reasoning, challenge assumptions, and resist unnecessary complexity.

---

## 1. First Principles Thinking

**Core idea:** Decompose any claim, assumption, or conventional wisdom to its fundamental truths — things that are mathematically proven, physically necessary, or empirically established beyond doubt — and rebuild understanding from there.

### The Method

1. **State the belief:** Write down the assumption or conventional wisdom being examined.
2. **Ask "Why is this true?"** repeatedly until you hit bedrock — a constraint backed by proof, physical law, or overwhelming empirical evidence.
3. **Separate bedrock from convention:**
   - **Bedrock:** "Attention is O(n^2) in sequence length" — this is a mathematical property of full dot-product attention.
   - **Convention:** "Transformers need attention for long-range dependencies" — this is widely accepted but challengeable (state-space models exist).
4. **Rebuild from bedrock only:** Given only the unchallengeable constraints, what is the most direct path to the research goal?

### Forcing Questions

- "Which claims in this field are proven vs. widely assumed?"
- "What would we try if no one had worked on this problem before?"
- "Are we constrained by a theorem, or by what prior papers chose to do?"
- "What assumption, if wrong, would change everything about our approach?"

### When to Apply

| Phase | Application |
|-------|-------------|
| Phase 0: Setup | Decompose the research idea — is the stated problem a real gap, or a symptom of framing conventions? |
| Phase 1: Literature | Audit prior work — which results are bedrock (proven theorems, replicated experiments) vs. convention (untested assumptions, community habits)? |
| Phase 2: Hypothesis | Is the mathematical justification built on proven results or common assumptions? |

---

## 2. Socratic Questioning

**Core idea:** Use structured, probing questions to surface hidden assumptions, test the strength of reasoning, and deepen understanding. Not interrogation — collaborative inquiry that helps discover what is actually known vs. assumed.

### The Six Question Types

1. **Clarification:** "What exactly do you mean by [X]?" / "Can you formalize that?"
   - Use when terms are vague or overloaded (e.g., "generalization," "robustness").

2. **Probing assumptions:** "What are we taking for granted here?" / "Why do we believe [X] holds in this setting?"
   - Use when a claim feels obvious — obvious claims hide the most dangerous assumptions in science.

3. **Probing evidence:** "What evidence supports this?" / "Has this been replicated, or is it a single result?"
   - Use when drawing conclusions from literature or experiment results.

4. **Exploring perspectives:** "What would a critic of this approach say?" / "How would [competing school of thought] explain this result?"
   - Use when the direction seems uncontested — lack of contest can mean lack of scrutiny.

5. **Examining consequences:** "If this hypothesis is true, what else must be true?" / "What's the worst case if our assumption is wrong?"
   - Use when evaluating hypotheses and interpreting results.

6. **Questioning the question:** "Are we solving the right problem?" / "Is this the right metric to optimize?"
   - Use when the research framing itself feels off.

### Application Rules

- **One question at a time.** Let the answer shape the next question.
- **Follow the thread.** Don't follow a script — respond to what emerges.
- **No leading questions.** "Don't you think X?" is persuasion, not inquiry.

### When to Apply

| Phase | Application |
|-------|-------------|
| Phase 0: Setup | Probe the research idea — "Why hasn't this been tried? What would have to be true for it to work?" |
| All user checkpoints | Don't just ask "approve?" — probe: "What are you least confident about? What assumption feels shakiest?" |
| Phase 2: Hypothesis | The theory reviewer should use Socratic structure when challenging claims |
| Phase 5: Analysis | "What's the simplest explanation for these results? What would change your mind?" |

---

## 3. Occam's Razor

**Core idea:** Among competing hypotheses or approaches that account for the evidence equally well, prefer the simplest. In science, this means: don't introduce complexity that the evidence doesn't demand.

### The Simplicity Test

For any hypothesis, experiment design, or result interpretation, ask:

1. **Is there a simpler hypothesis that explains the same expected outcome?** If yes, test that one first.
2. **Is every component of the experiment plan justified by a specific question?** Remove "just in case" experiments.
3. **Is the explanation proportional to the evidence?** Don't invoke a complex mechanism when a simple one accounts for the data.
4. **Does the complexity earn its keep?** Sometimes complexity is necessary — but it must be proportional to what it explains.

### Complexity Red Flags in Research

- A hypothesis with more free parameters than the evidence can constrain
- An experiment plan with ablations for components whose contribution is already theoretically predicted
- An explanation that requires multiple interacting mechanisms when one suffices
- A methodology section longer than the results it produces
- "Future-proofing" experiments that test conditions not relevant to the current hypothesis

### When to Apply

| Phase | Application |
|-------|-------------|
| Phase 2: Hypothesis | Prefer the simplest falsifiable hypothesis. If simpler and complex hypotheses predict the same outcome, test simpler first. |
| Phase 4: Experiments | Design the minimal experiment set that tests the core claim. Cut "just in case" runs. |
| Phase 5: Analysis | Prefer the simplest explanation of results. Flag when complex theories aren't needed. |
| Phase 6: Paper | Reviewer flags explanations more complex than the evidence warrants. |

---

## 4. Research Taste & Signals

**Core idea:** Research progress is stochastic gradient descent. Each experiment is a step, and a step is only useful if it produces a *gradient* — a signal about which direction to move next. Taste is the discipline of choosing steps that are likely to produce strong signals, and of reading the substantive (not surface) lessons of papers and results. The mental compass — *belief preceding sight* — directs the random walk; predictions and evidence ground each step.

### Three Operating Beliefs

1. **A result without a prediction is not a signal.** If you did not write down what you expected before the run, you cannot tell after the run whether you were right, lucky, or fooling yourself. The narrative will always rationalize the number. Prediction → Run → Compare is the loop that generates true gradients.

2. **Negative signals are valuable; null signals are expensive.** A disconfirmed prediction sharpens your model of the problem — it is a strong gradient pointing away from a wrong hypothesis. A run that produces no clear signal (you didn't know what you expected, or the experiment couldn't distinguish hypotheses) is the worst outcome: it consumed compute and yielded no direction. Eliminate null-signal experiments before running them, not after.

3. **Taste is repeated "why."** Reading a paper, do not stop at the proposed method. Ask: *why* did the authors choose this dataset, this baseline, this metric, this framing? *Which* prior decisions made this particular method seem natural? *What* would have made them choose differently? The published artifact is the surface; the substantive research is the chain of decisions that produced it. The same applies to your own work: every methodological choice should survive a "why" probe back to bedrock.

### The Predict–Run–Compare Loop

For every experiment (PoC or full run):

1. **Predict** — record a numeric prediction, a directional prediction (`beat-baseline` / `match-baseline` / `regress` / `unclear`), and a confidence level (`low` / `medium` / `high`).
2. **Justify** — write one paragraph: why this prediction, citing theory or prior runs.
3. **Run** — execute the experiment.
4. **Compare** — was the prediction `confirm` / `partial` / `disconfirm` / `null`?
5. **Update** — if confirmed, your model of the problem is unchanged but more credible. If disconfirmed, *something specific* in your model is wrong; identify what. If null, the experiment was poorly designed; redesign before next run.

### Reading and Writing — the Same Lens

Reading others' work and writing our own are the same skill applied in opposite directions. Both reach for the substance behind the surface.

**When reading a paper**, do not stop at the method. The published artifact is the surface. The substantive research is the chain of decisions that produced it. For each significant paper in the literature review, extract:

- **Motivation** — what did the authors actually care about? What problem were they living with that drove this work? (This is rarely fully written down; you have to infer it from the introduction's framing, the choice of benchmark, the choice of failure cases shown.)
- **Constraints** — what could the authors not do? Compute, data access, prior commitments, reviewer expectations. These constraints often explain methodological choices better than the stated motivation does.
- **Decisions** — why this baseline, this benchmark, this metric, this scale, this framing? For each, ask: what would have changed if they had chosen otherwise?
- **What they tried and discarded** — sometimes visible in ablations, footnotes, supplementary; often visible only between the lines. A paper rarely shows you its dead ends, but the shape of the dead ends is implied by the shape of what they kept.
- **Load-bearing assumptions** — which assumption, if wrong, would invalidate the whole paper? This is usually not the assumption the authors highlight.

A paper read this way is a much richer artifact than a paper read for "what method did they propose."

**When writing our own paper**, apply the same lens to ourselves. The reader will read us the way we read others — so write the version they would *want* to extract:

- **Tell the actual story** — why does this problem matter (not in generic-importance language, but in the specific way it mattered to us)? Why this approach and not the alternatives? What were our real constraints?
- **Show the journey** — what did we predict? What surprised us? What disconfirmations forced us to revise? The Introduction sets up the question; the Discussion is where the journey is honest. Disconfirmations recorded in the prediction ledger become first-class material for the Discussion, not buried.
- **Surface the load-bearing assumptions** — state them plainly, as the assumptions a future reader should challenge. This is the opposite of hiding them.
- **Resist the post-hoc narrative** — the temptation is to rewrite the story so the conclusion looks inevitable. Resist this. A paper that admits "we expected X, but observed ¬X, and that surprise led us to Y" teaches more, ages better, and is harder to dismiss than a paper that pretends Y was obvious from the start.
- **The personal "fire" should be visible** — not as autobiography, but as the conviction that motivated the specific framing. This is what makes a paper feel alive rather than mechanical, and it is what makes the reader trust that the authors actually believed what they were doing.

The duality is the discipline: every "why" we extract from others is a "why" we owe our own readers.

### Anti-Fragility

Treat shocks as fuel, not noise:

- A surprising negative result is the cheapest insight you can buy. Spend at least as much analysis time on disconfirmations as on confirmations.
- When the literature says X and your experiment shows ¬X, do not first assume your experiment is broken. First take the disagreement seriously: under what conditions could both be true? What does the literature implicitly assume that your setup violates?
- A research line that has not encountered a single surprise yet is suspicious — it usually means the experiments are too easy, too well-aligned with the hypothesis, or under-instrumented.

### Forcing Questions

- "What did I predict, and what did I actually observe? What does the gap teach me?"
- "If this experiment came out the opposite of my prediction, would I know what to do next? If not, the experiment is poorly designed."
- "Is this baseline strong enough that beating it means something, or am I improving over a strawman?"
- "Why did the authors of this paper make *this specific* methodological choice? What would have changed if they had chosen otherwise?"
- "What is the ‘fire’ behind this research direction — the conviction that brought us here? Is each step grounded in evidence, or am I drifting from the original idea DNA?"
- "Have I had any genuine surprises this iteration? If not, am I actually learning anything?"

### Complacency Red Flags

- Running an experiment without writing the prediction down first.
- Explaining away a disconfirmation ("the seed was unlucky") without rerunning to verify.
- A `results.tsv` where every `signal` is `confirm` — either the predictions are too vague, or the experiments are too easy.
- Treating a paper's claimed result as a fact rather than as the output of a chain of decisions.
- Comparing against a baseline because it is convenient, not because it is the strongest available.

### When to Apply

| Phase | Application |
|-------|-------------|
| Phase 0: Setup | Surface the personal "fire" — why does this idea matter? Capture it as part of the idea DNA so the project has a compass. |
| Phase 1: Literature | For top papers, do a "decision archaeology" pass: why these baselines, why these metrics, why this framing? Audit baseline strength. |
| Phase 2: Hypothesis | Predicted effect must be quantified with a confidence level, not just directional. |
| Phase 3: PoC | Record the prediction in `results.tsv` *before* dispatching. Write Prediction-vs-Reality in the log entry. |
| Phase 4: Experiments | Strong baseline gate. Predict-then-run for every experiment. Treat disconfirmations as primary outputs. |
| Phase 5: Analysis | Calibration audit — across all runs, where were predictions systematically off? That bias is the deepest finding. |
| Phase 6: Paper | Discussion section explicitly reports surprises and disconfirmations, not just successes. |

---

## How the Frameworks Interact

- **First Principles** strips claims to bedrock. **Occam's Razor** strips hypotheses to essentials. Together they prevent both question-bloat and approach-bloat.
- **Socratic Questioning** is the engine that drives both — it's how you probe whether a claim is bedrock (first principles) and whether complexity is justified (Occam's razor).
- **Research Taste & Signals** ties the loop closed: it ensures every experiment produces a gradient, that gradients are honestly interpreted, and that the substantive (not surface) lessons of prior work guide direction. It is the framework that transforms a sequence of runs into actual research.
- These frameworks reinforce the existing SciAgent principles: theory-before-experiments (first principles ensures the theory is on solid ground), predict-then-experiment (research taste makes signals first-class), simplicity criterion (Occam's razor applied to experiment results), and anti-stacking (first principles asks whether the combination is conceptually necessary or just conventional).
