/* The shell: masthead, the four numbered steps + the "under the hood" place
   tab, and the page the URL names. Lifted from Wirecut's App.tsx and
   restyled to the house. */
import { useEffect } from 'react'
import { flushSync } from 'react-dom'
import { api, MOCK } from './lib/api'
import { useEvents, useJob } from './lib/hooks'
import { Library } from './pages/Library'
import { Console } from './pages/Console'
import { Plates } from './pages/Plates'
import { Story } from './pages/Story'
import { SourcesStep } from './steps/SourcesStep'
import { BriefStep } from './steps/BriefStep'
import { DraftStep } from './steps/DraftStep'
import { DossierStep } from './steps/DossierStep'
import { consolePath, dossierPath, isStoryId, libraryPath, navigate, STEP_SLUGS, storyHome, useRoute, type StepSlug } from './router'
import { statusLabel, usd } from './lib/format'
import { statusRank, type DossierJob } from './types'

const MASTER_URL = (import.meta.env.VITE_MASTER_URL as string | undefined) || 'https://analyzer-mgmt-frontend.onrender.com'

const STEP_LABELS = ['1 · Your documents', '2 · The brief', '3 · The draft', '4 · Your dossier']

function stepLine(job: DossierJob | null, i: number): string {
  if (!job) return ''
  switch (i) {
    case 0: return job.profiles.length ? `${job.sources.length} ${job.sources.length === 1 ? 'source' : 'sources'} · ${job.profiles.length} profiled` : `${job.sources.length} ${job.sources.length === 1 ? 'source' : 'sources'}`
    case 1: {
      if (job.chosen_option && job.brief) return `chosen · ${job.brief.options.find((o) => o.key === job.chosen_option)?.title ?? job.chosen_option}`
      if (job.brief) return `${job.brief.options.length} deliverables · ${job.brief.entry === 'material' ? 'the material decided' : 'your choice'}`
      return 'after reading'
    }
    case 2: {
      if (job.status === 'done') return `${job.sections.length} sections · ${job.tables.length} tables · ${job.figures.length} figures`
      if (statusRank(job.status) >= statusRank('planning') || job.status === 'failed') return statusLabel(job.status).toLowerCase()
      return 'after the brief'
    }
    case 3: return job.status === 'done' ? `${usd(job.totals.cost_usd)} · pdf · md · html` : 'after the draft'
  }
  return ''
}

function stepAllowed(job: DossierJob | null, i: number): boolean {
  if (!job) return i === 0
  const r = statusRank(job.status)
  if (i === 0) return true
  if (i === 1) return r >= statusRank('awaiting_brief') || job.chosen_option !== null
  if (i === 2) return job.chosen_option !== null || r >= statusRank('planning') || job.status === 'failed'
  return job.status === 'done'
}

export default function App() {
  const route = useRoute()
  const jobId = route.kind === 'dossier' ? route.id : null
  const { job, error, setJob } = useJob(jobId)
  const live = !!job && job.status !== 'done' && job.status !== 'failed'
  const events = useEvents(jobId, live)

  useEffect(() => { document.title = job ? `${job.title} — The Analyst` : 'The Analyst' }, [job])

  const stepIndex = route.kind === 'dossier' ? STEP_SLUGS.indexOf(route.step) : -1
  const stepHref = (i: number): string | null =>
    route.kind === 'dossier' && stepAllowed(job, i) ? dossierPath(route.id, STEP_SLUGS[i] as StepSlug) : null

  // Landing normalisation: a step the job has not reached yet falls back to
  // the furthest step it has (the URL stays truthful).
  useEffect(() => {
    if (route.kind !== 'dossier' || !job) return
    if (!stepAllowed(job, stepIndex)) {
      const best = [3, 2, 1, 0].find((i) => stepAllowed(job, i)) ?? 0
      navigate(dossierPath(route.id, STEP_SLUGS[best] as StepSlug), { replace: true })
    }
  }, [route, job, stepIndex])

  const doneIndex = job ? (job.status === 'done' ? 4 : job.chosen_option ? 2 : job.brief ? 1 : 0) : 0
  // the story desk: its own routes, and the console of a story job
  const filmRoute = route.kind === 'story' || (route.kind === 'console' && isStoryId(route.id)) || (route.kind === 'library' && route.desk === 'film')

  return (
    <div className="shell">
      <header className="masthead">
        <div className="masthead-eyebrow">
          <span className="eyebrow">The Analyst · <b>{filmRoute ? 'story desk' : 'document desk'}</b></span>
          <span className="eyebrow masthead-right">
            {MOCK && <span className="chip chip-flat" title={`Fixture replay — no server. Remove ?mock=1 (or set analyst.mock=0) to use ${api ? 'the API' : ''}`}>mock</span>}
            <a href={libraryPath(filmRoute ? 'film' : 'dossier')} className={route.kind === 'library' ? 'on' : ''}>Library</a>
            {route.kind === 'dossier' && <a href={consolePath(route.id)}>Under the hood</a>}
            {route.kind === 'story' && <a href={consolePath(route.id)}>Under the hood</a>}
            {route.kind === 'console' && (isStoryId(route.id) ? <a href={storyHome(route.id)}>The film</a> : <a href={dossierPath(route.id, 'draft')}>The dossier</a>)}
            {route.kind === 'plates' && <a href={dossierPath(route.id, 'dossier')}>The dossier</a>}
            {route.kind === 'plates' && <a href={consolePath(route.id)}>Under the hood</a>}
            <a href={filmRoute ? `${MASTER_URL}/engines/wirecut_spine` : `${MASTER_URL}/processes/dossier_standard`} target="_blank" rel="noreferrer" title="The Master: the registry of every engine, process and grammar this desk draws on">The method ↗</a>
          </span>
        </div>
        <div className="masthead-title">
          <h1><a href="/">The Analyst</a></h1>
          {filmRoute
            ? <p className="thesis">Many sources in. One film plan out — <em>for Wirecut</em> — with every step on the record.</p>
            : <p className="thesis">Documents in. A dossier out — <em>text, tables, figures</em> — with every step on the record.</p>}
        </div>
      </header>

      {route.kind === 'dossier' && (
        <nav className="steps" aria-label="Steps">
          {STEP_LABELS.map((label, i) => {
            const href = stepHref(i)
            const cls = `step-tab${i === stepIndex ? ' active' : i < doneIndex ? ' done' : ''}`
            const line = stepLine(job, i)
            const inner = <><span>{label}</span><small>{line || ' '}</small></>
            return href ? (
              <a key={label} className={cls} href={href} aria-current={i === stepIndex ? 'step' : undefined} data-step-tab={i + 1}>{inner}</a>
            ) : (
              <div key={label} className={`${cls} inert`} aria-current={i === stepIndex ? 'step' : undefined} data-step-tab={i + 1}>{inner}</div>
            )
          })}
          <span className="steps-divider" aria-hidden="true" />
          <a className="step-tab place" href={consolePath(route.id)} data-step-tab="console">
            <span>Under the hood</span><small>{job ? `${Math.max(job.totals.calls, events.filter((e) => e.kind === 'call_finished').length)} calls · ${usd(job.totals.cost_usd)}` : ' '}</small>
          </a>
        </nav>
      )}

      {route.kind === 'library' && <Library desk={route.desk} />}
      {route.kind === 'story' && <Story id={route.id} step={route.step} element={route.element} />}

      {route.kind === 'dossier' && error && !job && (
        <div className="error-box" title={error}>This dossier could not be loaded. {error}</div>
      )}
      {route.kind === 'dossier' && !job && !error && <div className="waiting-inline panel"><span className="spinner" /><div><strong>Opening the dossier…</strong></div></div>}
      {route.kind === 'dossier' && job && (
        <>
          {route.step === 'sources' && (
            <SourcesStep job={job} events={events} onNext={() => navigate(dossierPath(job.id, 'brief'))} />
          )}
          {route.step === 'brief' && (
            <BriefStep job={job} onBack={() => navigate(dossierPath(job.id, 'sources'))}
                       onChosen={(j) => {
                         // The router store renders synchronously; commit the
                         // chosen job first so the landing check sees it.
                         flushSync(() => setJob(j))
                         navigate(dossierPath(j.id, 'draft'))
                       }} />
          )}
          {route.step === 'draft' && (
            <DraftStep job={job} events={events} item={route.item} onNext={() => navigate(dossierPath(job.id, 'dossier'))} />
          )}
          {route.step === 'dossier' && <DossierStep job={job} />}
        </>
      )}

      {route.kind === 'console' && <Console id={route.id} node={route.node} exec={route.exec} />}
      {route.kind === 'plates' && <Plates id={route.id} />}

      <footer className="foot">
        <span className="eyebrow">every visible fact is a recorded one · {MOCK ? 'fixture replay' : 'live api'}</span>
        <span className="eyebrow">a sibling of Wirecut</span>
      </footer>
    </div>
  )
}
