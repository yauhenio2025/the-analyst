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
export interface UploadedBundle extends Exemplar {
  name?: string
  documents: { key: string; title: string; char_count: number; pages?: number | null; filename?: string }[]
}

function unwrap<T>(d: unknown, key: string): T[] {
  if (Array.isArray(d)) return d as T[]
  const v = (d as Record<string, unknown> | null)?.[key]
  return Array.isArray(v) ? (v as T[]) : []
}
function normalizeExemplar(e: Record<string, unknown>): Record<string, unknown> {
  return {
    ...e,
    key: (e.key ?? e.name) as string,
    name: (e.name ?? e.key) as string,
    n_docs: Number(e.n_docs ?? e.document_count ?? 1) || 1,
    chars: Number(e.chars ?? e.char_count ?? 0) || 0,
    title: (e.title ?? e.name ?? e.key) as string,
    description: (e.description ?? '') as string,
  }
}
/* Brief options: the backend sends engines as [{engine_key, why}], estimates as strings,
   output_shape as an object; pages expect names, numbers and a one-line shape. */
function normalizeBriefOption(o: Record<string, unknown>): Record<string, unknown> {
  const rawEngines = Array.isArray(o.engines) ? (o.engines as unknown[]) : []
  const engines = rawEngines.map((e) => typeof e === 'string' ? e : String((e as Record<string, unknown>)?.engine_key ?? (e as Record<string, unknown>)?.key ?? ''))
    .filter(Boolean)
  const whys = rawEngines.map((e) => (typeof e === 'object' && e ? (e as Record<string, unknown>).why : null)).filter(Boolean) as string[]
  let shape: unknown = o.output_shape
  if (shape && typeof shape === 'object') {
    const sh = shape as Record<string, unknown>
    const n = (v: unknown) => Array.isArray(v) ? v.length : (typeof v === 'number' ? v : 0)
    const parts = [] as string[]
    if (n(sh.sections)) parts.push(`${n(sh.sections)} sections`)
    if (n(sh.tables)) parts.push(`${n(sh.tables)} tables`)
    if (n(sh.figures)) parts.push(`${n(sh.figures)} figures`)
    shape = parts.join(' · ')
  }
  return {
    ...o,
    engines,
    why: (typeof o.why === 'string' && o.why) ? o.why : whys.join(' '),
    est_cost_usd: Number(o.est_cost_usd ?? 0) || 0,
    est_minutes: Number(o.est_minutes ?? 0) || 0,
    est_llm_calls: Number(o.est_llm_calls ?? 0) || 0,
    output_shape: typeof shape === 'string' ? shape : undefined,
    telling: typeof o.telling === 'string' ? o.telling : String(o.telling ?? ''),
    title: String(o.title ?? o.key ?? ''),
  }
}
function normalizeBrief(b: unknown): Brief {
  const anyB = (b && typeof b === 'object' ? b : {}) as Record<string, unknown>
  const options = Array.isArray(anyB.options) ? (anyB.options as Record<string, unknown>[]).map(normalizeBriefOption) : []
  const defaults = (anyB.defaults && typeof anyB.defaults === 'object' ? anyB.defaults : {}) as Record<string, unknown>
  return { ...anyB, options, defaults } as unknown as Brief
}

function normalizeJob(j: DossierJob): DossierJob {
  const anyJ = j as unknown as Record<string, unknown>
  if (Array.isArray(anyJ.sources)) {
    anyJ.sources = (anyJ.sources as Record<string, unknown>[]).map((s) => ({ ...s, key: s.key ?? s.name, name: s.name ?? s.key }))
  }
  if (!anyJ.title) {
    const docs = anyJ.documents as Record<string, unknown>[] | undefined
    const srcs = anyJ.sources as Record<string, unknown>[] | undefined
    anyJ.title = (docs?.[0]?.title as string) || (srcs?.[0]?.title as string) || (srcs?.[0]?.name as string) || (anyJ.id as string)
    if (docs && docs.length > 1) anyJ.title = `${anyJ.title} (+${docs.length - 1} more)`
  }
  for (const k of ['profiles', 'tables', 'figures', 'receipts', 'notes', 'documents', 'sources']) {
    if (!Array.isArray(anyJ[k])) anyJ[k] = []
  }
  // The composer returns {title, subtitle, executive_summary[], sections[{number, heading, paragraphs[]}], conclusion[]};
  // pages expect DossierSection[] with {key, title, md}.
  const comp = anyJ.sections as unknown
  if (comp && !Array.isArray(comp) && typeof comp === 'object') {
    const c = comp as Record<string, unknown>
    const out: Record<string, unknown>[] = []
    const asMd = (v: unknown) => Array.isArray(v) ? (v as unknown[]).map(String).join('\n\n') : (typeof v === 'string' ? v : '')
    if (Array.isArray(c.executive_summary) && (c.executive_summary as unknown[]).length) out.push({ key: 'summary', title: 'Summary', md: asMd(c.executive_summary) })
    for (const sec of (Array.isArray(c.sections) ? (c.sections as Record<string, unknown>[]) : [])) {
      out.push({ key: `s${sec.number ?? out.length + 1}`, title: String(sec.heading ?? `Section ${sec.number ?? ''}`), md: asMd(sec.paragraphs),
                 number: sec.number, table_keys: sec.table_keys ?? [], figure_keys: sec.figure_keys ?? [] })
    }
    if (Array.isArray(c.conclusion) && (c.conclusion as unknown[]).length) out.push({ key: 'conclusion', title: 'Conclusion', md: asMd(c.conclusion) })
    anyJ.sections = out
    anyJ.composition = { title: c.title, subtitle: c.subtitle, claims_unanchored: c.claims_unanchored }
    if (!anyJ.title && c.title) anyJ.title = c.title
  }
  if (!Array.isArray(anyJ.sections)) anyJ.sections = []
  // paths must be URLs; the backend records filesystem paths, so keep only /v1/... or absolute http(s)
  if (anyJ.paths && typeof anyJ.paths === 'object') {
    const cleaned: Record<string, string> = {}
    for (const [k, v] of Object.entries(anyJ.paths as Record<string, unknown>)) {
      if (typeof v === 'string' && (/^https?:/.test(v) || v.startsWith('/v1/'))) cleaned[k] = v
    }
    anyJ.paths = cleaned
  }
  if (anyJ.brief && typeof anyJ.brief === 'object') anyJ.brief = normalizeBrief(anyJ.brief)
  const t = (anyJ.totals ?? {}) as Record<string, unknown>
  if (typeof t.calls !== 'number') {
    t.calls = (Number(t.llm_calls ?? 0) || 0) + (Number(t.image_calls ?? 0) || 0)
  }
  if (typeof t.cost_usd !== 'number') t.cost_usd = Number(t.cost_usd ?? 0) || 0
  anyJ.totals = t
  if (!anyJ.paths || typeof anyJ.paths !== 'object') anyJ.paths = {}
  const compTitle = (anyJ.composition as Record<string, unknown> | undefined)?.title
  if (compTitle) anyJ.title = compTitle
  return anyJ as unknown as DossierJob
}

async function requestText(path: string): Promise<string> {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new ApiError(res.status, await res.text().catch(() => ''), path)
  return res.text()
}

export interface Api {
  exemplars(): Promise<Exemplar[]>
  /** upload local files (pdf/md/txt) -> one bundle stored like an exemplar */
  uploadBundle(files: File[], title?: string): Promise<UploadedBundle>
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
  exemplars: () => request<unknown>('/v1/dossier/exemplars').then((d) => unwrap<Record<string, unknown>>(d, 'exemplars').map(normalizeExemplar) as unknown as Exemplar[]),
  uploadBundle: async (files, title) => {
    const fd = new FormData()
    for (const f of files) fd.append('files', f, f.name)
    if (title) fd.append('title', title)
    const res = await fetch(`${API_BASE}/v1/dossier/uploads`, { method: 'POST', body: fd })
    if (!res.ok) throw new ApiError(res.status, await res.text().catch(() => ''), '/v1/dossier/uploads')
    const d = (await res.json()) as Record<string, unknown>
    return { ...normalizeExemplar(d), documents: (d.documents as UploadedBundle['documents']) ?? [] } as UploadedBundle
  },
  listJobs: () => request<unknown>('/v1/dossier/jobs').then((d) =>
    unwrap<JobListEntry>(d, 'jobs').map((e) => {
      const anyE = e as unknown as Record<string, unknown>
      if (!anyE.totals || typeof anyE.totals !== 'object') {
        anyE.totals = { cost_usd: Number(anyE.cost_usd ?? 0) || 0, calls: Number(anyE.calls ?? 0) || 0 }
      }
      return anyE as unknown as JobListEntry
    })),
  createJob: (req) => {
    const anyReq = req as unknown as Record<string, unknown>
    const sources = (anyReq.sources as Record<string, unknown>[] | undefined)?.map((s) =>
      s.kind === 'exemplar' ? { ...s, name: s.name ?? s.key } : s)
    return request<CreateJobResponse>('/v1/dossier/jobs',
      { method: 'POST', body: JSON.stringify({ ...anyReq, sources }) })
  },
  getJob: (id) => request<DossierJob>(`/v1/dossier/jobs/${id}`).then(normalizeJob),
  getBrief: (id) => request<unknown>(`/v1/dossier/jobs/${id}/brief`).then(normalizeBrief),
  chooseBrief: (id, option_key, overrides) => request<DossierJob>(
    `/v1/dossier/jobs/${id}/brief`,
    { method: 'POST', body: JSON.stringify({ option_key, overrides: overrides ?? {} }) }).then(normalizeJob),
  getReceipts: (id) => request<unknown>(`/v1/dossier/jobs/${id}/receipts`).then((d) => unwrap<Receipt>(d, 'receipts')),
  getDossierHtml: (id) => requestText(`/v1/dossier/jobs/${id}/dossier.html`).then((html) =>
    // figures and downloads inside the composed page are API-relative; the desk is another origin
    html.replace(/(src|href)="\/v1\//g, `$1="${API_BASE}/v1/`)),
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
  uploadBundle: (f, t) => getApi().then((a) => a.uploadBundle(f, t)),
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
