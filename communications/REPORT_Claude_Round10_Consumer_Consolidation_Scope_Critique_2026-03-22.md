# Review: Round 10 / Consumer Consolidation Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-22
Documents Reviewed:
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_scope.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- Code inspection of `renderers-ui/` and `the-critic/webapp/src/components/renderers/`

---

## Verdict: Approve after revision

The round-10 direction is correct. Consumer consolidation is the right next step after round 9. The AOI proof slice is the right surface. The hard stops are well-placed.

But the memo significantly overstates the current gap and therefore risks scoping a round that either (a) proves something trivially small, or (b) drifts into registry-architecture work that the memo does not acknowledge as the real substance.

Three revisions are needed before planning begins.

---

## What The Memo Gets Right

**1. Roadmap alignment is correct.**

The roadmap memo said the post-round-8 sequence should be: freeze declarative substrate v1 → renderer contract validation → consumer consolidation → bounded compose-from-intent. Round 9 closed renderer contract validation. Round 10 targeting consumer consolidation is exactly on schedule.

**2. The older vision doc correction is accurate.**

The DYNAMIC_BESPOKE_APPS_VISION.md said the missing step was "publish and install `@the-syllabus/analysis-renderers`." The memo correctly identifies that the package is already installed, already consumed, and that the real question has shifted from "can it be published?" to "can the-critic stop owning the generic renderer path?"

**3. The AOI proof slice is the right choice.**

AOI exercises the generic `AnalysisWorkspacePage` path, avoids bespoke genealogy concerns, and has round-9 serve-time enforcement as a regression backstop. No better proof surface exists for a consolidation tranche.

**4. Hard stops are well-placed.**

The memo correctly blocks genealogy cleanup, broad renderer-catalog rewrites, CSS/token redesign, and compose-from-intent work. These are real drift risks and the memo names them.

**5. GenealogyPage exclusion is correct.**

`SynthesisRenderer` and `IdeaEvolutionRenderer` are view-key-specific genealogy renderers registered via `registerViewRenderer()`. They are not on the generic type-resolution path. Keeping them out of scope prevents round 10 from collapsing into a genealogy cleanup round.

---

## Findings

### Finding 1: The memo overstates the current consumer ownership gap

**The memo says** (line 85-100):

> `V2TabContent.tsx` still renders through local `ViewRenderer`
> `ViewRenderer.tsx` still resolves through a local registry
> `src/components/renderers/index.ts` still owns type/view-key resolution
> `src/components/renderers/initRenderers.ts` still registers the live renderer map

**What the code actually shows:**

The generic type-based renderer path is *already substantially package-backed*. Here is the actual `initRenderers.ts` registration:

| Registration | Source |
|---|---|
| `prose` → ProseRenderer | Thin re-export of `@the-syllabus/analysis-renderers` |
| `card_grid` → CardGridRenderer | Thin re-export |
| `accordion` → AccordionRenderer | Thin re-export |
| `table` → TableRenderer | Thin re-export |
| `stat_summary` → StatSummaryRenderer | Thin re-export |
| `card` → CardRenderer | Thin re-export |
| `nested_sections` → NestedSectionsRenderer | **Real local implementation (~150 lines)** |
| `timeline` → CardGridRenderer | Thin re-export (alias) |

7 of 8 type registrations are already single-line re-exports from the package. The implementations are package-owned. The consumer owns only:

1. The **plumbing** — `initRenderers.ts`, `index.ts` (dual registry maps), `ViewRenderer.tsx` (resolution dispatch)
2. One **real generic renderer** — `NestedSectionsRenderer.tsx`
3. Three **sub-renderer aliases** — `concept_dossier_cards`, `dimension_analysis_cards`, `directional_transfer_list` all map to the package's `mini_card_list`
4. Two **domain-specific cell renderers** — `TacticCardCell.tsx`, `RelationshipCardCell.tsx`
5. Two **genealogy view-key renderers** — correctly out of scope

The memo's framing of "parallel local renderer ownership still on the critical path" is misleading. The rendering itself is package-owned. What is consumer-owned is the **registry/resolution infrastructure** and **one real generic renderer** (`NestedSectionsRenderer`).

**Why this matters for scope:**

If the round is framed as "make the package authoritative for the generic renderer family," most of that is already true for the *implementations*. What remains is the *dispatch mechanism*. The memo needs to be honest about that distinction, or the planning phase will either:

- produce a trivially small deliverable (delete thin re-export files, import directly), or
- discover mid-implementation that the real work is restructuring the dispatch/registry, which the memo does not discuss

### Finding 2: The AOI path may already satisfy the proof standard without meaningful code changes

On the AOI proof slice specifically (`adaptive_aoi_theme_report_suite_v1`), the rendering path goes through:

1. `AnalysisWorkspacePage` → `V2TabContent` → `ViewRenderer`
2. `ViewRenderer` resolves by `renderer_type` (no view-key override on AOI views)
3. The resolved renderers are `AccordionRenderer`, `CardGridRenderer`, `ProseRenderer`, `StatSummaryRenderer`, etc. — all thin re-exports from the package

The AOI path **does not hit** `NestedSectionsRenderer`, `SynthesisRenderer`, `IdeaEvolutionRenderer`, or the domain-specific cell renderers. Those are genealogy concerns.

So the AOI proof slice may already be "package-backed for the generic renderer family" in substance, with the only consumer-owned seam being the registry plumbing itself.

**Required revision:** The memo should clarify whether the consolidation target is:

(a) Removing the thin re-export shim files and having `initRenderers.ts` import directly from `@the-syllabus/analysis-renderers` — this is trivial
(b) Moving the registry/resolution mechanism (`initRenderers.ts` + `index.ts` + `ViewRenderer.tsx`) into the package or replacing it with a package-provided helper — this is real architecture work
(c) Something else entirely

Without this clarification, the "likely structural move" section (lines 156-175) is too vague to plan against.

### Finding 3: The version drift story is more specific than the memo implies

The memo says (lines 103-104):

> `renderers-ui/package.json` is at `0.6.3`
> the-critic currently resolves `@the-syllabus/analysis-renderers` at `0.5.5`

**What the code actually shows:**

The-critic's `package.json` resolves the dependency via **local tarball**:

```
"@the-syllabus/analysis-renderers": "file:../../analyzer-v2/renderers-ui/the-syllabus-analysis-renderers-0.5.5.tgz"
```

This is not an npm registry version drift. It is a stale tarball. The tarball was packed at `0.5.5` and never re-packed after the package advanced to `0.6.3`.

**Implications for round 10:**

1. Resolving the version drift means re-packing the tarball (or switching to a workspace/symlink resolution). This is mechanically simple but has regression risk — 8 minor versions of changes between `0.5.5` and `0.6.3`.
2. The consolidation work and the version-drift resolution should probably happen together, not independently — consolidating on a stale package version would be pointless.
3. The memo should explicitly require that the version drift is resolved as a precondition, not left as optional ("whether the package-version drift was resolved as part of the tranche" on line 225).

**Required revision:** Make version-drift resolution a hard precondition for round 10, not an optional proof documentation item.

### Finding 4: NestedSectionsRenderer is the one real generic renderer ownership question

`NestedSectionsRenderer.tsx` is the only locally-implemented **type-level** renderer. It is ~150 lines of custom section rendering logic with collapsible state, metadata extraction, and section density scoring.

This renderer is registered at the type level (`registerTypeRenderer('nested_sections', NestedSectionsRenderer)`), meaning it participates in the generic resolution path just like the package-owned renderers.

The memo does not mention it by name. It should. The execution plan needs to decide:

- Does `NestedSectionsRenderer` move into the package as part of round 10?
- Or does it remain as an explicit local override (the "narrow consumer-owned override seam")?
- Does the AOI proof slice use `nested_sections`? If not, this can be deferred.

### Finding 5: Sub-renderer aliasing is a real but small seam

`SubRenderers.tsx` in the-critic wraps the package's `resolveSubRenderer` with three aliases:

```typescript
'concept_dossier_cards' → package's 'mini_card_list'
'dimension_analysis_cards' → package's 'mini_card_list'
'directional_transfer_list' → package's 'mini_card_list'
```

Plus it keeps `nested_sections` mapped to the local `NestedSectionsRenderer`.

This is a thin local seam but it is real. The question for round 10 is whether these aliases should move into the package's sub-renderer registry or remain as consumer-level routing.

### Finding 6: The cell renderer merge pattern is well-structured

The-critic's `cells/index.ts` cleanly merges:

```typescript
export const cellRenderers = {
  ...baseCellRenderers,              // from package
  tactic_card: TacticCardCell,       // local override
  relationship_card: RelationshipCardCell,  // local override
};
```

This is already the "explicit consumer-owned override seam" pattern the memo envisions. `TacticCardCell` and `RelationshipCardCell` are genealogy-specific and correctly stay local. The cell merge pattern may already be the round-10 proof of what the broader registry should look like.

### Finding 7: The proof standard needs one addition

The proof standard (lines 213-225) is reasonable but missing one check:

**Add:** "the package version consumed by the-critic matches the package source in renderers-ui" — without this, the consolidation could land on a stale base and the proof would be unreliable.

---

## Bottom Line

The memo is directionally right on all major calls:

- Consumer consolidation is the correct next step
- AOI is the correct proof slice
- Genealogy is correctly excluded
- Hard stops are correctly placed

But the memo overstates the current gap by conflating **renderer implementation ownership** (already largely package-backed via thin re-exports) with **registry/dispatch infrastructure ownership** (still consumer-local). This matters because the real consolidation work is in the plumbing, not the renderers, and the memo does not acknowledge that.

**Three revisions before planning:**

1. **Tighten the gap description.** Acknowledge that generic renderer implementations are already package-backed via re-exports. Reframe the consolidation target as the registry/dispatch infrastructure plus the version drift, not "the generic renderer path."

2. **Make version-drift resolution a hard precondition.** The tarball is at `0.5.5`, the source is at `0.6.3`. Consolidating on a stale package is not consolidation. This should be a gate, not an optional documentation item.

3. **Name the real scope question explicitly.** The round's substance is: does the-critic keep owning the registry/dispatch mechanism (with the package providing implementations), or does the package absorb the dispatch mechanism too? The memo should state this as the execution-plan decision rather than leaving it as a vague "likely structural move."

If those three revisions land, the scope is bounded, honest, and high-value. Without them, the planning phase will likely discover mid-flight that the nominal scope is either trivially small or architecturally larger than anticipated.
