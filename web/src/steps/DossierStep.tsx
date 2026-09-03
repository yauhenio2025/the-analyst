/* Step 4 · Your dossier — the composed document, the downloads, and the
   receipts: one row per model call, totals beneath. */
import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { duration, timeShort, tokens, usd } from '../lib/format'
import { Record } from '../components/Record'
import { consolePath } from '../router'
import type { DossierJob, Receipt } from '../types'

export function DossierStep({ job }: { job: DossierJob }) {
  const [html, setHtml] = useState<string | null>(null)
  const [htmlError, setHtmlError] = useState<string | null>(null)
  const [receipts, setReceipts] = useState<Receipt[] | null>(null)
  useEffect(() => {
    if (job.status !== 'done') return
    api.getDossierHtml(job.id).then(setHtml).catch((e) => setHtmlError(String((e as Error).message ?? e)))
    api.getReceipts(job.id).then(setReceipts).catch(() => setReceipts(job.receipts ?? []))
  }, [job.id, job.status, job.receipts])

  if (job.status !== 'done') {
    return (
      <section className="step">
        <div className="section-head"><h3>Your dossier</h3></div>
        <div className="panel waiting-inline"><span className="spinner" /><div><strong>Not composed yet</strong><p className="hint">The dossier appears once the draft is delivered.</p></div></div>
      </section>
    )
  }

  const t = job.totals
  const rows = receipts ?? job.receipts ?? []

  return (
    <section className="step dossier-step">
      <div className="section-head">
        <h3>Your dossier</h3>
        <span className="eyebrow">delivered · {job.sections.length} sections · {job.tables.length} tables · {job.figures.length} figures</span>
      </div>

      <Record tiles={[
        { num: usd(t.cost_usd), label: 'total spent, every call priced' },
        { num: String(t.calls), label: 'model calls on the record' },
        { num: `${tokens(t.input_tokens)} / ${tokens(t.output_tokens)}`, label: 'tokens in / out' },
        { num: duration(t.duration_ms), label: 'from first read to delivery' },
      ]} />

      <div className="actions downloads">
        <a className="primary" href={api.downloadUrl(job, 'pdf')} download={`${job.id}.pdf`} target="_blank" rel="noreferrer" data-download="pdf">Download PDF</a>
        <a className="secondary" href={api.downloadUrl(job, 'md')} download={`${job.id}.md`} target="_blank" rel="noreferrer" data-download="md">Markdown</a>
        <a className="secondary" href={api.downloadUrl(job, 'html')} download={`${job.id}.html`} target="_blank" rel="noreferrer" data-download="html">HTML</a>
        <a className="linkish" href={consolePath(job.id)} data-open-console>How this was made →</a>
      </div>

      <div className="dossier-frame panel" data-dossier-frame>
        {html === null && !htmlError && <div className="spinner" />}
        {htmlError && <div className="error-box" title={htmlError}>The composed page could not be fetched. The downloads above still work.</div>}
        {html !== null && <iframe title="The dossier" srcDoc={html} sandbox="allow-same-origin" />}
      </div>

      <div className="section-head">
        <h3>Receipts</h3>
        <span className="eyebrow">{rows.length} calls · ledger</span>
      </div>
      <div className="table-scroll">
        <table className="desk-table receipts" data-receipts>
          <thead>
            <tr><th>#</th><th>When</th><th>Step</th><th>Engine</th><th>Model</th><th className="r">In</th><th className="r">Out</th><th className="r">Cost</th><th className="r">Took</th><th>Prompt</th></tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={r.id ?? r.seq ?? i}>
                <td className="machine">{r.seq ?? i + 1}</td>
                <td className="machine">{r.ts ? timeShort(r.ts) : '—'}</td>
                <td>{r.phase ?? '—'}</td>
                <td>{r.engine ? r.engine.replace(/_/g, ' ') : '—'}</td>
                <td className="machine">{r.model ?? '—'}</td>
                <td className="r machine">{tokens(r.input_tokens)}</td>
                <td className="r machine">{tokens(r.output_tokens)}</td>
                <td className="r machine">{usd(r.cost_usd)}</td>
                <td className="r machine">{duration(r.duration_ms)}</td>
                <td className="machine hash">{r.prompt_hash ?? '—'}</td>
              </tr>
            ))}
            {rows.length === 0 && <tr><td colSpan={10} className="hint">No receipts served for this job.</td></tr>}
          </tbody>
          <tfoot>
            <tr>
              <td colSpan={5} className="eyebrow">totals</td>
              <td className="r machine">{tokens(t.input_tokens)}</td>
              <td className="r machine">{tokens(t.output_tokens)}</td>
              <td className="r machine">{usd(t.cost_usd)}</td>
              <td className="r machine">{duration(t.duration_ms)}</td>
              <td />
            </tr>
          </tfoot>
        </table>
      </div>
    </section>
  )
}
