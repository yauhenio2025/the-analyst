# Exemplar inputs

Files in this folder (other than this README) are served by `GET /v1/dossier/exemplars`
and can be used to start a run with one click:

```
POST /v1/dossier/jobs {"sources": [{"kind": "exemplar", "name": "fashion_bundle.txt"}], "depth": "simple", "autopilot": true}
```

The exemplar texts are **not committed** (see `.gitignore`). Expected on a demo machine:

- `fashion_bundle.txt` — a stacks export of 5 papers on fashion, sustainability and
  neoliberalism (~355K chars). Each item starts with a header line
  `===== [n/N] Creator (Year) — Title — Publication — [Library · Key] =====`; a CONTENTS
  block lists the headers first and is skipped by `src/sources/stacks.py:split_stacks_export`.

To add one: drop a `.txt`/`.md` file here. A stacks export is auto-split into documents;
any other text is one document.
