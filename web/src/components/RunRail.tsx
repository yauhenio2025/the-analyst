/* RunRail — the signature of the desk: eight numbered steps, live pips, and
   under the active step the machine's own narration set in the quote
   register. Every line here is a recorded event or the job's status. */
import { buildRail, type RailModel } from '../lib/run'
import { tokens, usd } from '../lib/format'
import type { DossierJob, RunEvent } from '../types'

export function Pip({ state }: { state: string }) {
  return <span className={`pip pip-${state}`} aria-hidden="true" />
}

export function RunRail({ job, events, compact = false, model }: {
  job: DossierJob | null
  events: RunEvent[]
  compact?: boolean
  model?: RailModel
}) {
  const rail = model ?? buildRail(job, events)
  return (
    <ol className={`runrail${compact ? ' compact' : ''}`} data-runrail aria-label="Steps of the run">
      {rail.steps.map((s, i) => {
        const active = i === rail.activeIndex
        return (
          <li key={s.step.key} className={`runrail-step is-${s.state}${active ? ' active' : ''}`}
              data-step={s.step.key} data-state={s.state}>
            <span className="runrail-n">{s.step.n}</span>
            <Pip state={s.state} />
            <div className="runrail-body">
              <div className="runrail-label">
                <span>{s.step.label}</span>
                {s.calls > 0 && (
                  <span className="machine runrail-cost">{s.calls} {s.calls === 1 ? 'call' : 'calls'} · {usd(s.cost)}</span>
                )}
              </div>
              {(active || (!compact && s.state === 'done' && s.narration)) && (s.narration || s.detail) && (
                <div className={`runrail-narration${active ? ' live' : ''}`} aria-live={active ? 'polite' : undefined}>
                  {s.narration && <p className="narration-line">{s.narration}</p>}
                  {active && s.detail && s.detail !== s.narration && <p className="machine runrail-detail">{s.detail}</p>}
                  {active && s.lastCall && (
                    <p className="machine runrail-detail">
                      {s.lastCall.kind === 'call_started' ? 'calling' : s.lastCall.kind === 'call_failed' ? 'refused' : 'returned'} · {s.lastCall.model ?? '—'}
                      {s.lastCall.engine ? ` · ${s.lastCall.engine.replace(/_/g, ' ')}` : ''}
                      {s.lastCall.input_tokens !== undefined && s.lastCall.input_tokens !== null
                        ? ` · ${tokens(s.lastCall.input_tokens)} in / ${tokens(s.lastCall.output_tokens)} out`
                        : s.lastCall.input_chars ? ` · ${tokens(s.lastCall.input_chars)} chars in` : ''}
                    </p>
                  )}
                </div>
              )}
            </div>
          </li>
        )
      })}
    </ol>
  )
}

export function CostMeter({ rail, live }: { rail: RailModel; live: boolean }) {
  return (
    <div className={`costmeter${live ? ' live' : ''}`} data-costmeter>
      <div><span className="num">{usd(rail.cost)}</span><span className="lbl">spent so far</span></div>
      <div><span className="num">{rail.calls}</span><span className="lbl">model calls</span></div>
      <div><span className="num">{tokens(rail.inputTokens)}</span><span className="lbl">tokens in</span></div>
      <div><span className="num">{tokens(rail.outputTokens)}</span><span className="lbl">tokens out</span></div>
    </div>
  )
}
