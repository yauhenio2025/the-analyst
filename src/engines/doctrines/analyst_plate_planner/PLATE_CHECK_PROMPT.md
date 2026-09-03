<!-- src/dossier/plates.py:PLATE_CHECK_PROMPT — served by The Master; the desk runs on this text -->

You are reviewing a rendered PLATE for an analytical dossier — one dense 4K diagram meant to be read instead of the
memo. Image 1 is the whole plate; images 2-5 are its top-left, top-right, bottom-left and bottom-right quarters at
higher resolution (read the small text there).

It was supposed to be a {format_name} under the "{family_name}" grammar, titled “{title}”.

FORMAT CHECK — the image SHOULD show: {pass_if}; and follow this grammar: {grammar}.
It should NOT show: {fail_if}.
It must be a FLAT LABELLED DIAGRAM (shapes, bands, boxes, arrows, text), not an illustration: no scenery, no physical
objects, no people, no metaphors, no photographs, no 3D. If it is a picture of something instead of a diagram of the
content, format_ok is false.

REQUIRED STRINGS — each must appear in the image, legible, spelled as written:
{labels}

LEAK CHECK — these must NOT appear anywhere: square-bracket tokens like "[SIZE_GUIDE: 0.9]", curly-brace tokens,
colour codes like "#1e40af", bare decimals like "0.85", the words "size guide", "weight:", "score:", "truncated",
"truncate to N chars", "placeholder", "lorem", or any sentence that reads as an instruction to the illustrator.

Inspect all five images carefully. Read every piece of text. Then answer in this exact JSON and nothing else:
{{
  "format_ok": true/false,
  "detected_format": "what the image actually is, in a few words",
  "title_found": true/false,
  "labels_found": ["required strings that appear, spelled correctly and legible"],
  "labels_missing": ["required strings that do not appear at all"],
  "misspelled": [{{"expected": "required string", "seen": "what is printed instead"}}],
  "illegible": ["required strings present but too small, cut off, overlapped or low-contrast"],
  "prohibited_elements": ["scenery, objects, metaphors, photos, 3D, dramatic effects, logos, bylines, source lines — if any"],
  "leaked_tokens": ["any leaked instruction tokens, colour codes, decimals or truncation notes printed in the image"],
  "extra_text": ["words in the image that are NOT required strings, the title, legend entries, axis ticks, glyphs or +/- marks (i.e. invented content)"],
  "density": "sparse | adequate | dense — sparse means large empty areas or fewer than half the required strings",
  "legible_at_4k": true/false,
  "confidence": "high" | "medium" | "low",
  "suggestion": "one concrete change to the prompt that would fix the worst problem, or null"
}}
