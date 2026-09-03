/* Step 1 · Your documents — what was given, and what the desk read in it. */
import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { chars, statusLabel } from '../lib/format'
import { statusRank } from '../types'
import type { DossierJob, Exemplar, RunEvent, SourceSpec } from '../types'
import { RunRail } from '../components/RunRail'
import { buildRail } from '../lib/run'

function sourceLine(s: SourceSpec, exemplars: Exemplar[]): { kind: string; title: string; meta: string } {
  switch (s.kind) {
    case 'paste': return { kind: 'pasted text', title: s.title || 'Untitled', meta: chars(s.text?.length ?? 0) }
    case 'exemplar': {
      const x = exemplars.find((e) => e.key === s.key)
      return { kind: 'exemplar bundle', title: x?.title ?? s.key, meta: x ? `${x.n_docs} documents · ${x.chars.toLocaleString()} chars` : s.key }
    }
    case 'stacks_view': return { kind: 'stacks view', title: s.view_id, meta: 'resolved on the server' }
    case 'stacks_uids': return { kind: 'stacks papers', title: `${s.uids.length} papers`, meta: s.uids.slice(0, 3).join(', ') }
  }
}

export function SourcesStep({ job, events, onNext }: { job: DossierJob; events: RunEvent[]; onNext: () => void }) {
  const [exemplars, setExemplars] = useState<Exemplar[]>([])
  useEffect(() => {
    if (job.sources.some((s) => s.kind === 'exemplar')) api.exemplars().then(setExemplars).catch(() => {})
  }, [job.sources])
  const reading = statusRank(job.status) < statusRank('awaiting_brief') && job.status !== 'failed'
  const canNext = statusRank(job.status) >= statusRank('awaiting_brief')
  const rail = buildRail(job, events)

  return (
    <section className="step sources-step">
      <div className="section-head">
        <h3>Your documents</h3>
        <span className="eyebrow">{job.sources.length} {job.sources.length === 1 ? 'source' : 'sources'} · {job.profiles.length} profiled</span>
      </div>
      <p className="lede">What you gave the desk, and what it read in each document before anything was planned. The profiles are the desk's reading; the quotes are the documents' own words.</p>

      <div className="sources-grid">
        <div>
          <div className="sheet" data-sources>
            {job.sources.map((s, i) => {
              const line = sourceLine(s, exemplars)
              return (
                <div key={i} className="slate-row static">
                  <div className="slate-main">
                    <span className="title">{line.title}</span>
                    <span className="meta machine">{line.kind} · {line.meta}</span>
                  </div>
                </div>
              )
            })}
          </div>

          {reading && (
            <div className="panel waiting-inline" data-reading>
              <span className="spinner" />
              <div>
                <strong>{statusLabel(job.status)}</strong>
                <p className="narration-line">{rail.narration ?? 'Reading the documents before anything is planned or spent.'}</p>
                <p className="hint">You can leave — the brief will be waiting in the library.</p>
              </div>
            </div>
          )}

          {job.status === 'failed' && (
            <div className="error-box">{job.error ?? 'Stopped.'}</div>
          )}

          {job.profiles.length > 0 && (
            <div className="profiles" data-profiles>
              {job.profiles.map((p) => (
                <article key={p.doc_key} className="panel profile">
                  <span className="eyebrow eyebrow-accent">{p.genre ?? 'document'}{p.year ? ` · ${p.year}` : ''}{p.chars ? ` · ${p.chars.toLocaleString()} chars` : ''}</span>
                  <h4 className="profile-title">{p.title}</h4>
                  {p.author && <p className="machine">{p.author}</p>}
                  <p className="profile-thesis">{p.thesis}</p>
                  <div className="claims">
                    {p.key_claims.map((c, i) => (
                      <div key={i} className="claim">
                        <span className="claim-n">{i + 1}</span>
                        <div>
                          <p className="claim-text">{c.claim}</p>
                          <blockquote className="claim-quote">“{c.quote}”</blockquote>
                        </div>
                      </div>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
        <aside className="rail-aside">
          <span className="eyebrow">the run so far</span>
          <RunRail job={job} events={events} compact />
        </aside>
      </div>

      <div className="actions dock">
        <button className="primary" disabled={!canNext} onClick={onNext} data-next>
          {canNext ? 'Next: the brief →' : 'Next: the brief — after reading'}
        </button>
        {!canNext && job.status !== 'failed' && <span className="hint">Enabled once the desk has read every document.</span>}
      </div>
    </section>
  )
}
