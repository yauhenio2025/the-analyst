/* Station 2 · Reading — one card per source: its question, its stance, its
   gaps, the elements it yielded by kind (each anchored to a verbatim quote,
   each marked with the passes it answers) and what the wall dropped. */
import { useEffect, useState } from 'react'
import { countByKind, docMeta, docTitle, storyStatusLabel, type StoryRailModel } from '../lib/story'
import { storyPath } from '../router'
import { ELEMENT_KINDS, type RunEvent, type StoryElement, type StoryJob, type StoryProfile } from '../types'

export function Dots({ n }: { n: number }) {
  return (
    <span className="dots" title={`intensity ${n} of 5`} aria-label={`intensity ${n} of 5`} data-intensity={n}>
      {[1, 2, 3, 4, 5].map((i) => <span key={i} className={`dot${i <= n ? ' on' : ''}`} />)}
    </span>
  )
}

export function ElementRow({ el, hl, showDoc, domId }: { el: StoryElement; hl?: boolean; showDoc?: boolean; domId?: string }) {
  const detail = Object.entries(el.detail ?? {}).filter(([, v]) => v)
  return (
    <div className={`element${hl ? ' hl' : ''}`} id={domId} data-element={el.id} data-kind={el.kind}>
      <span className="element-id">{el.id}</span>
      <div className="element-body">
        <p className="element-text">{el.text}</p>
        <div className="element-meta">
          <Dots n={el.intensity} />
          <span className="kind-chip">{el.kind}</span>
          {el.consumers.map((c) => (
            <span key={c} className="consumer" title={`answers a demand of ${c}`}>{c.replace(/^wirecut_/, '').replace(/_/g, ' ')}</span>
          ))}
        </div>
        {detail.length > 0 && <p className="machine element-detail">{detail.map(([k, v]) => `${k}: ${v}`).join(' · ')}</p>}
        {el.anchor?.quote && (
          <blockquote className="claim-quote">“{el.anchor.quote}”{showDoc && el.anchor.doc_key ? <span className="machine"> — {el.anchor.doc_key}</span> : null}</blockquote>
        )}
      </div>
    </div>
  )
}

function ProfileCard({ job, p, hlElement }: { job: StoryJob; p: StoryProfile; hlElement: string | null }) {
  const kinds = countByKind(p.elements)
  const mine = !!hlElement && p.elements.some((e) => e.id === hlElement)
  const [open, setOpen] = useState(mine)
  useEffect(() => { if (mine) setOpen(true) }, [mine])
  const known = ELEMENT_KINDS.filter((k) => p.elements.some((e) => e.kind === k)) as string[]
  const other = [...new Set(p.elements.map((e) => e.kind))].filter((k) => !known.includes(k))
  return (
    <article className="panel profile story-profile" data-profile={p.doc_key}>
      <span className="eyebrow eyebrow-accent">{p.doc_key}{p.genre ? ` · ${p.genre}` : ''} · {p.elements.length} elements · wall dropped {p.elements_dropped}</span>
      <h4 className="profile-title">{p.title || docTitle(job, p.doc_key)}</h4>
      <p className="machine">{docMeta(job, p.doc_key)}</p>
      {p.one_line && <p className="hint">{p.one_line}</p>}
      <p className="profile-thesis" data-question>{p.question}</p>
      <p className="strip" data-stance><span className="strip-label">stance</span> {p.stance || '—'}</p>
      <p className="strip notfor" data-gaps><span className="strip-label">gaps</span> {p.gaps.length ? p.gaps.join(' · ') : 'none declared'}</p>
      <div className="kind-chips" data-kinds>
        {kinds.map((k) => <span key={k.kind} className="kind-chip" data-kind={k.kind}><b>{k.n}</b>{k.kind}</span>)}
        <span className="kind-chip dropped" title="elements the wall dropped: no verbatim anchor, or a duplicate"><b>{p.elements_dropped}</b>wall dropped</span>
      </div>
      <details className="more" open={open} onToggle={(e) => setOpen((e.target as HTMLDetailsElement).open)} data-elements>
        <summary>the elements · {p.elements.length}</summary>
        {[...known, ...other].map((kind) => {
          const els = p.elements.filter((e) => e.kind === kind)
          return (
            <div key={kind} className="elements-group" data-group={kind}>
              <span className="block-label">{kind} · {els.length}</span>
              {els.map((el) => <ElementRow key={el.id} el={el} hl={el.id === hlElement} domId={`el-${el.id}`} />)}
            </div>
          )
        })}
      </details>
    </article>
  )
}

/* While the desk reads, the ledger says which source it is on and what each
   one yielded: "reading <key>: …" notes and "<key>: N anchored elements" artifacts. */
function ReadingProgress({ job, events }: { job: StoryJob; events: RunEvent[] }) {
  const now = new Set<string>()
  const yielded = new Map<string, string>()
  for (const e of events) {
    if (e.phase !== 'reconnaissance' || !e.detail) continue
    const note = /^reading (\S+):/.exec(e.detail)
    if (note) now.add(note[1])
    const art = /^(\S+): (\d+ anchored elements.*)$/.exec(e.detail)
    if (art) { yielded.set(art[1], art[2]); now.delete(art[1]) }
  }
  return (
    <div className="sheet" data-reading-progress>
      {job.documents.map((d) => (
        <div key={d.key} className="slate-row static">
          <div className="slate-main">
            <span className="title">{d.title}</span>
            <span className="meta machine">{yielded.get(d.key) ?? (now.has(d.key) ? 'reading against the registry’s demands…' : 'waiting')}</span>
          </div>
          <div className="row-badges">
            {yielded.has(d.key) ? <span className="chip chip-ok">read</span>
              : now.has(d.key) ? <span className="chip chip-live"><span className="pip pip-running" aria-hidden="true" />reading</span>
              : <span className="chip chip-flat">queued</span>}
          </div>
        </div>
      ))}
    </div>
  )
}

export function StoryReading({ job, events, rail, element }: { job: StoryJob; events: RunEvent[]; rail: StoryRailModel; element: string | null }) {
  useEffect(() => {
    if (!element) return
    const t = window.setTimeout(() => document.getElementById(`el-${element}`)?.scrollIntoView({ block: 'center' }), 50)
    return () => window.clearTimeout(t)
  }, [element, job.profiles.length])
  const total = job.profiles.reduce((s, p) => s + p.elements.length, 0)
  const dropped = job.profiles.reduce((s, p) => s + p.elements_dropped, 0)
  const reading = job.status === 'queued' || job.status === 'reading'
  const mapped = job.map !== null

  return (
    <section className="step story-reading" data-story-reading>
      <div className="section-head">
        <h3>The reading</h3>
        <span className="eyebrow">{job.profiles.length} of {job.documents.length} sources read · {total} elements · wall dropped {dropped}</span>
      </div>
      <p className="lede">What each source can give the film: the question it raises, the stance it takes, the elements it yields — faces, turns, reveals, numbers, quotable lines, filmable scenes — each anchored to the source's own words. Elements without a verbatim anchor were dropped by the wall.</p>

      {reading && job.profiles.length === 0 && (
        <>
          <div className="panel waiting-inline" data-reading>
            <span className="spinner" />
            <div>
              <strong>{storyStatusLabel(job.status)}</strong>
              <p className="narration-line">{rail.narration ?? 'Reading every source against the registry’s demands.'}</p>
              <p className="hint">One model call per source; the profiles appear together once every source is read.</p>
            </div>
          </div>
          <ReadingProgress job={job} events={events} />
        </>
      )}
      {!reading && job.profiles.length === 0 && <div className="panel"><p className="hint">Nothing read yet.</p></div>}

      {job.profiles.length > 0 && (
        <div className="profiles" data-profiles>
          {job.profiles.map((p) => <ProfileCard key={p.doc_key} job={job} p={p} hlElement={element} />)}
        </div>
      )}

      <div className="actions dock">
        <a className="secondary" href={storyPath(job.id, 'sources')}>← The sources</a>
        {mapped
          ? <a className="primary" href={storyPath(job.id, 'map')} data-next>Next: the map →</a>
          : <button className="primary" disabled data-next>Next: the map — after reading</button>}
      </div>
    </section>
  )
}
