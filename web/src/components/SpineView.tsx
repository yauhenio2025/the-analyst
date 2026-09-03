/* The spine and the findings ledger — the "analysis behind it" surfaces of the
   concretization passes. Every line is a recorded fact on the job: the spine
   the desk planned against, and the findings the walls, the clamps and the
   cross-check judge minted, each with its one cure and its fate. */
import type { CrossCheckVerdict, DossierSpine, Finding } from '../types'

const words = (s: string) => s.replace(/_/g, ' ')

export function SpineView({ spine }: { spine: DossierSpine }) {
  const read = spine.read
  return (
    <article className="section-view spine-view" data-spine>
      <span className="eyebrow eyebrow-accent">the spine · round {spine.round}</span>
      <h2 className="display">{spine.handle || 'What the dossier argues'}</h2>
      <p className="lede">{spine.thesis}</p>
      {spine.reader_question && <p className="hint">The reader's question: {spine.reader_question}</p>}
      <ol className="index spine-sections" data-spine-sections>
        {spine.sections.map((s, i) => (
          <li key={s.key} data-spine-section={s.key}>
            <strong>{i + 1}. {s.heading}</strong>
            <p className="claim-text">{s.claim}</p>
            <span className="machine">
              {s.evidence_kind ? words(s.evidence_kind) : ''}
              {s.table ? ` · table: one row = ${s.table.row_unit}` : ''}
              {s.figure ? ` · diagram: ${words(s.figure.visual_format)}` : ''}
              {s.anchors_planned?.length ? ` · ${s.anchors_planned.length} anchors planned` : ''}
            </span>
          </li>
        ))}
      </ol>
      <div className="quotecard">
        <blockquote>Summary's job — {spine.summary_job}</blockquote>
        <blockquote>Close's job — {spine.conclusion_job}</blockquote>
        <cite className="machine">two different jobs, declared before a word was written</cite>
      </div>
      {read && (read.plain_summary || read.buried_crux) && (
        <details className="more" data-spine-read>
          <summary>the composition read — what it says plainly, and what was buried</summary>
          {read.plain_summary && <p>{read.plain_summary}</p>}
          {read.buried_crux && <p><em>Buried or unstated:</em> {read.buried_crux}</p>}
          {read.cumulative_direction && <p><em>Where the evidence pushes:</em> {read.cumulative_direction}</p>}
          {!!read.strands?.length && <p><em>Strands:</em> {read.strands.map((x) => x.name + (x.accidental ? ' (accidental)' : '')).join(' · ')}</p>}
          {!!read.prose_to_table?.length && <p><em>Should be a table:</em> {read.prose_to_table.join(' · ')}</p>}
          {!!read.figures_dropped?.length && <p><em>Pictures dropped as decoration:</em> {read.figures_dropped.join(' · ')}</p>}
        </details>
      )}
      {!!spine.notes?.length && (
        <details className="more"><summary>what the walls changed · {spine.notes.length}</summary>
          <ul className="eventlist">{spine.notes.map((n, i) => <li key={i}>{n}</li>)}</ul>
        </details>
      )}
    </article>
  )
}

export function fateOf(f: Finding): string {
  return f.fates?.length ? f.fates[f.fates.length - 1].fate : f.status
}

export function FindingsView({ findings, verdict }: { findings: Finding[]; verdict: CrossCheckVerdict | null }) {
  const open = findings.filter((f) => f.status === 'open')
  return (
    <article className="section-view findings-view" data-findings>
      <span className="eyebrow eyebrow-accent">the cross-check · findings ledger</span>
      <h2 className="display">{verdict?.hangs_together ? 'It hangs together.' : `${findings.length} finding${findings.length === 1 ? '' : 's'}, ${open.length} open`}</h2>
      {verdict && (
        <p className="lede">
          {verdict.summary || (verdict.judged ? 'No summary recorded.' : 'The judge was unavailable; the clamps still ran.')}
          <span className="machine"> · round {verdict.round} · {verdict.clamps} by arithmetic · {verdict.realized?.length ?? 0} acted on</span>
        </p>
      )}
      {!verdict && <p className="hint">The cross-check has not run yet.</p>}
      {findings.length > 0 && (
        <div className="table-scroll">
          <table className="desk-table findings" data-findings-table>
            <thead><tr><th>Species</th><th>Where</th><th>Effect on the reader, then the cure</th><th>Cure</th><th>Fate</th></tr></thead>
            <tbody>
              {findings.map((f) => {
                const where = Object.entries(f.where ?? {}).filter(([, v]) => v !== null && v !== undefined && v !== '').map(([k, v]) => `${words(k).replace(' key', '')} ${v}`).join(' · ')
                const fate = fateOf(f)
                return (
                  <tr key={f.id} data-finding={f.id} data-fate={fate}>
                    <td><strong>{words(f.kind)}</strong><br /><span className="machine">{f.source}</span></td>
                    <td className="machine">{where || '—'}</td>
                    <td>{f.note}{f.quote ? <><br /><span className="machine">“{f.quote.slice(0, 160)}{f.quote.length > 160 ? '…' : ''}”</span></> : null}</td>
                    <td>{words(f.affordance)}</td>
                    <td><span className={`chip chip-${fate === 'resolved' || fate === 'executed' ? 'ok' : fate === 'failed' || fate === 'regressed' ? 'neg' : 'wait'}`}>{fate}</span></td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </article>
  )
}
