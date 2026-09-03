/* Mock mode — replays one realistic dossier job (the Kering study) from
   fixtures in web/mock/. Stage A (reading + brief) runs on creation; stage B
   (plan → analysis → tables → figures → compose) runs after the brief is
   chosen. Time is real: a fresh job takes ~8 s to reach the brief and ~46 s
   to deliver (VITE_MOCK_SPEED scales it). Created jobs persist in
   sessionStorage so a reload re-attaches, like the real server. */
import type {
  Brief, CreateJobRequest, DossierFigure, DossierJob, DossierStatus, Exemplar,
  ExecutorJob, JobListEntry, OrchestratorPlan, Receipt, RunEvent, SourceSpec,
  DossierOptions, Totals,
} from '../types'
import { statusRank } from '../types'
import type { Api } from './api'
import exemplarsJson from '../../mock/exemplars.json'
import profilesJson from '../../mock/profiles.json'
import briefJson from '../../mock/brief.json'
import tablesJson from '../../mock/tables.json'
import sectionsJson from '../../mock/sections.json'
import receiptsJson from '../../mock/receipts.json'
import planJson from '../../mock/plan.json'
import jobsJson from '../../mock/jobs.json'
import eventsJson from '../../mock/events.json'
import dossierHtmlRaw from '../../mock/dossier.html?raw'
import fig1Url from '../../mock/figures/fig-1.svg'
import fig2Url from '../../mock/figures/fig-2.svg'

type Mirror = { phase: string; phase_number: number; kind?: string }
type ScriptEvent = Partial<RunEvent> & { stage: 'A' | 'B'; at_ms: number; mirror?: Mirror }

const SCRIPT = eventsJson as ScriptEvent[]
const A = SCRIPT.filter((e) => e.stage === 'A')
const B = SCRIPT.filter((e) => e.stage === 'B')
const A_END = Math.max(...A.map((e) => e.at_ms))
const SPEED = Number(import.meta.env.VITE_MOCK_SPEED ?? '1') || 1
const BRIEF = briefJson as Brief
const PLAN = planJson as unknown as OrchestratorPlan
const FIGURES: DossierFigure[] = [
  { key: 'f1', caption: 'The three fields and the fourth', figure_id: 'fig-8a21c0', url: fig1Url, provider: 'gemini-3-pro-image', cost_usd: 0.12 },
  { key: 'f2', caption: 'One reset read against five levels — store network 600 → 450', figure_id: 'fig-3d9b7e', url: fig2Url, provider: 'gemini-3-pro-image', cost_usd: 0.12 },
]

interface Run {
  id: string
  title: string
  sources: SourceSpec[]
  options: DossierOptions
  created: number       // epoch ms
  aStart: number
  bStart: number | null
  chosen: string | null
  timeScale: number     // 1 = live wall-clock; seeded runs stretch to real durations
  failAt?: number       // script ms in stage B after which the run fails
}

const STORE_KEY = 'analyst.mock.runs'
const runs = new Map<string, Run>()

function seed() {
  const now = new Date()
  for (const j of jobsJson) {
    const d = new Date(now)
    d.setDate(d.getDate() - j.days_ago)
    d.setHours(j.hour, j.minute, 0, 0)
    const created = d.getTime()
    const done = j.outcome === 'done' || j.outcome === 'failed'
    runs.set(j.id, {
      id: j.id, title: j.title, sources: j.sources as SourceSpec[],
      options: { audience: 'executive', depth: 'medium', output: { text: true, tables: true, figures: 2, video: false }, autopilot: false },
      created, aStart: created, bStart: done ? created + 90_000 : null,
      chosen: j.chosen, timeScale: 14,
      failAt: j.outcome === 'failed' ? 13_000 : undefined,
    })
  }
  try {
    const raw = sessionStorage.getItem(STORE_KEY)
    if (raw) for (const r of JSON.parse(raw) as Run[]) runs.set(r.id, r)
  } catch { /* storage denied: in-memory only */ }
}
seed()

function persist() {
  try {
    const own = [...runs.values()].filter((r) => r.timeScale === 1)
    sessionStorage.setItem(STORE_KEY, JSON.stringify(own))
  } catch { /* ignore */ }
}

const wall = (start: number, atMs: number, scale: number) => start + (atMs * scale) / SPEED
const scriptNow = (start: number, scale: number) => ((Date.now() - start) * SPEED) / scale

/** Lazy state transitions that happen without a request (autopilot). */
function tick(run: Run) {
  if (run.bStart === null && run.options.autopilot && scriptNow(run.aStart, run.timeScale) >= A_END) {
    run.chosen = BRIEF.defaults?.option_key ?? BRIEF.options[0].key
    run.bStart = wall(run.aStart, A_END, run.timeScale)
    persist()
  }
}

function toEvent(run: Run, s: ScriptEvent, seq: number, start: number): RunEvent {
  const { stage: _stage, at_ms, mirror: _mirror, ...rest } = s
  return {
    ...rest,
    job_id: run.id, seq, kind: s.kind ?? 'note',
    ts: new Date(wall(start, at_ms, run.timeScale)).toISOString(),
  }
}

/** Every event that has happened for this run, in seq order. */
function happened(run: Run): RunEvent[] {
  tick(run)
  const out: RunEvent[] = []
  const tA = scriptNow(run.aStart, run.timeScale)
  let seq = 0
  for (const s of A) if (s.at_ms <= tA) out.push(toEvent(run, s, ++seq, run.aStart))
  if (run.bStart !== null && tA >= A_END) {
    const tB = scriptNow(run.bStart, run.timeScale)
    const limit = run.failAt !== undefined ? Math.min(tB, run.failAt) : tB
    for (const s of B) if (s.at_ms <= limit) out.push(toEvent(run, s, ++seq, run.bStart))
    if (run.failAt !== undefined && tB >= run.failAt) {
      const ts = new Date(wall(run.bStart, run.failAt + 400, run.timeScale)).toISOString()
      out.push({ job_id: run.id, seq: ++seq, ts, kind: 'call_failed', phase: 'analysis',
        chain: 'argument_and_framework', engine: 'argument_architecture', pass_name: 'pass 2',
        model: 'claude-sonnet-4-6', detail: 'context_length_exceeded after 3 retries', duration_ms: 182_000 })
      out.push({ job_id: run.id, seq: ++seq, ts, kind: 'job_failed', phase: 'analysis',
        detail: 'Stopped in phase 1: argument_architecture pass 2 refused three times.',
        narrator: 'Stopped. The argument pass would not fit the model window three times running; nothing after it was spent.' })
    }
  }
  return out
}

function deriveStatus(run: Run, ev: RunEvent[]): DossierStatus {
  let status: DossierStatus = 'queued'
  for (const e of ev) {
    if (e.kind === 'phase_started' && e.phase) status = e.phase as DossierStatus
    if (e.kind === 'job_finished') status = 'done'
    if (e.kind === 'job_failed') status = 'failed'
  }
  if (status === 'awaiting_brief' && run.bStart !== null && ev.some((e) => e.kind === 'phase_finished' && e.phase === 'awaiting_brief')) {
    status = 'planning'
  }
  return status
}

function totalsOf(ev: RunEvent[]): Totals {
  const calls = ev.filter((e) => e.kind === 'call_finished')
  const first = ev[0]?.ts, last = ev[ev.length - 1]?.ts
  return {
    calls: calls.length,
    input_tokens: calls.reduce((n, e) => n + (e.input_tokens ?? 0), 0),
    output_tokens: calls.reduce((n, e) => n + (e.output_tokens ?? 0), 0),
    cost_usd: Number(calls.reduce((n, e) => n + (e.cost_usd ?? 0), 0).toFixed(4)),
    duration_ms: first && last ? Date.parse(last) - Date.parse(first) : 0,
  }
}

const stepOf = (s: DossierStatus, ev: RunEvent[]) => {
  if (s === 'done') return 4
  // A stopped run keeps the step it stopped in — the last phase it entered.
  const at = s === 'failed'
    ? ([...ev].reverse().find((e) => e.kind === 'phase_started')?.phase as DossierStatus | undefined) ?? 'reconnaissance'
    : s
  return statusRank(at) >= statusRank('planning') ? 3 : at === 'awaiting_brief' ? 2 : 1
}

function snapshot(run: Run): DossierJob {
  const ev = happened(run)
  const status = deriveStatus(run, ev)
  const rank = statusRank(status)
  const finished = (phase: string) => ev.some((e) => e.kind === 'phase_finished' && e.phase === phase)
  const artifacts = ev.filter((e) => e.kind === 'artifact').map((e) => {
    try { return JSON.parse(e.payload_json ?? '{}') as Record<string, string> } catch { return {} }
  })
  const tableKeys = new Set(artifacts.map((a) => a.table_key).filter(Boolean))
  const figureKeys = new Set(artifacts.map((a) => a.figure_key).filter(Boolean))
  const analysisCalls = ev.filter((e) => e.kind === 'call_finished' && e.phase === 'analysis')
  const analysis: Record<string, string> = {}
  if (finished('analysis')) {
    for (const ph of PLAN.phases) {
      const prose = analysisCalls
        .filter((e) => ph.execution?.engines?.some((x) => x.engine_key === e.engine))
        .map((e) => `### ${e.engine} · ${e.pass_name}\n\n${e.output_excerpt ?? ''}`).join('\n\n')
      analysis[ph.phase_name] = prose
    }
  }
  const nCalls = ev.filter((e) => e.kind === 'call_finished').length
  const done = status === 'done'
  return {
    id: run.id, status, step: stepOf(status, ev),
    created_at: new Date(run.created).toISOString(), title: run.title,
    sources: run.sources, options: run.options,
    profiles: finished('reconnaissance') ? (profilesJson as DossierJob['profiles']) : [],
    brief: finished('awaiting_brief') ? BRIEF : null,
    chosen_option: run.chosen,
    plan_id: finished('planning') ? PLAN.plan_id : null,
    analysis_job_id: rank >= statusRank('analysis') ? `exec-${run.id}` : null,
    analysis,
    tables: (tablesJson as DossierJob['tables']).filter((t) => tableKeys.has(t.key)),
    figures: FIGURES.filter((f) => figureKeys.has(f.key)),
    sections: done ? (sectionsJson as DossierJob['sections']) : [],
    receipts: (receiptsJson as Receipt[]).slice(0, nCalls),
    totals: totalsOf(ev),
    paths: done ? { html: `/v1/dossier/jobs/${run.id}/dossier.html`, pdf: `/v1/dossier/jobs/${run.id}/dossier.pdf`, md: `/v1/dossier/jobs/${run.id}/dossier.md` } : {},
    error: status === 'failed' ? (ev.find((e) => e.kind === 'job_failed')?.detail ?? 'Stopped') : null,
    console_url: `/console/${run.id}`,
  }
}

function mirrored(run: Run): RunEvent[] {
  const ev = happened(run)
  const idx = new Map(SCRIPT.map((s, i) => [`${s.stage}:${s.at_ms}:${s.kind}`, i]))
  const out: RunEvent[] = []
  let seq = 0
  for (const e of ev) {
    if (e.kind === 'call_failed' || e.kind === 'job_failed') { out.push({ ...e, job_id: `exec-${run.id}`, seq: ++seq, phase: 'Map the argument and the framework' }); continue }
    const key = [...idx.keys()].find((k) => k.startsWith('B:') && k.endsWith(`:${e.kind}`) && e.phase === 'analysis' && SCRIPT[idx.get(k)!].at_ms === Math.round(((Date.parse(e.ts) - (run.bStart ?? 0)) * SPEED) / run.timeScale))
    const s = key !== undefined ? SCRIPT[idx.get(key)!] : undefined
    if (!s?.mirror) continue
    out.push({ ...e, job_id: `exec-${run.id}`, seq: ++seq, phase: s.mirror.phase,
      kind: (s.mirror.kind as RunEvent['kind']) ?? e.kind })
  }
  return out
}

function runOf(id: string): Run {
  const run = runs.get(id)
  if (!run) throw Object.assign(new Error(`404 /v1/dossier/jobs/${id} — no such dossier`), { status: 404 })
  return run
}

const delay = <T,>(v: T, ms = 120) => new Promise<T>((res) => setTimeout(() => res(v), ms))

function md(job: DossierJob): string {
  return `# ${job.title}\n\n${job.sections.map((s) => `## ${s.title}\n\n${s.md ?? ''}`).join('\n\n')}\n`
}

export const mockApi: Api = {
  exemplars: () => delay(exemplarsJson as Exemplar[]),
  listJobs: () => delay([...runs.values()]
    .sort((a, b) => b.created - a.created)
    .map((r): JobListEntry => {
      const s = snapshot(r)
      return { id: s.id, status: s.status, step: s.step, created_at: s.created_at, title: s.title, totals: s.totals }
    })),
  createJob: (req: CreateJobRequest) => {
    const id = `dj-${Date.now().toString(36)}`
    const first = req.sources[0]
    const title = first?.kind === 'paste' ? (first.title || first.text.slice(0, 60).replace(/\s+/g, ' ').trim() || 'Untitled dossier')
      : first?.kind === 'exemplar' ? (exemplarsJson.find((e) => e.key === first.key)?.title ?? first.key)
      : 'Untitled dossier'
    const now = Date.now()
    const { sources, ...options } = req
    runs.set(id, { id, title, sources, options, created: now, aStart: now, bStart: null, chosen: null, timeScale: 1 })
    persist()
    return delay({ job_id: id, status: 'reconnaissance' as DossierStatus, console_url: `/console/${id}` }, 300)
  },
  getJob: (id) => delay(snapshot(runOf(id))),
  getBrief: (id) => delay(snapshot(runOf(id)).brief ?? { options: [] }),
  chooseBrief: (id, option_key, overrides) => {
    const run = runOf(id)
    run.chosen = option_key
    run.bStart = Date.now()
    if (overrides) {
      const o = overrides as Partial<DossierOptions> & { figures?: number }
      run.options = { ...run.options, ...(o.audience ? { audience: o.audience } : {}), ...(o.depth ? { depth: o.depth } : {}),
        output: { ...(run.options.output ?? { text: true, tables: true, figures: 2, video: false }),
          ...(o.figures !== undefined ? { figures: o.figures } : {}) } }
    }
    persist()
    return delay(snapshot(run), 250)
  },
  getReceipts: (id) => delay(snapshot(runOf(id)).receipts),
  getDossierHtml: (id) => {
    const job = snapshot(runOf(id))
    return delay(dossierHtmlRaw.replace('__FIG1__', fig1Url).replace('__FIG2__', fig2Url)
      .replace('Kering study + the fourth field — dossier', `${job.title} — dossier`)
      .replace('<h1>Kering study + the fourth field</h1>', `<h1>${job.title}</h1>`))
  },
  downloadUrl: (job, kind) => {
    if (kind === 'md') return `data:text/markdown;charset=utf-8,${encodeURIComponent(md(job))}`
    const html = dossierHtmlRaw.replace('__FIG1__', fig1Url).replace('__FIG2__', fig2Url)
    return `data:text/html;charset=utf-8,${encodeURIComponent(html)}`
  },
  events: (jobId, afterSeq) => {
    const ev = jobId.startsWith('exec-') ? mirrored(runOf(jobId.slice(5))) : happened(runOf(jobId))
    return delay(ev.filter((e) => e.seq > afterSeq), 60)
  },
  watchEvents: (jobId, afterSeq, onEvent, onEnd) => {
    let last = afterSeq
    let stopped = false
    const timer = window.setInterval(() => {
      if (stopped) return
      void mockApi.events(jobId, last).then((batch) => {
        for (const e of batch) {
          if (stopped) return
          last = e.seq
          onEvent(e)
          if (e.kind === 'job_finished' || e.kind === 'job_failed') {
            stopped = true
            window.clearInterval(timer)
            onEnd?.()
          }
        }
      })
    }, 350)
    return () => { stopped = true; window.clearInterval(timer) }
  },
  executorJob: (id) => {
    const run = runOf(id.startsWith('exec-') ? id.slice(5) : id)
    const ev = mirrored(run)
    const statuses: Record<string, string> = {}
    let current = 0
    let phaseName = ''
    for (const e of ev) {
      const n = PLAN.phases.find((p) => p.phase_name === e.phase)?.phase_number
      if (n === undefined) continue
      if (e.kind === 'phase_started') { statuses[String(n)] = 'running'; current = n; phaseName = e.phase ?? '' }
      if (e.kind === 'phase_finished') statuses[String(n)] = 'completed'
      if (e.kind === 'job_failed') statuses[String(n)] = 'failed'
    }
    const failed = ev.some((e) => e.kind === 'job_failed')
    const allDone = PLAN.phases.every((p) => statuses[String(p.phase_number)] === 'completed')
    const t = totalsOf(ev)
    const job: ExecutorJob = {
      job_id: `exec-${run.id}`, plan_id: PLAN.plan_id,
      status: failed ? 'failed' : allDone ? 'completed' : ev.length ? 'running' : 'pending',
      workflow_key: 'dossier_standard', created_at: new Date(run.bStart ?? run.created).toISOString(),
      progress: { current_phase: current, total_phases: PLAN.phases.length, phase_name: phaseName,
        detail: ev[ev.length - 1]?.detail ?? '', phase_statuses: statuses },
      total_llm_calls: t.calls, total_input_tokens: t.input_tokens, total_output_tokens: t.output_tokens,
      total_cost_estimate: t.cost_usd, error: failed ? 'argument_architecture pass 2: context_length_exceeded' : null,
    }
    return delay(job)
  },
  plan: () => delay(PLAN),
  pipelineVisualization: () => delay(PLAN as unknown as { phases: OrchestratorPlan['phases'] }),
}
