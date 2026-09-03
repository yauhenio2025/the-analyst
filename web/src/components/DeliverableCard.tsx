/* DeliverableCard — one option of the brief as a promise about use (design §B3/§C4):
   what you get → what you will understand → what you will be able to (with the
   T1/§5/F1 that keeps each promise) → answers → NOT FOR (always visible) →
   shape / evidence strips → the "how" line with edit → price + best when.
   A v1 option (no shape) falls back to the old telling card. */
import { useState, type KeyboardEvent, type MouseEvent } from 'react'
import { minutes, usd } from '../lib/format'
import { EngineChips } from './Chips'
import { DELIVERABLE_LABEL, USE_KINDS, refLabel, type BriefOption, type BriefPromise, type Recommendation } from '../types'

export function useLabel(k: string): string {
  return USE_KINDS.find((u) => u.key === k)?.label ?? k.replace(/_/g, ' ')
}

export function DeliverableCard({ option: o, letter, selected, disabled, chosen, recommendation, onSelect, onEditPath }: {
  option: BriefOption
  letter: string
  selected: boolean
  disabled: boolean
  chosen: boolean
  recommendation?: Recommendation | null
  onSelect: () => void
  onEditPath?: () => void
}) {
  const [hl, setHl] = useState<string | null>(null)
  const rec = recommendation && recommendation.option_key === o.key ? recommendation : null
  const runnerUp = recommendation && recommendation.runner_up === o.key ? (recommendation.runner_up_because ?? 'runner-up') : null
  const legacy = o.version < 2 || !o.shape
  const kind = DELIVERABLE_LABEL[o.deliverable_kind] ?? (o.deliverable_kind || '').replace(/_/g, ' ')
  const stop = (e: MouseEvent) => e.stopPropagation()
  const key = (e: KeyboardEvent) => {
    if (disabled) return
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onSelect() }
  }
  const passes = o.est_llm_calls ? Math.max(1, o.est_llm_calls - 4) : o.path.steps.length

  const Ref = ({ r }: { r: { kind: 'section' | 'table' | 'figure'; index: number } }) => {
    const label = refLabel(r)
    return (
      <span className={`ref${hl === label ? ' hl' : ''}`} title={`kept by ${label}`} data-ref={label}
            onMouseEnter={() => setHl(label)} onMouseLeave={() => setHl(null)}>{label}</span>
    )
  }
  const Promise_ = ({ p }: { p: BriefPromise }) => (
    <li className={p.unsupported ? 'unsupported' : ''}>
      <span className="promise-text">{p.text}</span>
      <span className="refs">{p.supported_by.map((r, i) => <Ref key={i} r={r} />)}{p.unsupported && <span className="ref muted" title="no section, table or figure keeps this line">unkept</span>}</span>
    </li>
  )

  return (
    <div role="radio" aria-checked={selected} tabIndex={disabled ? -1 : 0} aria-disabled={disabled || undefined}
         className={`move telling deliverable${selected ? ' selected' : ''}${disabled ? ' disabled' : ''}${rec ? ' recommended' : ''}${o.alternative ? ' alternative' : ''}`}
         onClick={() => !disabled && onSelect()} onKeyDown={key} data-telling={o.key} data-use={o.use_kind || undefined}>
      <span className="phase">deliverable · {letter}{kind ? <> · <b>{kind}</b></> : null}{o.alternative ? ' · the desk’s alternative' : ''}</span>
      {rec && <p className="rec-line" data-recommended><span className="rec-star">★</span> recommended{rec.because ? <> — <span className="rec-because">{rec.because}</span></> : null}</p>}
      {!rec && runnerUp && <p className="rec-line runner"><span className="rec-star">☆</span> runner-up — <span className="rec-because">{runnerUp}</span></p>}
      <h4>{o.title}</h4>

      {legacy ? (
        <>
          <p className="telling-text">{o.telling}</p>
          <EngineChips engines={o.engines} />
          {o.why && <p className="tag telling-why">{o.why}</p>}
        </>
      ) : (
        <>
          <p className="deliverable-line">{o.deliverable}</p>
          {o.use_kind && <span className="use-chip">for: {useLabel(o.use_kind)}</span>}

          <span className="block-label">you will understand</span>
          <ul className="promises">{o.you_will_understand.map((p, i) => <Promise_ key={i} p={p} />)}</ul>

          <span className="block-label">you will be able to</span>
          <ul className="promises able">{o.you_will_be_able_to.map((p, i) => <Promise_ key={i} p={p} />)}</ul>

          {o.questions_answered.length > 0 && (
            <p className="strip"><span className="strip-label">answers</span> {o.questions_answered.join(' · ')}</p>
          )}
          <p className="strip notfor" data-notfor><span className="strip-label">not for</span> {o.not_for.length ? o.not_for.join(' ') : 'nothing declared'}</p>

          {o.shape && (
            <details className="strip disclosure" onClick={stop}>
              <summary><span className="strip-label">shape</span> {o.shape.sections.length} sections · {o.shape.tables.length} {o.shape.tables.length === 1 ? 'table' : 'tables'} · {o.shape.figures.length} {o.shape.figures.length === 1 ? 'figure' : 'figures'} <span className="machine">▸</span></summary>
              <ul className="shape-list machine">
                {o.shape.sections.map((s, i) => <li key={`s${i}`} className={hl === `§${i + 1}` ? 'hl' : ''}><b>§{i + 1}</b> {s.heading}{s.answers ? <span className="hint"> — {s.answers}</span> : null}</li>)}
                {o.shape.tables.map((t, i) => <li key={`t${i}`} className={hl === `T${i + 1}` ? 'hl' : ''}><b>T{i + 1}</b> {t.title} — {t.row_unit}{t.rows_expected ? ` (${t.rows_expected})` : ''}</li>)}
                {o.shape.figures.map((f, i) => <li key={`f${i}`} className={hl === `F${i + 1}` ? 'hl' : ''}><b>F{i + 1}</b> {f.title} — {f.format.replace(/_/g, ' ')}</li>)}
              </ul>
            </details>
          )}
          {(o.evidence_base.carrying_docs.length > 0 || o.evidence_base.thin_or_missing.length > 0) && (
            <details className="strip disclosure" onClick={stop}>
              <summary><span className="strip-label">evidence</span> {o.evidence_base.carrying_docs.map((d) => d.doc_key).join(' · ') || '—'}{o.evidence_base.thin_or_missing.length ? <span className="hint"> · thin: {o.evidence_base.thin_or_missing[0]}</span> : null} <span className="machine">▸</span></summary>
              <ul className="shape-list machine">
                {o.evidence_base.carrying_docs.map((d) => <li key={d.doc_key}><b>{d.doc_key}</b> carries {d.carries}</li>)}
                {o.evidence_base.thin_or_missing.map((t, i) => <li key={`thin${i}`} className="hint">thin or missing: {t}</li>)}
              </ul>
            </details>
          )}

          <p className="strip how" data-how>
            <span className="strip-label">how</span>
            <span className="machine">{o.path.steps.map((s) => s.plain_name || s.engine_key.replace(/_/g, ' ')).join(' → ')} · {o.path.depth} · {passes} {passes === 1 ? 'pass' : 'passes'}</span>
            {onEditPath && !disabled && <button type="button" className="linkish edit-path" onClick={(e) => { stop(e); onEditPath() }} data-edit-path>edit ▸</button>}
          </p>
          <details className="strip disclosure how-detail" onClick={stop}>
            <summary className="hint">what each step adds</summary>
            <ul className="shape-list machine">
              {o.path.steps.map((s, i) => <li key={i}><b>{s.plain_name || s.engine_key}</b> <span className="hint">({s.engine_key} @ {s.depth})</span> — {s.contributes}</li>)}
            </ul>
          </details>
        </>
      )}

      <span className="machine telling-est"><b>{usd(o.est_cost_usd, true)}</b> · {minutes(o.est_minutes)}{legacy && o.output_shape ? ` · ${o.output_shape}` : ''}</span>
      {o.best_when && <p className="tag best-when">{o.best_when}</p>}
      {o.notes && o.notes.length > 0 && <p className="hint card-notes" title={o.notes.join('\n')}>desk notes · {o.notes.length}</p>}
      <span className={`chip-mini${selected ? ' on' : ''}`}>{chosen ? 'chosen' : selected ? 'selected' : ''}</span>
    </div>
  )
}
