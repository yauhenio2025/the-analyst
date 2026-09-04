/* Station 3 · Map — the through-lines the sources carry between them, the
   coverage matrix (which source carries which line), the recurrences, the
   contradictions and the timeline; then the approaches, ranked for this
   material. Everything here is the desk's reading of the profiles. */
import { approachLabel, docHandle, docTitle, storyStatusLabel, type StoryRailModel } from '../lib/story'
import { storyPath } from '../router'
import type { StoryJob, ThroughLine, ValueTurn } from '../types'

export function ValueTurnView({ vt }: { vt: ValueTurn }) {
  if (!vt || (!vt.value && !vt.before && !vt.after)) return null
  return (
    <div className="turn" data-value-turn>
      <span className="strip-label">value</span><span>{vt.value || '—'}</span>
      <span className="strip-label">turn</span>
      <span><span className="turn-before">{vt.before || '—'}</span> <span className="arrow">→</span> <span className="turn-after">{vt.after || '—'}</span>{vt.turned_by ? <span className="hint"> · turned by {vt.turned_by}</span> : null}</span>
    </div>
  )
}

function ThroughLineCard({ job, t }: { job: StoryJob; t: ThroughLine }) {
  return (
    <article className="panel tl-card" data-through-line={t.key}>
      <span className="eyebrow eyebrow-accent">{t.key} · carried by {t.carried_by.length} of {job.documents.length}{t.single_source ? ' · ' : ''}{t.single_source && <span className="chip chip-neg" title="only one source carries this line">single source</span>}</span>
      <h4>{t.title}</h4>
      <p className="tl-q">{t.question}</p>
      {t.face_on_the_stake && <p className="strip"><span className="strip-label">face on the stake</span> {t.face_on_the_stake}</p>}
      <ValueTurnView vt={t.value_turn} />
      {t.antagonism && <p className="strip"><span className="strip-label">antagonism</span> {t.antagonism}</p>}
      {t.open_loop && <p className="strip"><span className="strip-label">open loop</span> {t.open_loop}</p>}
      <p className="strip"><span className="strip-label">verdict possible</span> {t.verdict_possible || '—'}</p>
      {t.why && <p className="tag telling-why">{t.why}</p>}
      <p className="strip"><span className="strip-label">carried by</span> {t.carried_by.map((k) => <span key={k} className="chip chip-flat" title={docTitle(job, k)}>{docHandle(job, k)}</span>)}
        {t.not_carried_by.length > 0 && <span className="hint"> · not by {t.not_carried_by.map((k) => docHandle(job, k)).join(', ')}</span>}</p>
      <span className="machine">{t.element_ids.length} elements cited</span>
    </article>
  )
}

export function StoryMap({ job, rail }: { job: StoryJob; rail: StoryRailModel }) {
  const map = job.map
  const docs = job.documents
  const mapping = job.status === 'mapping' || job.status === 'ranking'

  if (!map) {
    return (
      <section className="step story-map" data-story-map>
        <div className="section-head"><h3>The map</h3></div>
        <div className="panel waiting-inline">
          {mapping && <span className="spinner" />}
          <div>
            <strong>{mapping ? storyStatusLabel(job.status) : 'Not mapped yet'}</strong>
            <p className="narration-line">{mapping ? (rail.narration ?? 'Finding what the sources carry between them.') : 'The map is drawn once every source is read.'}</p>
          </div>
        </div>
        <div className="actions dock"><a className="secondary" href={storyPath(job.id, 'reading')}>← The reading</a></div>
      </section>
    )
  }

  const carried = (t: ThroughLine, key: string) => map.coverage[t.key]?.[key] ?? t.carried_by.includes(key)
  const ranked = [...(job.approaches?.ranked ?? [])].sort((a, b) => a.rank - b.rank)

  return (
    <section className="step story-map" data-story-map>
      <div className="section-head">
        <h3>The map</h3>
        <span className="eyebrow">{map.through_lines.length} through-lines · {map.recurrences.length} recurrences · {map.contradictions.length} contradictions{map.timeline.length ? ` · ${map.timeline.length} dated events` : ''}</span>
      </div>
      <p className="lede">What the sources carry between them. A through-line is one question the film could hold open, with a face on the stake, a value that turns, an antagonism and a verdict the material can actually support. The matrix shows which source carries which line.</p>

      <div className="tl-cards" data-through-lines>
        {map.through_lines.map((t) => <ThroughLineCard key={t.key} job={job} t={t} />)}
        {map.through_lines.length === 0 && <p className="hint">No through-line found.</p>}
      </div>

      <div className="section-head"><h3>Coverage</h3><span className="eyebrow">rows · through-lines · columns · sources · a filled cell is a source that carries the line</span></div>
      <div className="table-scroll">
        <table className="desk-table coverage" data-coverage>
          <thead>
            <tr>
              <th>Through-line</th>
              {docs.map((d) => <th key={d.key} className="c" title={d.title}>{docHandle(job, d.key)}</th>)}
              <th className="r">carried by</th>
            </tr>
          </thead>
          <tbody>
            {map.through_lines.map((t) => (
              <tr key={t.key} data-coverage-row={t.key}>
                <td><strong>{t.title}</strong><br /><span className="machine">{t.key}</span></td>
                {docs.map((d) => {
                  const on = carried(t, d.key)
                  return <td key={d.key} className="c cell" data-carried={on ? '1' : '0'}><span className={on ? 'cell-on' : 'cell-off'} role="img" aria-label={on ? `${docHandle(job, d.key)} carries ${t.title}` : `${docHandle(job, d.key)} does not carry ${t.title}`} /></td>
                })}
                <td className="r machine">{docs.filter((d) => carried(t, d.key)).length} / {docs.length}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {ranked.length > 0 && (
        <>
          <div className="section-head"><h3>The approaches, ranked</h3><span className="eyebrow">{ranked.length} ways to tell it · for this material{job.approaches?.note ? ` · ${job.approaches.note}` : ''}</span></div>
          <ol className="approaches" data-approaches>
            {ranked.map((r) => (
              <li key={r.key} className="approach" data-approach={r.key}>
                <span className="approach-rank">{r.rank}</span>
                <div>
                  <strong>{approachLabel(r.key)}</strong> <span className="machine">{r.key}</span>
                  {r.why && <p className="approach-why">{r.why}</p>}
                  <p className="strip"><span className="strip-label">carried by</span> {r.carried_by.length ? r.carried_by.map((k) => docHandle(job, k)).join(' · ') : '—'}{r.must_cut ? <><span className="strip-label must-cut"> · must cut</span> {r.must_cut}</> : null}</p>
                </div>
              </li>
            ))}
          </ol>
        </>
      )}

      {map.recurrences.length > 0 && (
        <>
          <div className="section-head"><h3>Recurrences</h3><span className="eyebrow">what more than one source says or shows</span></div>
          <div className="sheet" data-recurrences>
            {map.recurrences.map((r, i) => (
              <div key={i} className="slate-row static">
                <div className="slate-main">
                  <span className="rec-what">{r.what}</span>
                  <span className="meta machine">{r.kind ? `${r.kind} · ` : ''}{r.doc_keys.map((k) => docHandle(job, k)).join(' · ')}{r.element_ids.length ? ` · ${r.element_ids.length} elements` : ''}</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {map.contradictions.length > 0 && (
        <>
          <div className="section-head"><h3>Contradictions</h3><span className="eyebrow">where the sources disagree — and whether the film can use it</span></div>
          <div className="contradictions" data-contradictions>
            {map.contradictions.map((c, i) => (
              <article key={i} className="panel contradiction">
                <div className="contradiction-head">
                  <h4>{c.about}</h4>
                  <span className={`chip ${c.usable_as === 'antagonism' ? 'chip-live' : c.usable_as === 'none' ? 'chip-flat' : 'chip-wait'}`} data-usable-as={c.usable_as}>usable as {c.usable_as || '—'}</span>
                </div>
                <div className="positions">
                  {c.positions.map((p, j) => (
                    <div key={j} className="position">
                      <span className="eyebrow">{docHandle(job, p.doc_key)}</span>
                      <p>{p.says}</p>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </>
      )}

      {map.timeline.length > 0 && (
        <>
          <div className="section-head"><h3>Timeline</h3><span className="eyebrow">dated events across the sources</span></div>
          <div className="table-scroll">
            <table className="desk-table timeline-map" data-timeline>
              <thead><tr><th>When</th><th>What</th><th>Sources</th></tr></thead>
              <tbody>
                {map.timeline.map((e, i) => (
                  <tr key={i}><td className="machine">{e.when}</td><td>{e.what}</td><td className="machine">{e.doc_keys.map((k) => docHandle(job, k)).join(' · ')}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <div className="actions dock">
        <a className="secondary" href={storyPath(job.id, 'reading')}>← The reading</a>
        {job.brief
          ? <a className="primary" href={storyPath(job.id, 'brief')} data-next>Next: the brief →</a>
          : <button className="primary" disabled data-next>Next: the brief — after the map</button>}
      </div>
    </section>
  )
}
