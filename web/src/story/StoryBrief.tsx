/* Station 4 · Brief — three films the material can carry, deliverable-first:
   what the viewer will understand, feel and be able to do; the through-line,
   the approach, the sources used and left out, the price. One choice.
   The law of the station: nothing has been rendered yet. */
import { useState } from 'react'
import { api } from '../lib/api'
import { minutes, usd } from '../lib/format'
import { OutcomeButton } from '../components/OutcomeButton'
import { approachLabel, docHandle, docTitle, seconds, storyStatusLabel, type StoryRailModel } from '../lib/story'
import { storyPath } from '../router'
import type { StoryJob, StoryOption } from '../types'

function OptionCard({ job, o, letter, recommended, why, chosen, disabled, busy, onChoose }: {
  job: StoryJob; o: StoryOption; letter: string; recommended: boolean; why: string
  chosen: boolean; disabled: boolean; busy: boolean; onChoose?: () => void
}) {
  const tl = job.map?.through_lines.find((t) => t.key === o.through_line_key)
  return (
    <div className={`move telling deliverable film-option${chosen ? ' selected' : ''}${disabled ? ' disabled' : ''}${recommended ? ' recommended' : ''}`}
         data-option={o.key} data-recommended={recommended || undefined}>
      <span className="phase">film · {letter} · <b>{seconds(o.length_seconds)}</b> · {approachLabel(o.approach_key)}</span>
      {recommended && <p className="rec-line" data-recommended><span className="rec-star">★</span> recommended{why ? <> — <span className="rec-because">{why}</span></> : null}</p>}
      <h4>{o.title}</h4>

      <span className="block-label">you will understand</span>
      <p className="deliverable-line">{o.viewer_will_understand || '—'}</p>
      <span className="block-label">you will feel</span>
      <p className="deliverable-line feel">{o.viewer_will_feel || '—'}</p>
      <span className="block-label">you will be able to</span>
      <p className="deliverable-line able">{o.viewer_will_be_able_to || '—'}</p>

      <p className="strip"><span className="strip-label">through-line</span> {tl?.title ?? o.through_line_key ?? '—'}</p>
      <p className="strip"><span className="strip-label">approach</span> {approachLabel(o.approach_key)} <span className="machine">{o.approach_key}</span></p>
      <p className="strip"><span className="strip-label">sources used</span> {o.sources_used.length ? o.sources_used.map((k) => <span key={k} className="chip chip-flat" title={docTitle(job, k)}>{docHandle(job, k)}</span>) : '—'}</p>
      <p className="strip notfor"><span className="strip-label">left out</span> {o.sources_left_out.length ? o.sources_left_out.map((k) => docHandle(job, k)).join(' · ') : 'nothing — every source is used'}</p>
      {o.risks.length > 0 && (
        <p className="strip"><span className="strip-label">risks</span> {o.risks.join(' · ')}</p>
      )}
      {o.why && <p className="tag telling-why">{o.why}</p>}

      <span className="machine telling-est"><b>{usd(o.est_cost_usd, true)}</b> · {minutes(o.est_minutes)} · indicative, for the passes downstream</span>
      <div className="option-actions">
        {onChoose && !disabled && !chosen && (
          <OutcomeButton verb="Choose" object="this film" amount={usd(o.est_cost_usd, true)} minutes={minutes(o.est_minutes)}
                         disabled={busy} onClick={onChoose} data-choose={o.key}
                         effect="the spine is built from the sources and handed to Wirecut — nothing is rendered here" />
        )}
        {chosen && <span className="hint" data-chosen>the spine is built from this film</span>}
      </div>
      <span className={`chip-mini${chosen ? ' on' : ''}`}>chosen</span>
    </div>
  )
}

export function StoryBrief({ job, rail, onChosen }: { job: StoryJob; rail: StoryRailModel; onChosen: (job: StoryJob) => void }) {
  const brief = job.brief
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const chosen = job.chosen_option
  const canChoose = job.status === 'awaiting_brief' && !chosen
  const writing = job.status === 'briefing'

  const choose = async (key: string) => {
    if (busy) return
    setBusy(key)
    setError(null)
    try {
      const r = await api.chooseStoryBrief(job.id, key)
      onChosen({ ...job, chosen_option: r.chosen_option, status: r.status, step: 'spine' })
    } catch (e) {
      setError(String((e as Error).message ?? e))
      setBusy(null)
    }
  }

  if (!brief) {
    return (
      <section className="step story-brief" data-story-brief>
        <div className="section-head"><h3>The brief</h3><span className="eyebrow law">nothing has been rendered yet</span></div>
        <div className="panel waiting-inline">
          {writing && <span className="spinner" />}
          <div>
            <strong>{writing ? storyStatusLabel(job.status) : 'Not written yet'}</strong>
            <p className="narration-line">{writing ? (rail.narration ?? 'Writing three films the material can carry.') : 'The brief is written once the map is drawn and the approaches are ranked.'}</p>
          </div>
        </div>
        <div className="actions dock"><a className="secondary" href={storyPath(job.id, 'map')}>← The map</a></div>
      </section>
    )
  }

  const recTitle = brief.options.find((o) => o.key === brief.recommendation)?.title ?? brief.recommendation
  const chosenTitle = brief.options.find((o) => o.key === chosen)?.title ?? chosen

  return (
    <section className="step story-brief" data-story-brief>
      <div className="section-head">
        <h3>The brief</h3>
        <span className="eyebrow law" data-law>nothing has been rendered yet · {brief.options.length} films · {chosen ? 'chosen' : canChoose ? 'your choice' : storyStatusLabel(job.status).toLowerCase()}</span>
      </div>
      {chosen ? (
        <p className="lede" data-chosen-line>You chose <b>{chosenTitle}</b>. The spine is built from it; the other films stay readable.</p>
      ) : (
        <p className="lede">Each card is a film, said the way a viewer will have it: what they will understand, feel and be able to do. The desk recommends <b>{recTitle}</b>{brief.why ? <> — {brief.why}</> : null}. Nothing more is spent until you choose.</p>
      )}

      <div className="tellings deliverables film-options" role="radiogroup" data-options>
        {brief.options.map((o, i) => (
          <OptionCard key={o.key} job={job} o={o} letter={String.fromCharCode(65 + i)}
                      recommended={o.key === brief.recommendation} why={brief.why}
                      chosen={chosen === o.key} disabled={!!chosen && chosen !== o.key}
                      busy={busy !== null} onChoose={canChoose ? () => choose(o.key) : undefined} />
        ))}
      </div>

      {error && <div className="error-box" title={error}>{error}</div>}

      <div className="actions dock">
        <a className="secondary" href={storyPath(job.id, 'map')}>← The map</a>
        {chosen && <a className="primary" href={storyPath(job.id, 'spine')} data-next>Next: the spine →</a>}
        {!chosen && !canChoose && <span className="hint">{storyStatusLabel(job.status)}.</span>}
      </div>
    </section>
  )
}
