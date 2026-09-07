# DISTINCTIONS — the engine report (Parts 1–2 of the one ambitious session, 2026-07-13)

> Build of record for `PROMPT_DISTINCTIONS_AND_LIVING_THEORY_BUILD.md` Parts 1–2; design of record
> `DESIGN_DISTINCTIONS_AND_LIVING_THEORY.md` §A. Companion: `LIVING_THEORY_REPORT.md` (Part 3).
> Commits: backend `352b04b` (Part 1) + `d3cd5aa` (Part 2); frontend `9b983ba` + `6751e42`. Both pushed.

## 1. What was built

### Part 1 — the Distinction object (re-periodize absorbed, not forked)
A **Distinction** is now first-class (`review_distinctions`): `target` (what we define against), `axis`
(periodization / modernity / method / …), `position_slug`, `skeleton_slug`, `register_slug`, status,
origin. **One source of record by reference, not by copy**: the position and skeleton PROSE live in
Definitions-panel rows (versioned, ratifiable, owner-edited there or through the Distinctions panel —
same endpoint; the engine reads the CURRENT body on every run), and the register is the chartered
register the distinction's reframes grow. Nothing is duplicated in three places.

- **Neoliberalism = Distinction #1** (periodization axis), losslessly: `why_not_neoliberalism` IS its
  position, `reperiodization_skeleton` IS its skeleton, `rival_period_labels` IS its register; every
  pre-existing re-periodization row and edge is backfilled to it (idempotent migrate in
  `ensure_distinction_seeds`). The `rival_label` edge kind generalized to **`reframed_against`** (rows
  migrated in the schema file; the old kind stays in the CHECK for ledger replays; the per-kind label
  switch renders "reframed against ⟨target⟩" — one switch, `EDGE_PREFIX`).
- **`reframe_through_distinction(distinction, card)`** = the shipped re-periodize operation
  parameterized by which distinction ([distinctions.py](../factory/review_pilot/distinctions.py)):
  llm_guard + THAT distinction's skeleton + position ([prompts/reframe_v1.md](../factory/review_pilot/prompts/reframe_v1.md))
  → versioned restatement + title → `reframed_against` edge (carrying `distinction_id`) → grows THAT
  distinction's register on accept ([reformulation.py](../factory/review_pilot/reformulation.py)
  `_materialize_edge` takes the register from the edge) → owner-confirmed harvest-style re-route →
  parked would-be revised unit, undoable single-shot → **vocabulary quarantine enforced server-side
  (one repair re-ask, then 502) — inherited by every distinction**.
- **The `/reperiodize/*` endpoints are thin delegates** to the generic path — the shipped URL surface
  and payload shapes unchanged, zero forked logic. `test_reperiodize.py` was adapted (not weakened) and
  passes THROUGH the generic path: the absorb-without-regression proof the cross-feature rules demanded.
- **Modernity (contra Perry Anderson / Fredric Jameson) = Distinction #2**: a real authorable second
  instance — starter position ("their periodization runs through cultural logic; ours through freedom";
  the Jameson late-capitalism substrate already demoted by §6.6; an explicitly NOT-YET-RULED §5 left to
  the owner) + starter skeleton (P1 spine · P2 correspondence table · P3/P4 negative rule generalized ·
  P5 restatement task), both clearly marked STARTER and landing as drafts in Core Definitions; an empty
  chartered register (`distinction_modernity`) that grows from reframes only — no owner theory invented.
- **Distinctions panel** ([DistinctionsPanel.tsx](../../oaas-frontend/src/components/reviewPilot/DistinctionsPanel.tsx),
  sibling of Core Definitions): list + author (target/axis voice-first; optional starter position/
  skeleton), edit the prose through the definitions machinery ("Open in Core Definitions" jumps to
  versions + ratification), per-distinction register + reframe counts, retire (no-erasure), Explainer.
  The per-card section ([ReframeSection.tsx](../../oaas-frontend/src/components/reviewPilot/ReframeSection.tsx),
  replacing ReperiodizeSection) runs ANY distinction via a picker and carries the provisional-at-accept
  affordance (Part 3's primitive, built early per the cross-feature rule).

### Part 2 — dependency-impact propagation + bulk (the big new capability)
The Phase-B "dependency-impact queue" obligation (§A.3), built as its SHADOW half; the one canonical
step — **bulk-applying approved reframes to the theory of record — stays Phase-B-gated** (appended as
`PHASE_B_OBLIGATIONS.md` §A.11).

- **Impact scan** (`review_distinction_impact`; [prompts/impact_scan_v1.md](../factory/review_pilot/prompts/impact_scan_v1.md)):
  given a distinction, llm_guard re-reads the base in batches of 12 and returns per-unit verdicts —
  `affected` + one-line `why` + `confidence` (high/medium/low). **Incremental by construction**: every
  verdict is keyed to fingerprints of BOTH sides (distinction substance = target+axis+position+skeleton;
  the unit's LIVE formulation). An unchanged re-run reads nothing; a **sharpen** re-reads under the new
  fingerprint and the response reports the **delta** (`newly_affected`); an edited or reframed unit
  re-reads alone. Ruled verdicts (reframed/dismissed) are never rewritten — a re-affecting scan files a
  new pending row beside the old ruling. Per-batch commits: a long scan never loses finished work.
  Detection = the impact scan for one distinction (the Part 6 scan generalized; the per-card badge now
  reads **"affected by ⟨target⟩"**, legacy flags kept as the pre-impact fallback).
- **Bulk reframe**: the single-card operation batched over the pending affected set, ONE TRANSACTION
  PER UNIT — a vocabulary refusal (502) is recorded and the batch continues; already-proposed units
  skip; the impact why rides into each prompt as the detection hint; impact rows advance
  pending→reframed (linked to their proposal), reopen on undo, dismiss on discard.
- **Bulk review / bulk approve** ([BulkReviewSurface.tsx](../../oaas-frontend/src/components/reviewPilot/BulkReviewSurface.tsx)):
  the whole batch skimmable — editable title/text (voice), why-affected + confidence, demotion chips,
  route override, tension line — approve selected / **select-all-that-pass** (pure `itemPasses`
  predicate: no strain line) / dismiss. Each ruling goes through the SAME single-card resolve on its own
  transaction. **Bulk accepts are provisional by default** (origin `bulk_reframe` → the Living Theory
  unstable front); an item may opt out. The surface states plainly: would-be units awaiting the Phase B go.
- **"Update through the base"** (per-distinction, in the panel): scan → affected counts (+ a
  "judged under an older sharpening" badge when the fingerprint moved) → propose → review the batch.
- **Aggressive audit** (`review_llm_pass_log`): one queryable row per LLM call — unit_refs asked over,
  EXPECTED vs ACTUAL (verdicts returned, missing, affected counts), the model's REASONING (the why
  lines), beside the content-addressed prompt/output shas of the preflight chain.
  `GET /distinctions/llm-passes` filters by pass/distinction; `GET /llm-passes/{id}` resolves the FULL
  prompt + raw output from the object store via the hash-linked ledger.

## 2. Live verification (isolated fixture stack, REAL model calls)
Fixture DB `oaas_factory_test_pwf80465` (dropped after), scratch ledgers + manifest, factory :8127,
vite :5273 (`FACTORY_PROXY_TARGET`), the shared relay :8017. The live stack on :8027/:5173 was never
touched; the fence stayed on the fixture app the whole time.

- **Full-base impact scan from the UI** ("Update through the base"): 243 units in 21 batches,
  ~7 minutes, verdicts persisting batch-by-batch (watched live: 24 → 48 → 72 → … → 243). Affected set:
  EXACTLY the three neoliberalism-leaning fixture cards, all high confidence, real why-lines
  ("Explains through neoliberalism as operative category (market as medium of freedom)…"); the
  mere-mention technofeudalism card, the postmodernism card, and the care-work card correctly cleared.
  Panel showed **"3 affected, awaiting reframe · 240 not affected"**. `pw-impact-scan-done.png`.
- **Bulk reframe**: 3 real proposals, persisting one-by-one. The model's restatements kept the
  vocabulary discipline unprompted — one used the flag form `(old appendix: "competitive release")`
  instead of canonizing the coinage. **Select-all-that-pass picked only 1 of 3**: the model had
  reported real strain on two ("the card's Foucauldian machinery … is not reproduced"; "the agentive
  'winning move' framing is softened") — the predicate working on real output. Approved 2 (one with an
  owner-edited title, honored: "The entrepreneur-debtor: competitionism's subject-form"; both parked
  provisional `bulk_reframe/bulk_default`), dismissed 1 → its impact claim ruled `dismissed`.
  `pw-bulk-ruled.png`.
- **Generality in fact**: the postmodernism card reframed live THROUGH THE STARTER MODERNITY SKELETON
  via the per-card picker — "postmodernism (Jameson's cultural logic of late capitalism)" demoted,
  maps to disorganized, the `distinction_modernity` register grew its first source-linked entry;
  accepted with a provisional mark, uncertain span "depthless".
- **Sharpen → incremental delta**: skeleton sharpened live through the panel prose slot (a new P6);
  the bounded re-scan under the new fingerprint (scan_version 2) came back with the loop VISIBLY
  CLOSING — the two approved units now judged **"Already speaks the owner's apparatus"** (not
  affected), the settled postmodern card "Speaks the owner's frame", the dismissed unit re-pending
  beside its kept ruling, `newly_affected` empty.
- **Authoring**: a third distinction ("actor-network theory (Latour)", method axis) authored through
  the panel — position/skeleton definition entries + register auto-created. `pw-distinctions-final.png`.
- **Canonical state**: per-table `factory_*` digest **byte-identical before and after the whole live
  session**. 26 LLM passes in the queryable log (22 impact_scan · 3 bulk_reframe · 1 consolidation),
  all `ok`, each with expected-vs-actual + reasoning.

## 3. Suites
Backend **148 passed** (new: `test_distinctions.py` 6 · `test_propagation.py` 3 — incremental/delta,
per-unit persistence under a mid-batch vocabulary refusal, provisional-by-default; adapted:
`test_reperiodize.py` through the generic path). Frontend **124 passed** (edgeLabels extended;
`reframe.test.ts` pins the absorb: the section talks only to `/api/review-pilot/distinctions`, the
panel edits prose only through `/definitions`). `tsc` + vite build green. Fence inventory line refs
refreshed once (69 refs) after the two router mounts shifted `main.py`; `fence.py` and the `allowed`
list untouched; `FENCE_ACTIVE = True` throughout.

## 4. Honest notes / deferred
- **First-touch race (pre-existing class)**: on the fresh fixture DB, one parallel panel load 500'd
  (`harvest/state`, Postgres deadlock between schema-ensure ALTERs and seed writes) and recovered on
  the next load; the frontend failed calm. Same class the productivity batch hardened once before;
  a per-table advisory-lock sweep is the durable fix if it recurs on deploy.
- The **"Update through the base" button always re-reads the whole base** after a sharpen (that is its
  meaning); a bounded-scope control (scan these N units) exists at the API (`unit_refs`) but has no UI
  affordance yet — worth adding if scans grow expensive.
- Canonical bulk-apply: `PHASE_B_OBLIGATIONS.md` §A.11 (extends §A.9 re-routes; excludes undone/
  dismissed rows; item-by-item idempotent through the deposit transaction).
