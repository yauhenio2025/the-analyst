# Preserve the provenance of length-shortened anchors

The held-out Hegel run exposed a missing disclosure in the frozen quotation wall: `verify_quote` cut an anchor to 200 characters before initializing `trimmed=False`. A resulting exact prefix match could therefore be reported without a shortening marker. The dossier's separate `verify_anchor` path had the same behavior and also lost an existing anchor's `trimmed` flag on re-verification.

In the revised Conditions/Ganzinger reading, raw Sol F8 has 214 characters and the frozen output retains 200, ending at “Kant’s”. The critic's 204-character V.F1 becomes final F25 at 200 characters, ending midword at “internally oppo”. Neither length cut carries a marker in that frozen output. These differ from V.F2/final F26, whose 116-character quote is shortened to 84 because PDF footer text interrupts the passage; the frozen wall already marks that substring recovery.

The main implementation now initializes shortening provenance from the original quote length in both paths, and the dossier path preserves an existing marker. The selected quote prefixes and membership decisions are unchanged. This makes the existing marker and counters disclose length cuts as well as later prefix recovery; it does not restore omitted wording or establish that a shortened passage supports the finding.

**Validation:** 182 affected tests passed across length provenance, existing anchor repairs, dossier table walls, corpus ledgers, workflow dispatch, process shape and desk handoff. Four new regressions cover primary/secondary anchor serialization and re-verification, dossier history, an exact quote at the limit, and a cut inside a word. `git diff --check` is clean. Existing deprecation warnings remain.

The [held-out protocol](STUDY_ideas_HEGEL_HELDOUT_PROTOCOL_2026-09-05.md) continues to import archived `d9cfc6e`. Its identity `43f051bdd4d89076`, prompts, receipts and outputs are preserved. Report that run's original counters separately from this subsequent implementation fix. No additional model calls were made for the fix.
