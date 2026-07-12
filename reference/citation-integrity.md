# Citation Integrity and Retrieval Protocol

How literature is retrieved reproducibly, how references are verified beyond existence, and how the support relation between a claim and its citation is graded. Extends Phase 1's spot-check verification (which stays: random-sample fetch + number check) with field-level and claim-level machinery. Consumed by Phase 1, the literature-searcher output contract, and Phase 6's citation checks.

## 1. Source-tier retrieval routing

Search sources in tiers; escalate only when the lower tier is insufficient:

- **T1 — authoritative APIs, search first, in parallel:** Crossref (DOI metadata), arXiv, PubMed (biomedical). Fast, structured, rate-limit-friendly.
- **T2 — aggregators, escalate when T1 coverage is thin:** Semantic Scholar, bioRxiv/medRxiv, OpenAlex.
- **T3 — scraped/manual, last resort, always flagged:** Google Scholar, publisher pages, CNKI (Chinese literature). Every source's lit JSON records its `tier` (the orchestrator supplies it in the searcher dispatch); tier-3 batches may be stale or unparseable and get verified first.

Fallback algorithm: T1 in parallel → insufficient coverage → add T2 → still insufficient → T3 with a logged warning → return partial results + suggest query refinement. A per-source failure is reported and worked around, never silently dropped.

## 2. Reproducible search record

Two kinds of search, recorded separately:

- **Exploratory search** (following leads, interviewing the literature) — logged as narrative in the research log. Free-form.
- **The systematic record** — for every batch query a searcher runs, the lit JSON carries a `search_record` array: `{query: "<verbatim string>", platform, date, result_count}`. This is what makes "we surveyed the field" auditable when a reviewer challenges related-work completeness — and it costs one line per query.

For `reproduction` projects and Deep intensity, additionally fix the **inclusion/exclusion criteria before batch screening** (in the Phase 1 log, before step 2's dispatches) and record counts through the funnel: identified → screened → included, with one-line exclusion reasons. Deviations from the pre-stated criteria are logged with time, reason, and effect on conclusions.

## 3. Field-level reference verification

"The paper exists" is not "the reference is right." When a citation enters the paper's reference list (Phase 6), verify fields against the authoritative record (Crossref by DOI first; title+author lookup as fallback) and grade mismatches:

| Severity | Mismatch |
|---|---|
| 🔴 Critical — fix before the draft leaves | **DOI resolves to a different paper** (title/authors don't match); author name or order wrong; title core words wrong; venue wrong |
| 🟡 Warning — check | year in the citation ≠ year in the DOI record; missing/wrong volume, issue, or pages; preprint cited where a published version exists |
| 🟢 Info — normalize silently | title casing, journal abbreviation vs. full name, punctuation |

Per-reference status recorded in the lit database: `verified | needs_fix | unverifiable`. An `unverifiable` reference supporting a load-bearing claim is treated as absent — find a verifiable source or cut the claim.

## 4. Claim-support grading

Separate question from §3: does the cited work actually SUPPORT the sentence citing it? For each citation-bearing claim (systematically in the Phase 6 claim-to-source table; the faithfulness spot-check then samples from it), grade the support:

- **strong** — the source directly demonstrates the claim (its own results/proof)
- **partial** — the source supports a weaker or narrower version → **narrow the sentence to what the source supports** (the narrow-the-sentence rule)
- **background** — topically related context; establishes that the area exists, not that the claim is true
- **contradictory/limiting** — the source cuts against the claim → must be cited as such, never laundered into support
- **metadata-only** — known from title/abstract-listing alone

Hard rules:

1. **Never cite a metadata-only source** — read at least the abstract/results before the citation is legal.
2. A **mechanism, method, or quantitative claim** may not rest on a `background`-grade citation. Background citations motivate; they do not substantiate.
3. Reviews/surveys are context: where a primary source exists for a specific claim, cite the primary.
4. Claims are typed before grading (`mechanism | association | method | quantitative | background/definitional`); a claim too broad to grade is split into subclaims.

## 5. Extraction provenance

For structured data extracted FROM papers (SOTA tables, baseline numbers, `key_results`):

- **Pilot the schema on 2 differently-structured papers** before a batch extraction round; fix the schema mismatches the pilot exposes, then run the batch.
- Key fields carry a **location**: page / table / figure / section ("Table 2", "§4.1"), so verification is a lookup, not a re-read.
- **`not_reported` ≠ `missing` ≠ `not_applicable` ≠ zero.** Four different values; a number the paper doesn't report is `not_reported`, never 0 and never silently skipped (the same rule `results.tsv` already applies to crashes).
- Extracted numeric fields carry `extraction_confidence: high|low` (set by the searcher) and `reviewed: yes|no` (always `no` from the searcher; the orchestrator flips it to `yes` at the Phase 1 verification step for the papers it checked). A low-confidence unreviewed number never enters the SOTA table that baselines are chosen from — verify it first.
