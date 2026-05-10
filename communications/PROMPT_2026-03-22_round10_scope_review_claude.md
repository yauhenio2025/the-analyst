# Prompt: Claude Review / Round 10 Consumer Consolidation Scope

Read the following first:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_scope.md`

Then inspect the real code seams in both repos:

- analyzer-v2:
  - `renderers-ui/package.json`
  - `renderers-ui/src/index.ts`
  - `renderers-ui/src/renderers/`
  - `renderers-ui/src/sub-renderers/`
- the-critic:
  - `webapp/package.json`
  - `webapp/src/pages/AnalysisWorkspacePage.tsx`
  - `webapp/src/components/V2TabContent.tsx`
  - `webapp/src/components/ViewRenderer.tsx`
  - `webapp/src/components/renderers/initRenderers.ts`
  - `webapp/src/components/renderers/index.ts`
  - `webapp/src/components/renderers/SubRenderers.tsx`
  - `webapp/src/components/renderers/`

Your task:

1. Critique the round-10 memo as a strategic scope document.
2. Test whether it is genuinely aligned with the roadmap after round 9.
3. Check whether the memo corrects the older vision doc accurately, or overcorrects.
4. Check whether the tranche is bounded and high-value, or whether it is secretly:
   - too broad
   - too trivial
   - or still under-specified
5. Identify what the memo gets wrong or leaves ambiguous about the real codebase.
6. Focus especially on:
   - whether the package is already materially consumed
   - where the live generic renderer path is still consumer-owned
   - whether `GenealogyPage` and view-key overrides are correctly kept out of scope
   - whether the package-version drift (`0.5.5` vs `0.6.3`) changes the scope story
   - whether the proof standard is strong enough
   - whether the proposed bounded AOI slice is the right proof slice
7. Tell me whether this round is coherent with the big picture:
   - thin consumer thesis
   - analyzer-v2-owned renderer assets
   - eventual compose-from-intent

Output requirements:

- Save your review to exactly:
  - `communications/REPORT_Claude_Round10_Consumer_Consolidation_Scope_Critique_2026-03-22.md`
- The review should be written as a direct engineering critique, not a chat reply.
- Start with:
  - `Verdict: Approve`
  - or `Verdict: Approve after revision`
  - or `Verdict: Do not approve`
- Then include:
  - `What the memo gets right`
  - `Findings`
  - `Bottom line`

Review standard:

- Be skeptical.
- Test claims against the actual code.
- Prefer concrete code references over abstract objections.
- If the memo is directionally right but needs tightening, say exactly what should change before planning begins.

