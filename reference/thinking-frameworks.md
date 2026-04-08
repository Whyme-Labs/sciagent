# Thinking Frameworks

Three cross-cutting reasoning frameworks applied throughout the research process. These are not phases — they are lenses applied within existing phases to sharpen scientific reasoning, challenge assumptions, and resist unnecessary complexity.

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

## How the Frameworks Interact

- **First Principles** strips claims to bedrock. **Occam's Razor** strips hypotheses to essentials. Together they prevent both question-bloat and approach-bloat.
- **Socratic Questioning** is the engine that drives both — it's how you probe whether a claim is bedrock (first principles) and whether complexity is justified (Occam's razor).
- These frameworks reinforce the existing SciAgent principles: theory-before-experiments (first principles ensures the theory is on solid ground), simplicity criterion (Occam's razor applied to experiment results), and anti-stacking (first principles asks whether the combination is conceptually necessary or just conventional).
