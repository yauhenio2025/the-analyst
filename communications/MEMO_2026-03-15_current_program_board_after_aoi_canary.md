# Memo: Current Program Board After AOI Canary

Date: 2026-03-15

## Purpose

This memo is the short operating-board version of the current AOI / canary / styling state.

It is meant to answer:

- what the March 13 program was trying to prove
- what is actually done
- what is blocked right now
- what decision should be made next
- what evidence would make the current tranche trustworthy

## March 13 Thesis, Restated

The March 13 direction was:

- analyzer-v2 should own semantics and presentation intent upstream
- downstream apps should stay thin
- the architecture should generalize beyond one legacy app surface or one semantic shape

AOI plus the canary is the first serious test of that thesis outside genealogy.

## Working Definition: “Bounded Proof”

In this program, a **bounded proof** means:

- one explicitly scoped workflow/page/consumer slice
- with semantic output, rendering, and operator inspection all lining up
- without the downstream app repairing domain meaning locally
- and without claiming that the same result already generalizes everywhere else

So “bounded proof” here does **not** mean universal proof.

It means:

- one slice is real enough to trust and study

## Done

### 1. AOI is now a real non-genealogy semantic surface

Analyzer-v2 is no longer only proven on genealogy-shaped semantics.

The AOI tranche established:

- a single-thinker thematic AOI workflow
- source-corpus vs subject-corpus separation
- explicit source-document provenance
- theme-led navigation
- sin-type regrouping
- structured AOI report synthesis

The pinned Benanav vs Otto Neurath artifacts are the strongest bounded semantic proof of this tranche.

### 2. A separate thin consumer now exists

The AOI canary is a genuine second app:

- separate repo
- separate deployment
- no imports from the-critic
- no imports from analyzer-mgmt
- minimal local shell over shared renderers

This is the first bounded app-agnosticism proof:

- analyzer-v2 can drive a second app
- that app does not need to become a semantic co-author

### 3. Styling activation moved upstream

The canary showed that the next bottleneck was not AOI semantics but upstream presentation activation.

The first activation pass is now in place:

- AOI delivery styling moved onto analyzer-v2 ordinary page delivery for the canary slice
- `page` became the delivery payload
- `manifest` and `trace` remained semantic truth
- AOI `By Theme` and `By Sin Type` were shaped more explicitly for shared renderers

### 4. Fake card-grid interactions were fixed and generalized into a guardrail

We hit the same bug twice on the AOI app:

- `Source Documents` looked expandable when it was not
- `By Sin Type` looked expandable when it was not

Those were analyzer-v2 view-definition problems, not canary problems.

They were fixed individually, then generalized into a repo-wide hardening pass:

- raw-registry `card_grid` audit
- explicit `expandable` declarations required on active registered `card_grid` views
- warn-only startup logging
- pytest gate as the real enforcement path

### 5. AOI card rendering is functionally corrected

The live canary card surfaces are functionally better than they were:

- no fake expansion on `Source Documents`
- no fake expansion on `By Sin Type`
- no raw field dumping from the default card cell when explicit field mappings exist
- subtitle, truncation, and severity badge rendering now work on the AOI cards

## Status

**Status: bounded proof established, but deployment reliability is still a near-term blocker.**

That is the right status call because two things are true at once:

- the March 13 architecture now has a real bounded foundation
- some of the strongest “done” claims still depend on whether the live canary is actually serving the renderer bundle we think it is serving

So the semantic and architectural result is real.

But the deployed thin-consumer proof is still more operationally fragile than it should be.

## Current Tranche Blockers

### 1. Renderer-package / deploy reliability

This is now a first-class blocker, not a side issue.

The AOI handoff work showed that the current delivery path can obscure reality:

- a shared-renderer change can be accidentally reverted by a parallel agent pass
- vendored tarballs in `aoi-canary` can silently stay stale if the version is not bumped
- npm can reuse same-version tarballs and make a local install look “updated” when it is not
- a deployment can appear refreshed while actually serving the old bundle

Until that is tightened, some “done” claims are only conditionally true:

- true in code
- maybe true in the live deployment

That is not good enough for a trustworthy proof surface.

### 2. AOI visual quality is still behind AOI functional correctness

The canary is now functionally much better.

It is still visually rough.

The main remaining roughness is upstream:

- analyzer-v2 composition
- shared renderer presentation

not:

- missing AOI-specific canary logic

That distinction remains an important architectural guardrail.

## Next-Wave Risks

### 1. Capability onboarding discipline is still weak

AOI exposed a broader platform problem:

- new analytical capabilities can enter the system before affinities, activation, runtime truth, composition, and proof artifacts are fully wired

So the platform still lacks a durable presentation-readiness discipline.

This is not blocking closure of the current tranche in the same way as renderer delivery reliability.

It is a structural risk for the next capability tranche unless it gets a more explicit checklist and review path.

### 2. The March 13 generalization claim is still proven only once

AOI plus the canary is meaningful.

It is still only one bounded proof.

That means the broader generalization claim remains partially open.

## Current Focus

The current focus is not “invent more AOI semantics.”

It is:

### A. Keep the AOI proof surface honest

Continue catching cases where analyzer-v2 view config silently creates misleading UI behavior in thin consumers.

The `card_grid` audit is the first systematic version of that.

### B. Improve upstream presentation without cheating in the canary

If AOI still looks rough, the default assumption should be:

- analyzer-v2 composition problem
- shared-renderer presentation problem

not:

- smuggle AOI-specific repair logic into the canary

### C. Make the live canary trustworthy as a deployed artifact

The current proof surface must become trustworthy not only in code but in deployment.

That means:

- renderer version discipline
- vendored tarball discipline
- live-bundle verification
- tighter file-boundary control during parallel agent work

## Next Decision

The next decision should be explicit:

### Decision to make now

**Do we spend the next tranche on renderer delivery hardening before further semantic expansion?**

My recommendation is:

- yes

Reason:

- the operational reliability problem is now strong enough to distort the live proof surface
- expanding semantics before fixing that will make future results harder to trust, not easier

### Secondary decision after that

Once delivery reliability is tightened, choose the next bounded generalization test:

- a second thin consumer
- or a second non-genealogy surface

One plausible example is the-critic, because it already exists and would stress different rendering assumptions than the AOI canary.

## Exit Criteria

The current tranche should be treated as trustworthy when all of the following are true:

### 1. Live bundle trust

- every shared-renderer change bumps the package version
- the vendored canary tarball version matches the intended renderer package version
- build-time verification confirms the expected renderer code is present in the local canary bundle
- post-deploy verification confirms the expected renderer code is present in the live bundle

Verification signal:

- produced by the canary build/deploy workflow
- using explicit bundle-content checks before push and after deploy
- recorded in the deploy handoff or release note for the tranche

### 2. Live / artifact parity trust

- artifact mode and live mode render the same intended AOI behavior on the current pinned slice
- no fake card expansion affordances remain on the AOI card-grid surfaces
- no raw field dumping reappears in the live canary

### 3. Architectural boundary trust

- the canary remains thin
- AOI roughness is still fixed upstream, not by local semantic repair logic in the app

### 4. Governance trust

- the next capability-facing checklist includes explicit presentation-readiness items
- at minimum: style declaration, activation decision, runtime truth visibility, and one frozen styled proof artifact

## Status Call

The right current description is:

- the March 13 vision is no longer just a thesis
- it now has one real bounded non-genealogy semantic proof
- one real bounded thin-consumer proof
- one early styling-activation proof
- one first platform hardening pass against misleading renderer defaults

The honest caveat is:

- the live proof surface is still more operationally brittle than it should be

So the immediate job is not to retreat from the March 13 direction.

It is to make the current bounded proof:

- visually stronger
- operationally trustworthy
- and easier to extend without breaking the semantic-ownership boundary
