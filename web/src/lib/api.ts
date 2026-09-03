/* The Analyst — API client. One base URL, fetch + EventSource. Mock mode
   (VITE_MOCK=1 at build time, or ?mock=1 / localStorage analyst.mock=1 at
   run time) swaps every call for the fixture replay in ./mock.ts. */
import type {
  Brief, CreateJobRequest, CreateJobResponse, DossierJob, Exemplar,
  ExecutorJob, JobListEntry, OrchestratorPlan, Receipt, RunEvent,
} from '../types'

export const API_BASE: string = (import.meta.env.VITE_API_BASE
  ?? 'https://the-analyst-kcuc.onrender.com').replace(/\/$/, '')

function runtimeMock(): boolean {
  try {
    const q = new URLSearchParams(window.location.search)
    if (q.get('mock') === '1') { localStorage.setItem('analyst.mock', '1'); return true }
    if (q.get('mock') === '0') { localStorage.removeItem('analyst.mock'); return false }
    return localStorage.getItem('analyst.mock') === '1'
  } catch { return false }
}

export const MOCK: boolean = import.meta.env.VITE_MOCK === '1' || runtimeMock()

export class ApiError extends Error {
  status: number
  body: string
  constructor(status: number, body: string, url: string) {
    super(`${status} ${url}${body ? ` — ${body.slice(0, 200)}` : ''}`)
    this.status = status
    this.body = body
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`
  const res = await fetch(url, {
    ...init,
    headers: { Accept: 'application/json', ...(init?.body ? { 'Content-Type': 'application/json' } : {}),
               ...(init?.headers ?? {}) },
  })
  if (!res.ok) throw new ApiError(res.status, await res.text().catch(() => ''), path)
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

/* The backend wraps lists ({jobs:[…]}, {exemplars:[…]}, {receipts:[…]}) and
   leaves not-yet-produced job fields null; normalize here so pages can
   assume arrays. */
function unwrap<T>(d: unknown, key: string): T[] {
  if (Array.isArray(d)) return d as T[]
  const v = (d as Record<string, unknown> | null)?.[key]
  return Array.isArray(v) ? (v as T[]) : []
}
function normalizeJob(j: DossierJob): DossierJob {
  const anyJ = j as unknown as Record<string, unknown>
  for (const k of ['profiles', 'sections', 'tables', 'figures', 'receipts', 'notes', 'documents', 'sources']) {
    if (!Array.isArray(anyJ[k])) anyJ[k] = []
  }
  const t = (anyJ.totals ?? {}) as Record<string, unknown>
  if (typeof t.calls !== 'number') {
    t.calls = (Number(t.llm_calls ?? 0) || 0) + (Number(t.image_calls ?? 0) || 0)
  }
  if (typeof t.cost_usd !== 'number') t.cost_usd = Number(t.cost_usd ?? 0) || 0
  anyJ.totals = t
  if (!anyJ.paths || typeof anyJ.paths !== 'object') anyJ.paths = {}
  return anyJ as unknown as DossierJob
}

async function requestText(path: string): Promise<string> {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new ApiError(res.status, await res.text().catch(() => ''), path)
  return res.text()
}

export interface Api {
  exemplars(): Promise<Exemplar[]>
  listJobs(): Promise<JobListEntry[]>
  createJob(req: CreateJobRequest): Promise<CreateJobResponse>
  getJob(id: string): Promise<DossierJob>
  getBrief(id: string): Promise<Brief>
  chooseBrief(id: string, option_key: string, overrides?: Record<string, unknown>): Promise<DossierJob>
  getReceipts(id: string): Promise<Receipt[]>
  getDossierHtml(id: string): Promise<string>
  /** absolute URL for a download (pdf|md|html) */
  downloadUrl(job: DossierJob, kind: 'html' | 'pdf' | 'md'): string
  events(jobId: string, afterSeq: number): Promise<RunEvent[]>
  /** live watcher: SSE with poll fallback; returns unsubscribe */
  watchEvents(jobId: string, afterSeq: number, onEvent: (e: RunEvent) => void,
              onEnd?: () => void): () => void
  executorJob(id: string): Promise<ExecutorJob>
  plan(planId: string): Promise<OrchestratorPlan>
  pipelineVisualization(planId: string): Promise<{ phases: OrchestratorPlan['phases'] } & Record<string, unknown>>
}

const live: Api = {
  exemplars: () => request<unknown>('/v1/dossier/exemplars').then((d) => unwrap<Exemplar>(d, 'exemplars')),
  listJobs: () => request<unknown>('/v1/dossier/jobs').then((d) =>
    unwrap<JobListEntry>(d, 'jobs').map((e) => {
      const anyE = e as unknown as Record<string, unknown>
      if (!anyE.totals || typeof anyE.totals !== 'object') {
        anyE.totals = { cost_usd: Number(anyE.cost_usd ?? 0) || 0, calls: Number(anyE.calls ?? 0) || 0 }
      }
      return anyE as unknown as JobListEntry
    })),
  createJob: (req) => request<CreateJobResponse>('/v1/dossier/jobs',
    { method: 'POST', body: JSON.stringify(req) }),
  getJob: (id) => request<DossierJob>(`/v1/dossier/jobs/${id}`).then(normalizeJob),
  getBrief: (id) => request<Brief>(`/v1/dossier/jobs/${id}/brief`),
  chooseBrief: (id, option_key, overrides) => request<DossierJob>(
    `/v1/dossier/jobs/${id}/brief`,
    { method: 'POST', body: JSON.stringify({ option_key, overrides: overrides ?? {} }) }).then(normalizeJob),
  getReceipts: (id) => request<unknown>(`/v1/dossier/jobs/${id}/receipts`).then((d) => unwrap<Receipt>(d, 'receipts')),
  getDossierHtml: (id) => requestText(`/v1/dossier/jobs/${id}/dossier.html`),
  downloadUrl: (job, kind) => {
    const p = job.paths?.[kind]
    if (p && /^https?:/.test(p)) return p
    if (p && p.startsWith('/')) return `${API_BASE}${p}`
    return `${API_BASE}/v1/dossier/jobs/${job.id}/dossier.${kind}`
  },
  events: (jobId, afterSeq) => request<unknown>(`/v1/events/${jobId}?after=${afterSeq}`).then((d) => unwrap<RunEvent>(d, 'events')),
  watchEvents: (jobId, afterSeq, onEvent, onEnd) =>
    watchSse(`${API_BASE}/v1/events/${jobId}/stream?after=${afterSeq}`,
             (after) => live.events(jobId, after), afterSeq, onEvent, onEnd),
  executorJob: (id) => request<ExecutorJob>(`/v1/executor/jobs/${id}`),
  plan: (planId) => request<OrchestratorPlan>(`/v1/orchestrator/plans/${planId}`),
  pipelineVisualization: (planId) => request(`/v1/orchestrator/plans/${planId}/pipeline-visualization`),
}

/* SSE with poll fallback (Wirecut's watchOperation pattern): the server
   closes only after a terminal event, so an error mid-run means the
   connection died — poll /v1/events?after= to completion. */
export function watchSse(
  streamUrl: string,
  poll: (afterSeq: number) => Promise<RunEvent[]>,
  afterSeq: number,
  onEvent: (e: RunEvent) => void,
  onEnd?: () => void,
): () => void {
  let closed = false
  let last = afterSeq
  let timer: number | undefined
  let source: EventSource | null = null
  const finish = () => {
    if (closed) return
    closed = true
    source?.close()
    if (timer !== undefined) window.clearInterval(timer)
    onEnd?.()
  }
  const deliver = (e: RunEvent) => {
    if (closed || e.seq <= last) return
    last = e.seq
    onEvent(e)
    if (e.kind === 'job_finished' || e.kind === 'job_failed') finish()
  }
  const startPolling = () => {
    if (timer !== undefined || closed) return
    timer = window.setInterval(() => {
      void poll(last).then((batch) => { for (const e of batch) deliver(e) })
        .catch(() => { /* transient — keep polling */ })
    }, 2500)
  }
  try {
    source = new EventSource(streamUrl)
    const handle = (msg: MessageEvent) => {
      try { deliver(JSON.parse(msg.data) as RunEvent) } catch { /* ignore */ }
    }
    source.addEventListener('run_event', handle as EventListener)
    source.onmessage = handle
    source.onerror = () => {
      if (closed) return
      source?.close()
      startPolling()
    }
  } catch {
    startPolling()
  }
  return () => { closed = true; source?.close(); if (timer !== undefined) window.clearInterval(timer) }
}

let impl: Api | null = null
let loading: Promise<Api> | null = null

/** Resolve the API implementation (mock module is code-split). */
export function getApi(): Promise<Api> {
  if (impl) return Promise.resolve(impl)
  if (!loading) {
    loading = MOCK
      ? import('./mock').then((m) => { impl = m.mockApi; return impl })
      : Promise.resolve((impl = live))
  }
  return loading
}

/* Convenience: every call goes through getApi() so mock/live is one seam. */
export const api: Api = {
  exemplars: () => getApi().then((a) => a.exemplars()),
  listJobs: () => getApi().then((a) => a.listJobs()),
  createJob: (r) => getApi().then((a) => a.createJob(r)),
  getJob: (id) => getApi().then((a) => a.getJob(id)),
  getBrief: (id) => getApi().then((a) => a.getBrief(id)),
  chooseBrief: (id, k, o) => getApi().then((a) => a.chooseBrief(id, k, o)),
  getReceipts: (id) => getApi().then((a) => a.getReceipts(id)),
  getDossierHtml: (id) => getApi().then((a) => a.getDossierHtml(id)),
  downloadUrl: (job, kind) => (impl ?? live).downloadUrl(job, kind),
  events: (id, after) => getApi().then((a) => a.events(id, after)),
  watchEvents: (id, after, onEvent, onEnd) => {
    let stop: (() => void) | null = null
    let cancelled = false
    void getApi().then((a) => {
      if (cancelled) return
      stop = a.watchEvents(id, after, onEvent, onEnd)
    })
    return () => { cancelled = true; stop?.() }
  },
  executorJob: (id) => getApi().then((a) => a.executorJob(id)),
  plan: (id) => getApi().then((a) => a.plan(id)),
  pipelineVisualization: (id) => getApi().then((a) => a.pipelineVisualization(id)),
}
