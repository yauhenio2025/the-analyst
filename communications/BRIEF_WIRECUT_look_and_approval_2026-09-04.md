# Brief for the Wirecut (veo2) session — the look is chosen, and a film can run until approved (2026-09-04)

Owner's feedback after the first end-to-end film from a story-desk handoff (`sb_a879453ed293`, `asm_fa188e2554f5`): "it shows real footage where I would have preferred animated. In the fully automated mode the API should ask a model to choose the best look from our sixteen… we just went for the default, photorealistic. And an API parameter for a simpler condition and a more complex condition where the video runs through changes until the judge fully approves it and there are no further comments. All from within Wirecut."

## 1. The look is chosen, never defaulted
- `StoryboardRequest.style_preset` accepts `"auto"`. On `auto`, a **look desk** call chooses one of the sixteen presets from the source (or the handoff's through-line, spine, motif and audience) and records `look_why` on the board and the receipt. Standing preference from the owner, to be written into the look desk's doctrine: animated and illustrated forms (animated_friendly, poster_art, editorial_illustration, motion_graphics, paper_cutout, bw_ink, shadow_play, isometric_world, claymation, blueprint, stitched, sand_art, neon_glow, riso_print) over photorealistic footage (documentary_calm, news_urgent) unless the material is itself footage-shaped (an event with real faces the audience must see). The desk names the runner-up and why.
- When a handoff carries `look` (the story desk now recommends one: `handoff.look = {preset_key, why, alternatives[]}`), `auto` adopts it unless the look desk disagrees, in which case it records the reason (same law as spine adoption).
- The wizard's Look step shows the chosen preset with its reason and lets the operator override.

## 2. Two finish conditions, one parameter
Add `finish: "simple" | "approved"` to `/api/storyboards/{id}/produce` (and the wizard's confirm):
- `simple`: today's behaviour, one pass, whatever coherence tier is set.
- `approved`: coherence at `studio`; after assembly, run the screening; while the punch list is non-empty and `ship_ready` is false, draft the work order, realize it (re-film, re-fit, re-cut as the items say), re-assemble and screen again; stop when the judge has no further comments, or when the spend cap or `max_rounds` (default 3) is reached, and say which. The operation's events narrate each round; the film's record keeps every round's punch list and what was done about it. Reuse `screening`, `workorder`, `iterate` and `dailies` as they are; the new thing is the loop and its stopping rule.

## 3. Honour a pinned length
For a 90-second ask the write adopted 121 s (`length_pinned` was false). The story desk's driver now sends `length_pinned: true` with `target_seconds` from the handoff; please make the handoff's `spine.length_seconds` the default pinned target on the corpus road, and record any adoption away from it with a reason, as the spine does for sources.

## 4. Provider
Never Veo. Seedance 2.5 is the owner's choice for these films; make it the default `provider_override` on the corpus road unless the request says otherwise.

## 5. Test
Re-run the corpus road on `GET https://the-analyst-kcuc.onrender.com/v1/story/jobs/story-3f5149582332/handoff` with `style_preset: "auto"`, `finish: "approved"`, `length_pinned: true` (90 s), Seedance 2.5, cap $40. Report the chosen look and why, the rounds the approval loop took, the final punch list (empty), the length, the cost. The Analyst side will point the handoff page's "Open in Wirecut" at whatever create-from-URL entry you expose.
