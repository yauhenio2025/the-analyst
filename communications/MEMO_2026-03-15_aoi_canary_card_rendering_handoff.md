# AOI Canary Card Rendering — Handoff Memo

> Date: 2026-03-15
> Session: debugging live AOI canary visual/interaction quality
> Status: **functional fixes done, visual design quality still poor**

## What Was Accomplished

### Bug 1: False expansion affordance on By Sin Type cards — FIXED
- Cards showed "click to expand" with pointer cursor, but expansion revealed nothing (0px height change)
- **Fix**: `expandable: false` in `src/views/definitions/aoi_by_sin_type.json`
- Deployed via clean export to analyzer-v2 backend (commit `a3fc3ee`)
- Fixture patched in aoi-canary

### Bug 2: Raw field dumping in DefaultCardCell — FIXED (functionally)
- The `DefaultCardCell` in `renderers-ui/src/cells/index.ts` was dumping ALL item fields as raw text
- Fields like `sin_type`, `sin_type_label`, `source_document_id`, `target_quote`, `source_quote`, `implication_for_argument` were rendered as raw `key: value` tags
- **Root cause**: The cell renderer checked `config.card_title_field` / `config.card_body_field` but the view definitions use `config.title_field` / `config.description_field` — keys didn't match
- **Fix**: Added explicit field mapping path that reads `title_field`, `subtitle_field`, `description_field`, `badge_field` from renderer_config and renders ONLY those fields
- When explicit mappings exist, unmapped fields are suppressed entirely
- Falls back to original auto-classification when no mappings exist

### Bug 3: No CSS for new card elements — FIXED (minimally)
- Added CSS for `.card-cell-subtitle`, `.card-cell-body` (4-line clamp), `.card-cell-badge` (severity-colored pills)
- Severity variants: `--critical`, `--high`, `--medium`/`--moderate`, `--low`/`--minor`

### Complication: ui-feedback agent reverted the JS fix
- The ui-feedback agent was spawned to improve visual design
- It modified CSS but **reverted `cells/index.ts` back to the original** version without the explicit field mapping
- This was caught and restored in v0.6.2

## Current State of Deployed Site

Live at https://aoi-canary.onrender.com — renderer v0.6.2.

**What's working:**
- No raw field dumps (sin_type, implication_for_argument etc. are gone)
- Description truncated to 4 lines
- Subtitle (theme_name) shown below title with separator
- Severity badges color-coded (CRITICAL dark red, HIGH light red)
- Source Documents cards: no expansion affordance
- By Sin Type cards: no expansion affordance
- Live and artifact modes match

**What's still wrong — visual design quality:**
- Cards look like "styled HTML" not professionally designed components
- The type indicator "Selective Citation" is redundant with the group header
- Card boundaries within groups are weak
- Badge placement and sizing is poor
- Overall the cards lack visual polish — they're functional but ugly
- The subtitle separator line is flimsy
- No clear visual distinction between card elements

## Key Files

### analyzer-v2 (backend + shared renderers)
- `src/views/definitions/aoi_by_sin_type.json` — view config with `expandable: false`
- `renderers-ui/src/cells/index.ts` — **DefaultCardCell** with explicit field mapping (the critical fix)
- `renderers-ui/src/styles/renderers.css` — card cell CSS (subtitle, badge, body clamp)
- `renderers-ui/src/renderers/CardGridRenderer.tsx` — card grid layout, grouping, card wrapper
- `renderers-ui/package.json` — currently v0.6.2

### aoi-canary (thin consumer)
- `vendor/the-syllabus-analysis-renderers-0.6.2.tgz` — vendored renderer package
- `src/fixtures/neurath-page.json` — artifact fixture (already has `expandable: false`)

## Deploy Workflow

When changing renderers-ui:
```bash
cd /home/evgeny/projects/analyzer-v2/renderers-ui
# 1. Bump version in package.json
# 2. Build and pack
npm run build && npm pack
# 3. Copy to canary
cp the-syllabus-analysis-renderers-X.Y.Z.tgz /home/evgeny/projects/aoi-canary/vendor/
# 4. Update canary package.json to reference new tarball
# 5. CRITICAL: rm -rf node_modules/@the-syllabus (npm caches same-version tarballs!)
cd /home/evgeny/projects/aoi-canary
rm -rf node_modules/@the-syllabus
npm install && npm run build
# 6. VERIFY before pushing:
grep -c 'card-cell-subtitle' dist/assets/*.js   # must be >= 1
grep -c 'card-cell-subtitle' dist/assets/*.css   # must be >= 1
# 7. Push
git add -A && git commit && git push origin main
# 8. VERIFY after deploy:
curl -s https://aoi-canary.onrender.com/ | grep -o 'assets/index-[^"]*\.js'
# then curl that JS file and verify card-cell-subtitle is present
```

## Critical Gotcha: npm Tarball Caching

If you rebuild the renderer at the SAME version number, `npm install` will use its cached copy and NOT re-extract the tarball. You MUST bump the version number on every change. This wasted significant debugging time in this session.

## What Needs to Happen Next

The functional layer is correct. The visual design needs a proper pass:

1. **Card visual structure** — proper shadows, borders, padding, spacing between cards in a group
2. **Hide redundant type indicator** — when cards are in a typed group (e.g. "Selective Citation" group), the per-card type label is redundant
3. **Badge design** — severity badges need to be more prominent and better placed; non-severity badges (like thinker names in Source Documents) should be subtle
4. **Typography hierarchy** — title, subtitle, body need clear visual differentiation
5. **Card separation** — cards within a group run together; need clear boundaries

The design work should happen in `renderers-ui/src/styles/renderers.css` and potentially `renderers-ui/src/cells/index.ts`. The CardGridRenderer component (`renderers-ui/src/renderers/CardGridRenderer.tsx`) controls card wrapper structure, type indicators, group headers.

**Do NOT use an automated agent for this** — the ui-feedback agent reverted the critical JS fix last time. Manual CSS iteration with Playwright verification is safer.
