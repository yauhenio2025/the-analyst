/* CatalogPicker — the competent user's lane (design §C5): the executable engines
   grouped by PURPOSE ("Test a position", "See the structure", …) with "use when
   you need to…" and "yields…" one-liners, depth chips priced on this corpus,
   recipes (pre-composed paths), the engines that are off for this corpus greyed
   with their reason, and "Your path" — ordered steps with a depth each and a
   running estimate. Used by the Library (lane 2) and by the brief step
   ("how ▸ edit", "I know the analysis I want ▸"). */
import { useMemo, useState } from 'react'
import { minutes, usd } from '../lib/format'
import type { Catalog, CatalogEngine, StepDepth } from '../types'

export interface PickedStep { engine_key: string; depth: StepDepth }

const DEPTHS: StepDepth[] = ['surface', 'standard', 'deep']

/** Client-side price of a path from the catalog's per-depth estimates (the server confirms on choose). */
export function estimatePath(catalog: Catalog | null, steps: PickedStep[]): { cost: number; minutes: number; calls: number } | null {
  if (!catalog || !catalog.corpus_chars) return null
  const engines = new Map(catalog.groups.flatMap((g) => g.engines.map((e) => [e.engine_key, e] as const)))
  let cost = catalog.own_overhead?.est_cost_usd ?? 0
  let mins = catalog.own_overhead?.est_minutes ?? 0
  let calls = catalog.own_overhead?.calls ?? 4
  for (const s of steps) {
    const d = engines.get(s.engine_key)?.depths[s.depth] ?? engines.get(s.engine_key)?.depths.surface
    if (!d) continue
    cost += d.est_cost_usd ?? 0
    mins += d.est_minutes ?? 0
    calls += d.passes
  }
  return { cost: Math.round(cost * 100) / 100, minutes: Math.round(mins * 10) / 10, calls }
}

export function pathDepth(catalog: Catalog | null, steps: PickedStep[]): 'simple' | 'medium' | 'advanced' {
  const engines = new Map((catalog?.groups ?? []).flatMap((g) => g.engines.map((e) => [e.engine_key, e] as const)))
  const passes = steps.reduce((n, s) => n + (engines.get(s.engine_key)?.depths[s.depth]?.passes ?? 1), 0)
  if (steps.length <= 1 && passes <= 1) return 'simple'
  if (steps.length <= 3 && passes <= 4) return 'medium'
  return 'advanced'
}

export function CatalogPicker({ catalog, loading, error, steps, onChange, onDone, doneLabel = 'Use this path', onCancel }: {
  catalog: Catalog | null
  loading?: boolean
  error?: string | null
  steps: PickedStep[]
  onChange: (steps: PickedStep[]) => void
  onDone?: () => void
  doneLabel?: string
  onCancel?: () => void
}) {
  const [tab, setTab] = useState<string>('recipes')
  const [q, setQ] = useState('')
  const groups = catalog?.groups ?? []
  const all = useMemo(() => groups.flatMap((g) => g.engines.map((e) => ({ ...e, group: g.title }))), [groups])
  const byKey = useMemo(() => new Map(all.map((e) => [e.engine_key, e])), [all])
  const query = q.trim().toLowerCase()
  const listed: (CatalogEngine & { group: string })[] = query
    ? all.filter((e) => [e.plain_name, e.engine_name, e.use_when, e.yields, e.engine_key].join(' ').toLowerCase().includes(query))
    : (groups.find((g) => g.key === tab)?.engines ?? []).map((e) => ({ ...e, group: tab }))
  const est = estimatePath(catalog, steps)
  const has = (k: string) => steps.some((s) => s.engine_key === k)
  const add = (e: CatalogEngine) => { if (!has(e.engine_key) && steps.length < 4) onChange([...steps, { engine_key: e.engine_key, depth: 'surface' }]) }
  const move = (i: number, d: -1 | 1) => {
    const j = i + d
    if (j < 0 || j >= steps.length) return
    const next = [...steps]; [next[i], next[j]] = [next[j], next[i]]; onChange(next)
  }
  const nameOf = (k: string) => byKey.get(k)?.plain_name ?? k.replace(/_/g, ' ')
  const price = (e: CatalogEngine, d: string) => { const x = e.depths[d]; return x ? `${x.passes}p${x.est_cost_usd !== undefined ? ` · ${usd(x.est_cost_usd, true)}` : ''}` : '' }

  return (
    <div className="picker" data-picker>
      <div className="picker-rail">
        <input className="picker-search" placeholder="search the catalog" value={q} onChange={(e) => setQ(e.target.value)} data-picker-search />
        <button type="button" className={`mode-btn${tab === 'recipes' && !query ? ' on' : ''}`} onClick={() => { setTab('recipes'); setQ('') }}>recipes · {catalog?.recipes.length ?? 0}</button>
        {groups.map((g) => (
          <button key={g.key} type="button" className={`mode-btn${tab === g.key && !query ? ' on' : ''}`} onClick={() => { setTab(g.key); setQ('') }} title={g.purpose} data-picker-group={g.key}>
            {g.title} · {g.engines.length}
          </button>
        ))}
        {catalog && catalog.excluded.length > 0 && (
          <details className="picker-excluded">
            <summary className="hint">not for a document dossier · {catalog.excluded.length}</summary>
            <ul className="machine">{catalog.excluded.map((x) => <li key={x.engine_key}><b>{x.engine_key.replace(/_/g, ' ')}</b> — {x.why}</li>)}</ul>
          </details>
        )}
      </div>

      <div className="picker-list">
        {loading && <p className="hint"><span className="spinner" /> loading the catalog…</p>}
        {error && <div className="error-box" title={error}>{error}</div>}
        {!loading && catalog && tab === 'recipes' && !query && (
          <ul className="recipes">
            {catalog.recipes.map((r) => (
              <li key={r.key} className="recipe">
                <div className="recipe-main">
                  <b className="recipe-title">{r.title}</b>
                  <span className="hint"> — {r.use_when}</span>
                  <p className="machine">{r.steps.map((s) => `${s.plain_name || nameOf(s.engine_key)}@${s.depth}`).join(' → ')} · yields {r.yields}</p>
                </div>
                <div className="recipe-side">
                  {r.est_cost_usd > 0 && <span className="machine">{usd(r.est_cost_usd, true)} · {minutes(r.est_minutes)}</span>}
                  <button type="button" className="secondary" onClick={() => onChange(r.steps.map((s) => ({ engine_key: s.engine_key, depth: s.depth })))} data-recipe={r.key}>use this path</button>
                </div>
              </li>
            ))}
          </ul>
        )}
        {!loading && catalog && (tab !== 'recipes' || query) && (
          <>
            {query && listed.length === 0 && <p className="hint">Nothing in the catalog matches “{q}”.</p>}
            <ul className="engines">
              {listed.map((e) => {
                const off = e.fit === 'off' || e.fit === 'not_for_dossier'
                const added = has(e.engine_key)
                return (
                  <li key={e.engine_key} className={`engine${off ? ' off' : ''}${added ? ' added' : ''}`} data-engine={e.engine_key}>
                    <div className="engine-main">
                      <b className="engine-name">{e.plain_name}</b>
                      {e.plain_name !== e.engine_name && <span className="hint"> · {e.engine_name}</span>}
                      {query && <span className="hint"> · {e.group}</span>}
                      <p className="engine-when">use when you need to {e.use_when}</p>
                      <p className="engine-yields machine">yields {e.yields}{e.row_unit ? ` · ${e.row_unit}` : ''}</p>
                      <p className="machine engine-depths">{DEPTHS.filter((d) => e.depths[d]).map((d) => <span key={d} className="engchip">{d} {price(e, d)}</span>)}
                        {e.pairs_with.length > 0 && <span className="hint"> pairs with {e.pairs_with.map((p) => nameOf(p)).join(', ')}</span>}</p>
                      {e.fit !== 'ok' && <p className={`hint fit fit-${e.fit}`}>{e.fit === 'off' ? 'off for this corpus' : 'conditional'}{e.fit_note ? ` — ${e.fit_note}` : ''}</p>}
                    </div>
                    <button type="button" className="secondary" disabled={off || added || steps.length >= 4} onClick={() => add(e)} data-add={e.engine_key}>
                      {added ? 'in your path' : off ? 'off' : 'add'}
                    </button>
                  </li>
                )
              })}
            </ul>
          </>
        )}
      </div>

      <div className="picker-path" data-picker-path>
        <span className="eyebrow">your path · {steps.length} of 4</span>
        {steps.length === 0 && <p className="hint">Add engines in run order, or start from a recipe. Each later step reads the earlier ones.</p>}
        <ol className="path-steps">
          {steps.map((s, i) => (
            <li key={`${s.engine_key}-${i}`} className="path-step" data-path-step={s.engine_key}>
              <span className="path-n machine">{i + 1}</span>
              <span className="path-name">{nameOf(s.engine_key)}<span className="hint machine"> · {s.engine_key}</span></span>
              <select value={s.depth} onChange={(e) => onChange(steps.map((x, j) => (j === i ? { ...x, depth: e.target.value as StepDepth } : x)))} aria-label="depth">
                {DEPTHS.filter((d) => (byKey.get(s.engine_key)?.depths[d] ?? true)).map((d) => <option key={d} value={d}>{d}{byKey.get(s.engine_key) ? ` · ${price(byKey.get(s.engine_key)!, d)}` : ''}</option>)}
              </select>
              <span className="path-ctl">
                <button type="button" className="linkish" onClick={() => move(i, -1)} disabled={i === 0} aria-label="earlier">↑</button>
                <button type="button" className="linkish" onClick={() => move(i, 1)} disabled={i === steps.length - 1} aria-label="later">↓</button>
                <button type="button" className="linkish" onClick={() => onChange(steps.filter((_, j) => j !== i))} aria-label="remove">✕</button>
              </span>
            </li>
          ))}
        </ol>
        <p className="machine path-est" data-path-est>
          {!steps.length ? ' ' : est ? <><b>{usd(est.cost, true)}</b> · {minutes(est.minutes)} · {est.calls} calls · {pathDepth(catalog, steps)}</> : `${pathDepth(catalog, steps)} · priced once the corpus is known`}
        </p>
        <p className="hint">The brief will say what this path lets you understand and do, and propose one alternative.</p>
        <div className="actions">
          {onDone && <button type="button" className="primary" disabled={steps.length === 0} onClick={onDone} data-picker-done>{doneLabel}</button>}
          {onCancel && <button type="button" className="secondary" onClick={onCancel}>cancel</button>}
        </div>
      </div>
    </div>
  )
}
