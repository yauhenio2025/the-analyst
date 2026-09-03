# images agent (E2) — change note

Branch `feat/images`. Owner of `src/images/*`, `src/api/routes/figures.py`,
`tests/test_images_storage.py`, `tests/test_figure_prompts.py`. Verified live 2026-09-03.

## CHANGELOG entries (fold into docs/CHANGELOG.md [Unreleased])

### Added
- Provider-agnostic image generation package `src/images/` — registry of four key-gated
  providers (Gemini 3 Pro Image, Gemini 3.1 Flash Image, Seedream 5.0 Pro, Qwen-Image 2.0 Pro),
  one `generate_image()` entry point with retry/throttle/policy semantics, Gemini edit mode,
  fallback chain, and a CLI ([src/images/providers.py](../../src/images/providers.py),
  [src/images/adapter.py](../../src/images/adapter.py)).
- Figure prompt builder lifting analyzer v1's style-override sandwich + simplicity rules and
  veo2's register openers + NO-TEXT closer; four registers (editorial, diagrammatic,
  photographic, archival); optional Sonnet `declutter_scene`
  ([src/images/figure_prompts.py](../../src/images/figure_prompts.py)).
- Claude-vision compliance check `check_figure` (fail-open, key-gated)
  ([src/images/compliance.py](../../src/images/compliance.py)).
- Figure storage on disk under `FIGURES_DIR` with JSON sidecars and content-addressed ids
  ([src/images/storage.py](../../src/images/storage.py)).
- `/v1/figures` routes: providers, generate, by-job, image serving, meta
  ([src/api/routes/figures.py](../../src/api/routes/figures.py)).
- Tests (no network): `tests/test_images_storage.py` (11), `tests/test_figure_prompts.py` (20).
- Sample renders: `communications/changes/images-samples/*.jpg`.

### Changed
- `requirements.txt`: added `Pillow>=10.0` (ref downscaling, dimensions, compliance re-encode)
  and `python-dotenv>=1.0` (repo-root `.env` loaded once, never overriding real env).
- `src/api/routes/figures.py`: stub replaced by the full router (prefix and `/health` kept).

## FEATURES entries (fold into docs/FEATURES.md)

### Image Generation — Provider Fleet
- **Status**: Active
- **Description**: One call renders a figure on any of four image models; cost recorded at call
  time from the registry; unconfigured providers are absent, not disabled.
- **Entry Points**:
  - `src/images/providers.py:80-143` — `PROVIDERS` registry (model ids, cost per size, rpm, env keys, sizes, aspects, max_refs)
  - `src/images/providers.py:59-72` — `ARK_SIZES` / `DASHSCOPE_SIZES` size-per-aspect tables
  - `src/images/providers.py:171-232` — `available_providers`, `coerce_size`, `check_aspect`, `estimate_cost`, `describe_providers`
  - `src/images/adapter.py:73-90` — `ImageResult` dataclass (+ `to_meta()`)
  - `src/images/adapter.py:93-121` — `ImageProviderError`, `PolicyRejection`, `Throttled(retry_after)`, `NoImageReturned`
  - `src/images/adapter.py:182-256` — Gemini SDK transport (`generate_content` + `ImageConfig`, policy/no-image detection)
  - `src/images/adapter.py:258-296` — Gemini REST `/interactions` fallback (veo2 transport, GA model id)
  - `src/images/adapter.py:327-362` — Seedream via Ark `images/generations` (refs as ARRAY, ≤1568 px)
  - `src/images/adapter.py:365-402` — Qwen-Image via DashScope multimodal generation (65 s throttle backoff)
  - `src/images/adapter.py:427-508` — `generate_image()` (retry policy, structured logging)
  - `src/images/adapter.py:511-573` — `edit_image()` (Gemini only; others `NotImplementedError`)
  - `src/images/adapter.py:576-608` — `generate_with_fallback()`
  - `src/images/adapter.py:611-677` — CLI `python -m src.images.adapter`
- **Dependencies**: google-genai, httpx, Pillow (optional at runtime), python-dotenv (optional); env `GEMINI_API_KEY`|`GOOGLE_VEO_API_KEY`, `ARK_API_KEY`, `DASHSCOPE_API_KEY`
- **Added**: 2026-09-03

### Figure Prompts (registers, style sandwich, NO-TEXT)
- **Status**: Active
- **Description**: Turns a scene description into a full image prompt: register opener → scene → palette/caption context → composition rules → prohibitions → NO-TEXT closer (or legibility rules), optionally wrapped in analyzer's MANDATORY STYLE OVERRIDE sandwich.
- **Entry Points**:
  - `src/images/figure_prompts.py:37-102` — `REGISTERS` (editorial, diagrammatic, photographic, archival)
  - `src/images/figure_prompts.py:107-146` — `SIMPLICITY_RULES`, `FIGURE_PROHIBITIONS`, `NO_TEXT_CLOSER`, `TEXT_LEGIBILITY_RULES`
  - `src/images/figure_prompts.py:162-274` — `build_style_override` / `build_style_closing` (lifted analyzer gemini_image.py 2640-2830)
  - `src/images/figure_prompts.py:286-354` — `build_figure_prompt()`
  - `src/images/figure_prompts.py:357-362` — `ensure_no_text()` (idempotent closer)
  - `src/images/figure_prompts.py:370-436` — `DECLUTTER_PROMPT`, `declutter_scene()` (Sonnet, key-gated, fail-safe)
- **Dependencies**: anthropic (declutter only)
- **Added**: 2026-09-03

### Figure Compliance Check
- **Status**: Active
- **Description**: Claude vision verdict on a rendered figure (matches expectation? rendered text? artefacts? real persons? clutter?). Never raises; returns `ok=True` + "check skipped" without a key.
- **Entry Points**:
  - `src/images/compliance.py:28-51` — `CHECK_PROMPT`
  - `src/images/compliance.py:54-77` — `_prepare` (≤1568 px JPEG re-encode for the vision call)
  - `src/images/compliance.py:93-174` — `check_figure()` → `{ok, issues, suggestion, confidence, detected, has_text, checked, model, usage}`
- **Dependencies**: anthropic, Pillow (optional); env `ANTHROPIC_API_KEY`
- **Added**: 2026-09-03

### Figure Storage and Serving
- **Status**: Active
- **Description**: Figures persisted as `<figure_id>.png|jpg|webp` + `<figure_id>.json` sidecar under `FIGURES_DIR` (default `./data/figures`); `figure_id = {job}-{slug}-{sha256[:8]}` (idempotent per bytes). Served at `/v1/figures/{id}` with the correct media type and immutable cache headers.
- **Entry Points**:
  - `src/images/storage.py:41-46` — `figures_dir()` (env resolved at call time)
  - `src/images/storage.py:54-79` — `sniff_mime_strict`/`sniff_mime` (bytes are the authority), `image_dimensions`
  - `src/images/storage.py:94-139` — `save_figure()`
  - `src/images/storage.py:142-197` — `figure_url`, `figure_meta`, `figure_path`, `figure_mime`, `list_figures`, `delete_figure`
  - `src/api/routes/figures.py:47-65` — `GenerateFigureRequest`
  - `src/api/routes/figures.py:73-78` — `GET /v1/figures/providers`
  - `src/api/routes/figures.py:81-160` — `POST /v1/figures/generate`
  - `src/api/routes/figures.py:163-184` — `GET /by-job/{job_id}`, `GET /{figure_id}/meta`, `GET /{figure_id}`
- **Dependencies**: FastAPI; env `FIGURES_DIR`
- **Added**: 2026-09-03

## Contract as implemented

```python
from src.images.providers import PROVIDERS, available_providers, estimate_cost, describe_providers
from src.images.adapter import (ImageResult, generate_image, edit_image, generate_with_fallback,
                                ImageProviderError, PolicyRejection, Throttled)
from src.images.figure_prompts import build_figure_prompt, declutter_scene, REGISTERS
from src.images.compliance import check_figure
from src.images.storage import save_figure, figure_path, figure_meta, list_figures, figure_url

@dataclass ImageResult(image_bytes: bytes, mime_type: str, provider: str, model: str, cost_usd: float,
                       prompt_sent: str, width: int|None, height: int|None, raw: dict)
    .to_meta() -> dict   # sidecar-ready (no bytes; adds bytes/sha256)

generate_image(prompt, *, provider="gemini_pro", size="2K", aspect="16:9", refs: list[bytes]|None=None,
               style: dict|None=None, no_text=True, timeout_s=600) -> ImageResult
    # style → analyzer MANDATORY STYLE OVERRIDE sandwich; no_text → NO-TEXT closer appended (idempotent)
    # size coerced to provider support (raw["size_used"]); aspect validated (ValueError)
    # retry: 2 attempts on transient / text-instead-of-image; Throttled → sleep retry_after (≤3×);
    # PolicyRejection never retried; unconfigured provider → ImageProviderError
edit_image(source: bytes, instruction: str, *, provider="gemini_pro", size=None, aspect=None,
           no_text=True, timeout_s=600) -> ImageResult      # NotImplementedError for non-Gemini
generate_with_fallback(prompt, providers=["gemini_pro","seedream_5_pro"], **generate_kwargs) -> ImageResult
    # skips unconfigured, continues past PolicyRejection; raw["fallback_trace"]; raises ImageProviderError if all fail

build_figure_prompt(scene, *, register="editorial", palette=None, caption=None, no_text=True,
                    extra_prohibitions=None, aspect=None, style=None) -> str
declutter_scene(scene, *, model="claude-sonnet-4-6", api_key=None) -> str   # returns input unchanged without key / on error
check_figure(image_bytes, expectation, *, model="claude-sonnet-4-6", no_text=True) ->
    {ok, issues, suggestion, confidence, detected, has_text, checked, model, usage}   # never raises
save_figure(image_bytes, mime_type, *, job_id, name, meta) -> figure_id     # "{job}-{slug}-{8hex}"
figure_path(figure_id) -> Path (FileNotFoundError) ; figure_meta(figure_id) -> dict ; list_figures(job_id) -> list[dict]
figure_url(figure_id) -> "/v1/figures/{figure_id}"
```

HTTP (prefix `/v1/figures`, mounted in `src/api/main.py:287` — untouched):

| Route | Body / params | Returns |
|---|---|---|
| `GET /providers` (`?all=true` to include unconfigured) | — | `{providers:[{key,label,model,api,available,usd_per_image,usd_by_size,rpm,sizes,aspects,max_refs,supports_edit,required_env_any}], default, registers}` |
| `POST /generate` | `{prompt, provider?, size?, aspect?, job_id?, name?, register?, caption?, palette?, no_text?, check?, declutter?, fallback?: [..], style?, extra_prohibitions?, meta?}` | `{figure_id, url, cost_usd, provider, model, mime_type, width, height, latency_ms, compliance, prompt_chars}` — 400 bad provider/register/aspect, 422 policy, 429 + Retry-After throttled, 502 provider error, 503 nothing configured |
| `GET /by-job/{job_id}` | — | `{job_id, count, figures:[sidecar…]}` |
| `GET /{figure_id}` | — | image bytes, correct `Content-Type`, immutable cache |
| `GET /{figure_id}/meta` | — | sidecar JSON |
| `GET /health` | — | `{ok, component, providers}` |

Sidecar keys: `figure_id, job_id, name, mime_type, ext, bytes, sha256, width, height, created_at, url,
prompt, prompt_sent, provider, model, cost_usd, size, aspect, caption, register, scene, compliance,
latency_ms, meta{…}`.

CLI: `python -m src.images.adapter --provider gemini_pro --size 2K --aspect 16:9 --out /tmp/x.png "prompt"`
(+ `--register`, `--palette`, `--caption`, `--ref path…`, `--fallback a,b`, `--allow-text`, `--json`, `-v`).
If the provider returns a different mime than the `--out` extension, the extension is corrected and noted on stderr.

## Provider table — measured 2026-09-03 (one call each, same fashion-house lattice scene)

| key | model | size/aspect | latency | cost | output | notes |
|---|---|---|---|---|---|---|
| `gemini_pro` | `gemini-3-pro-image-preview` (SDK) | 2K 16:9 | **32.7 s** | $0.134 | 2752×1536 JPEG 2.8 MB (648 in / 1428 out tokens) | best adherence to register + NO-TEXT (only an empty speech bubble); 4K = $0.24, 1K/2K same price |
| `gemini_flash` | `gemini-3.1-flash-image-preview` (SDK) | 1K 16:9 | **11.5 s** (10.6 s via route) | $0.067 | 1376×768 JPEG 0.4–0.7 MB | clean diagrammatic register; bottom tier drew text-like marks in bubbles |
| `seedream_5_pro` | `doubao-seedream-5-0-pro-260628` | 2K 16:9 | **66.1 s** | $0.06 | 1920×1080 JPEG 385 KB (8100 output tokens) | strongest watercolor register hold, no text; slowest; 4K coerced to 2K (price tier + bench quality) |
| `qwen_image_2_pro` | `qwen-image-2.0-pro` | 1K 16:9 | **11.5 s** | $0.075 | 1664×928 PNG 2.1 MB | 2 rpm; ignored several prohibitions (boxes, gift packages, lightbulbs, crowds) — use as last fallback only |
| `check_figure` | `claude-sonnet-4-6` vision | — | 7.8 s | ~1.9K in / 0.18K out tokens | `{ok:true, has_text:false, issues:[speech bubble], suggestion:…}` | image re-encoded to ≤1568 px JPEG before upload |

Prompt built by `build_figure_prompt(register="editorial")` is ~2.8K chars; Gemini and Seedream honored it
without a declutter pass.

## Sample figures
- `communications/changes/images-samples/gemini_pro-fashion-house-lattice.jpg` (165 KB, 1600×893)
- `communications/changes/images-samples/seedream_5_pro-fashion-house-lattice.jpg` (229 KB, 1600×900)
- Registered on this machine (under `data/figures`, not committed):
  `demo-kering-001-meaning-lattice-6e6d27c7` (gemini_flash via `POST /v1/figures/generate`, check=true),
  `sample-fashion-lattice-gemini-pro-1b353d16`, `sample-fashion-lattice-seedream-5-pro-b14e7243`.

## Findings for the integrator / deployer
- **`.env` `ANTHROPIC_API_KEY` is invalid** (401 from `count_tokens`; the key exported in the interactive
  shell is a different, valid one). `check_figure` and `declutter_scene` fail open, so figures still
  generate — but compliance verdicts will read "check error: 401" until the key in `.env` / Render env is
  replaced. Gemini, Ark and DashScope keys in `.env` all work.
- `data/` is not in `.gitignore`; I committed with explicit paths. Suggest the integrator add `data/` there.
- `src/api/main.py` does not load `.env`; `src/images/providers.py` loads the repo-root `.env` once at
  import (override=False), so the routes work under `uvicorn` without `set -a; source .env`.
- Booting the API touches the tracked `src/executor/executor.db` (restored with `git checkout` before commit).
- Pydantic: a request field named `register` shadows `BaseModel.register`; the model uses `register_`
  with `alias="register"` so the JSON contract is unchanged.

## Not done / deferred
- No R2/S3 backend (env-gated local disk only; Render persistent disk works by pointing `FIGURES_DIR`).
- `edit_image` verified only by unit test + Gemini docs (no live edit call spent).
- Reference-image conditioning implemented per bench shapes (Ark array, DashScope inline, Gemini parts)
  but not live-tested with refs.
- Live Qwen test used 1K only (its only size class); Seedream 1K sizes are conservative guesses inside the
  cheap tier and were not live-tested (2K was).
