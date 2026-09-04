/* The film — /s/:id/:station. Six stations (sources · reading · map · brief ·
   spine · handoff), each its own URL; the rail reflects the job's status and
   the event ledger live; under the rail the receipts line and the last
   narrated event, like the dossier console. Every line is a recorded fact. */
import { useEffect, useMemo, useState } from 'react'
import { flushSync } from 'react-dom'
import { api } from '../lib/api'
import { useEvents, useStoryJob } from '../lib/hooks'
import { buildStoryRail, storyStatusLabel } from '../lib/story'
import { usd } from '../lib/format'
import { consolePath, navigate, storyPath, type StoryStepSlug } from '../router'
import { StatusChip } from '../components/StatusChip'
import { StorySources } from '../story/StorySources'
import { StoryReading } from '../story/StoryReading'
import { StoryMap } from '../story/StoryMap'
import { StoryBrief } from '../story/StoryBrief'
import { StorySpine } from '../story/StorySpine'
import { StoryHandoff } from '../story/StoryHandoff'

const TERMINAL = new Set(['done', 'failed', 'cancelled'])

export function Story({ id, step, element }: { id: string; step: StoryStepSlug | null; element: string | null }) {
  const { job, error, setJob, reload } = useStoryJob(id)
  const live = !!job && !TERMINAL.has(job.status)
  const events = useEvents(id, live)
  const rail = useMemo(() => buildStoryRail(job, events), [job, events])
  const [busy, setBusy] = useState<'cancel' | 'resume' | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)

  useEffect(() => { document.title = job ? `${job.title} — a film — The Analyst` : 'The Analyst' }, [job])

  // A bare /s/:id lands on the station the status names (the URL stays truthful).
  useEffect(() => {
    if (step === null && job) navigate(storyPath(id, rail.best), { replace: true })
  }, [step, job, rail.best, id])

  const stepIndex = step ? rail.steps.findIndex((s) => s.station.slug === step) : -1

  const act = async (what: 'cancel' | 'resume') => {
    setBusy(what)
    setActionError(null)
    try {
      if (what === 'cancel') await api.cancelStory(id)
      else { await api.resumeStory(id); reload() }
    } catch (e) {
      setActionError(String((e as Error).message ?? e))
    } finally {
      setBusy(null)
    }
  }

  return (
    <>
      <nav className="steps story" aria-label="Stations of the film" data-story-rail>
        {rail.steps.map((s, i) => {
          const cls = `step-tab${i === stepIndex ? ' active' : s.state === 'done' ? ' done' : ''}${s.state === 'failed' ? ' failed' : ''}`
          return (
            <a key={s.station.slug} className={cls} href={storyPath(id, s.station.slug)}
               aria-current={i === stepIndex ? 'step' : undefined} data-step-tab={s.station.n} data-state={s.state}>
              <span>{s.station.n} · {s.station.label}</span><small>{s.line || ' '}</small>
            </a>
          )
        })}
        <span className="steps-divider" aria-hidden="true" />
        <a className="step-tab place" href={consolePath(id)} data-step-tab="console">
          <span>Under the hood</span><small>{job ? `${rail.calls} calls · ${usd(rail.cost)}` : ' '}</small>
        </a>
      </nav>

      {error && !job && <div className="error-box" title={error}>This film could not be loaded. {error}</div>}
      {!job && !error && <div className="waiting-inline panel"><span className="spinner" /><div><strong>Opening the film…</strong></div></div>}

      {job && (
        <div className="ledger-line" data-ledger>
          <StatusChip status={job.status} label={storyStatusLabel(job.status)} />
          <span className="machine" data-ledger-totals>{rail.calls} {rail.calls === 1 ? 'call' : 'calls'} · {usd(rail.cost)}{rail.lastEvent ? ` · event #${rail.lastEvent.seq}` : ''}</span>
          {rail.narration
            ? <p className="narration-line" aria-live="polite" data-ledger-narration>{rail.narration}</p>
            : <p className="narration-line hint">Nothing recorded yet.</p>}
          {live && job.status !== 'awaiting_brief' && (
            <button type="button" className="linkish" onClick={() => act('cancel')} disabled={busy !== null} data-cancel>stop</button>
          )}
          {(job.status === 'failed' || job.status === 'cancelled') && (
            <button type="button" className="linkish" onClick={() => act('resume')} disabled={busy !== null} data-resume>resume</button>
          )}
        </div>
      )}
      {actionError && <div className="error-box" title={actionError}>{actionError}</div>}
      {job?.error && job.status === 'failed' && <div className="error-box" data-job-error>{job.error}</div>}

      {job && step === 'sources' && <StorySources job={job} rail={rail} />}
      {job && step === 'reading' && <StoryReading job={job} events={events} rail={rail} element={element} />}
      {job && step === 'map' && <StoryMap job={job} rail={rail} />}
      {job && step === 'brief' && (
        <StoryBrief job={job} rail={rail} onChosen={(next) => {
          // The router store renders synchronously; commit the chosen job first
          // so the rail already shows the spine station running.
          flushSync(() => setJob(next))
          navigate(storyPath(id, 'spine'))
        }} />
      )}
      {job && step === 'spine' && <StorySpine job={job} rail={rail} />}
      {job && step === 'handoff' && <StoryHandoff job={job} rail={rail} />}
    </>
  )
}
