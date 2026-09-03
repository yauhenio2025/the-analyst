/* Plates — /d/:id/plates. Each plate is one dense 4K diagram that IS the analysis: shown full width
   with the narrative the reader needs, the perspective it claims, its family/format, the vision
   check's verdict, and a download of the 4K file. A delivered job with no plates offers the desk:
   how many (1-3) and, optionally, which perspectives. Everything shown is a recorded fact. */
import { useCallback, useEffect, useState } from 'react'
import { api } from '../lib/api'
import { useJob } from '../lib/hooks'
import { duration, usd } from '../lib/format'
import { Record } from '../components/Record'
import { consolePath, dossierPath } from '../router'
import type { DossierPlate, PlatesResponse } from '../types'

const LEVEL: Record<number, string> = { 1: 'helicopter', 2: 'framework', 3: 'analytical', 4: 'evidential', 5: 'granular' }
const fam = (s: string | undefined) => (s ?? '').replace(/_/g, ' ')

function Verdict({ p }: { p: DossierPlate }) {
  const v = p.compliance
  if (p.status === 'failed') return <span className="chip chip-neg" data-verdict="failed">failed</span>
  if (p.status === 'planned') return <span className="chip chip-wait" data-verdict="planned">planned</span>
  if (!v || !v.checked) return <span className="chip chip-flat" data-verdict="unchecked">not checked</span>
  const found = v.labels_found?.length ?? 0
  if (v.ok) return <span className="chip chip-ok" data-verdict="ok">check passed · {found}/{v.n_labels ?? '?'} strings</span>
  return <span className="chip chip-neg" data-verdict="flagged">flagged · {found}/{v.n_labels ?? '?'} strings</span>
}

function PlateCard({ jobId, p, index }: { jobId: string; p: DossierPlate; index: number }) {
  const kept = p.attempts.find((a) => a.kept) ?? p.attempts[p.attempts.length - 1]
  const src = p.status === 'generated' ? api.plateImageUrl(jobId, p) : null
  const v = p.compliance
  return (
    <figure className={`plate-card${p.status !== 'generated' ? ' plate-planned' : ''}`} data-plate={p.key} data-status={p.status}>
      {src && <a href={src} target="_blank" rel="noreferrer"><img src={src} alt={p.title} loading="lazy" /></a>}
      {!src && <div className="empty-line">{p.status === 'planned' ? 'Rendering at 4K — the plate appears here when it is checked.' : `Not rendered${p.note ? ` — ${p.note}` : ''}.`}</div>}
      <figcaption>
        <div className="plate-meta">
          <span className="eyebrow eyebrow-accent">Plate {index}</span>
          <span className="chip chip-flat" title="perspective">{p.perspective || '—'}</span>
          <span className="chip chip-flat" title="family / format">{fam(p.family)} · {fam(p.visual_format)}</span>
          <span className="chip chip-flat" title="abstraction level">level {p.abstraction_level} · {LEVEL[p.abstraction_level] ?? ''}</span>
          <Verdict p={p} />
        </div>
        <div className="plate-title">{p.title}</div>
        {p.narrative && <p className="plate-narrative" data-narrative>{p.narrative}</p>}
        {p.why_this_perspective && <p className="plate-why">Why this perspective — {p.why_this_perspective}</p>}
        {v && v.checked && !v.ok && (v.issues?.length ?? 0) > 0 && <p className="plate-issues">{v.issues!.join(' · ')}</p>}
        <div className="plate-meta">
          <span className="machine">
            {p.width && p.height ? `${p.width}×${p.height}` : '4K'} · {p.aspect ?? ''} · {p.style_school ? fam(p.style_school) : 'house style'}
            {' · '}{p.attempts.length} attempt{p.attempts.length === 1 ? '' : 's'}{kept?.latency_ms ? ` · ${duration(kept.latency_ms)}` : ''}
            {' · '}{usd(p.cost_usd)} incl. checks{p.provider ? ` · ${p.provider}` : ''}
          </span>
          {src && <a className="linkish" href={src} download={`${jobId}-${p.key}.jpg`} target="_blank" rel="noreferrer" data-download-plate={p.key}>Download 4K</a>}
        </div>
      </figcaption>
    </figure>
  )
}

export function Plates({ id }: { id: string }) {
  const { job, error: jobError } = useJob(id)
  const [data, setData] = useState<PlatesResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [n, setN] = useState(2)
  const [perspectives, setPerspectives] = useState('')
  const [starting, setStarting] = useState(false)

  const load = useCallback(() => api.getPlates(id).then((d) => { setData(d); setError(null) })
    .catch((e) => setError(String((e as Error).message ?? e))), [id])
  useEffect(() => { void load() }, [load])
  useEffect(() => {
    if (!data?.running) return
    const t = window.setInterval(() => { void load() }, 3000)
    return () => window.clearInterval(t)
  }, [data?.running, load])

  const start = async () => {
    setStarting(true)
    try {
      const list = perspectives.split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 3)
      await api.startPlates(id, list.length ? undefined : n, list.length ? list : undefined)
      await load()
    } catch (e) {
      setError(String((e as Error).message ?? e))
    } finally {
      setStarting(false)
    }
  }

  const plates = data?.plates ?? []
  const generated = plates.filter((p) => p.status === 'generated')
  const cost = plates.reduce((s, p) => s + (p.cost_usd ?? 0), 0)
  const passed = generated.filter((p) => p.compliance?.ok).length
  const canMake = !!job && job.status === 'done' && !data?.running

  return (
    <section className="step plates" data-plates>
      <div className="section-head">
        <div>
          <span className="eyebrow">plates · <b>{id}</b></span>
          <h3>{job?.title ?? 'Plates'}</h3>
        </div>
        <span className="eyebrow">
          <a className="linkish" href={dossierPath(id, 'dossier')}>← the dossier</a>{' · '}
          <a className="linkish" href={consolePath(id)}>under the hood</a>
        </span>
      </div>
      <p className="plates-intro">A plate is one dense 4K diagram that <em>is</em> the analysis — a scorecard, a framework map, a flow of commitments, a register — read instead of the memo. Every string on it comes from the analysis and the tables; each plate is checked against its own manifest, and re-drawn once when the check fails.</p>

      {jobError && !job && <div className="error-box" title={jobError}>This dossier could not be loaded. {jobError}</div>}
      {error && <div className="error-box" title={error}>{error}</div>}

      {plates.length > 0 && (
        <Record tiles={[
          { num: String(plates.length), label: plates.length === 1 ? 'plate' : 'plates' },
          { num: `${passed}/${generated.length}`, label: 'passed the vision check' },
          { num: usd(cost), label: 'spent on renders and checks' },
          { num: data?.running ? 'running' : 'delivered', label: data?.running ? `plates run · ${data.run?.n ?? ''} planned` : 'the plates run' },
        ]} />
      )}

      {data?.running && (
        <div className="panel waiting-inline" data-plates-running><span className="spinner" /><div><strong>Making plates</strong><p className="hint">Planning the perspectives, rendering each at 4K, checking every string. A plate takes two to four minutes.</p></div></div>
      )}

      {canMake && (
        <div className="panel plate-form" data-make-plates>
          <label className="field"><span className="field-label">How many</span>
            <select value={n} onChange={(e) => setN(Number(e.target.value))} data-plates-n>
              <option value={1}>1 plate</option><option value={2}>2 plates</option><option value={3}>3 plates</option>
            </select>
          </label>
          <label className="field"><span className="field-label">Perspectives <span className="hint">optional · one per line · e.g. “scorecard of gains and losses”, “stakeholder power map”</span></span>
            <textarea value={perspectives} onChange={(e) => setPerspectives(e.target.value)} placeholder="Let the desk choose, or name the perspectives you want" data-plates-perspectives />
          </label>
          <button className="primary" onClick={() => { void start() }} disabled={starting} data-start-plates>
            {starting ? 'Starting…' : plates.length ? 'Make more plates' : 'Make plates'}
          </button>
        </div>
      )}
      {job && job.status !== 'done' && <div className="panel"><p className="hint">Plates are made from a delivered dossier. This one is still {job.status.replace(/_/g, ' ')}.</p></div>}

      {plates.map((p, i) => <PlateCard key={p.key} jobId={id} p={p} index={i + 1} />)}
      {data && plates.length === 0 && !data.running && <p className="hint" data-plates-empty>No plates yet for this dossier.</p>}
    </section>
  )
}
