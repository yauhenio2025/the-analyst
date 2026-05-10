# Note: Close Read Public Route Matrix And Browser Diagnosis

Date: 2026-04-13
Program: Dynamic Bespoke Apps Platformization
Related Scope:
- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_scope.md`
Companion Evidence:
- `communications/NOTE_2026-04-13_close_read_public_host_topology_evidence.md`

## Purpose

Freeze the browser-truth matrix for the actual public Close Read umbrella and admitted-family routes after the live frontend fixes deployed.

## Bundle Proven Against

The final matrix below was re-run against:

- `https://the-critic-1.onrender.com`
- frontend bundle: `main.1d26cf69.js`

Screenshots were captured during the run to:

- `/tmp/close-read-umbrella.png`
- `/tmp/close-read-genealogy.png`
- `/tmp/close-read-aoi-index.png`
- `/tmp/close-read-aoi-detail.png`
- `/tmp/close-read-concepts-index.png`
- `/tmp/close-read-concept-detail.png`

## Route Matrix

| Route | Specimen | HTTP | Browser Result | Diagnosis |
| --- | --- | --- | --- | --- |
| `/p/cutover-concept-artifact-closeout-20260411-090918/close-read` | concept proof project | `200` | hydrated umbrella with exactly 3 admitted families | pass |
| `/p/morozov-on-varoufakis/close-read/genealogy` | live genealogy specimen | `200` | hydrated genealogy page with saved-result content and admitted-family nav | pass |
| `/p/morozov-benanav-001/close-read/aoi` | live AOI specimen | `200` | hydrated AOI thinker index | pass |
| `/p/morozov-benanav-001/close-read/aoi/john-oneill` | live AOI thinker specimen | `200` | hydrated AOI thematic reader with real theme content | pass |
| `/p/cutover-concept-artifact-closeout-20260411-090918/close-read/concepts` | concept proof project | `200` | hydrated concept family landing with admitted modes only | pass |
| `/p/cutover-concept-artifact-closeout-20260411-090918/close-read/concepts/innovation` | concept proof project | `200` | hydrated concept detail with inferential/logical tabs and synthesis content | pass |

## What Had To Be Fixed

The tranche did require narrow frontend changes in `the-critic`:

1. publish the public Close Read umbrella on the real frontend bundle
2. unblock Close Read detail pages that were still relying on the wrong data path
3. stop the AOI detail route from depending on the slow/brittle analyzer-v2 discovery line
4. remove stale public `Close Read V1` / `genealogy pilot` wording from the genealogy page

## Residual Notes

- The genealogy page still emitted two browser console `ERR_CONNECTION_REFUSED` messages during the final probe, but the route hydrated and rendered the saved genealogy surface correctly.
- No route in the final matrix rendered a React/app `404`.
- No extra family and no extra concept submode leaked into the public umbrella.

## Bottom Line

The real public product question from the April 13 scope is now answered:

- the current public Close Read umbrella is not merely route-reachable
- it is browser-hydrated and usable across the admitted family set on the actual live frontend host
