# Report: Close Read Concept-Analysis Family Admission Audit

## Context Check

Read in full before concluding:

- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md`
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`

Code inspected directly:

- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx`

## Verdict

**Approve with corrections.**

The memo gets the strategic framing right:

- the old Critic estate is a `concept-analysis` family, not a mere `logic` page
- `Close Read` currently admits genealogy and AOI, not concept analysis
- the next serious admission question should therefore be the concept-analysis family boundary

But the memo should be corrected in three places before it is treated as the clean boundary setter:

1. it understates analyzer-v2 inventory breadth for the family, especially `assumption_excavation`
2. it does not sharply enough distinguish analyzer-v2 inventory from live Critic adoption, especially for `logical`
3. it misses live concept-family follow-up operations beyond reading, especially premise scrutiny and corpus-ammunition search

## Code-Backed Assessment

### 1. The memo is right to frame the next admission line as `concept analysis family`, not `logic` in isolation

This is strongly supported by product structure, not just by interpretation.

- The old Critic route family is explicitly `concept-analysis`, with concept and type subpaths, in `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:14-16` and `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:153-156`.
- The old concept estate exposes six submodes, not just `logical`: `semantic_field`, `logical`, `inferential`, `assumption`, `causal`, `metaphorical`, in `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:906-913`, `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:934-940`, and `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:1256-1261`.
- The backend enum matches the same six-mode family in `/home/evgeny/projects/the-critic/api/server.py:1030-1036`.

So the memo’s core correction to the roadmap is sound: if the roadmap says “admit logic next,” it is reading the old product estate too narrowly.

### 2. The memo is also right that current `Close Read` does not already include this family

Current `Close Read` is narrower and explicitly dual-family.

- Routes only admit `close-read/genealogy` and `close-read/aoi` in `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:23-26` and `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:255-275`.
- The family switcher hard-codes only `genealogy | aoi` in `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx:4-31`.
- The genealogy page literally presents itself as a “Genealogy family reading surface” in `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx:410-418`.
- The AOI pages present themselves as AOI family surfaces and reuse `AoiV2ThematicPanel` in `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx:73-81` and `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx:283-289`.

That supports the memo’s roadmap order:

- genealogy and AOI are the currently admitted default families
- concept analysis is a next admission question
- it is not already implicitly included by the current umbrella

### 3. The memo is correct that migration reality is mixed, but it needs sharper calibration

The mixed-state claim is directionally right.

Live Critic execution is clearly split:

- `inferential` still runs through a local prompt-and-script path in `/home/evgeny/projects/the-critic/api/server.py:3900-3902` and `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py:33-90`.
- `logical` still runs through a local multi-pass orchestrator in `/home/evgeny/projects/the-critic/api/server.py:3903-3910` and `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py:1-17`.
- `semantic_field`, `causal`, and `metaphorical` already use analyzer-v2 prompt composition through `run_generic_analysis()` in `/home/evgeny/projects/the-critic/api/server.py:3923-3931` and `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py:24-59`.

But two important corrections are needed.

#### Correction A: analyzer-v2 inventory is broader than the memo says

The memo calls out the 12-phase chain, concept suite, and inferential engine. That is true, but incomplete.

There is also serious analyzer-v2 inventory for:

- `assumption_excavation` in `/home/evgeny/projects/analyzer-v2/src/engines/definitions/assumption_excavation.json:2-10`
- `concept_semantic_field` in `/home/evgeny/projects/analyzer-v2/src/engines/definitions/concept_semantic_field.json:2-9`
- `concept_causal_mechanisms` in `/home/evgeny/projects/analyzer-v2/src/engines/definitions/concept_causal_mechanisms.json:2-9`
- `concept_metaphorical_ground` in `/home/evgeny/projects/analyzer-v2/src/engines/definitions/concept_metaphorical_ground.json:2-9`

So the right correction is not “analyzer-v2 is less capable than the memo says.”
It is:

- analyzer-v2 inventory is broader than the memo explicitly inventories
- live Critic adoption of that inventory is thinner and more uneven than the inventory alone suggests

#### Correction B: the memo should stress harder that `logical` is still materially legacy-bridged

The 12-phase chain is good evidence of analyzer-v2 concept-analysis ambition:

- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json:2-19`

And the old Critic logical path clearly reuses analyzer-v2-style engine keys:

- `concept_argument_formalization` in `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py:19-25`
- five dedicated vulnerability engine keys in `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py:21-32`

But the live logical path is not yet cleanly equivalent to a published analyzer-v2 family contract.

Most notably:

- the live Critic vulnerability phase spans five subpasses in `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py:21-32`
- the published analyzer-v2 12-phase chain only names one vulnerability engine, `concept_vulnerability_inferential_gaps`, in `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json:75-80`

So the memo should not merely say “mixed.”
It should say:

- inferential has a clear analyzer-v2 capability analogue but still runs legacy-local
- logical has meaningful analyzer-v2 overlap, but current product behavior is still materially anchored in the old Critic orchestrator and auxiliary Critic services

## What The Memo Misses

### 1. It does not miss a material old-product submode

The six old-product submodes are all named:

- `inferential`
- `logical`
- `assumption`
- `semantic_field`
- `causal`
- `metaphorical`

On that question, the memo is complete.

### 2. It does miss material follow-up operations from the old concept-analysis estate

This is the most important omission.

The memo is right that concept analysis is the first family where `Close Read` cannot honestly remain “just a reading shell,” but it should say more concretely what already exists in the old product.

Live code shows at least two material follow-up operations beyond reading:

- **premise scrutiny** as a dedicated operation family, with `quick`, `deep`, and `both` modes in `/home/evgeny/projects/the-critic/api/server.py:6708-6716`
- **corpus-ammunition search** from scrutiny outputs, launched from logical attacks and routed through corpus selection plus LLM analysis in `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:2068-2185`

The logical detail surface is therefore not just:

- arguments
- chains
- vulnerabilities

It is also:

- attack generation
- premise stress-testing
- follow-on corpus search for supporting ammunition

That is more specific than the memo’s current phrasing around “lines of attack style follow-on work,” and it matters because this family is likely the first serious test of engine-specific operation law under `Close Read`.

## First-Cut Calibration

### Is the “likely first core = inferential + logical” hypothesis reasonable?

**Yes, with one explicit caveat.**

It is reasonable because:

- the original dictation explicitly centers logical premise-testing and weak-point identification
- the old Critic product gives `inferential` and `logical` the richest family-specific depth
- those two submodes most clearly express the “engine-specific follow-up operations” thesis the roadmap is trying to recover

Code supports that:

- inferential has dedicated commitment, incompatibility, tension, stakes, and package tabs in `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:2270-2304`
- logical has dedicated arguments, chains, causal, and vulnerabilities tabs in `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:2306-2332`
- logical also carries live scrutiny and ammunition follow-up paths in `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:2068-2185`

The caveat is:

- the boundary memo should not treat `inferential` and `logical` as equally ready

More honest posture:

- `inferential` = core submode with analyzer-v2 engine contract already present, but still legacy-executed
- `logical` = core submode by product importance, but legacy-bridged and not yet cleanly analyzer-v2-backed end to end

### Should another submode be treated as equally primary?

**No, not equally primary.**

But `assumption` deserves stronger treatment than the memo currently gives it.

Why:

- it is a visible old-product submode in `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:1509-1520`
- live Critic uses an `assumption_excavation` engine path in `/home/evgeny/projects/the-critic/api/server.py:1692-1758`
- analyzer-v2 also contains a substantive `assumption_excavation` engine definition in `/home/evgeny/projects/analyzer-v2/src/engines/definitions/assumption_excavation.json:2-10`

So I would not promote `assumption` to equal-primary with `inferential + logical`.
But I would make it the strongest explicitly named second-wave/support-mode candidate, not lump it together casually with the lighter semantic/causal/metaphorical remainder.

## Roadmap Fit

The memo keeps the right order of work.

It does **not** drift prematurely into:

- standalone-host resolution
- composition-layer implementation
- generic shell harmonization

That is consistent with the surrounding roadmap memos:

- bounded `Close Read V1`
- dual-family `V1.5` coexistence
- then next family admission work
- only later broader composition-layer freezing

So on the larger roadmap question, the memo is well disciplined.

## Explicit Answers

### Is the memo right to frame the next admission line as `concept analysis family`, not `logic` in isolation?

Yes. The old Critic product is structurally a concept-analysis family with six submodes, not a single logical-analysis product.

### Does the memo miss any material concept-analysis submode or follow-up operation from the old Critic product?

It does not miss a material submode. It does miss material follow-up operations:

- premise scrutiny
- scrutiny mode selection (`quick` / `deep` / `both`)
- corpus-ammunition search launched from logical attacks

### Does the memo overstate analyzer-v2 readiness, or understate how much legacy behavior still matters?

Both, slightly.

- It **understates analyzer-v2 inventory breadth** by not naming `assumption_excavation` and the already-defined semantic/causal/metaphorical engines.
- It **overstates practical readiness if read too optimistically**, because live inferential and logical execution remain Critic-local, and logical follow-up behavior still depends on Critic-specific scrutiny/ammunition services.

### Is the “likely first core = inferential + logical” hypothesis reasonable, or should the next boundary memo treat another submode as equally primary?

It is reasonable. No other submode should be treated as equally primary. But `assumption` should be called out as the strongest support-mode / second-wave candidate rather than treated as generic residue.

### Does the memo keep the right order of work, or does it drift prematurely into composition-layer or standalone-host concerns?

It keeps the right order of work. It remains family-admission-focused and appropriately defers composition-layer implementation and standalone-host resolution.

## Recommended Corrections Before Reuse

1. Add one paragraph explicitly stating that analyzer-v2 inventory also includes `assumption_excavation`, `concept_semantic_field`, `concept_causal_mechanisms`, and `concept_metaphorical_ground`, even though live Critic adoption is uneven.
2. Tighten the migration section so `logical` is described as a **legacy-bridged core submode**, not merely “mixed.”
3. Add a concrete note that the old concept-analysis estate already includes live follow-up operations:
   - premise scrutiny
   - quick/deep scrutiny modes
   - corpus-ammunition search from scrutiny results
4. In the “first admitted submodes” discussion, keep `inferential + logical` as the likely core, but explicitly name `assumption` as the strongest next support-mode candidate.

## Final Reading

The memo is strategically right and materially useful.

The correct next admission question is indeed:

- not “logic next”
- but “what is the first honest `Close Read` admission of the concept-analysis family?”

But the next boundary memo should enter that question with stricter wording:

- broader analyzer-v2 inventory than this memo currently names
- deeper live legacy dependence than “mixed” alone conveys
- and more explicit acknowledgment that concept analysis already embodied real engine-specific follow-up operations in the old Critic product

With those corrections, this is the right bridge artifact between the current genealogy/AOI umbrella and the next serious default-family admission line.
