/* The Analyst — API types. Mirrors communications/IMPLEMENTATION_TRACKER.md §4
   and the W1 brief. Fields marked "assumed" are contract assumptions logged
   in communications/changes/web.md. */

export type SourceSpec =
  | { kind: 'paste'; title: string; text: string }
  | { kind: 'stacks_view'; view_id: string }
  | { kind: 'stacks_uids'; uids: string[] }
  | { kind: 'exemplar'; key: string }

export type Audience = 'executive' | 'researcher' | 'analyst'
export type Depth = 'simple' | 'medium' | 'advanced'

export interface OutputShape {
  text: boolean
  tables: boolean
  figures: number
  video: boolean
}

export interface DossierOptions {
  intent?: string
  audience?: Audience
  depth?: Depth
  output?: OutputShape
  spend_cap_usd?: number
  autopilot?: boolean
  image_provider?: string
}

export interface CreateJobRequest extends DossierOptions {
  sources: SourceSpec[]
}

export interface CreateJobResponse {
  job_id: string
  status: DossierStatus
  console_url?: string
}

export type DossierStatus =
  | 'queued' | 'reconnaissance' | 'awaiting_brief' | 'planning' | 'analysis'
  | 'tables' | 'figures' | 'composing' | 'done' | 'failed'

export const STATUS_ORDER: DossierStatus[] = [
  'queued', 'reconnaissance', 'awaiting_brief', 'planning', 'analysis',
  'tables', 'figures', 'composing', 'done',
]

export function statusRank(s: DossierStatus | undefined | null): number {
  if (!s) return -1
  if (s === 'failed') return -1
  return STATUS_ORDER.indexOf(s)
}

export interface Totals {
  calls: number
  input_tokens: number
  output_tokens: number
  cost_usd: number
  duration_ms: number
}

export interface JobListEntry {
  id: string
  status: DossierStatus
  step: number
  created_at: string
  title: string
  totals?: Partial<Totals>
}

/* assumed shape — produced by reconnaissance */
export interface KeyClaim { claim: string; quote: string }
export interface DocProfile {
  doc_key: string
  title: string
  year?: string | number | null
  author?: string | null
  genre?: string | null
  chars?: number
  thesis: string
  key_claims: KeyClaim[]
}

export interface BriefOption {
  key: string
  title: string
  telling: string
  engines: string[]
  why: string
  est_cost_usd: number
  est_minutes: number
  output_shape?: string
}

export interface Brief {
  options: BriefOption[]
  defaults?: { option_key?: string; audience?: Audience; depth?: Depth; figures?: number }
}

export interface Anchor { doc_key: string; quote: string }
export interface TableCell { value: string; anchor?: Anchor | null }
export interface TableRow { cells: TableCell[] }
export interface DossierTable {
  key: string
  caption: string
  columns: string[]
  rows: TableRow[]
  note?: string | null
}

export interface DossierFigure {
  key: string
  caption: string
  figure_id?: string
  url: string
  provider?: string
  cost_usd?: number
  prompt?: string
}

export interface DossierSection {
  key: string
  title: string
  html?: string
  md?: string
}

/* assumed shape — one row per model call */
export interface Receipt {
  seq?: number
  id?: string
  ts?: string
  phase?: string
  engine?: string
  model?: string
  input_tokens?: number
  output_tokens?: number
  cost_usd?: number
  duration_ms?: number
  prompt_hash?: string
  [k: string]: unknown
}

export interface DossierJob {
  id: string
  status: DossierStatus
  step: number
  created_at: string
  title: string
  sources: SourceSpec[]
  options: DossierOptions
  profiles: DocProfile[]
  brief: Brief | null
  chosen_option: string | null
  plan_id: string | null
  analysis_job_id: string | null
  analysis: Record<string, string>
  tables: DossierTable[]
  figures: DossierFigure[]
  sections: DossierSection[]
  receipts: Receipt[]
  totals: Totals
  paths: { html?: string; pdf?: string; md?: string }
  error?: string | null
  console_url?: string
}

export interface Exemplar {
  key: string
  title: string
  description: string
  n_docs: number
  chars: number
}

export type EventKind =
  | 'job_started' | 'phase_started' | 'phase_finished' | 'chain_started'
  | 'chain_finished' | 'call_started' | 'call_finished' | 'call_failed'
  | 'narration' | 'artifact' | 'note' | 'job_finished' | 'job_failed'

export interface RunEvent {
  job_id: string
  seq: number
  ts: string
  kind: EventKind
  phase?: string | null
  chain?: string | null
  engine?: string | null
  pass_name?: string | null
  stance?: string | null
  work_key?: string | null
  model?: string | null
  input_chars?: number | null
  output_chars?: number | null
  input_tokens?: number | null
  output_tokens?: number | null
  cost_usd?: number | null
  duration_ms?: number | null
  prompt_hash?: string | null
  prompt_excerpt?: string | null
  output_excerpt?: string | null
  detail?: string | null
  narrator?: string | null
  payload_json?: string | null
}

/* executor + orchestrator (existing analyzer-v2 shapes, read defensively) */
export interface ExecutorProgress {
  current_phase: number
  total_phases: number
  phase_name: string
  detail: string
  phase_statuses: Record<string, string>
}
export interface ExecutorJob {
  job_id: string
  plan_id: string
  status: string
  progress: ExecutorProgress
  workflow_key?: string
  created_at?: string
  total_llm_calls?: number
  total_input_tokens?: number
  total_output_tokens?: number
  total_cost_estimate?: number
  error?: string | null
}

export interface PlanPhase {
  phase_number: number
  phase_name: string
  rationale?: string
  depth?: string
  depends_on?: number[]
  execution?: { type?: string; chain_key?: string; chain_name?: string
    engines?: { engine_key: string; engine_name?: string
      passes?: { pass_number: number; label?: string; stance_name?: string }[] }[] }
  [k: string]: unknown
}
export interface OrchestratorPlan {
  plan_id: string
  workflow_key?: string
  strategy_summary?: string
  strategy_rationale?: string
  alternatives_considered?: string[]
  estimated_llm_calls?: number
  phases: PlanPhase[]
  decision_trace?: {
    overall_strategy_rationale?: string
    phase_decisions?: { phase_name?: string; alternatives_considered?: string[] }[]
  }
  [k: string]: unknown
}
