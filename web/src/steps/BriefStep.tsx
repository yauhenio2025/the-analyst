/* Step 2 · The brief — three tellings from the desk, one choice from you.
   The cards are the desk's recorded proposal; the dials are your overrides;
   the button says what it costs before anything is spent. */
import { useEffect, useState } from 'react'
import { api } from '../lib/api'
import { minutes, usd } from '../lib/format'
import { EngineChips } from '../components/Chips'
import { OutcomeButton } from '../components/OutcomeButton'
import type { Audience, Depth, DossierJob } from '../types'
import { statusRank } from '../types'

export function BriefStep({ job, onChosen, onBack }: {
  job: DossierJob
  onChosen: (job: DossierJob) => void
  onBack: () => void
}) {
  const brief = job.brief
  const defaults = brief?.defaults ?? {}
  const [option, setOption] = useState<string | null>(job.chosen_option ?? defaults.option_key ?? brief?.options[0]?.key ?? null)
  const [audience, setAudience] = useState<Audience>(job.options.audience ?? defaults.audience ?? 'executive')
  const [depth, setDepth] = useState<Depth>(job.options.depth ?? defaults.depth ?? 'medium')
  const [figures, setFigures] = useState<number>(job.options.output?.figures ?? defaults.figures ?? 2)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    if (job.chosen_option) setOption(job.chosen_option)
    else if (!option && brief?.options.length) setOption(defaults.option_key ?? brief.options[0].key)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [job.chosen_option, brief])

  const chosen = brief?.options.find((o) => o.key === option) ?? null
  const alreadyChosen = job.chosen_option !== null && statusRank(job.status) >= statusRank('planning')

  const write = async () => {
    if (!option || busy) return
    setBusy(true)
    setError(null)
    try {
      const next = await api.chooseBrief(job.id, option, { audience, depth, figures })
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

  return (
    <section className="step brief-step">
      <div className="section-head">
        <h3>The brief</h3>
        <span className="eyebrow">{brief.options.length} tellings · {alreadyChosen ? 'chosen' : 'your choice'}</span>
      </div>
      <p className="lede">Three ways to tell what these documents say. Each card names the engines it would run, what it would cost, and roughly how long. Pick one; the desk writes the draft and records every step.</p>

      <div className="tellings" role="radiogroup" data-tellings>
        {brief.options.map((o, i) => {
          const on = option === o.key
          return (
            <button key={o.key} type="button" role="radio" aria-checked={on}
                    className={`move telling${on ? ' selected' : ''}`}
                    disabled={alreadyChosen && !on}
                    onClick={() => !alreadyChosen && setOption(o.key)} data-telling={o.key}>
              <span className="phase">telling · {String.fromCharCode(65 + i)}{defaults.option_key === o.key ? ' · recommended' : ''}</span>
              <h4>{o.title}</h4>
              <p className="telling-text">{o.telling}</p>
              <EngineChips engines={o.engines} />
              <p className="tag telling-why">{o.why}</p>
              <span className="machine telling-est">{usd(o.est_cost_usd, true)} · {minutes(o.est_minutes)}{o.output_shape ? ` · ${o.output_shape}` : ''}</span>
              <span className={`chip-mini${on ? ' on' : ''}`}>{alreadyChosen ? 'chosen' : on ? 'selected' : ''}</span>
            </button>
          )
        })}
      </div>

      <div className="panel dials-panel">
        <span className="eyebrow">the dials</span>
        <div className="dials">
          <label className="field">
            <span className="field-label">Written for</span>
            <select value={audience} disabled={alreadyChosen} onChange={(e) => setAudience(e.target.value as Audience)}>
              <option value="executive">An executive</option>
              <option value="analyst">An analyst</option>
              <option value="researcher">A researcher</option>
            </select>
          </label>
          <label className="field">
            <span className="field-label">Depth</span>
            <select value={depth} disabled={alreadyChosen} onChange={(e) => setDepth(e.target.value as Depth)}>
              <option value="simple">Simple</option>
              <option value="medium">Medium</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>
          <label className="field">
            <span className="field-label">Figures</span>
            <select value={figures} disabled={alreadyChosen} onChange={(e) => setFigures(Number(e.target.value))}>
              {[0, 1, 2, 3, 4].map((n) => <option key={n} value={n}>{n === 0 ? 'None' : n}</option>)}
            </select>
          </label>
        </div>
      </div>

      {error && <div className="error-box" title={error}>{error}</div>}

      <div className="actions dock">
        <button className="secondary" onClick={onBack}>← Your documents</button>
        {alreadyChosen ? (
          <span className="hint">The draft is being written from “{chosen?.title}”.</span>
        ) : (
          <OutcomeButton verb="Write" object="the draft" disabled={!chosen || busy} onClick={write} data-write
                         amount={chosen ? usd(chosen.est_cost_usd, true) : null}
                         minutes={chosen ? minutes(chosen.est_minutes) : null}
                         effect="every step recorded — you can watch it write, or leave and come back" />
        )}
      </div>
    </section>
  )
}
