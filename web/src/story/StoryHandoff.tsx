/* Station 6 · Handoff — the contract between this desk and Wirecut: the
   through-line, the approach, the spine, the ledger of verified elements,
   the sources with their hashes, the doctrines it was built under. Copy it
   or download it; Wirecut's corpus intake is being built. */
import { useMemo, useState } from 'react'
import { api } from '../lib/api'
import { Record } from '../components/Record'
import { usd } from '../lib/format'
import { approachLabel, docHandle, seconds, storyStatusLabel, type StoryRailModel } from '../lib/story'
import { storyPath } from '../router'
import type { StoryJob } from '../types'

export function StoryHandoff({ job, rail }: { job: StoryJob; rail: StoryRailModel }) {
  const h = job.handoff
  const [copied, setCopied] = useState<'ok' | 'fail' | null>(null)
  const json = useMemo(() => (h ? JSON.stringify(h, null, 2) : ''), [h])
  const writing = job.status === 'handing_off'

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(json)
      setCopied('ok')
    } catch {
      setCopied('fail')
    }
    window.setTimeout(() => setCopied(null), 2500)
  }

  if (!h) {
    return (
      <section className="step story-handoff" data-story-handoff>
        <div className="section-head"><h3>The handoff</h3></div>
        <div className="panel waiting-inline">
          {writing && <span className="spinner" />}
          <div>
            <strong>{writing ? storyStatusLabel(job.status) : 'Not written yet'}</strong>
            <p className="narration-line">{writing ? (rail.narration ?? 'Assembling the contract for Wirecut.') : 'The handoff is written once the spine is built.'}</p>
          </div>
        </div>
        <div className="actions dock"><a className="secondary" href={storyPath(job.id, 'spine')}>← The spine</a></div>
      </section>
    )
  }

  const doctrines = Object.entries(h.doctrines ?? {})
  const coverage = Object.entries(h.coverage ?? {})

  return (
    <section className="step story-handoff" data-story-handoff>
      <div className="section-head">
        <h3>The handoff</h3>
        <span className="eyebrow">contract v{h.version} · {h.story_job_id} · {rail.calls} calls · {usd(rail.cost)}</span>
      </div>
      <p className="lede">Everything Wirecut needs to make the film and nothing it must guess: the through-line, the approach, the spine, every verified element the spine cites with its verbatim anchor, the sources with their hashes, and the doctrines this desk worked under.</p>

      <Record tiles={[
        { num: h.through_line?.title ?? '—', label: 'through-line', title: h.through_line?.question },
        { num: approachLabel(h.approach?.key ?? h.spine?.approach_key), label: 'approach' },
        { num: String(h.spine?.movements.length ?? 0), label: `movements · ${seconds(h.spine?.length_seconds)}` },
        { num: String(h.sources.length), label: h.sources.length === 1 ? 'source' : 'sources' },
        { num: String(h.ledger.length), label: 'verified elements in the ledger' },
        { num: String(doctrines.length), label: 'doctrine files, hash-pinned' },
      ]} columns={3} />

      <div className="panel handoff-actions" data-handoff-actions>
        <button type="button" className="secondary" onClick={copy} data-copy-json>{copied === 'ok' ? 'Copied ✓' : copied === 'fail' ? 'Copy failed — use download' : 'Copy JSON'}</button>
        <a className="secondary" href={api.storyHandoffUrl(job.id)} download="handoff.json" target="_blank" rel="noreferrer" data-download-json>Download handoff.json</a>
        <span className="outcome-unit">
          <button type="button" className="primary ghost" disabled aria-disabled="true" data-open-wirecut>Open in Wirecut</button>
          <span className="outcome-subline">Wirecut's corpus intake is being built; paste the JSON there for now.</span>
        </span>
        <span className="machine">{(json.length / 1024).toFixed(0)} KB</span>
      </div>

      <div className="section-head"><h3>Sources handed over</h3><span className="eyebrow">{h.sources.length} with sha256 · full text served by this API</span></div>
      <div className="table-scroll">
        <table className="desk-table handoff-sources" data-handoff-sources>
          <thead><tr><th>Source</th><th>Creators · year</th><th className="r">Chars</th><th>sha256</th><th>Carried</th><th>Text</th></tr></thead>
          <tbody>
            {h.sources.map((s) => (
              <tr key={s.doc_key} data-handoff-source={s.doc_key}>
                <td><strong>{s.title}</strong><br /><span className="machine">{s.doc_key}{s.publication ? ` · ${s.publication}` : ''}</span></td>
                <td>{[s.creators, s.year].filter(Boolean).join(' · ') || '—'}</td>
                <td className="r machine">{s.chars.toLocaleString()}</td>
                <td className="machine hash" title={s.sha256}>{s.sha256.slice(0, 12)}…</td>
                <td>{h.coverage?.[s.doc_key] === false ? <span className="chip chip-flat">not carried</span> : <span className="chip chip-ok">carried</span>}</td>
                <td><a className="linkish" href={api.storySourceUrl(job.id, s.doc_key)} target="_blank" rel="noreferrer">text ↗</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {coverage.length > h.sources.length && (
        <p className="hint" data-left-out>Left out of the film: {coverage.filter(([k]) => !h.sources.some((s) => s.doc_key === k)).map(([k]) => docHandle(job, k)).join(' · ')}.</p>
      )}

      <div className="section-head"><h3>Doctrines</h3><span className="eyebrow">the registry files this desk worked under, hash-pinned</span></div>
      <div className="sheet" data-doctrines>
        {doctrines.map(([k, sha]) => (
          <div key={k} className="slate-row static">
            <div className="slate-main"><span className="machine">{k}</span></div>
            <div className="row-badges"><span className="machine hash" title={sha}>{sha.slice(0, 16)}…</span></div>
          </div>
        ))}
        {doctrines.length === 0 && <p className="empty-line">No doctrine files were pinned.</p>}
      </div>

      <details className="more" data-handoff-json>
        <summary>the contract, as JSON · {(json.length / 1024).toFixed(0)} KB</summary>
        <div className="excerpt"><pre>{json}</pre></div>
      </details>

      <div className="actions dock">
        <a className="secondary" href={storyPath(job.id, 'spine')}>← The spine</a>
        <span className="hint">Handed off {h.created_at ? `at ${new Date(h.created_at).toLocaleString()}` : ''} · {rail.calls} calls · {usd(rail.cost)} · every step on the record.</span>
      </div>
    </section>
  )
}
