# Phase 6: Paper Writing

Goal: a publication-quality paper — deterministically verified for internal consistency BEFORE the reviewer gate, so LLM review effort goes to judgment, not typo-hunting.

## Steps

1. **Write the story before the outline.** A paper is an argument, not a report. In 3-5 sentences, write the narrative arc:
   - **Tension** — the problem from `PROBLEM.md`, stated so the reader feels why it matters
   - **Gap** — why existing approaches don't resolve it (from the literature map)
   - **Insight** — the named concept from Phase 2, in one sentence
   - **Evidence** — the one or two results that carry the claim (including the distinguishing prediction's outcome)
   - **Resolution** — what is now true that wasn't before, and what it costs (limitations)

   Every section must advance this arc; every writer dispatch includes it. If a planned section doesn't serve the story, cut or merge it.

2. **Plan the structure** — title, section-by-section outline mapped to the story arc, and a mapping of which research-log content feeds each section. Draft the outline from the story first, then refine it against the research logs (draft-then-refine beats outlining directly from the material — the story keeps the material from dictating the structure). The complete structure:
   - **Title** — concise, descriptive
   - **Abstract** — problem, approach, key result, significance (150-300 words, includes the headline number)
   - **Introduction** — motivation, gap, approach, numbered contributions, outline
   - **Related Work** — organized by technique family, fair positioning
   - **Methodology** — formal presentation, all assumptions stated, proofs included
   - **Experimental Setup** — reproducible from this section alone
   - **Results** — tables, figures, statistical significance
   - **Discussion** — interpretation, honest limitations, unexpected findings
   - **Conclusion** — contributions, implications, evidence-based future work
   - **References** — all cited papers, properly formatted

3. **Fresh literature pass (before writing):** one bounded searcher round on the exact claim — what has been published since Phase 1? New papers go through the same verification pipeline into `research-log/lit/`; genuinely concurrent work gets cited and positioned honestly. Reviewers reject for missing the concurrent paper that did the same thing; the citation-database-only rule must not become a staleness trap.

4. **Dispatch section writer subagents in parallel** for independent sections (`prompts/section-writer.md`). Each writer receives the story arc alongside its source material, writes to `paper/sections/[NN]-[name].md` (**NN = the section's position in the outline, 01-09**), and returns a summary. The Discussion and Conclusion writers ALWAYS receive the full `tried_and_failed` array and every `results.tsv` row (all statuses) — the 3,000-word trimming rule never applies to failure evidence. Groups:
   - **Group 1 (parallel):** Related Work, Methodology, Experimental Setup
   - **Group 2 (after 1):** Results, Discussion
   - **Group 3 (after 2):** Introduction, Abstract, Conclusion

   Paste each writer's source material in full; if a source file exceeds ~3,000 words, paste only the parts relevant to that section. Include `learnings` from `state.json`.

5. **Assemble and edit** — merge `paper/sections/` into a coherent paper: fix cross-references, unify notation, write transitions, verify the narrative follows the story arc and is anchored in the idea DNA — and that the paper answers `PROBLEM.md`'s core question, or honestly states how far it got. The introduction must pose the same problem `PROBLEM.md` does; if the paper has quietly become about something else, stop and resolve that with the user before review.

   **Disclosure requirements (top venues require these; omitting them manufactures a policy violation):**
   - Pre-specified vs. post-hoc: the primary comparison from Phase 2 is presented as the pre-specified test; everything else is labeled secondary/exploratory. Disclose the number of hypothesis iterations attempted (the forking-paths disclosure).
   - Headline numbers are the once-run test-set numbers; validation numbers appear as tuning history.
   - AI-assistance disclosure per the target venue's policy — this paper was drafted by an autonomous system; check and follow the venue's LLM policy explicitly.
   - Compute disclosure: total compute used, from `results.tsv` runtime columns.

6. **Run the deterministic consistency checks yourself (VERIFY — before any reviewer dispatch):**
   - [ ] Every figure referenced in the text exists in `paper/figures/`; every generated figure is referenced
   - [ ] Every result number in the paper appears in `results.tsv` or the analyzer tables — check at minimum every number in the abstract and results tables
   - [ ] Every citation exists in `research-log/lit/*.json` (the verified citation database). A citation not in the database is presumed fabricated — remove it or verify it by fetching the source
   - [ ] No placeholder text: `grep -niE "TODO|PLACEHOLDER|\[CITATION\]|lorem|conclusions here" paper/`
   - [ ] No results claimed for experiments that don't have a `results.tsv` row
   - [ ] Crashed/discarded runs are not presented as findings (negative results ARE presented, honestly labeled)
   - [ ] **Citation faithfulness spot-check:** number all citation-bearing sentences and select 5 **at random with a logged `shuf` command** (paste command + selection as evidence); open each source (from `research-log/lit/*.json`) and confirm the sentence actually follows from it — not just that the source exists. If any fail, sweep that writer's whole section
   - [ ] **Connective-tissue check:** for claims that LINK two cited facts ("X implies Y", "this explains why…"), each link is either itself sourced, or supported by our own experimental evidence, or explicitly marked as our interpretation. Unverifiable links between individually-true facts are the signature failure of automated writing — hunt them

   Fix every failure before proceeding. These checks are cheap; reviewer rounds are not.

7. **Supplementary materials:** full experiment table from `results.tsv` (all runs, all statuses, including failures and exploratory runs), hyperparameter configs per run, additional figures, long proofs, environment and reproducibility checklist.

8. **Dispatch paper reviewer subagent** (most capable model available; `prompts/paper-reviewer.md`). The dispatch is **sterile** (template content only); the reviewer reads the assembled paper **from disk** and reports its line count (VERIFY against `git show HEAD:<path> | wc -l`). Budget: 2 review rounds — **`spent` increments at dispatch time, every dispatch; every verdict is logged verbatim before any re-dispatch; an adverse verdict can never be declared invalid.** At Deep intensity, dispatch TWO independent reviewers in parallel with different emphases (methodology/statistics vs. claims/novelty) and reconcile.
   - **PUBLISH_READY** — valid only with evidence of scrutiny (what was checked, strongest objection considered). Otherwise one invalid-scrutiny re-dispatch per round.
   - **NEEDS_REVISION** — fix issues (or dispatch targeted section writers), re-dispatch. The re-review receives the previous issue list, judges each issue RESOLVED/IMPROVED/UNCHANGED/WORSE, and must also spend part of its report hunting new issues.
   - Budget exhausted → present the draft to the user with remaining open issues listed honestly.

9. **Generate output** in the format chosen at Phase 0: DOCX (primary), LaTeX (.tex + .bib), or Markdown in `paper/`.

10. **Present to user:** "Paper draft complete: [title]. [word count] words, [N] figures, [M] references. Saved to [path]. Please review."

## Gate (record evidence in `state.json.gates["6"]`)

- [ ] Test set was evaluated exactly once, and the paper's headline numbers are those numbers (empirical projects)
- [ ] Fresh literature pass done; concurrent work cited
- [ ] All deterministic consistency checks passed (list them with results, including the logged random selections)
- [ ] Disclosure requirements met (pre-specified vs post-hoc, iteration count, AI-assistance per venue policy, compute)
- [ ] Paper reviewer verdict PUBLISH_READY with evidence of scrutiny, OR review budget exhausted with open issues disclosed to user; all dispatches counted, all verdicts logged
- [ ] User has reviewed the draft

## Outputs

- Research log: `research-log/[N]-paper-draft.md` — compilation decisions, check results, reviewer findings and fixes, Gate Check
- Commit: `research: paper draft v1 — [title]`
