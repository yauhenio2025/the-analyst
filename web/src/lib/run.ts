/* The run model — derives everything the rail and the console show from
   recorded facts: the job's status and the event ledger. No guessing: a
   step is "done" because a phase_finished event exists or the job's status
   has moved past it. */
import type { DossierJob, DossierStatus, RunEvent } from '../types'
import { statusRank } from '../types'

export interface RailStep { n: number; key: DossierStatus; label: string }

export const RAIL_STEPS: RailStep[] = [
  { n: 1, key: 'reconnaissance', label: 'Read the documents' },
  { n: 2, key: 'awaiting_brief', label: 'The brief' },
  { n: 3, key: 'planning', label: 'Plan the analysis' },
  { n: 4, key: 'analysis', label: 'Run the analysis' },
  { n: 5, key: 'tables', label: 'Build the tables' },
  { n: 6, key: 'figures', label: 'Draw the figures' },
  { n: 7, key: 'composing', label: 'Compose the dossier' },
  { n: 8, key: 'done', label: 'Delivered' },
]

export type PipState = 'pending' | 'running' | 'done' | 'failed' | 'waiting'

const RAIL_KEYS = new Set<string>(RAIL_STEPS.map((s) => s.key))

/** Which rail step an event belongs to. Dossier-level events carry the
 * status name in `phase`; mirrored analysis sub-job events carry the
 * executor phase name — those fold into "Run the analysis". */
export function stepOfEvent(e: RunEvent): DossierStatus | null {
  if (e.phase && RAIL_KEYS.has(e.phase)) return e.phase as DossierStatus
  if (e.kind === 'job_finished') return 'done'
  if (e.engine || e.chain || e.pass_name || e.phase) return 'analysis'
  return null
}

export interface RailStepModel {
  step: RailStep
  state: PipState
  narration: string | null
  detail: string | null
  lastCall: RunEvent | null
  cost: number
  calls: number
}

export interface RailModel {
  steps: RailStepModel[]
  activeIndex: number
  cost: number
  calls: number
  inputTokens: number
  outputTokens: number
  narration: string | null
  lastCall: RunEvent | null
  failed: boolean
}

export function buildRail(job: DossierJob | null, events: RunEvent[]): RailModel {
  const status = job?.status ?? null
  const rank = statusRank(status)
  const failed = status === 'failed' || events.some((e) => e.kind === 'job_failed')
  const started = new Set<string>()
  const finished = new Set<string>()
  const failedIn = new Set<string>()
  for (const e of events) {
    const k = stepOfEvent(e)
    if (!k) continue
    if (e.kind === 'phase_started' || e.kind === 'call_started' || e.kind === 'chain_started') started.add(k)
    if (e.kind === 'phase_finished') finished.add(k)
    if (e.kind === 'job_failed' || e.kind === 'call_failed') failedIn.add(k)
    if (e.kind === 'job_finished') { finished.add('done'); finished.add(k) }
  }
  let activeIndex = -1
  const steps = RAIL_STEPS.map((step, i): RailStepModel => {
    const mine = events.filter((e) => stepOfEvent(e) === step.key)
    const calls = mine.filter((e) => e.kind === 'call_finished')
    const narrationEv = [...mine].reverse().find((e) => e.narrator)
    const detailEv = [...mine].reverse().find((e) => e.detail)
    const lastCall = [...mine].reverse().find((e) => e.kind === 'call_finished' || e.kind === 'call_started' || e.kind === 'call_failed') ?? null
    let state: PipState = 'pending'
    const r = statusRank(step.key)
    if (failedIn.has(step.key)) state = 'failed'
    else if (finished.has(step.key) || (rank > r && !failed) || (status === 'done')) state = 'done'
    else if (started.has(step.key) || rank === r) {
      state = step.key === 'awaiting_brief' && status === 'awaiting_brief' ? 'waiting' : 'running'
    }
    if (status === 'awaiting_brief' && step.key === 'awaiting_brief' && !job?.chosen_option) state = 'waiting'
    if (failed && state === 'running') state = 'failed'
    if (state === 'running' || state === 'waiting' || state === 'failed') activeIndex = i
    return {
      step, state,
      narration: narrationEv?.narrator ?? null,
      detail: detailEv?.detail ?? null,
      lastCall,
      cost: calls.reduce((n, e) => n + (e.cost_usd ?? 0), 0),
      calls: calls.length,
    }
  })
  if (activeIndex === -1) activeIndex = status === 'done' ? RAIL_STEPS.length - 1 : Math.max(0, steps.findIndex((s) => s.state === 'pending') - 1)
  const allCalls = events.filter((e) => e.kind === 'call_finished')
  const lastNarr = [...events].reverse().find((e) => e.narrator)
  const lastCallAny = [...events].reverse().find((e) => e.kind === 'call_finished' || e.kind === 'call_started' || e.kind === 'call_failed') ?? null
  const evCost = allCalls.reduce((n, e) => n + (e.cost_usd ?? 0), 0)
  return {
    steps, activeIndex,
    cost: Math.max(evCost, job?.totals?.cost_usd ?? 0),
    calls: Math.max(allCalls.length, job?.totals?.calls ?? 0),
    inputTokens: Math.max(allCalls.reduce((n, e) => n + (e.input_tokens ?? 0), 0), job?.totals?.input_tokens ?? 0),
    outputTokens: Math.max(allCalls.reduce((n, e) => n + (e.output_tokens ?? 0), 0), job?.totals?.output_tokens ?? 0),
    narration: lastNarr?.narrator ?? null,
    lastCall: lastCallAny,
    failed,
  }
}

/* ---------- the console tree: phases → chains → engines → passes → calls */

export type TreeLevel = 'phase' | 'chain' | 'engine' | 'pass' | 'call'

export interface TreeNode {
  id: string
  level: TreeLevel
  label: string
  sub?: string
  state: PipState
  children: TreeNode[]
  events: RunEvent[]
  cost: number
  calls: number
  model?: string | null
  narrations: string[]
}

function stateOf(events: RunEvent[], children: TreeNode[], startKinds: string[], endKinds: string[]): PipState {
  if (events.some((e) => e.kind === 'call_failed' || e.kind === 'job_failed') || children.some((c) => c.state === 'failed')) return 'failed'
  if (events.some((e) => endKinds.includes(e.kind))) return 'done'
  if (children.some((c) => c.state === 'running')) return 'running'
  if (children.length && children.every((c) => c.state === 'done')) {
    return events.some((e) => startKinds.includes(e.kind)) && !events.some((e) => endKinds.includes(e.kind)) && children.length === 0 ? 'running' : 'done'
  }
  if (events.some((e) => startKinds.includes(e.kind))) return 'running'
  return 'pending'
}

function group<T>(items: T[], key: (t: T) => string): Map<string, T[]> {
  const m = new Map<string, T[]>()
  for (const it of items) {
    const k = key(it)
    const arr = m.get(k)
    if (arr) arr.push(it); else m.set(k, [it])
  }
  return m
}

const sumCost = (ev: RunEvent[]) => ev.filter((e) => e.kind === 'call_finished').reduce((n, e) => n + (e.cost_usd ?? 0), 0)
const countCalls = (ev: RunEvent[]) => ev.filter((e) => e.kind === 'call_finished' || e.kind === 'call_failed').length

export function buildTree(events: RunEvent[], phaseLabel?: (phase: string) => string): TreeNode[] {
  const byPhase = group(events, (e) => e.phase ?? (e.kind === 'job_finished' ? 'done' : e.kind === 'job_started' ? 'start' : 'other'))
  const phases: TreeNode[] = []
  for (const [phase, pev] of byPhase) {
    const phaseId = `p:${phase}`
    const chains: TreeNode[] = []
    const byChain = group(pev.filter((e) => e.engine || e.chain), (e) => e.chain ?? '')
    for (const [chain, cev] of byChain) {
      const chainId = chain ? `${phaseId}/c:${chain}` : phaseId
      const engines: TreeNode[] = []
      const byEngine = group(cev.filter((e) => e.engine), (e) => e.engine!)
      for (const [engine, eev] of byEngine) {
        const engineId = `${chainId}/e:${engine}`
        const passes: TreeNode[] = []
        const byPass = group(eev, (e) => e.pass_name ?? 'pass')
        for (const [pass, psev] of byPass) {
          const passId = `${engineId}/s:${pass}`
          const calls: TreeNode[] = []
          let open: RunEvent[] = []
          const flush = () => {
            if (!open.length) return
            const st = open.find((e) => e.kind === 'call_started')
            const fin = open.find((e) => e.kind === 'call_finished' || e.kind === 'call_failed')
            const ref = fin ?? st ?? open[0]
            calls.push({
              id: `${passId}/k:${ref.seq}`, level: 'call',
              label: `call · ${ref.model ?? st?.model ?? '—'}`,
              sub: ref.work_key ?? undefined,
              state: fin ? (fin.kind === 'call_failed' ? 'failed' : 'done') : st ? 'running' : 'pending',
              children: [], events: open, cost: sumCost(open), calls: countCalls(open),
              model: ref.model ?? st?.model, narrations: [],
            })
            open = []
          }
          for (const e of psev) {
            if (e.kind === 'call_started') { flush(); open.push(e) }
            else if (e.kind === 'call_finished' || e.kind === 'call_failed') { open.push(e); flush() }
            else open.push(e)
          }
          flush()
          const st = psev.find((e) => e.stance)?.stance
          passes.push({
            id: passId, level: 'pass', label: pass, sub: st ?? undefined,
            state: stateOf([], calls, [], []),
            children: calls, events: psev, cost: sumCost(psev), calls: countCalls(psev),
            model: psev.find((e) => e.model)?.model, narrations: [],
          })
        }
        engines.push({
          id: engineId, level: 'engine', label: engine.replace(/_/g, ' '), sub: undefined,
          state: stateOf([], passes, [], []),
          children: passes, events: eev, cost: sumCost(eev), calls: countCalls(eev),
          model: eev.find((e) => e.model)?.model, narrations: [],
        })
      }
      if (chain) {
        chains.push({
          id: chainId, level: 'chain', label: chain.replace(/_/g, ' '),
          state: stateOf(cev, engines, ['chain_started'], ['chain_finished']),
          children: engines, events: cev, cost: sumCost(cev), calls: countCalls(cev),
          narrations: [],
        })
      } else {
        chains.push(...engines)
      }
    }
    const label = phaseLabel ? phaseLabel(phase) : phase
    phases.push({
      id: phaseId, level: 'phase', label,
      state: stateOf(pev, chains, ['phase_started', 'job_started', 'call_started'], ['phase_finished', 'job_finished']),
      children: chains, events: pev, cost: sumCost(pev), calls: countCalls(pev),
      narrations: pev.filter((e) => e.narrator).map((e) => e.narrator!),
    })
  }
  return phases
}

export function findNode(nodes: TreeNode[], id: string): TreeNode | null {
  for (const n of nodes) {
    if (n.id === id) return n
    const hit = findNode(n.children, id)
    if (hit) return hit
  }
  return null
}

export function activeNodeId(nodes: TreeNode[]): string | null {
  for (const n of nodes) {
    if (n.state === 'running' || n.state === 'failed') {
      const deeper = activeNodeId(n.children)
      return deeper ?? n.id
    }
  }
  return null
}

export const KIND_TONE: Record<string, string> = {
  job_started: 'flat', job_finished: 'ok', job_failed: 'neg',
  phase_started: 'accent', phase_finished: 'ok',
  chain_started: 'accent', chain_finished: 'ok',
  call_started: 'live', call_finished: 'ok', call_failed: 'neg',
  narration: 'ink', artifact: 'accent', note: 'flat',
}
