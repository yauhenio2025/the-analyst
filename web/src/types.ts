/* The Analyst — API types. Mirrors communications/IMPLEMENTATION_TRACKER.md §4,
   the W1 brief and the brief v2 contract (communications/changes/brief-v2.md).
   Fields marked "assumed" are contract assumptions logged in
   communications/changes/web.md. */

export type SourceSpec =
  | { kind: 'paste'; title: string; text: string }
  | { kind: 'stacks_view'; view_id: string }
  | { kind: 'stacks_uids'; uids: string[] }
  | { kind: 'exemplar'; key: string }

export type Audience = 'executive' | 'researcher' | 'analyst'
export type Depth = 'simple' | 'medium' | 'advanced'
export type StepDepth = 'surface' | 'standard' | 'deep'

/* brief v2 — the three lanes and the use register */
export type Entry = 'use' | 'chosen' | 'material'
export type UseKind = 'decide' | 'brief' | 'prepare' | 'stress_test' | 'compare' | 'watch' | 'learn' | 'argue'
export const USE_KINDS: { key: UseKind; label: string; hint: string }[] = [
  { key: 'decide', label: 'Decide something', hint: 'choose between courses of action; retire or advance something' },
  { key: 'brief', label: 'Brief someone', hint: 'bring a board, a CEO, a committee up to speed for a meeting' },
  { key: 'prepare', label: 'Prepare for a meeting or negotiation', hint: 'a negotiation, a pitch, a challenge, a hearing' },
  { key: 'stress_test', label: 'Stress-test our position', hint: 'test our own claims before they are attacked' },
  { key: 'compare', label: 'Compare cases', hint: 'set two or more cases side by side to choose' },
  { key: 'watch', label: "Watch for what's coming", hint: 'what to monitor and the early signs to look for' },
  { key: 'learn', label: 'Learn the field fast', hint: 'get up to speed on a set of papers' },
  { key: 'argue', label: 'Build an argument', hint: 'build or defend a case with the strongest evidence' },
]
export const DELIVERABLE_LABEL: Record<string, string> = {
  stress_test: 'stress test', decision_memo: 'decision memo', briefing: 'briefing', playbook: 'playbook',
  comparison: 'comparison', watchlist: 'watch-list', reading_guide: 'reading guide', decoder: 'decoder',
  risk_register: 'risk register', case_file: 'case file',
}

export interface UseFrame {
  use_kind?: UseKind | null
  occasion?: string | null
  who_reads?: string | null
  decision?: string | null
}
export interface PathStepRequest { engine_key: string; depth?: StepDepth }
export interface PathRequest {
  steps: PathStepRequest[]
  chain_key?: string | null
  depth?: Depth | null
}

export interface OutputShape {
  text: boolean
  tables: boolean
  figures: number
  plates?: number
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
  entry?: Entry
  use_frame?: UseFrame | null
  path?: PathRequest | null
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
  | 'queued' | 'reconnaissance' | 'awaiting_brief' | 'planning' | 'analysis' | 'spine'
  | 'tables' | 'figures' | 'plates' | 'composing' | 'crosscheck' | 'done' | 'failed'

export const STATUS_ORDER: DossierStatus[] = [
  'queued', 'reconnaissance', 'awaiting_brief', 'planning', 'analysis', 'spine',
  'tables', 'figures', 'composing', 'crosscheck', 'done',
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

/* ── brief v2: a deliverable, verified against its shape ── */
export interface ShapeRef { kind: 'section' | 'table' | 'figure'; index: number }
export interface BriefPromise { text: string; supported_by: ShapeRef[]; unsupported?: boolean }
export interface SectionSpec { heading: string; answers: string }
export interface TableSpec { title: string; row_unit: string; columns: string[]; rows_expected: string; carried_by: string[] }
export interface FigureSpec { title: string; format: string; scene: string }
export interface BriefShape { sections: SectionSpec[]; tables: TableSpec[]; figures: FigureSpec[] }
export interface EvidenceBase { carrying_docs: { doc_key: string; carries: string }[]; thin_or_missing: string[] }
export interface PathStep { engine_key: string; plain_name: string; contributes: string; depth: StepDepth }
export interface BriefPath { steps: PathStep[]; depth: Depth; primitives?: string[]; chain_key?: string | null }

export const refLabel = (r: ShapeRef) => `${r.kind === 'section' ? '§' : r.kind === 'table' ? 'T' : 'F'}${r.index}`

export interface BriefOption {
  version: number
  key: string
  title: string
  deliverable_kind: string
  deliverable: string
  use_kind: UseKind | ''
  you_will_understand: BriefPromise[]
  you_will_be_able_to: BriefPromise[]
  questions_answered: string[]
  not_for: string[]
  shape: BriefShape | null
  evidence_base: EvidenceBase
  path: BriefPath
  best_when: string
  alternative?: boolean
  notes?: string[]
  est_cost_usd: number
  est_minutes: number
  est_llm_calls?: number
  /* legacy views (v1 cards and old consumers): the paragraph, engine names, a one-line shape */
  telling: string
  engines: string[]
  why: string
  output_shape?: string
}

export interface Recommendation {
  option_key: string
  because: string
  runner_up?: string | null
  runner_up_because?: string | null
}

export interface Brief {
  version?: number
  entry?: Entry
  options: BriefOption[]
  recommendation?: Recommendation | null
  defaults?: { option_key?: string; audience?: Audience; depth?: Depth; figures?: number }
  notes?: string[]
}

/* ── the purpose-first catalog (GET /v1/dossier/catalog) ── */
export interface CatalogDepth { passes: number; est_cost_usd?: number; est_minutes?: number }
export interface CatalogEngine {
  engine_key: string
  engine_name: string
  plain_name: string
  executive_name?: string
  use_when: string
  yields: string
  row_unit: string
  deliverable_kinds: string[]
  pairs_with: string[]
  depths: Record<string, CatalogDepth>
  fit: 'ok' | 'conditional' | 'off' | 'not_for_dossier'
  fit_note: string
  category?: string
}
export interface CatalogGroup { key: string; title: string; purpose: string; engines: CatalogEngine[] }
export interface CatalogRecipe {
  key: string; title: string; use_when: string; yields: string; depth: Depth
  steps: PathStep[]; est_cost_usd: number; est_minutes: number; est_llm_calls: number
}
export interface Catalog {
  audience: Audience
  corpus_chars?: number | null
  n_docs?: number | null
  groups: CatalogGroup[]
  recipes: CatalogRecipe[]
  excluded: { engine_key: string; why: string }[]
  own_overhead: { est_cost_usd: number; est_minutes: number; calls: number; why?: string }
  use_kinds?: string[]
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
  section_key?: string
  proves?: string
}

export interface DossierFigure {
  key: string
  caption: string
  figure_id?: string
  url: string
  provider?: string
  cost_usd?: number
  prompt?: string
  title?: string
  visual_format?: string
  section_key?: string
  detected?: string
  checked_ok?: boolean | null
  status?: string
}

export interface DossierSection {
  key: string
  title: string
  html?: string
  md?: string
  section_key?: string
}

/* ── the concretization passes (communications/changes/concretize.md) ── */
export interface SpineTableSpec { intent: string; row_unit: string; columns: string[]; carries_claims: string[] }
export interface SpineFigureSpec { primitive: string; visual_format: string; picture_shows: string; caption_says: string; why_a_picture: string }
export interface SpineSection {
  key: string
  heading: string
  claim: string
  reader_needs_next?: string
  evidence_kind?: string
  table?: SpineTableSpec | null
  figure?: SpineFigureSpec | null
  anchors_planned?: Anchor[]
  feeds?: string[]
}
export interface CompositionRead {
  plain_summary?: string
  buried_crux?: string
  readers?: { type: string; mode: string; wants: string }[]
  strands?: { name: string; carried_by: string[]; accidental: boolean; note: string }[]
  prose_to_table?: string[]
  table_to_prose?: string[]
  figures_earned?: string[]
  figures_dropped?: string[]
  cumulative_direction?: string
  form_capacity?: string
}
export interface DossierSpine {
  round: number
  read?: CompositionRead
  thesis: string
  reader_question?: string
  handle?: string
  through_line?: string
  summary_job: string
  conclusion_job: string
  sections: SpineSection[]
  exhibits_budget?: { tables: number; figures: number }
  notes?: string[]
}
export interface FindingFate { round: number; fate: string; rationale: string; by: string; ts?: string }
export interface Finding {
  id: string
  kind: string
  where: { section_key?: string | null; table_key?: string | null; figure_key?: string | null; paragraph_index?: number | null; anchor_n?: number | null }
  quote?: string
  note: string
  affordance: string
  realization?: string | null
  recommended?: boolean
  source: string
  round?: number
  status: string
  fates: FindingFate[]
}
export interface CrossCheckVerdict {
  round: number
  hangs_together: boolean | null
  summary: string
  findings_minted: number
  clamps: number
  judged: boolean
  what_changed?: string | null
  realized: string[]
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
  spine: DossierSpine | null
  findings: Finding[]
  crosscheck: CrossCheckVerdict | null
  receipts: Receipt[]
  totals: Totals
  paths: { html?: string; pdf?: string; md?: string }
  error?: string | null
  console_url?: string
  documents?: { key: string; title: string; char_count?: number }[]
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

/* ── plates: one dense 4K diagram per perspective (communications/changes/plates.md) ── */
export interface PlateCompliance {
  checked: boolean
  ok: boolean | null
  format_ok?: boolean | null
  detected_format?: string | null
  title_found?: boolean | null
  labels_found?: string[]
  labels_missing?: string[]
  misspelled?: { expected: string; seen?: string }[]
  illegible?: string[]
  prohibited_elements?: string[]
  leaked_tokens?: string[]
  extra_text?: string[]
  density?: string | null
  legible_at_4k?: boolean | null
  issues?: string[]
  suggestion?: string | null
  confidence?: string
  n_labels?: number
}
export interface PlateAttempt {
  n: number
  provider?: string
  model?: string
  cost_usd?: number
  latency_ms?: number
  width?: number | null
  height?: number | null
  kept?: boolean
  compliance?: PlateCompliance | null
  revision_notes?: string[]
}
export type PlateStatus = 'planned' | 'generated' | 'skipped' | 'failed'
export interface DossierPlate {
  key: string
  family: string
  visual_format: string
  perspective: string
  title: string
  narrative: string
  why_this_perspective?: string
  claimed_territory?: string
  excludes?: string[]
  abstraction_level: number
  aspect?: string
  style_school?: string
  status: PlateStatus
  note?: string
  url?: string | null
  figure_id?: string | null
  provider?: string | null
  model?: string | null
  width?: number | null
  height?: number | null
  cost_usd: number
  compliance?: PlateCompliance | null
  attempts: PlateAttempt[]
  size_guides?: Record<string, number>
  created_at?: string
  prompt_chars?: number
}
export interface PlatesRun { started_at: string; n: number; perspectives: string[] }
export interface PlatesResponse { job_id: string; running: boolean; run: PlatesRun | null; plates: DossierPlate[] }
export interface StartPlatesResponse { job_id: string; status: string; n: number; perspectives: string[]; phase: string }

/* ── the story desk (src/story/schemas.py): many sources → one film plan for Wirecut ── */
export type StoryStatus =
  | 'queued' | 'reading' | 'mapping' | 'ranking' | 'briefing' | 'awaiting_brief' | 'spining' | 'handing_off'
  | 'done' | 'failed' | 'cancelled'
export type StoryStep = 'reconnaissance' | 'map' | 'approaches' | 'brief' | 'spine' | 'handoff'
export const STORY_STATUS_ORDER: StoryStatus[] = [
  'queued', 'reading', 'mapping', 'ranking', 'briefing', 'awaiting_brief', 'spining', 'handing_off', 'done',
]
export function storyRank(s: StoryStatus | string | null | undefined): number {
  if (!s) return -1
  return STORY_STATUS_ORDER.indexOf(s as StoryStatus)
}
export const ELEMENT_KINDS = ['question', 'face', 'turn', 'antagonism', 'reveal', 'motif', 'filmable', 'quotable', 'number'] as const
export type ElementKind = typeof ELEMENT_KINDS[number]

export interface StoryElement {
  id: string
  kind: string
  text: string
  detail: Record<string, string>
  anchor: Anchor & { verified?: boolean; trimmed?: boolean }
  intensity: number
  consumers: string[]
}
export interface StoryProfile {
  doc_key: string
  title: string
  genre?: string
  one_line?: string
  question: string
  stance: string
  elements: StoryElement[]
  gaps: string[]
  elements_dropped: number
}
export interface Recurrence { what: string; kind?: string; doc_keys: string[]; element_ids: string[] }
export interface Position { doc_key: string; says: string }
export interface Contradiction { about: string; positions: Position[]; usable_as: string }
export interface TimelineEntry { when: string; what: string; doc_keys: string[] }
export interface ValueTurn { value: string; before: string; after: string; turned_by: string }
export interface ThroughLine {
  key: string
  title: string
  question: string
  face_on_the_stake: string
  value_turn: ValueTurn
  antagonism: string
  open_loop: string
  verdict_possible: string
  carried_by: string[]
  not_carried_by: string[]
  element_ids: string[]
  why: string
  single_source: boolean
}
export interface StoryMap {
  recurrences: Recurrence[]
  contradictions: Contradiction[]
  timeline: TimelineEntry[]
  through_lines: ThroughLine[]
  coverage: Record<string, Record<string, boolean>>
}
export interface ApproachRank { key: string; rank: number; why: string; carried_by: string[]; must_cut: string }
export interface ApproachSlate { ranked: ApproachRank[]; note?: string }
export interface StoryOption {
  key: string
  title: string
  viewer_will_understand: string
  viewer_will_feel: string
  viewer_will_be_able_to: string
  length_seconds: number
  through_line_key: string
  approach_key: string
  sources_used: string[]
  sources_left_out: string[]
  est_cost_usd: number
  est_minutes: number
  why: string
  risks: string[]
}
export interface StoryBrief { options: StoryOption[]; recommendation: string; why: string }
export interface Movement {
  n: number
  title: string
  job: string
  value_turn: ValueTurn
  sources: string[]
  element_ids: string[]
  entry_of: string[]
  narration_hint: string
}
export interface Motif { what: string; plant_movement: number; payoff_movement: number; element_ids: string[] }
export interface Hook { element_id: string; why: string }
export interface StorySpine {
  through_line_key: string
  approach_key: string
  movements: Movement[]
  motif: Motif
  hook: Hook
  open_loop: string
  colour_script: string
  musical_arc: string
  verdict: string
  length_seconds: number
}
export interface HandoffSource {
  doc_key: string; title: string; creators: string; year: string; publication: string; chars: number; sha256: string; text_url: string
}
export interface StoryHandoff {
  version: string
  story_job_id: string
  created_at: string
  intent: string
  audience: string
  through_line: ThroughLine
  approach: ApproachRank | null
  spine: StorySpine
  ledger: StoryElement[]
  sources: HandoffSource[]
  coverage: Record<string, boolean>
  doctrines: Record<string, string>
  totals: Record<string, unknown>
}
export interface StoryDocument {
  key: string; title: string; creators?: string; year?: string; publication?: string; library?: string; char_count?: number
}
export interface StoryOptions {
  intent?: string | null
  audience: string
  preset?: string | null
  length_seconds?: number | null
  autopilot: boolean
  from_job?: string | null
}
export interface StoryJob {
  id: string
  status: StoryStatus
  step: StoryStep | ''
  created_at: string
  updated_at: string
  sources: SourceSpec[]
  documents: StoryDocument[]
  options: StoryOptions
  profiles: StoryProfile[]
  map: StoryMap | null
  approaches: ApproachSlate | null
  brief: StoryBrief | null
  chosen_option: string | null
  spine: StorySpine | null
  handoff: StoryHandoff | null
  receipts: Receipt[]
  totals: Totals
  error?: string | null
  notes: Record<string, unknown>[]
  /** derived by the client: the first document's title (+ n more) */
  title: string
}
export interface StoryJobSummary {
  id: string
  status: StoryStatus
  step: StoryStep | ''
  created_at: string
  updated_at: string
  n_documents: number
  n_elements: number
  intent?: string | null
  chosen_option?: string | null
  cost_usd: number
}
export interface StoryDemand { engine_key: string; engine_name: string; demands: string[] }
export interface CreateStoryRequest {
  sources: SourceSpec[]
  from_job?: string
  intent?: string
  audience: string
  length_seconds?: number
  autopilot?: boolean
}
export interface CreateStoryResponse { job_id: string; status: StoryStatus; documents: StoryDocument[] }
export const FILM_LENGTHS = [60, 90, 120, 180, 240] as const
