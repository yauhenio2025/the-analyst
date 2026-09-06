---
name: owner-working-rules
description: How the owner wants sessions run in the-analyst — LLM-first, walls check arithmetic never meaning, commit and push per phase, ask before real spend, update tracker and memory
metadata:
  type: feedback
---

The owner's standing rules for this project: judgment goes to the model, plumbing to code ("walls check arithmetic — anchors verbatim, ids exist — never meaning"); commit and push after each phase (master auto-deploys to Render); update `communications/IMPLEMENTATION_TRACKER.md` and memory; ask before launching API spend of tens of dollars; never Veo (Seedance 2.5 for films). Design work should start from the ideal output and assume the current design may be faulty. For one-off judgments of weight (triage, redesign decisions) the owner wants the strongest model (Codex on gpt-6-astra xhigh, invoked with `codex exec --yolo -m gpt-6-astra -c model_reasoning_effort=xhigh "<prompt>"`), not the value model; Sol is for volume reading. When killing processes by pattern, use the bracket trick (`pkill -f "gpt-6-astr[a]"`) so the shell's own command line does not match.

**Why:** stated in the 2026-09-04 next-session prompt and the study brief; the study's own plumbing bugs came from code that judged (composability tails) and prose hand-offs that lost the contract.
**How to apply:** when adding a check, ask whether it verifies shape or meaning; if meaning, give it to a model. Build everything reversible before stopping for a spend decision. Related: [[engine-redesign-process-shape]].

Spend during the catalogue consolidation (2026-09-06): the owner said "don't worry about the caps - just get this done" when asked about the second-queue cap. Caps in Codex briefs are guidance, not gates, for this arc; keep reporting actual cost. The general ask-before-spend rule still applies to new arcs.
