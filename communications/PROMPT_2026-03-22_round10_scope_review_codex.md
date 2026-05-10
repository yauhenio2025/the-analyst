# Prompt: Codex Review / Round 10 Consumer Consolidation Scope

Audit the round-10 scope memo against the actual analyzer-v2 and the-critic codebases.

Read first:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_scope.md`

Then inspect these code paths directly:

- analyzer-v2:
  - `renderers-ui/package.json`
  - `renderers-ui/src/index.ts`
  - `renderers-ui/src/renderers/`
  - `renderers-ui/src/sub-renderers/`
  - `renderers-ui/release-artifacts/`
- the-critic:
  - `webapp/package.json`
  - `webapp/node_modules/@the-syllabus/analysis-renderers/package.json`
  - `webapp/src/pages/AnalysisWorkspacePage.tsx`
  - `webapp/src/components/V2TabContent.tsx`
  - `webapp/src/components/ViewRenderer.tsx`
  - `webapp/src/components/renderers/initRenderers.ts`
  - `webapp/src/components/renderers/index.ts`
  - `webapp/src/components/renderers/SubRenderers.tsx`
  - `webapp/src/components/renderers/NestedSectionsRenderer.tsx`
  - `webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
  - `webapp/src/components/renderers/SynthesisRenderer.tsx`

Your job:

1. Audit whether the scope memo matches the real code seams.
2. Identify exactly which parts of the the-critic renderer path are:
   - already package-backed
   - thin local wrappers
   - real local logic
   - still on the live critical path
3. Test the memo’s key assumptions:
   - package install is no longer the missing step
   - the generic renderer path is still substantially consumer-owned
   - AOI is the right bounded proof slice
   - genealogy-specific overrides should remain out of scope
   - version drift is real enough to matter
4. Tell me whether the memo is a real bounded consolidation round or a disguised framework rewrite.
5. Call out any execution traps that the eventual plan must handle.
6. Evaluate whether the proof standard is strong enough to prove actual consolidation rather than cosmetic import churn.

Output requirements:

- Save your review to exactly:
  - `communications/REPORT_Codex_Round10_Consumer_Consolidation_Scope_Audit_2026-03-22.md`
- Write the review as a repo-grounded audit.
- Start with:
  - `Verdict: Approve`
  - or `Verdict: Approve after revision`
  - or `Verdict: Do not approve`
- Then include:
  - `Repo-grounded observations`
  - `Findings`
  - `Bottom line`

Audit standard:

- Use concrete code references.
- Prefer identifying drift seams and hidden scope expansion risks.
- If you think the memo is right, say what still needs to be nailed down before implementation planning.
- If you think the memo is wrong, say whether the right next move should instead be:
  - a narrower consolidation slice
  - stronger renderer/sub-renderer law
  - or compose-from-intent

