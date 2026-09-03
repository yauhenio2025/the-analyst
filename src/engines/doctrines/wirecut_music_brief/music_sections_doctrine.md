# Composing against the finished cut — timed sections

This time you can SEE the film. The context carries a contact sheet (several
real frames per clip, in clip order), the measured timeline (each clip's
actual start time in the stitched video), and the on-screen text moments.
Compose for THIS footage, not for the storyboard's intentions.

## Sections

Alongside the brief, declare the composition's **sections**: contiguous clip
ranges, in order, covering every clip exactly once. Each section is one
musical idea; the turn between two sections lands, mechanically, at the
measured start of the later section's first clip. Craft rules:

- **Put turns where the film turns.** A register change (HOOK → CONTEXTUALIZE,
  the pivot into PROBLEMATIZE, the landing on CONCLUDE), a location change
  visible in the frames, a held dissolve — these earn a section turn. A cut
  that merely continues the same idea does not. Two to five sections is the
  usual shape for a one-minute film; never one section per clip.
- **The acts are a contract.** When the task text lists THE FILM'S ACTS,
  a section MUST start at every act-opening clip — the score turns with the
  acts, audibly: consecutive sections across an act boundary should differ
  the way the acts differ (a rise resolving, a counter-wave hardening, a
  vindication opening up). Inside an act, sub-sections remain your free
  choice. Where a boundary declares `resolve_quiet`, the outgoing section
  should be able to RESOLVE (land on something that can end quietly) —
  the renderer ducks the bed to near-silence across that seam and the new
  section enters after the breath.
- **Name the change.** Consecutive sections must differ audibly — energy,
  density, instrumentation. If you cannot say what changes at the turn, merge
  the sections.
- **positive_styles** (3–6 short phrases): concrete musical vocabulary for
  the section — instrumentation, energy, feel ("sparse questioning solo
  piano", "quiet steady momentum", "sustained high string harmonics").
  Restate the palette that must persist across sections in every section —
  sections are generated as one piece, but say what carries through.
- **negative_styles** (0–4 phrases): what this section must avoid
  ("big drums", "resolution before the end"). Instrumental enforcement is
  already handled — spend these on craft, not on "no vocals".
- The first section opens the film (a title card, when used, rides its
  intro); the last section must land an ending, not stop mid-phrase.
- Respect what the narrator needs: mid-range melodic content that survives
  ducking, in every section (the brief's craft rules apply per section).
- **A section may be sparser, never absent.** This is a BED under
  continuous narration: never style a section toward silence ("near
  silence", "silence", long dropouts, a lone barely-audible drone) — a
  viewer hears that as the music breaking, not as drama (live case
  2026-08-30: a 'near silence' section left a third of the film
  scoreless). Compose the whole piece's dynamics inside a window of
  roughly 5 LU; the quietest section still carries audible musical
  content. TRUE silence at an act break belongs to the renderer's
  `resolve_quiet` dip, which you declare on the boundary — not to the
  composition. (The renderer also measures each section and LIFTS any
  that collapses more than 5 LU under the loudest — extreme authored
  quiet will not survive as composed.)

## Using the picture evidence

- Read the frames before deciding ambience keep/drop: you can now see whether
  a clip's world plausibly carries diegetic sound worth keeping (machinery,
  a market, weather) or whether its ambience will fight the score. Cite what
  you SEE in each rationale.
- Where an on-screen text moment lands (a STAT, a chip), prefer music that
  leaves it air — do not schedule a swell on top of a number the viewer must
  read.
- The measured starts are exact for section timing; treat them as the truth
  of the cut.

The `brief` remains required and must describe the same piece the sections
spell out — it is the plan's human-readable summary (and the fallback
transport).
