/* Step 3 · The draft — while it writes, the waiting screen narrated live by
   the event ledger; once delivered, a master-detail of sections, tables and
   figures. */
import { useEffect, useMemo, useState } from 'react'
import { buildRail } from '../lib/run'
import { statusLabel, usd, duration } from '../lib/format'
import { CostMeter, RunRail } from '../components/RunRail'
import { Md } from '../components/Md'
import { TableView } from '../components/TableView'
import { FigureView } from '../components/FigureView'
import { FindingsView, SpineView } from '../components/SpineView'
import { consolePath, dossierPath, navigate } from '../router'
import type { DossierJob, RunEvent } from '../types'
import { statusRank } from '../types'

type Item = { id: string; kind: 'section' | 'table' | 'figure' | 'analysis' | 'spine' | 'findings'; label: string; sub?: string }

export function DraftStep({ job, events, item, onNext }: {
  job: DossierJob; events: RunEvent[]; item: string | null; onNext: () => void
}) {
  const rail = useMemo(() => buildRail(job, events), [job, events])
  const running = job.status !== 'done' && job.status !== 'failed'
  const items: Item[] = useMemo(() => [
    ...job.sections.map((s, i): Item => ({ id: `s:${s.key}`, kind: 'section', label: s.title, sub: `section ${i + 1}` })),
    ...job.tables.map((t, i): Item => ({ id: `t:${t.key}`, kind: 'table', label: t.caption, sub: `table ${i + 1} · ${t.rows.length} rows` })),
    ...job.figures.map((f, i): Item => ({ id: `f:${f.key}`, kind: 'figure', label: f.title || f.caption, sub: `figure ${i + 1} · ${f.provider ?? 'image'}${f.checked_ok === true ? ' · checked' : f.checked_ok === false ? ' · flagged' : ''}` })),
    ...(job.spine ? [{ id: 'spine', kind: 'spine' as const, label: 'The spine', sub: `${job.spine.sections.length} claims · ${job.spine.sections.filter((x) => x.table).length} tables · ${job.spine.sections.filter((x) => x.figure).length} diagrams` }] : []),
    ...((job.findings.length || job.crosscheck) ? [{ id: 'findings', kind: 'findings' as const, label: 'Cross-check findings',
        sub: job.crosscheck?.hangs_together ? 'hangs together' : `${job.findings.filter((f) => f.status === 'open').length} open · ${job.findings.filter((f) => f.status !== 'open').length} resolved` }] : []),
    ...Object.keys(job.analysis).map((k): Item => ({ id: `a:${k}`, kind: 'analysis', label: k, sub: 'analysis phase' })),
  ], [job])
  const [selected, setSelected] = useState<string | null>(item)
  useEffect(() => { if (item) setSelected(item) }, [item])
  const current = items.find((i) => i.id === selected) ?? items[0] ?? null
  const docTitles = Object.fromEntries(job.profiles.map((p) => [p.doc_key, p.title]))

  const pick = (id: string) => {
    setSelected(id)
    navigate(dossierPath(job.id, 'draft', `?item=${encodeURIComponent(id)}`), { replace: true })
  }

  if (running || (job.status === 'failed' && items.length === 0)) {
    const activeStep = rail.steps[rail.activeIndex]
    return (
      <section className="step draft-step">
        <div className="section-head">
          <h3>The draft</h3>
          <span className="eyebrow">{statusLabel(job.status)}</span>
        </div>
        <div className="waiting" data-draft-waiting>
          <div className="waiting-head">
            {job.status !== 'failed' && <span className="spinner big" />}
            <div>
              <h2 className="display">{job.status === 'failed' ? 'Stopped.' : 'Writing your draft.'}</h2>
              <p className="narration-line lead" aria-live="polite" data-live-narration>
                {rail.narration ?? activeStep?.detail ?? 'Starting.'}
              </p>
              <p className="hint">
                {job.status === 'failed' ? (job.error ?? 'The run stopped; everything before it was recorded and kept.')
                  : 'You can leave — it keeps working, and the draft will be waiting in the library.'}
              </p>
            </div>
          </div>
          <div className="waiting-grid">
            <RunRail job={job} events={events} model={rail} />
            <aside className="waiting-aside">
              <span className="eyebrow">on the meter</span>
              <CostMeter rail={rail} live={running} />
              {job.chosen_option && job.brief && (
                <p className="machine">telling · {job.brief.options.find((o) => o.key === job.chosen_option)?.title ?? job.chosen_option}</p>
              )}
              {job.plan_id && <p className="machine">plan · {job.plan_id}</p>}
              <a className="linkish" href={consolePath(job.id)} data-open-console>Open the console →</a>
            </aside>
          </div>
          {items.length > 0 && (
            <div className="panel">
              <span className="eyebrow">already on the desk</span>
              <ul className="index">
                {items.map((i) => <li key={i.id}><button className="linkish" onClick={() => pick(i.id)}>{i.label}</button> <span className="machine">{i.sub}</span></li>)}
              </ul>
            </div>
          )}
        </div>
      </section>
    )
  }

  return (
    <section className="step draft-step">
      <div className="section-head">
        <h3>The draft</h3>
        <span className="eyebrow">{job.sections.length} sections · {job.tables.length} tables · {job.figures.length} figures · {usd(job.totals.cost_usd)} · {duration(job.totals.duration_ms)}</span>
      </div>
      <p className="lede">Everything the desk wrote, one item at a time. Numbers in the tables carry the sentence they were taken from — hover to read it, click to keep it open.</p>
      <div className="master-detail">
        <nav className="index-rail" aria-label="Draft contents" data-draft-index>
          {(['section', 'table', 'figure', 'analysis'] as const).map((kind) => {
            const rows = kind === 'analysis' ? items.filter((i) => i.kind === 'spine' || i.kind === 'findings' || i.kind === 'analysis') : items.filter((i) => i.kind === kind)
            if (!rows.length) return null
            return (
              <div key={kind} className="index-group">
                <span className="eyebrow">{kind === 'analysis' ? 'the analysis behind it' : `${kind}s`}</span>
                {rows.map((i) => (
                  <button key={i.id} className={`index-row${current?.id === i.id ? ' on' : ''}`} onClick={() => pick(i.id)} data-index-item={i.id}>
                    <span className="index-label">{i.label}</span>
                    <span className="machine">{i.sub}</span>
                  </button>
                ))}
              </div>
            )
          })}
          <a className="linkish index-console" href={consolePath(job.id)} data-open-console>Open the console →</a>
        </nav>
        <div className="detail" data-draft-detail>
          {current?.kind === 'section' && (() => {
            const s = job.sections.find((x) => `s:${x.key}` === current.id)!
            const n = job.sections.indexOf(s) + 1
            return (
              <article className="section-view">
                <span className="eyebrow eyebrow-accent">section {n}</span>
                <h2 className="display">{s.title}</h2>
                <Md md={s.md} html={s.html} className="article" />
              </article>
            )
          })()}
          {current?.kind === 'table' && <TableView table={job.tables.find((x) => `t:${x.key}` === current.id)!} docTitles={docTitles} />}
          {current?.kind === 'figure' && (() => {
            const f = job.figures.find((x) => `f:${x.key}` === current.id)!
            return <FigureView figure={f} index={job.figures.indexOf(f) + 1} />
          })()}
          {current?.kind === 'spine' && job.spine && <SpineView spine={job.spine} />}
          {current?.kind === 'findings' && <FindingsView findings={job.findings} verdict={job.crosscheck} />}
          {current?.kind === 'analysis' && (
            <article className="section-view">
              <span className="eyebrow eyebrow-accent">analysis phase</span>
              <h2 className="display">{current.label}</h2>
              <Md md={job.analysis[current.label]} className="article machine-prose" />
            </article>
          )}
          {!current && <p className="hint">Nothing on the desk yet.</p>}
        </div>
      </div>
      <div className="actions dock">
        <button className="secondary" onClick={() => navigate(dossierPath(job.id, 'brief'))}>← The brief</button>
        <button className="primary" disabled={statusRank(job.status) < statusRank('done')} onClick={onNext} data-next>Next: your dossier →</button>
      </div>
    </section>
  )
}
