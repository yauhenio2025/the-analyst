/* Under the hood — /console/:id. Header (job, status, totals); left: the
   phase tree with live pips; centre: the selected node's prompt | output,
   model, tokens, cost, duration; top strip: the planner's rationale and the
   alternatives it rejected; bottom: the timeline, one row per event.
   "Executive view" hides hashes and JSON and keeps narration, step names
   and cost. Everything here is a recorded event or a stored plan. */
import { useEffect, useMemo, useState } from 'react'
import { api } from '../lib/api'
import { useEvents, useJob } from '../lib/hooks'
import { activeNodeId, buildRail, buildTree, findNode, KIND_TONE, type TreeNode } from '../lib/run'
import { duration, statusLabel, timeShort, tokens, usd } from '../lib/format'
import { Pip, RunRail } from '../components/RunRail'
import { StatusChip } from '../components/StatusChip'
import { Record } from '../components/Record'
import { consolePath, dossierPath, navigate } from '../router'
import type { DossierJob, ExecutorJob, OrchestratorPlan, RunEvent } from '../types'
import { STATUS_LABEL } from '../lib/format'

function TreeRow({ node, depth, selected, onSelect, exec }: {
  node: TreeNode; depth: number; selected: string | null; onSelect: (id: string) => void; exec: boolean
}) {
  const [open, setOpen] = useState(node.state === 'running' || node.state === 'failed' || node.level === 'phase' || node.level === 'chain' || node.level === 'engine')
  useEffect(() => { if (node.state === 'running' || node.state === 'failed') setOpen(true) }, [node.state])
  const children = exec ? [] : node.children
  return (
    <li className={`tree-node level-${node.level} is-${node.state}${selected === node.id ? ' on' : ''}`} data-node={node.id}>
      <div className="tree-row" style={{ paddingLeft: `${depth * 14}px` }}>
        {children.length > 0 ? (
          <button className="tree-toggle" aria-label={open ? 'collapse' : 'expand'} onClick={() => setOpen(!open)}>{open ? '−' : '+'}</button>
        ) : <span className="tree-toggle" aria-hidden="true">·</span>}
        <Pip state={node.state} />
        <button className="tree-label" onClick={() => onSelect(node.id)}>
          <span className="tree-name">{node.label}</span>
          {node.sub && <span className="machine tree-sub">{node.sub}</span>}
        </button>
        <span className="machine tree-cost">{node.calls > 0 ? `${node.calls} · ${usd(node.cost)}` : ''}</span>
      </div>
      {open && children.length > 0 && (
        <ul>{children.map((c) => <TreeRow key={c.id} node={c} depth={depth + 1} selected={selected} onSelect={onSelect} exec={exec} />)}</ul>
      )}
    </li>
  )
}

function NodeDetail({ node, exec }: { node: TreeNode; exec: boolean }) {
  const st = [...node.events].reverse().find((e) => e.kind === 'call_started')
  const fin = [...node.events].reverse().find((e) => e.kind === 'call_finished' || e.kind === 'call_failed')
  const ref = fin ?? st
  // The prompt rides the call_started event; the output rides call_finished.
  const prompt = ref?.prompt_excerpt ?? st?.prompt_excerpt ?? null
  const hash = ref?.prompt_hash ?? st?.prompt_hash ?? null
  const phaseEnd = node.events.find((e) => e.kind === 'phase_finished' || e.kind === 'chain_finished')
  return (
    <div className="node-detail" data-node-detail>
      <div className="node-head">
        <span className="eyebrow eyebrow-accent">{node.level}</span>
        <h3>{node.label}{node.sub ? <span className="machine"> · {node.sub}</span> : null}</h3>
        <StatusChip status={node.state === 'done' ? 'done' : node.state === 'failed' ? 'failed' : node.state === 'running' ? 'analysis' : 'queued'}
                    label={node.state} />
      </div>
      <Record columns={4} tiles={[
        { num: ref?.model ?? node.model ?? '—', label: 'model' },
        { num: `${tokens(ref?.input_tokens ?? undefined)} / ${tokens(ref?.output_tokens ?? undefined)}`, label: 'tokens in / out' },
        { num: usd(node.level === 'call' ? ref?.cost_usd : node.cost), label: node.level === 'call' ? 'cost of this call' : `cost · ${node.calls} calls` },
        { num: duration(ref?.duration_ms ?? phaseEnd?.duration_ms ?? undefined), label: 'duration' },
      ]} />
      {node.narrations.length > 0 && (
        <div className="quotecard">
          {node.narrations.map((n, i) => <blockquote key={i}>{n}</blockquote>)}
          <cite className="machine">the narrator, as the step ran</cite>
        </div>
      )}
      {(prompt || ref?.output_excerpt) && (
        <div className="excerpts">
          <div className="excerpt">
            <span className="eyebrow">prompt{!exec && hash ? ` · ${hash}` : ''}</span>
            <pre>{prompt ?? '—'}</pre>
          </div>
          <div className="excerpt">
            <span className="eyebrow">output{ref?.output_chars ? ` · ${ref.output_chars.toLocaleString()} chars` : ''}</span>
            <pre>{ref?.output_excerpt ?? (st && !fin ? 'waiting for the model…' : '—')}</pre>
          </div>
        </div>
      )}
      {!exec && node.events.some((e) => e.detail || e.payload_json) && (
        <details className="more">
          <summary>every event on this node · {node.events.length}</summary>
          <ul className="eventlist">
            {node.events.map((e) => (
              <li key={`${e.job_id}-${e.seq}`}>
                <span className="machine">{e.seq} · {timeShort(e.ts)}</span>
                <span className={`kind tone-${KIND_TONE[e.kind] ?? 'flat'}`}>{e.kind}</span>
                <span>{e.detail ?? e.narrator ?? ''}</span>
                {e.payload_json && <code className="payload">{e.payload_json}</code>}
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  )
}

export function Console({ id, node: nodeParam, exec }: { id: string; node: string | null; exec: boolean }) {
  const { job, error } = useJob(id)
  const isDossier = job !== null
  const [execJob, setExecJob] = useState<ExecutorJob | null>(null)
  const [plan, setPlan] = useState<OrchestratorPlan | null>(null)
  const live = !job || (job.status !== 'done' && job.status !== 'failed')
  const events = useEvents(id, live)
  const subId = job?.analysis_job_id ?? null
  const subEvents = useEvents(subId, live)

  // Not a dossier job? Then it may be a bare executor job.
  useEffect(() => {
    if (job || !error) return
    api.executorJob(id).then(setExecJob).catch(() => setExecJob(null))
  }, [id, job, error])
  useEffect(() => {
    if (!subId) return
    const t = window.setInterval(() => api.executorJob(subId).then(setExecJob).catch(() => {}), live ? 3000 : 3600e3)
    api.executorJob(subId).then(setExecJob).catch(() => {})
    return () => window.clearInterval(t)
  }, [subId, live])
  const planId = job?.plan_id ?? execJob?.plan_id ?? null
  useEffect(() => {
    if (!planId) return
    api.plan(planId).then(setPlan).catch(() => setPlan(null))
  }, [planId])

  const merged = useMemo(() => {
    const seen = new Set(events.map((e) => `${e.phase}|${e.kind}|${e.engine}|${e.pass_name}|${e.ts}`))
    const extra = subEvents.filter((e) => !seen.has(`${'analysis'}|${e.kind}|${e.engine}|${e.pass_name}|${e.ts}`))
    return [...events, ...extra.map((e) => ({ ...e, seq: e.seq + 100000 }))].sort((a, b) => Date.parse(a.ts) - Date.parse(b.ts) || a.seq - b.seq)
  }, [events, subEvents])

  const phaseNames = useMemo(() => {
    const m: Record<string, string> = { ...STATUS_LABEL, start: 'Started', other: 'Notes' }
    for (const p of plan?.phases ?? []) m[String(p.phase_number)] = p.phase_name
    return m
  }, [plan])
  const tree = useMemo(() => buildTree(events.length ? events : subEvents, (p) => phaseNames[p] ?? p), [events, subEvents, phaseNames])
  const subTree = useMemo(() => (events.length && subEvents.length) ? buildTree(subEvents, (p) => phaseNames[p] ?? p) : [], [events, subEvents, phaseNames])
  const allTree = useMemo(() => {
    if (!subTree.length) return tree
    // Graft the mirrored analysis sub-job under "Run the analysis".
    return tree.map((p) => p.id === 'p:analysis' ? { ...p, children: subTree } : p)
  }, [tree, subTree])

  const selectedId = nodeParam ?? activeNodeId(allTree) ?? allTree[0]?.id ?? null
  const selected = selectedId ? findNode(allTree, selectedId) : null
  const select = (nid: string) => navigate(consolePath(id, `?node=${encodeURIComponent(nid)}${exec ? '&view=executive' : ''}`), { replace: true })
  const toggleExec = () => navigate(consolePath(id, `${selectedId ? `?node=${encodeURIComponent(selectedId)}` : '?'}${exec ? '' : `${selectedId ? '&' : ''}view=executive`}`), { replace: true })

  const rail = useMemo(() => buildRail(job, events), [job, events])
  const rationale = plan?.strategy_rationale ?? plan?.decision_trace?.overall_strategy_rationale ?? plan?.strategy_summary ?? null
  const alternatives = plan?.alternatives_considered
    ?? plan?.decision_trace?.phase_decisions?.flatMap((d) => (d.alternatives_considered ?? []).map((a) => d.phase_name ? `${d.phase_name}: ${a}` : a))
    ?? []

  const totals = job?.totals ?? (execJob ? {
    calls: execJob.total_llm_calls ?? 0, input_tokens: execJob.total_input_tokens ?? 0,
    output_tokens: execJob.total_output_tokens ?? 0, cost_usd: execJob.total_cost_estimate ?? 0, duration_ms: 0,
  } : null)
  const status = job?.status ?? execJob?.status ?? null
  const title = job?.title ?? (execJob ? `${execJob.workflow_key ?? 'workflow'} · ${execJob.job_id}` : id)

  const timeline: RunEvent[] = exec
    ? merged.filter((e) => e.narrator || e.kind === 'phase_started' || e.kind === 'phase_finished' || e.kind === 'job_finished' || e.kind === 'job_failed')
    : merged

  return (
    <section className="console" data-console>
      <div className="console-head">
        <div>
          <span className="eyebrow">under the hood · {isDossier ? 'dossier job' : execJob ? 'executor job' : 'job'} · <b>{id}</b></span>
          <h2 className="display">{title}</h2>
          <div className="console-status">
            <StatusChip status={status} label={status ? (isDossier ? statusLabel(status) : status) : 'loading'} />
            {execJob && isDossier && <span className="machine">analysis sub-job · {execJob.job_id} · {execJob.status} · phase {execJob.progress?.current_phase ?? 0} of {execJob.progress?.total_phases ?? '—'}</span>}
            {isDossier && <a className="linkish" href={dossierPath(id, job.status === 'done' ? 'dossier' : 'draft')}>← back to the dossier</a>}
          </div>
        </div>
        <div className="console-tools">
          <button className={`mode-btn${!exec ? ' on' : ''}`} aria-pressed={!exec} onClick={() => exec && toggleExec()} data-view="full">Full record</button>
          <button className={`mode-btn${exec ? ' on' : ''}`} aria-pressed={exec} onClick={() => !exec && toggleExec()} data-view="executive">Executive view</button>
        </div>
      </div>

      {error && !execJob && <div className="error-box" title={error}>No dossier or executor job answers to “{id}”.</div>}

      {totals && (
        <Record tiles={[
          { num: usd(Math.max(totals.cost_usd, rail.cost)), label: 'spent' },
          { num: String(Math.max(totals.calls, rail.calls)), label: 'model calls' },
          { num: `${tokens(Math.max(totals.input_tokens, rail.inputTokens))} / ${tokens(Math.max(totals.output_tokens, rail.outputTokens))}`, label: 'tokens in / out' },
          { num: duration(totals.duration_ms || (merged.length > 1 ? Date.parse(merged[merged.length - 1].ts) - Date.parse(merged[0].ts) : 0)), label: 'elapsed' },
        ]} />
      )}

      {(rationale || alternatives.length > 0) && (
        <details className="panel strategy" open data-strategy>
          <summary className="eyebrow">the planner's reasoning{plan?.plan_id ? ` · ${plan.plan_id}` : ''}</summary>
          <div className="strategy-body">
            {rationale && (
              <div>
                <span className="eyebrow eyebrow-accent">why this plan</span>
                <p>{rationale}</p>
              </div>
            )}
            {alternatives.length > 0 && (
              <div>
                <span className="eyebrow eyebrow-accent">considered and set aside</span>
                <ul className="alts">{alternatives.map((a, i) => <li key={i}>{a}</li>)}</ul>
              </div>
            )}
          </div>
        </details>
      )}

      <div className={`console-grid${exec ? ' exec' : ''}`}>
        <aside className="console-tree panel">
          <span className="eyebrow">{exec ? 'the steps' : 'phases → chains → engines → passes → calls'}</span>
          {isDossier && exec ? (
            <RunRail job={job} events={events} model={rail} />
          ) : (
            <ul className="tree" data-tree>
              {allTree.map((n) => <TreeRow key={n.id} node={n} depth={0} selected={selectedId} onSelect={select} exec={exec} />)}
              {allTree.length === 0 && <li className="hint">No events recorded yet.</li>}
            </ul>
          )}
        </aside>
        <div className="console-detail panel">
          {selected ? <NodeDetail node={selected} exec={exec} /> : <p className="hint">Select a node on the left.</p>}
        </div>
      </div>

      <div className="section-head">
        <h3>Timeline</h3>
        <span className="eyebrow">{timeline.length} events · by seq</span>
      </div>
      <div className="table-scroll">
        <table className="desk-table timeline" data-timeline>
          <thead><tr><th>#</th><th>When</th><th>Kind</th><th>Step</th><th>What</th>{!exec && <th className="r">Cost</th>}</tr></thead>
          <tbody>
            {timeline.map((e) => (
              <tr key={`${e.job_id}-${e.seq}`} className={`tone-${KIND_TONE[e.kind] ?? 'flat'}`}>
                <td className="machine">{e.seq > 100000 ? `↳${e.seq - 100000}` : e.seq}</td>
                <td className="machine">{timeShort(e.ts)}</td>
                <td><span className={`kind tone-${KIND_TONE[e.kind] ?? 'flat'}`}>{e.kind.replace(/_/g, ' ')}</span></td>
                <td>{e.phase ? (phaseNames[e.phase] ?? e.phase) : '—'}{e.engine ? <span className="machine"> · {e.engine.replace(/_/g, ' ')}{e.pass_name ? ` · ${e.pass_name}` : ''}</span> : null}</td>
                <td>
                  {e.narrator ? <span className="narration-inline">{e.narrator}</span> : (e.detail ?? (e.kind === 'call_finished' ? `${e.model ?? ''} · ${tokens(e.input_tokens)} in / ${tokens(e.output_tokens)} out` : e.kind === 'call_started' ? `${e.model ?? ''} · ${e.input_chars ? `${e.input_chars.toLocaleString()} chars` : ''}` : ''))}
                </td>
                {!exec && <td className="r machine">{e.cost_usd !== undefined && e.cost_usd !== null && e.kind !== 'phase_finished' && e.kind !== 'chain_finished' ? usd(e.cost_usd) : ''}</td>}
              </tr>
            ))}
            {timeline.length === 0 && <tr><td colSpan={6} className="hint">Nothing recorded yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export type { DossierJob }
