# Phase 7: Submission & Rebuttal (optional, user-triggered)

Goal: turn the delivered draft into a submission that satisfies the venue's actual current requirements — and, when external reviews arrive, run a tracked, evidence-based revision loop instead of ad-hoc rebuttal prose.

This phase never starts on its own. It is entered only when the user asks to prepare a submission (Part A) or to respond to external reviews (Part B). The cycle retrospective has already run at Phase 6 close; Part B events feed the next cycle's correction record.

## Part A — Submission prep

1. **Verify the venue's current requirements from the official page** — never from memory: scope, format/template, page/word limits, anonymization policy, LLM policy, checklist requirements. Record the **URL and verification date** in the log. Venue requirements change; a stale memory of them manufactures a desk reject.

2. **Separated disclosure checklist** — six distinct items, each checked on its own (one blob invites omissions):
   - [ ] Conflicts of interest
   - [ ] Funding
   - [ ] Ethics (approvals for any human-subjects/personal data — must trace to the Phase 0 data-governance record)
   - [ ] Data & code availability statement
   - [ ] AI-use disclosure per the venue's current policy (this project is AI-conducted — the check is whether the venue's required wording/placement is satisfied, not whether to disclose)
   - [ ] Duplicate/related submissions and preprint status disclosed per venue policy

3. **Data-availability audit** (blocking conditions — submission does not proceed past any of these):
   - No data-availability statement at all
   - Data behind a central conclusion has no stable identifier or access path
   - "Available upon request" without a genuine access restriction (licensing, privacy) recorded in `data-governance.md`
   - The statement says "data are in the paper" while figure source-data files (`paper/figures/*.source.csv`) are absent
   - Code that produced headline numbers is neither included nor covered by a stated restriction

4. **Submission package assembly** — manuscript in venue format, supplementary materials, source-data files, reproducibility checklist. **Cover letter rule:** it does not repeat the abstract, does not fabricate editor interest, and contains no claim the paper does not support (the letter is checked against the paper like any other claim surface).

5. **Checkpoint:** present the package + checklist state to the user. The user submits; you never do.

## Part B — Revision / rebuttal loop (when external reviews arrive)

1. **Ingest every reviewer comment into a tracked ledger** — `paper/rebuttal/comments.yaml`, one entry per distinct comment:

   ```yaml
   - id: R2-03
     reviewer: R2
     quote: "<the comment, verbatim>"
     severity: minor | major | blocking | unclear
     category: editorial | evidence | methodological | statistical | data-code | citation-positioning | scope | ethics
     action: ACCEPT_TEXT | ACCEPT_ANALYSIS | ACCEPT_EXPERIMENT | CLARIFY_EXISTING |
             ADD_CITATION | SOFTEN_CLAIM | PARTIAL | DISAGREE | AUTHOR_INPUT_NEEDED
     readiness: ready | draft_with_placeholders | needs_user_input | blocked
     location: "<manuscript section/paragraph the response points to>"
   ```

   Every comment gets an entry — including ones you think are wrong (`DISAGREE` is a legal action; ignoring a comment is not). The ledger is append-only like all sciagent state: actions and readiness update, entries never vanish.

2. **Set the revision budget with the user at Part B entry.** New experiments require iteration budget, and only the user grants budget: their approval (quoted verbatim in the log) raises `research_iterations.limit` in `state.json` by the agreed amount — the standard user-override path, not a new budget type. `ACCEPT_EXPERIMENT` items then re-enter the normal machinery — evaluation contract, predict-then-run, `results.tsv` rows, code review — and each re-entry into Phases 1-4 consumes a research iteration exactly as SKILL.md specifies; a reviewer request never suspends the gates. If unspent iterations remain from the original grant, they may be used with the user's explicit OK (quoted). `ACCEPT_ANALYSIS` items route to Phase 5 machinery (declaration block, comparison family — the family grows with every reviewer-requested comparison; re-declare it) without consuming an iteration.

3. **Route each comment by Branch-of-Origin** (SKILL.md) — a methodological comment is a Phase 2-owned fix even now; and apply the **claim-downgrade route** (`reference/bias-frameworks.md` §5): when a flagged limitation cannot be fixed within the revision budget, the response is `SOFTEN_CLAIM` — narrow the claim in the manuscript itself, not only in the response letter.

4. **Write the response letter from the ledger** — one response block per comment, in the reviewers' order. Conduct rules:
   - Every response **points to the exact change location** in the revised manuscript ("§4.2, para 2, revised") **or explains why no change was made** — never a thank-you without one of the two.
   - Disagreement is argued from methods and evidence, never by evaluating the reviewer.
   - No response claims a change the diff does not contain (VERIFY: each `ACCEPT_*` item's stated location actually changed — `git diff` on the manuscript is the evidence).
   - Changes made but not asked for are listed separately and honestly.

5. **One version ledger** — revised manuscript, clean copy, response letter, and supplementary all reference the same version tag (`v2`, `v3` …) recorded in the log; a response letter pointing into a different draft than the one submitted is the classic self-inflicted reject.

6. **Anti-shallow-revision metrics apply** to any substantively revised section (Phase 6 step 8 machinery) — a rebuttal-driven revision can be patch writing too.

7. **Checkpoint:** present the ledger (counts by action + readiness), the response letter, and the revised-manuscript diff summary to the user for approval before anything leaves the workspace.

## Gate (record evidence in `state.json.gates["7"]` — Part A and/or Part B items as applicable)

- [ ] Venue requirements verified from the official page; URL + date logged
- [ ] All six disclosures separately checked
- [ ] Data-availability audit passed (no blocking condition), or the block surfaced to the user
- [ ] (Part B) Every reviewer comment has a ledger entry with action + readiness; none unaddressed
- [ ] (Part B) Every `ACCEPT_*` response's change location verified against the actual diff
- [ ] (Part B) Revision experiments, if any, ran under the user-set budget with full ledger discipline
- [ ] User approved the package / response letter (quoted verbatim)

## Outputs

- Research log: `research-log/[NNN]-submission.md` or `research-log/[NNN]-rebuttal-r[K].md`
- `paper/rebuttal/comments.yaml`, `paper/rebuttal/response-letter.md` (Part B)
- Commit: `research: submission package — [venue]` / `research: rebuttal round [K] — [N] comments addressed`
