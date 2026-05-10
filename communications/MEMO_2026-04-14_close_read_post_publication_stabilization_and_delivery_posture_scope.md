# Memo: Close Read Post-Publication Stabilization And Delivery Posture Scope

Subtitle: Clear the residual live public-route defects, add one repeatable browser-proof harness, and freeze whether the next honest move remains bounded Critic-host stabilization rather than standalone extraction or family expansion

Date: 2026-04-14
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Immediate Prior Completion:
- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
Immediate Prior Roadmap Update:
- `communications/MEMO_2026-04-13_close_read_roadmap_update_after_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
Companion Evidence:
- `communications/NOTE_2026-04-13_close_read_public_host_topology_evidence.md`
- `communications/NOTE_2026-04-13_close_read_public_route_matrix_and_browser_diagnosis.md`
Relevant Product Boundary Context:
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`

## Purpose

Define the next honest tranche after public Close Read publication has been completed and browser-proved on the actual live Critic host pair.

This memo is not:

- a reopening of public-host topology
- a re-proof of concept authority
- a new family-admission memo
- a standalone-host extraction memo

It exists to freeze one narrower question:

- now that the public Close Read surface is real, is the right next move a bounded stabilization tranche on the live Critic host, or is there already enough evidence that delivery posture itself is the blocker?

## Bottom Line

The next bounded move should be:

1. stabilize the already-public Critic-hosted Close Read surface
2. add one repeatable repo-owned browser-proof harness for the admitted route matrix
3. use that stabilization evidence to freeze the near-term delivery posture explicitly

The default posture in this tranche should be:

- stay on the current Critic host pair
  - frontend: `the-critic-1`
  - API: `the-critic`
- fix only the residual public defects that the browser matrix still exposes
- defer standalone extraction unless the stabilization audit proves that current-host entanglement is the actual blocker

## Why This Is The Right Next Corridor

The previous tranche answered the publication question in bounded form:

- the public host pair is now documentary-stable
- the admitted-family Close Read routes are browser-hydrated on the live frontend
- the umbrella exposes the admitted set only:
  - genealogy
  - AOI thematic single-thinker
  - concept analysis:
    - `inferential`
    - `logical`

What remains open is smaller and more practical:

- one known public residual still exists:
  - the live genealogy route still emits two failed design-token requests to:
    - `http://localhost:8001/v1/styles/tokens/humanist_craft`
  - with paired `DesignTokens` fallback warnings while the page otherwise renders correctly
- the browser proof is currently documentary-stable, but still too dependent on ad hoc execution rather than one repo-owned replay harness
- the strategic question of host delivery posture should be answered from the stabilized public product surface, not from the pre-stabilization state

The exact origin of that residual is not yet frozen.

Phase 1 should be prepared to distinguish between:

- live frontend build/env drift
- a the-critic-local or vendored-renderer fallback defect
- transient analyzer-v2 availability on a direct-request path

while still keeping the implementation slice local to `the-critic` unless a later proof demonstrates a real analyzer-v2 runtime blocker.

So the next honest corridor is not:

- add more families
- widen concept modes
- extract into a standalone host by default

It is:

- make the current public product surface cleaner and more repeatable
- then decide whether there is any real remaining reason to leave the Critic host before widening product scope again

## Decisions To Freeze

### 1. Near-term host posture remains the current Critic host pair

This tranche should assume the current delivery vehicle remains:

- `the-critic-1`
- `the-critic`

It should not treat standalone extraction as the default next move.

### 2. The admitted family set remains frozen

Do not widen beyond:

- genealogy
- `anxiety_of_influence_thematic_single_thinker`
- concept analysis:
  - `inferential`
  - `logical`

### 3. Stabilization means public-surface truth, not redesign

In this tranche, stabilization means:

- browser-hydrated route correctness
- removal or explanation of residual public errors/noise
- repeatable route-matrix replay from repo-owned tooling
- documentary deployment/config truth staying aligned

It does not mean:

- shell redesign
- family-architecture rewrite
- generic downstream operation-law rewrite

### 4. Delivery-posture escalation must be evidence-driven

If the stabilization audit proves that the remaining blockers are fundamentally caused by Critic-host entanglement, record that explicitly and let that become the reason for a later extraction corridor.

Do not smuggle extraction into this tranche just because the public product now exists.

## Scope

### In scope

- reproduce the known live genealogy design-token failure and identify its actual source
- fix residual public-route defects only where they are truly part of the Close Read public surface
- add one repeatable repo-owned browser-proof harness for the six admitted public routes
- verify that documentary deployment truth remains aligned:
  - live pair
  - repo-tracked deployment/config sources such as `render.yaml` and `.env.example` where relevant
  - live bundle/runtime behavior
- freeze the near-term delivery-posture decision from that stabilized evidence

### Out of scope

- analyzer-v2 runtime changes
- analyzer-mgmt changes
- standalone-host extraction
- new family admission
- new concept submodes
- broad Close Read UI redesign
- generic destination-policy redesign

## Current Starting Point

### What is already closed

- actual public host pair identified and frozen
- admitted-family Close Read routes published and browser-proved
- stale public `Close Read V1` / `genealogy pilot` wording removed
- public concept detail and AOI detail routes no longer stuck on the previously wrong loading paths

### What remains open

- one residual live genealogy design-token/runtime seam
- no repo-owned replay harness yet frozen as the standard way to rerun the public route matrix
- no explicit post-publication delivery-posture freeze yet written as an implementation outcome

### Repo-truth caution

The tracked repo-facing env/config story is not fully normalized yet:

- `the-critic/webapp/.env` is local and gitignored, not tracked documentary truth
- `.env.example` does not currently document the analyzer-v2 URL for this seam
- `render.yaml` is documentary truth for repo readers, not proof that the live Render services are blueprint-managed

So this tranche must treat live bundle behavior plus repo-tracked config files as the governing evidence, not local `.env` files.

## Proposed Implementation Sequence

### Phase 0: Align to deployed truth

Before changing code:

- source-align `the-critic` to deployed `origin/master`
- use an aligned clean worktree or equivalent deployed-source-aligned branch; do not implement from the dirty main trees
- verify the live frontend bundle identity by public asset evidence or deploy timestamp if available
- treat route-level `200` as insufficient; browser truth remains the gate

### Phase 1: Reproduce the residual public errors on the live routes

Re-run the final six-route matrix on:

- `/p/:projectId/close-read`
- `/p/:projectId/close-read/genealogy`
- `/p/:projectId/close-read/aoi`
- `/p/:projectId/close-read/aoi/:thinkerId`
- `/p/:projectId/close-read/concepts`
- `/p/:projectId/close-read/concepts/:conceptSlug`

Classify each route by:

- hydrated and clean
- hydrated with non-blocking console/network noise
- hydrated with real public defect
- broken

Treat the genealogy residual as the primary defect until disproven, but classify its origin explicitly:

- the-critic frontend defect
- the-critic backend failure
- vendored renderer/design-token fallback defect
- transient analyzer-v2 availability seam on the direct-request path

The current observed failure mode to test directly is:

- live requests from the genealogy route to:
  - `http://localhost:8001/v1/styles/tokens/humanist_craft`

If the origin turns out to be analyzer-v2 availability, the fix should still remain the-critic-local where possible:

- graceful fallback
- retry behavior
- suppression of spurious public noise

rather than reopening analyzer-v2 runtime scope by default.

### Phase 2: Add one repo-owned browser-proof harness

Add one bounded replay artifact inside `the-critic` that can re-run the admitted public route matrix against a configurable host/specimen set.

It may be:

- a Playwright script/spec
- or another equally narrow browser automation harness

But it should:

- live in repo
- target the six admitted routes
- capture route result plus screenshot/trace evidence
- capture browser console errors and network request failures per route
- record the live bundle fingerprint used for the replay
- avoid pretending to be a generic cross-app QA framework

### Phase 3: Fix only the residual public defects that the replay harness confirms

If the genealogy design-token defect or any similarly narrow route residuals are genuinely part of the public Close Read surface:

- fix them in `the-critic`
- keep the fix local and bounded

If the defect originates in the vendored renderer/design-token path consumed by `the-critic`, fixing that vendored/package path inside `the-critic` is still in scope.

If a residual turns out to be external to the public Close Read path and not user-facing, document it rather than widening scope.

### Phase 4: Freeze the near-term delivery posture

At the end of the tranche, write down one explicit answer:

- either the live Critic-hosted surface is clean enough that the next corridor should remain on the current host
- or the remaining defects show that delivery posture itself has become the next blocker

That decision should be based on the stabilized public surface, not on architectural preference alone.

Concrete escalation triggers that would justify a later extraction corridor should be named explicitly if encountered:

- residual defects caused by shared Critic host infrastructure rather than Close Read code
- fixes that require changes to non-Close-Read Critic code paths with real regression risk
- browser-proof failures caused by shared Critic state/context contamination
- network-topology issues that would not exist on a standalone host

## Acceptance Criteria

This tranche is complete only if all of the following are true:

- the six admitted public routes can be replayed from one repo-owned browser harness
- that harness records screenshots or trace evidence plus browser console errors, network request failures, and the live bundle fingerprint
- no route in that replay renders a React/app `404`
- the admitted family set on the public umbrella remains exactly:
  - genealogy
  - AOI
  - concept analysis
- no extra concept submode leaks into the public concept family
- the stale `Close Read V1` / `genealogy pilot` public wording remains absent
- no admitted public route in the final replay makes requests to dev-only hosts such as `localhost`
- the genealogy design-token/runtime residual is either:
  - eliminated
  - or explicitly documented with evidence as external/non-blocking to the public Close Read path
- the tranche ends with one explicit near-term delivery-posture freeze

## Strategic Reading

This tranche is intentionally modest.

It does not ask:

- what is the final host for Close Read?
- what is the next new family?
- how should every current host-local seam be generalized?

It asks only:

- now that the public product surface is real, can we make it clean and repeatable enough to justify keeping the next move on the current host?

That is the smallest honest question before extraction or expansion.
