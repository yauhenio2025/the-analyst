/* The Analyst — API client. One base URL, fetch + EventSource. Mock mode
   (VITE_MOCK=1 at build time, or ?mock=1 / localStorage analyst.mock=1 at
   run time) swaps every call for the fixture replay in ./mock.ts. */
import type {
  Audience, Brief, BriefOption, BriefPromise, BriefShape, Catalog, CreateJobRequest, CreateJobResponse, Depth, DossierJob, Exemplar,
  ExecutorJob, JobListEntry, OrchestratorPlan, Receipt, RunEvent, ShapeRef, StepDepth,
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
/* Brief options — v2 (deliverable, promises with refs, shape, evidence, path) AND the old shape
   (telling, engines as [{engine_key, why}] or names, string estimates, output_shape object).
   Every option comes out with the v2 fields present (empty for v1) and the legacy views
   (`engines` as names, `why`, one-line `output_shape`) that the older pages read. */
const strList = (v: unknown): string[] => Array.isArray(v) ? v.map((x) => String(x ?? '')).filter(Boolean) : []
const num = (v: unknown): number => Number(v ?? 0) || 0
function normalizePromise(p: unknown): BriefPromise {
  if (typeof p === 'string') return { text: p, supported_by: [] }
  const anyP = (p && typeof p === 'object' ? p : {}) as Record<string, unknown>
  const refs = Array.isArray(anyP.supported_by) ? (anyP.supported_by as unknown[]) : []
  return {
    text: String(anyP.text ?? ''),
    supported_by: refs.map((r) => {
      if (typeof r === 'string') {
        const m = /^([§STF])\s*(\d+)$/i.exec(r.trim())
        return m ? { kind: (m[1] === 'T' || m[1] === 't') ? 'table' : (m[1] === 'F' || m[1] === 'f') ? 'figure' : 'section', index: Number(m[2]) } as ShapeRef : null
      }
      const anyR = (r && typeof r === 'object' ? r : {}) as Record<string, unknown>
      const kind = String(anyR.kind ?? 'section')
      return { kind: (kind === 'table' || kind === 'figure' ? kind : 'section'), index: Math.max(1, num(anyR.index) || 1) } as ShapeRef
    }).filter(Boolean) as ShapeRef[],
    unsupported: Boolean(anyP.unsupported),
  }
}
export function normalizeBriefOption(o: Record<string, unknown>): BriefOption {
  const rawPath = (o.path && typeof o.path === 'object' ? o.path : {}) as Record<string, unknown>
  const pathSteps = (Array.isArray(rawPath.steps) ? (rawPath.steps as Record<string, unknown>[]) : []).map((s) => ({
    engine_key: String(s.engine_key ?? ''), plain_name: String(s.plain_name ?? ''), contributes: String(s.contributes ?? ''),
    depth: (['surface', 'standard', 'deep'].includes(String(s.depth)) ? String(s.depth) : 'surface') as StepDepth,
  })).filter((s) => s.engine_key)
  const rawEngines = Array.isArray(o.engines) ? (o.engines as unknown[]) : []
  const engineObjs = rawEngines.map((e) => typeof e === 'string' ? { engine_key: e, why: '' } : { engine_key: String((e as Record<string, unknown>)?.engine_key ?? (e as Record<string, unknown>)?.key ?? ''), why: String((e as Record<string, unknown>)?.why ?? '') })
    .filter((e) => e.engine_key)
  const engines = pathSteps.length ? pathSteps.map((s) => s.engine_key) : engineObjs.map((e) => e.engine_key)
  const whys = pathSteps.length ? pathSteps.map((s) => s.contributes).filter(Boolean) : engineObjs.map((e) => e.why).filter(Boolean)
  const rawShape = o.shape && typeof o.shape === 'object' ? (o.shape as Record<string, unknown>) : null
  const shape: BriefShape | null = rawShape ? {
    sections: (Array.isArray(rawShape.sections) ? rawShape.sections as unknown[] : []).map((s) => typeof s === 'string' ? { heading: s, answers: '' } : { heading: String((s as Record<string, unknown>).heading ?? ''), answers: String((s as Record<string, unknown>).answers ?? '') }),
    tables: (Array.isArray(rawShape.tables) ? rawShape.tables as unknown[] : []).map((t) => typeof t === 'string' ? { title: t, row_unit: '', columns: [], rows_expected: '', carried_by: [] } : { title: String((t as Record<string, unknown>).title ?? ''), row_unit: String((t as Record<string, unknown>).row_unit ?? ''), columns: strList((t as Record<string, unknown>).columns), rows_expected: String((t as Record<string, unknown>).rows_expected ?? ''), carried_by: strList((t as Record<string, unknown>).carried_by) }),
    figures: (Array.isArray(rawShape.figures) ? rawShape.figures as unknown[] : []).map((f) => typeof f === 'string' ? { title: f, format: 'scene', scene: '' } : { title: String((f as Record<string, unknown>).title ?? ''), format: String((f as Record<string, unknown>).format ?? 'scene'), scene: String((f as Record<string, unknown>).scene ?? '') }),
  } : null
  // one-line shape for the legacy card: from the v2 shape, or the v1 output_shape object / string
  let line: string | undefined
  const legacyShape = o.output_shape
  if (shape) {
    const parts = [] as string[]
    if (shape.sections.length) parts.push(`${shape.sections.length} sections`)
    if (shape.tables.length) parts.push(`${shape.tables.length} tables`)
    if (shape.figures.length) parts.push(`${shape.figures.length} figures`)
    line = parts.join(' · ')
  } else if (legacyShape && typeof legacyShape === 'object') {
    const sh = legacyShape as Record<string, unknown>
    const n = (v: unknown) => Array.isArray(v) ? v.length : (typeof v === 'number' ? v : 0)
    const parts = [] as string[]
    if (n(sh.sections)) parts.push(`${n(sh.sections)} sections`)
    if (n(sh.tables)) parts.push(`${n(sh.tables)} tables`)
    if (n(sh.figures)) parts.push(`${n(sh.figures)} figures`)
    line = parts.join(' · ')
  } else if (typeof legacyShape === 'string') line = legacyShape
  const rawEv = (o.evidence_base && typeof o.evidence_base === 'object' ? o.evidence_base : {}) as Record<string, unknown>
  const version = num(o.version) || (shape ? 2 : 1)
  const understand = Array.isArray(o.you_will_understand) ? (o.you_will_understand as unknown[]).map(normalizePromise) : []
  const deliverable = String(o.deliverable ?? '')
  const telling = typeof o.telling === 'string' && o.telling ? o.telling
    : (deliverable ? `${deliverable.replace(/\.$/, '')}. ${understand.map((p) => p.text).join(' ')}` : String(o.telling ?? ''))
  return {
    ...(o as object),
    version, key: String(o.key ?? ''), title: String(o.title ?? o.key ?? ''),
    deliverable_kind: String(o.deliverable_kind ?? ''), deliverable, use_kind: String(o.use_kind ?? '') as BriefOption['use_kind'],
    you_will_understand: understand,
    you_will_be_able_to: Array.isArray(o.you_will_be_able_to) ? (o.you_will_be_able_to as unknown[]).map(normalizePromise) : [],
    questions_answered: strList(o.questions_answered), not_for: strList(o.not_for),
    shape,
    evidence_base: {
      carrying_docs: (Array.isArray(rawEv.carrying_docs) ? rawEv.carrying_docs as unknown[] : []).map((d) => typeof d === 'string' ? { doc_key: d, carries: '' } : { doc_key: String((d as Record<string, unknown>).doc_key ?? ''), carries: String((d as Record<string, unknown>).carries ?? '') }),
      thin_or_missing: strList(rawEv.thin_or_missing),
    },
    path: { steps: pathSteps.length ? pathSteps : engineObjs.map((e) => ({ engine_key: e.engine_key, plain_name: '', contributes: e.why, depth: 'surface' as StepDepth })),
            depth: (['simple', 'medium', 'advanced'].includes(String(rawPath.depth)) ? String(rawPath.depth) : 'simple') as Depth,
            primitives: strList(rawPath.primitives), chain_key: typeof rawPath.chain_key === 'string' ? rawPath.chain_key : null },
    best_when: String(o.best_when ?? ''), alternative: Boolean(o.alternative), notes: strList(o.notes),
    est_cost_usd: num(o.est_cost_usd), est_minutes: num(o.est_minutes), est_llm_calls: num(o.est_llm_calls),
    telling, engines, why: (typeof o.why === 'string' && o.why) ? o.why : whys.join(' '), output_shape: line,
  }
}
function normalizeBrief(b: unknown): Brief {
  const anyB = (b && typeof b === 'object' ? b : {}) as Record<string, unknown>
  const options = Array.isArray(anyB.options) ? (anyB.options as Record<string, unknown>[]).map(normalizeBriefOption) : []
  const defaults = (anyB.defaults && typeof anyB.defaults === 'object' ? anyB.defaults : {}) as Record<string, unknown>
  const rawRec = anyB.recommendation && typeof anyB.recommendation === 'object' ? (anyB.recommendation as Record<string, unknown>) : null
  const recommendation = rawRec && rawRec.option_key ? {
    option_key: String(rawRec.option_key), because: String(rawRec.because ?? ''),
    runner_up: typeof rawRec.runner_up === 'string' ? rawRec.runner_up : null, runner_up_because: typeof rawRec.runner_up_because === 'string' ? rawRec.runner_up_because : null,
  } : (typeof defaults.option_key === 'string' ? { option_key: defaults.option_key, because: '', runner_up: null, runner_up_because: null } : null)
  const entry = ['use', 'chosen', 'material'].includes(String(anyB.entry)) ? String(anyB.entry) as Brief['entry'] : 'use'
  return { ...anyB, version: num(anyB.version) || (options.some((o) => o.version >= 2) ? 2 : 1), entry, options, recommendation, defaults, notes: strList(anyB.notes) } as unknown as Brief
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
  /** the purpose-first engine catalog (lane 2 picker); priced when the corpus size is known */
  catalog(audience: Audience, corpusChars?: number | null, nDocs?: number | null): Promise<Catalog>
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
  catalog: (audience, corpusChars, nDocs) => {
    const q = new URLSearchParams({ audience })
    if (corpusChars) q.set('corpus_chars', String(Math.round(corpusChars)))
    if (nDocs) q.set('n_docs', String(nDocs))
    return request<Catalog>(`/v1/dossier/catalog?${q.toString()}`)
  },
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
  catalog: (aud, c, n) => getApi().then((a) => a.catalog(aud, c, n)),
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
