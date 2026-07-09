# Mathematical Thinking

The Phase 2 justification gate is the spine of SciAgent: no experiment runs without mathematical/theoretical justification. But "justification" can degrade into mechanical citation — quoting a theorem number, applying a formula, producing symbols that look rigorous but carry no understanding. This reference exists to keep the justification *deep* rather than *decorative*.

The thesis: mathematics in research is not calculation. It is intuition about structure — seeing matrices as transformations of space, mapping a hard problem into a space where it is easy, controlling error rather than chasing exact solutions, and treating probability as a measure over a space rather than a frequency count. An agent that reaches for these lenses produces justifications that survive a skeptical reviewer; an agent that memorizes formulas produces justifications that collapse at the first "why?".

These are lenses applied *within* the existing phases — primarily Phase 2 (hypothesis justification) and the theory-reviewer subagent — not a new phase. They reinforce **First Principles** (decompose to bedrock) and **Research Taste** (substance behind surface). See [thinking-frameworks.md](thinking-frameworks.md).

---

## 1. High-Dimensional Geometric Intuition

**Core idea:** A matrix is not a table of numbers — it is a transformation of space (stretch, rotate, compress). A vector is a point or a direction in that space. Multiplying a matrix by a vector moves the vector to a new position. A deep network is a sequence of these transformations interleaved with non-linearities, folding and unfolding a high-dimensional data manifold until classes become linearly separable.

When a justification touches linear algebra, demand the geometric reading alongside the algebraic one:

- **Eigenvectors / eigenvalues** — directions left unchanged by a transformation, and the stretch/compress ratio along them. Not "roots of the characteristic polynomial."
- **PCA** — the eigenvector of largest eigenvalue is the direction of maximum variance (maximum information) in the data cloud. Not "the top of a sorted list."
- **SVD** — *any* linear transformation decomposes into rotate → scale-along-axes → rotate. The foundation of compression, low-rank approximation, and recommender systems.
- **Condition number / spectrum** — the ratio of largest to smallest eigenvalue tells you the *shape* of the loss landscape. An ill-conditioned covariance means steep gradients in some directions and flat ones in others; the optimizer oscillates in a narrow ravine and never settles. (The opening anecdote of the source material: an over-fit diagnosis that was actually a spectrum problem, invisible to anyone treating the matrix as numbers rather than as a shape.)
- **Trace** — geometrically the divergence of the transformation, the instantaneous rate of volume change. Not just "the sum of the diagonal."

### Forcing questions
- "What does this matrix *do* to the space — stretch, rotate, project, collapse a dimension?"
- "If I plotted the data manifold, what is the geometry of the operation this hypothesis proposes?"
- "Is a pathology here actually a spectral/conditioning problem masquerading as something else (over-fitting, slow convergence, instability)?"

---

## 2. Isomorphism and Mapping

**Core idea:** If a problem is intractable in its current space, map it to a space where it is easy, solve it there, and map the answer back. The hard structure is preserved; only the representation changes.

- **Fourier transform** — convolution in the time domain becomes multiplication in the frequency domain. A noise signal that looks structureless in time decomposes into a handful of sine waves in frequency; zero the offending frequency, invert, and the noise is gone. The philosophy: when facing a tangle, do not force it open in the current dimension — find the transform that steps outside it.
- **Word / token embeddings** — language cannot be added arithmetically, but mapped into a dense continuous vector space, semantic relationships become geometric distances. Generation is a nearest-vector search in that space, then an inverse map back to language. This is structure-preserving mapping, not a trick.
- **Log / exp, kernel maps, change of variables, the reparameterization trick** — all the same move: relocate the problem to where its structure is simple.

When a hypothesis is hard to justify directly, ask whether the difficulty is intrinsic or an artifact of the chosen representation. A reframing that maps the problem into a more natural space is often a stronger (and more *anti-stacking*) contribution than adding machinery in the original space.

### Forcing questions
- "Is this hard because the problem is hard, or because I am in the wrong space?"
- "Is there a transform under which this operation becomes trivial?"
- "What structure am I preserving across the map, and does the inverse map back cleanly?"

---

## 3. Limit Thinking and Error-Bound Control

**Core idea:** Real systems rarely have closed-form solutions. The work is not to find the exact answer but to *approximate* it and *control the error*. This is the dividing line between school algebra (solve for the clean root) and analysis (bound the gap to the truth).

- **Gradient descent** is limit thinking in practice: you cannot see the global minimum, only the local slope; you step, re-evaluate, and approach. The questions that matter are convergence, rate of convergence, and the error envelope — not "the solution."
- **Validity domains are load-bearing.** A Taylor expansion is an excellent approximation *inside its radius of convergence* and diverges catastrophically outside it. The cautionary case from the source material: an options-pricing model using a local Taylor approximation lost a large sum in an extreme-volatility regime that pushed past the convergence radius — the formula did not just degrade, it *diverged* and emitted absurd signals. An engineer who understood the remainder term and the convergence domain would have clamped at the boundary. One who memorized "the first three terms" would not.
- **Discipline: do not memorize conclusions — interrogate boundary conditions.** The preconditions of a theorem are frequently more important than the theorem. "Use at room temperature" is part of the spec; running the device in a furnace and blaming the device is not the device's fault.

This is the lens that turns the Phase 2 justification from "the math says it works" into "the math says it works *under these stated conditions*, and here is what happens at the boundary." Every assumption stated in the justification should come with the regime in which it holds.

### Forcing questions
- "Am I assuming an exact solution exists when I should be bounding an approximation?"
- "What is the validity domain of this approximation, and what happens at and beyond its boundary?"
- "Which precondition of this theorem, if violated by my setting, makes the result not just weaker but wrong?"
- "Have I stated the regime in which each assumption holds, or only the assumption?"

---

## 4. Probability as Measure over a Space

**Core idea:** In the generative-model era, probability is not coin-flipping and urn-drawing — it is a *measure over a set in a space*, and it must be read geometrically. Probability density lives on a manifold; sampling and generation are walks and drifts over that manifold.

- **Diffusion models** make this concrete: the forward process adds Gaussian noise step by step (an easily-described Markov transition) until the image is pure noise; the network learns the *reverse* process, drifting the probability density back from noise to a meaningful image manifold. Read with this lens, the integrals and expectation symbols are an elegant random walk plus reverse drift in a high-dimensional density space — not an impenetrable wall of notation.
- **Quantization, distillation, pruning** require measuring the distance between distributions — relative entropy (KL divergence) between the original weight distribution and the quantized one. To argue a compression scheme is sound, you measure how much probability mass moved, not whether the code runs.
- **The variational lower bound (ELBO)** is the canonical example of bounding an intractable quantity (the evidence) by a tractable one — limit thinking (§3) and probability-as-measure meeting in one object.

When a hypothesis is probabilistic, the justification should reason about distributions, densities, and divergences as objects in a space — what is the measure, what is its support, how far does the proposed operation move mass — not about isolated point estimates or frequencies.

### Forcing questions
- "What is the probability measure here, and what space does it live on?"
- "What is the support of this distribution, and does the proposed operation move mass off it?"
- "If I need to compare two distributions, what divergence am I using and why is it the right one?"
- "Can I bound this intractable quantity by a tractable one (a variational bound), the way ELBO bounds the evidence?"

---

## Meta-Discipline: How to Use Math Without Faking It

These rules govern *how* SciAgent and its theory reviewer engage with mathematics, regardless of which lens applies. They exist because the failure mode is not "wrong math" — it is *hollow* math that looks rigorous and isn't.

1. **The agent's job is to define the problem; the math serves the definition.** The hardest, most human part of research is abstracting a messy real situation into a mathematical model — choosing what to keep, what to discard, what structure to impose. This is taste, and it is where the idea DNA lives. Formula manipulation is downstream of it. A justification that jumps straight to equations without first arguing *why this is the right model* has skipped the load-bearing step.

2. **Beware the illusion of knowledge.** Reading a smooth derivation and nodding is not understanding. The Phase 2 self-critique requires *re-deriving* the key steps, not re-reading them. If a derivation cannot be reconstructed from a blank page, it is not yet owned and must not be cited as if it were settled.

3. **Prize the proof over the result.** When mining a paper for justification (Phase 1 decision archaeology), read the appendix — the convergence proof, the error-bound derivation — not just the headline number. The proof reveals *how the authors thought* and *what they had to assume*; the result is a by-product. A justification anchored in a result you have not seen proven is anchored in faith.

4. **Bind every abstraction to a concrete meaning.** Never let a symbol float. Trace (§1) means volume-change rate; KL divergence (§4) means probability mass moved; a Taylor remainder (§3) means the size of the approximation gap. Bound abstractions surface unreasonable model behavior fast — an engineer who knows what the trace *means* spots a broken model before the metrics do.

5. **Deconstruct intimidating notation; do not skip it.** A long expression of sums, integrals, and Greek letters is a composition of operations you already understand. Peel it like an onion to the familiar pieces — addition, multiplication, limits, expectations — then reassemble. The reflex to skip to the conclusion when notation looks scary is the single largest barrier; the theory reviewer must refuse to let a justification pass on notation it has not unpacked.

6. **The breakthrough is usually a structure, not more compute.** Self-attention is mathematically simple; its power is that it dissolved the long-range-decay problem and parallelizes as matrix multiplication — one structural insight, not brute force. When a hypothesis proposes "more scale" as the mechanism, ask whether the real lever is a better mathematical structure (this is the anti-stacking instinct in mathematical clothing).

---

## When to Apply

| Phase | Application |
|-------|-------------|
| Phase 1: Literature | Decision archaeology reads the *proofs and error bounds* in appendices, not just results (meta-rule 3). Audit which lens each key result lives in (geometric / mapping / approximation / measure). |
| Phase 2: Hypothesis | The mathematical-justification gate must reason in the appropriate lens, state validity domains for every assumption (§3), and survive re-derivation in the self-critique (meta-rule 2). |
| Phase 2: Theory review | The reviewer unpacks notation rather than passing on it (meta-rule 5), checks that abstractions are bound to concrete meaning (meta-rule 4), and verifies boundary/validity conditions are stated (§3). |
| Phase 5: Analysis | When results surprise, check whether the cause is geometric/spectral (§1) or a violated validity domain (§3) before inventing a new mechanism. |
| Phase 6: Paper | Methodology states load-bearing assumptions *with their regimes of validity*; proofs that justify bounds belong in the supplementary, derived, not asserted. |
