/* The story run model — the six stations of the film desk, derived the
   same way run.ts derives the dossier rail: a station is done because the
   job holds its product or the status has moved past it; running because
   the status names it; waiting because the brief is yours to choose. */
import type { RunEvent, StoryElement, StoryJob, StoryProfile, StoryStatus, StoryStep } from '../types'
import { storyRank } from '../types'
import type { StoryStepSlug } from '../router'
import type { PipState } from './run'
import { tokens, usd } from './format'

export interface StoryStation { n: number; slug: StoryStepSlug; label: string; running: StoryStatus[] }

export const STORY_RAIL: StoryStation[] = [
  { n: 1, slug: 'sources', label: 'Sources', running: ['queued'] },
  { n: 2, slug: 'reading', label: 'Reading', running: ['reading'] },
  { n: 3, slug: 'map', label: 'Map', running: ['mapping', 'ranking'] },
  { n: 4, slug: 'brief', label: 'Brief', running: ['briefing', 'awaiting_brief'] },
  { n: 5, slug: 'spine', label: 'Spine', running: ['spining'] },
  { n: 6, slug: 'handoff', label: 'Handoff', running: ['handing_off'] },
]

export const STORY_STATUS_LABEL: Record<string, string> = {
  queued: 'Queued',
  reading: 'Reading the sources',
  mapping: 'Mapping the through-lines',
  ranking: 'Ranking the approaches',
  briefing: 'Writing the brief',
  awaiting_brief: 'Brief ready — your choice',
  spining: 'Building the spine',
  handing_off: 'Writing the handoff',
  done: 'Handed off',
  failed: 'Stopped',
  cancelled: 'Cancelled',
}
export const storyStatusLabel = (s: string | null | undefined) => (s && STORY_STATUS_LABEL[s]) || s || '—'

/** the backend's step names, as the event ledger carries them in `phase` */
export const STORY_PHASE_LABEL: Record<string, string> = {
  reconnaissance: 'Reading the sources', map: 'The map', approaches: 'The approaches',
  brief: 'The brief', spine: 'The spine', handoff: 'The handoff',
}

export const STEP_TO_STATION: Record<StoryStep, StoryStepSlug> = {
  reconnaissance: 'reading', map: 'map', approaches: 'map', brief: 'brief', spine: 'spine', handoff: 'handoff',
}

export const APPROACH_LABEL: Record<string, string> = {
  helicopter_view: 'Helicopter view', one_scene_first: 'One scene first', the_case: 'The case', the_portrait: 'The portrait',
  the_timeline: 'The timeline', the_verdict: 'The verdict', open_question: 'Open question', the_numbers: 'The numbers',
  the_correction: 'The correction', the_object: 'The object', the_hindsight: 'The hindsight', the_choice: 'The choice',
}
export const approachLabel = (k: string | null | undefined) =>
  k ? (APPROACH_LABEL[k] ?? k.replace(/_/g, ' ').replace(/^./, (c) => c.toUpperCase())) : '—'

export const words = (s: string | null | undefined) => (s ?? '').replace(/_/g, ' ')

export const seconds = (n: number | null | undefined) => n ? `${n} s` : '—'

export function stationOfEvent(e: RunEvent): StoryStepSlug | null {
  if (e.phase && STEP_TO_STATION[e.phase as StoryStep]) return STEP_TO_STATION[e.phase as StoryStep]
  if (e.kind === 'job_started') return 'sources'
  if (e.kind === 'job_finished') return 'handoff'
  return null
}

/** whether the job already holds a station's product */
export function produced(job: StoryJob | null, slug: StoryStepSlug): boolean {
  if (!job) return false
  switch (slug) {
    case 'sources': return job.documents.length > 0
    case 'reading': return job.profiles.length > 0
    case 'map': return job.map !== null && job.approaches !== null
    case 'brief': return job.brief !== null
    case 'spine': return job.spine !== null
    case 'handoff': return job.handoff !== null
  }
}

/** the one-line fact under each station tab */
export function stationLine(job: StoryJob | null, slug: StoryStepSlug): string {
  if (!job) return ''
  const n = job.documents.length
  switch (slug) {
    case 'sources': return `${n} ${n === 1 ? 'source' : 'sources'} · ${tokens(job.documents.reduce((s, d) => s + (d.char_count ?? 0), 0))} chars`
    case 'reading': {
      if (job.profiles.length) return `${job.profiles.length} profiled · ${job.profiles.reduce((s, p) => s + p.elements.length, 0)} elements`
      return job.status === 'reading' ? 'reading…' : 'after the sources'
    }
    case 'map': {
      if (job.map) return `${job.map.through_lines.length} through-lines · ${job.approaches?.ranked.length ?? 0} approaches`
      return job.status === 'mapping' || job.status === 'ranking' ? storyStatusLabel(job.status).toLowerCase() : 'after reading'
    }
    case 'brief': {
      if (job.chosen_option && job.brief) return `chosen · ${job.brief.options.find((o) => o.key === job.chosen_option)?.title ?? job.chosen_option}`
      if (job.brief) return `${job.brief.options.length} films proposed · your choice`
      return job.status === 'briefing' ? 'writing…' : 'after the map'
    }
    case 'spine': {
      if (job.spine) return `${job.spine.movements.length} movements · ${seconds(job.spine.length_seconds)}`
      return job.status === 'spining' ? 'building…' : 'after the brief'
    }
    case 'handoff': {
      if (job.handoff) return `${job.handoff.ledger.length} elements · ${usd(job.totals.cost_usd)}`
      return job.status === 'handing_off' ? 'writing…' : 'after the spine'
    }
  }
}

export interface StoryRailStep {
  station: StoryStation
  state: PipState
  line: string
  narration: string | null
  cost: number
  calls: number
}
export interface StoryRailModel {
  steps: StoryRailStep[]
  activeIndex: number
  cost: number
  calls: number
  inputTokens: number
  outputTokens: number
  /** the last narrated event: the narrator's line, else the event's detail */
  narration: string | null
  lastEvent: RunEvent | null
  failed: boolean
  live: boolean
  /** the station the URL should land on when none is named */
  best: StoryStepSlug
}

const TERMINAL = new Set<string>(['done', 'failed', 'cancelled'])

export function buildStoryRail(job: StoryJob | null, events: RunEvent[]): StoryRailModel {
  const status = job?.status ?? null
  const rank = storyRank(status)
  const failed = status === 'failed' || status === 'cancelled' || events.some((e) => e.kind === 'job_failed')
  const failedStation: StoryStepSlug | null = failed && job ? (STEP_TO_STATION[job.step as StoryStep] ?? null) : null
  let activeIndex = -1
  const steps = STORY_RAIL.map((station, i): StoryRailStep => {
    const mine = events.filter((e) => stationOfEvent(e) === station.slug)
    const calls = mine.filter((e) => e.kind === 'call_finished')
    const narrationEv = [...mine].reverse().find((e) => e.narrator || e.detail)
    const isRunning = !!status && station.running.includes(status)
    const pastRank = Math.max(...station.running.map(storyRank))
    let state: PipState = 'pending'
    if (status === 'done') state = 'done'
    else if (failed && (failedStation === station.slug || (failedStation === null && isRunning))) state = 'failed'
    else if (station.slug === 'sources') state = job && job.documents.length ? 'done' : 'pending'
    else if (station.slug === 'brief') {
      if (job?.chosen_option) state = 'done'
      else if (job?.brief && status === 'awaiting_brief') state = 'waiting'
      else if (isRunning) state = 'running'
      else if (rank > pastRank) state = 'done'
    }
    else if (isRunning) state = 'running'
    else if (produced(job, station.slug) || (rank > pastRank && rank >= 0)) state = 'done'
    if (state === 'running' || state === 'waiting' || state === 'failed') activeIndex = i
    return {
      station, state, line: stationLine(job, station.slug),
      narration: narrationEv?.narrator ?? narrationEv?.detail ?? null,
      cost: calls.reduce((n, e) => n + (e.cost_usd ?? 0), 0), calls: calls.length,
    }
  })
  if (activeIndex === -1) {
    const lastDone = steps.map((s) => s.state).lastIndexOf('done')
    activeIndex = status === 'done' ? steps.length - 1 : Math.max(0, lastDone)
  }
  const allCalls = events.filter((e) => e.kind === 'call_finished')
  const lastEv = [...events].reverse().find((e) => e.narrator || e.detail) ?? null
  const evCost = allCalls.reduce((n, e) => n + (e.cost_usd ?? 0), 0)
  // where a bare /s/:id lands: the station the status names, or the furthest one produced
  let best: StoryStepSlug = 'sources'
  if (job) {
    if (status === 'done') best = 'handoff'
    else if (failed) best = failedStation ?? (STORY_RAIL.slice().reverse().find((s) => produced(job, s.slug))?.slug ?? 'sources')
    else best = STORY_RAIL.find((s) => status && s.running.includes(status))?.slug ?? 'sources'
  }
  return {
    steps, activeIndex,
    cost: Math.max(evCost, job?.totals?.cost_usd ?? 0),
    calls: Math.max(allCalls.length, job?.totals?.calls ?? 0),
    inputTokens: Math.max(allCalls.reduce((n, e) => n + (e.input_tokens ?? 0), 0), job?.totals?.input_tokens ?? 0),
    outputTokens: Math.max(allCalls.reduce((n, e) => n + (e.output_tokens ?? 0), 0), job?.totals?.output_tokens ?? 0),
    narration: lastEv?.narrator ?? lastEv?.detail ?? null,
    lastEvent: lastEv,
    failed,
    live: !!status && !TERMINAL.has(status),
    best,
  }
}

/* ---------- lookups the pages share */

export interface ElementRef { el: StoryElement; profile: StoryProfile }

export function elementIndex(job: StoryJob): Map<string, ElementRef> {
  const m = new Map<string, ElementRef>()
  for (const p of job.profiles) for (const el of p.elements) m.set(el.id, { el, profile: p })
  return m
}

export function docTitle(job: StoryJob, key: string): string {
  return job.documents.find((d) => d.key === key)?.title || job.profiles.find((p) => p.doc_key === key)?.title || key
}

export function docMeta(job: StoryJob, key: string): string {
  const d = job.documents.find((x) => x.key === key)
  if (!d) return key
  return [d.creators, d.year, d.publication].filter(Boolean).join(' · ') || key
}

/** a short handle for a source in chips and on the current: "Wijaya 2025" or the key */
export function docHandle(job: StoryJob, key: string): string {
  const d = job.documents.find((x) => x.key === key)
  if (!d) return key
  const surname = (d.creators ?? '').split(/[;,]/)[0]?.trim()
  return surname ? `${surname}${d.year ? ` ${d.year}` : ''}` : (d.title.length > 28 ? `${d.title.slice(0, 26)}…` : d.title)
}

export function countByKind(elements: StoryElement[]): { kind: string; n: number }[] {
  const m = new Map<string, number>()
  for (const el of elements) m.set(el.kind, (m.get(el.kind) ?? 0) + 1)
  return [...m.entries()].map(([kind, n]) => ({ kind, n })).sort((a, b) => b.n - a.n)
}
