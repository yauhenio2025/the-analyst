/* Station 1 · Sources — what was given, and what the film's passes ask of
   every source: the demands the registry declares for the Wirecut engines,
   read against each document before anything is mapped, proposed or spent. */
import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { Record } from '../components/Record'
import { docHandle, seconds, storyStatusLabel, type StoryRailModel } from '../lib/story'
import { storyPath } from '../router'
import type { StoryDemand, StoryJob } from '../types'

const MASTER_URL = (import.meta.env.VITE_MASTER_URL as string | undefined) || 'https://the-mastermind.onrender.com'

export function StorySources({ job, rail }: { job: StoryJob; rail: StoryRailModel }) {
  const [demands, setDemands] = useState<StoryDemand[] | null>(null)
  const [demandsError, setDemandsError] = useState<string | null>(null)
  useEffect(() => {
    api.storyDemands().then(setDemands).catch((e) => setDemandsError(String((e as Error).message ?? e)))
  }, [])
  const n = job.documents.length
  const totalChars = job.documents.reduce((s, d) => s + (d.char_count ?? 0), 0)
  const reading = job.status === 'queued' || job.status === 'reading'
  const readKeys = new Set(job.profiles.map((p) => p.doc_key))

  return (
    <section className="step story-sources" data-story-sources>
      <div className="section-head">
        <h3>The sources</h3>
        <span className="eyebrow">{n} {n === 1 ? 'source' : 'sources'} · {job.profiles.length} read</span>
      </div>
      <p className="lede">What you gave the desk. Every source is read against the same list — what the film's passes downstream will ask of it — before anything is mapped, proposed or spent.</p>

      <Record tiles={[
        { num: String(n), label: n === 1 ? 'source' : 'sources' },
        { num: totalChars.toLocaleString(), label: 'characters' },
        { num: job.options.audience || 'executive', label: 'written for' },
        { num: seconds(job.options.length_seconds), label: 'length asked for' },
      ]} />

      {job.options.intent && (
        <div className="quotecard" data-intent>
          <blockquote>{job.options.intent}</blockquote>
          <cite className="machine">what the film is for — the brief is written around it</cite>
        </div>
      )}

      <div className="sources-grid">
        <div>
          <div className="sheet" data-sources>
            {job.documents.map((d) => (
              <div key={d.key} className="slate-row static" data-doc={d.key}>
                <div className="slate-main">
                  <span className="title">{d.title}</span>
                  <span className="meta machine">
                    {[d.creators, d.year, d.publication].filter(Boolean).join(' · ')}
                    {d.char_count ? ` · ${d.char_count.toLocaleString()} chars` : ''}
                    {' · '}<a className="linkish" href={api.storySourceUrl(job.id, d.key)} target="_blank" rel="noreferrer">text ↗</a>
                  </span>
                </div>
                <div className="row-badges">
                  <span className="chip chip-flat" title={d.key}>{docHandle(job, d.key)}</span>
                  {readKeys.has(d.key) && <span className="chip chip-ok">read</span>}
                </div>
              </div>
            ))}
            {n === 0 && <p className="empty-line">No documents resolved.</p>}
          </div>

          {reading && (
            <div className="panel waiting-inline" data-reading>
              <span className="spinner" />
              <div>
                <strong>{storyStatusLabel(job.status)}</strong>
                <p className="narration-line">{rail.narration ?? 'Reading every source against the registry’s demands before anything is planned or spent.'}</p>
                <p className="hint">You can leave — the brief will be waiting in the library.</p>
              </div>
            </div>
          )}
        </div>

        <aside className="rail-aside demands-aside" data-demands>
          <span className="eyebrow">what the film’s passes ask of every source</span>
          {demands === null && !demandsError && <div className="spinner" />}
          {demandsError && <p className="hint">The registry did not answer. {demandsError}</p>}
          {demands && (
            <div className="demands">
              {demands.map((d) => (
                <div key={d.engine_key} className="demand" data-demand={d.engine_key}>
                  <h4>{d.engine_name}</h4>
                  <ul>{d.demands.map((x, i) => <li key={i}>{x}</li>)}</ul>
                </div>
              ))}
              {demands.length === 0 && <p className="hint">No demands declared.</p>}
            </div>
          )}
          <p className="machine demands-cite">declared in the registry; edit them in <a className="linkish" href={`${MASTER_URL}/engines/wirecut_spine`} target="_blank" rel="noreferrer">the Mastermind ↗</a></p>
        </aside>
      </div>

      <div className="actions dock">
        <a className="primary" href={storyPath(job.id, 'reading')} data-next>Next: the reading →</a>
      </div>
    </section>
  )
}
