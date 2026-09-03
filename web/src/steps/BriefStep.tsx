/* Step 2 · The brief — three deliverables from the desk, one choice from you.
   Each card says what you get, what you will understand and what you will be
   able to do; the how is underneath (design §C4). Lanes: "use" (three cards,
   one recommended with its reason), "chosen" (your path + the desk's
   alternative), "material" (the desk chose; the reason is shown). The dials
   are two: figures and who it is written for. "edit ▸" on a card's how-line
   and "I know the analysis I want ▸" open the catalog picker. */
import { useEffect, useMemo, useState } from 'react'
import { api } from '../lib/api'
import { minutes, usd } from '../lib/format'
import { CatalogPicker, estimatePath, pathDepth, type PickedStep } from '../components/CatalogPicker'
import { DeliverableCard } from '../components/DeliverableCard'
import { OutcomeButton } from '../components/OutcomeButton'
import type { Audience, BriefOption, Catalog, DossierJob } from '../types'
import { statusRank } from '../types'

const OWN_PATH = 'own_path'

export function BriefStep({ job, onChosen, onBack }: {
  job: DossierJob
  onChosen: (job: DossierJob) => void
  onBack: () => void
}) {
  const brief = job.brief
  const defaults = brief?.defaults ?? {}
  const rec = brief?.recommendation ?? null
  const entry = brief?.entry ?? job.options.entry ?? 'use'
  const [option, setOption] = useState<string | null>(job.chosen_option ?? rec?.option_key ?? defaults.option_key ?? brief?.options[0]?.key ?? null)
  const [audience, setAudience] = useState<Audience>(job.options.audience ?? defaults.audience ?? 'executive')
  const [figures, setFigures] = useState<number>(job.options.output?.figures ?? defaults.figures ?? 2)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  // the picker: editing one card's how-line, or composing your own path (a fourth card)
  const [picker, setPicker] = useState<{ mode: 'edit' | 'own'; key: string } | null>(null)
  const [steps, setSteps] = useState<PickedStep[]>([])
  const [edits, setEdits] = useState<Record<string, PickedStep[]>>({})
  const [ownPath, setOwnPath] = useState<PickedStep[] | null>(null)
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [catalogError, setCatalogError] = useState<string | null>(null)

  const corpusChars = useMemo(() => (job.documents ?? []).reduce((n, d) => n + (d.char_count ?? 0), 0) || job.profiles.reduce((n, p) => n + (p.chars ?? 0), 0), [job])
  useEffect(() => {
    if (job.chosen_option) setOption(job.chosen_option)
    else if (!option && brief?.options.length) setOption(rec?.option_key ?? defaults.option_key ?? brief.options[0].key)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [job.chosen_option, brief])
  useEffect(() => {
    if (!picker || catalog) return
    api.catalog(audience, corpusChars || null, job.documents?.length ?? job.profiles.length ?? null).then(setCatalog)
      .catch((e) => setCatalogError(String((e as Error).message ?? e)))
  }, [picker, catalog, audience, corpusChars, job])

  const alreadyChosen = job.chosen_option !== null && statusRank(job.status) >= statusRank('planning')
  const engineName = (k: string) => {
    const e = catalog?.groups.flatMap((g) => g.engines).find((x) => x.engine_key === k)
    return e?.plain_name ?? k.replace(/_/g, ' ')
  }
  /* cards as displayed: an edited how-line replaces the path and re-prices the card client-side */
  const options: BriefOption[] = useMemo(() => (brief?.options ?? []).map((o) => {
    const e = edits[o.key]
    if (!e) return o
    const est = estimatePath(catalog, e)
    return { ...o, path: { ...o.path, steps: e.map((s) => ({ engine_key: s.engine_key, plain_name: engineName(s.engine_key), contributes: o.path.steps.find((x) => x.engine_key === s.engine_key)?.contributes ?? '', depth: s.depth })), depth: pathDepth(catalog, e) },
             est_cost_usd: est?.cost ?? o.est_cost_usd, est_minutes: est?.minutes ?? o.est_minutes, est_llm_calls: est?.calls ?? o.est_llm_calls,
             notes: [...(o.notes ?? []), 'how-line edited — the server confirms the price on choose'] }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }), [brief, edits, catalog])
  const chosen = options.find((o) => o.key === option) ?? null
  const ownEst = ownPath ? estimatePath(catalog, ownPath) : null

  const openPicker = (mode: 'edit' | 'own', key: string) => {
    const base = mode === 'edit' ? (edits[key] ?? options.find((o) => o.key === key)?.path.steps.map((s) => ({ engine_key: s.engine_key, depth: s.depth })) ?? []) : (ownPath ?? [])
    setSteps(base)
    setPicker({ mode, key })
  }
  const donePicker = () => {
    if (!picker) return
    if (picker.mode === 'edit') setEdits((e) => ({ ...e, [picker.key]: steps }))
    else { setOwnPath(steps); setOption(OWN_PATH) }
    setPicker(null)
  }

  const write = async () => {
    if (!option || busy) return
    setBusy(true)
    setError(null)
    try {
      const overrides: Record<string, unknown> = { audience, figures }
      const edited = option === OWN_PATH ? ownPath : edits[option]
      if (edited && edited.length) overrides.path = { steps: edited }
      const next = await api.chooseBrief(job.id, option, overrides)
      onChosen(next)
    } catch (e) {
      setError(String((e as Error).message ?? e))
      setBusy(false)
    }
  }

  if (!brief) {
    return (
      <section className="step">
        <div className="section-head"><h3>The brief</h3></div>
        <div className="panel waiting-inline"><span className="spinner" /><div><strong>Not written yet</strong><p className="hint">The brief appears once the desk has read every document.</p></div></div>
      </section>
    )
  }

  const eyebrow = entry === 'chosen' ? 'your path + the desk’s alternative'
    : entry === 'material' ? 'the material decided'
    : `${options.length} deliverables · ${alreadyChosen ? 'chosen' : 'your choice'}`
  const recTitle = rec ? options.find((o) => o.key === rec.option_key)?.title ?? rec.option_key : null

  return (
    <section className="step brief-step">
      <div className="section-head">
        <h3>The brief</h3>
        <span className="eyebrow">{eyebrow}</span>
      </div>
      {entry === 'material' && rec ? (
        <p className="lede" data-material-reason>The desk chose <b>{recTitle}</b>{rec.because ? <> — because {rec.because}</> : null}. The cards below stay readable; the draft is written from the chosen one.</p>
      ) : (
        <p className="lede">Each card says what you get, what you will understand and what you will be able to do. Pick by use; the how is underneath. Nothing more is spent until you choose.</p>
      )}

      <div className="tellings deliverables" role="radiogroup" data-tellings>
        {options.map((o, i) => (
          <DeliverableCard key={o.key} option={o} letter={String.fromCharCode(65 + i)} selected={option === o.key}
                           disabled={alreadyChosen && option !== o.key} chosen={alreadyChosen && option === o.key}
                           recommendation={rec} onSelect={() => !alreadyChosen && setOption(o.key)}
                           onEditPath={alreadyChosen ? undefined : () => openPicker('edit', o.key)} />
        ))}
        {ownPath && (
          <div role="radio" aria-checked={option === OWN_PATH} tabIndex={0} className={`move telling deliverable own${option === OWN_PATH ? ' selected' : ''}`}
               onClick={() => !alreadyChosen && setOption(OWN_PATH)} onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (!alreadyChosen) setOption(OWN_PATH) } }} data-telling={OWN_PATH}>
            <span className="phase">deliverable · yours</span>
            <h4>Your own path</h4>
            <p className="deliverable-line">A dossier along the path you chose. The brief will say what this path lets you understand and do once it runs.</p>
            <p className="strip how"><span className="strip-label">how</span><span className="machine">{ownPath.map((s) => engineName(s.engine_key)).join(' → ')} · {pathDepth(catalog, ownPath)} · {ownEst?.calls ? ownEst.calls - 4 : ownPath.length} {ownPath.length === 1 ? 'pass' : 'passes'}</span>
              {!alreadyChosen && <button type="button" className="linkish edit-path" onClick={(e) => { e.stopPropagation(); openPicker('own', OWN_PATH) }}>edit ▸</button>}</p>
            <span className="machine telling-est"><b>{ownEst ? usd(ownEst.cost, true) : '—'}</b> · {ownEst ? minutes(ownEst.minutes) : 'priced on choose'}</span>
            <span className={`chip-mini${option === OWN_PATH ? ' on' : ''}`}>{alreadyChosen ? 'chosen' : 'selected'}</span>
          </div>
        )}
      </div>

      {!alreadyChosen && !picker && (
        <p className="under-cards"><button type="button" className="linkish" onClick={() => openPicker('own', OWN_PATH)} data-own-path>I know the analysis I want ▸</button>
          <span className="hint"> pick the engines from the purpose-first catalog; the desk proposes one alternative.</span></p>
      )}

      {picker && (
        <div className="panel picker-panel" data-picker-panel>
          <div className="section-head"><h3>{picker.mode === 'edit' ? `Edit the how-line · ${options.find((o) => o.key === picker.key)?.title ?? ''}` : 'Your own path'}</h3>
            <span className="eyebrow">the catalog by purpose</span></div>
          <CatalogPicker catalog={catalog} loading={!catalog && !catalogError} error={catalogError} steps={steps} onChange={setSteps}
                         onDone={donePicker} doneLabel={picker.mode === 'edit' ? 'Use this how-line' : 'Add as a card'} onCancel={() => setPicker(null)} />
        </div>
      )}

      <div className="panel dials-panel">
        <span className="eyebrow">the dials</span>
        <div className="dials">
          <label className="field">
            <span className="field-label">Figures</span>
            <select value={figures} disabled={alreadyChosen} onChange={(e) => setFigures(Number(e.target.value))} data-dial="figures">
              {[0, 1, 2, 3, 4].map((n) => <option key={n} value={n}>{n === 0 ? 'None' : n}</option>)}
            </select>
          </label>
          <label className="field">
            <span className="field-label">Written for</span>
            <select value={audience} disabled={alreadyChosen} onChange={(e) => setAudience(e.target.value as Audience)} data-dial="audience">
              <option value="executive">An executive</option>
              <option value="analyst">An analyst</option>
              <option value="researcher">A researcher</option>
            </select>
            {audience !== (job.options.audience ?? 'executive') && <span className="hint">The draft will be written for {audience === 'analyst' ? 'an analyst' : audience === 'researcher' ? 'a researcher' : 'an executive'}; the cards keep the register they were written in.</span>}
          </label>
        </div>
        {brief.notes && brief.notes.length > 0 && <p className="hint desk-notes" title={brief.notes.join('\n')}>desk notes · {brief.notes.length} — what the checks changed</p>}
      </div>

      {error && <div className="error-box" title={error}>{error}</div>}

      <div className="actions dock">
        <button className="secondary" onClick={onBack}>← Your documents</button>
        {alreadyChosen ? (
          <span className="hint">The draft is being written from “{chosen?.title ?? (option === OWN_PATH ? 'your own path' : option)}”.</span>
        ) : (
          <OutcomeButton verb="Write" object="the draft" disabled={(!chosen && option !== OWN_PATH) || busy} onClick={write} data-write
                         amount={chosen ? usd(chosen.est_cost_usd, true) : ownEst ? usd(ownEst.cost, true) : null}
                         minutes={chosen ? minutes(chosen.est_minutes) : ownEst ? minutes(ownEst.minutes) : null}
                         effect={`every step recorded — you can watch it write, or leave and come back${chosen?.deliverable ? ` · ${chosen.deliverable}` : ''}`} />
        )}
      </div>
    </section>
  )
}
