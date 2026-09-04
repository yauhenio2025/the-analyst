/* Station 5 · Spine — the movements as a current: numbered stations left to
   right, each source a tributary entering at the movement it enters; then the
   movement cards with their value turns, sources, cited elements (click to
   reveal the text and its verbatim anchor) and narration hints; the motif
   (plant → payoff), the hook, the open loop, the colour script, the musical
   arc, the verdict. Every id resolves to a profile's element. */
import { useMemo, useState } from 'react'
import { approachLabel, docHandle, docTitle, elementIndex, seconds, storyStatusLabel, type ElementRef, type StoryRailModel } from '../lib/story'
import { storyPath } from '../router'
import { ElementRow } from './StoryReading'
import { ValueTurnView } from './StoryMap'
import type { StoryJob, StorySpine as Spine } from '../types'

const GAP = 200
const PAD = 100
const LANE0 = 26
const LANE = 20

/* The current: stations on a baseline; tributaries curve in from above at
   the movement each source enters; the motif runs under the baseline from
   its plant to its payoff. Tokens only — colours come from styles.css. */
function Current({ job, spine }: { job: StoryJob; spine: Spine }) {
  const mv = spine.movements
  const n = Math.max(1, mv.length)
  const W = n * GAP
  const entries = job.documents
    .map((d) => {
      let k = mv.findIndex((m) => m.entry_of.includes(d.key))
      if (k < 0) k = mv.findIndex((m) => m.sources.includes(d.key))
      return { key: d.key, k }
    })
    .filter((e) => e.k >= 0)
    .sort((a, b) => a.k - b.k)
  const baseY = LANE0 + entries.length * LANE + 44
  const motif = spine.motif && spine.motif.what && spine.motif.plant_movement !== spine.motif.payoff_movement
    && mv.some((m) => m.n === spine.motif.plant_movement) && mv.some((m) => m.n === spine.motif.payoff_movement)
  const H = baseY + (motif ? 78 : 30)
  const xOf = (i: number) => PAD + i * GAP
  const xOfN = (num: number) => xOf(Math.max(0, mv.findIndex((m) => m.n === num)))
  return (
    <div className="current-wrap" data-current>
      <svg className="current" viewBox={`0 0 ${W} ${H}`} role="img"
           aria-label={`${mv.length} movements; ${entries.length} sources entering the film`}>
        <line className="current-base" x1={PAD - 70} y1={baseY} x2={W - PAD + 70} y2={baseY} />
        {entries.map((e, j) => {
          const x = xOf(e.k)
          const y = LANE0 + j * LANE
          const x0 = Math.max(8, x - 150)
          const x1 = Math.max(x0 + 12, x - 56)
          return (
            <g key={e.key} className="current-trib-g" data-tributary={e.key}>
              <path className="current-trib" d={`M ${x0} ${y} H ${x1} Q ${x} ${y} ${x} ${baseY - 17}`} />
              <text className="current-label" x={x0} y={y - 5}>{docHandle(job, e.key)}</text>
            </g>
          )
        })}
        {motif && (
          <g className="current-motif-g">
            <path className="current-motif" d={`M ${xOfN(spine.motif.plant_movement)} ${baseY + 17} C ${xOfN(spine.motif.plant_movement)} ${baseY + 62}, ${xOfN(spine.motif.payoff_movement)} ${baseY + 62}, ${xOfN(spine.motif.payoff_movement)} ${baseY + 17}`} />
            <text className="current-label motif" x={(xOfN(spine.motif.plant_movement) + xOfN(spine.motif.payoff_movement)) / 2} y={baseY + 58} textAnchor="middle">motif · plant → payoff</text>
          </g>
        )}
        {mv.map((m, i) => (
          <g key={m.n} data-station={m.n}>
            <circle className="current-station" cx={xOf(i)} cy={baseY} r={16} />
            <text className="current-n" x={xOf(i)} y={baseY + 5} textAnchor="middle">{m.n}</text>
          </g>
        ))}
      </svg>
      <div className="stations" style={{ gridTemplateColumns: `repeat(${n}, minmax(0, 1fr))` }}>
        {mv.map((m) => (
          <div key={m.n} className="station" data-station-label={m.n}>
            <div className="st-title">{m.title}</div>
            <div className="st-job">{m.job}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function ElementChips({ job, ids, index, open, onToggle }: { job: StoryJob; ids: string[]; index: Map<string, ElementRef>; open: Set<string>; onToggle: (id: string) => void }) {
  if (!ids.length) return null
  return (
    <>
      <p className="strip elchips"><span className="strip-label">cites</span>
        {ids.map((id) => {
          const ref = index.get(id)
          return (
            <button key={id} type="button" className={`elchip${open.has(id) ? ' on' : ''}${ref ? '' : ' missing'}`} onClick={() => onToggle(id)}
                    title={ref ? `${ref.el.kind} · ${docHandle(job, ref.profile.doc_key)} — click to reveal` : 'not in any profile'} data-cite={id}>{id}</button>
          )
        })}
      </p>
      {ids.filter((id) => open.has(id)).map((id) => {
        const ref = index.get(id)
        return ref ? (
          <div key={id} className="revealed" data-revealed={id}>
            <ElementRow el={ref.el} showDoc />
            <a className="linkish machine" href={storyPath(job.id, 'reading', `?element=${encodeURIComponent(id)}`)}>in the reading of {docHandle(job, ref.profile.doc_key)} →</a>
          </div>
        ) : <p key={id} className="hint" data-revealed={id}>{id} is not in any profile.</p>
      })}
    </>
  )
}

export function StorySpine({ job, rail }: { job: StoryJob; rail: StoryRailModel }) {
  const spine = job.spine
  const index = useMemo(() => elementIndex(job), [job])
  const [open, setOpen] = useState<Set<string>>(new Set())
  const toggle = (id: string) => setOpen((s) => { const n = new Set(s); if (n.has(id)) n.delete(id); else n.add(id); return n })
  const building = job.status === 'spining'

  if (!spine) {
    return (
      <section className="step story-spine" data-story-spine>
        <div className="section-head"><h3>The spine</h3></div>
        <div className="panel waiting-inline">
          {building && <span className="spinner" />}
          <div>
            <strong>{building ? storyStatusLabel(job.status) : job.status === 'awaiting_brief' ? 'Waiting for your choice' : 'Not built yet'}</strong>
            <p className="narration-line">{building ? (rail.narration ?? 'Deciding the movements, the motif, the hook.') : job.status === 'awaiting_brief' ? 'Choose one of the three films at the brief; the spine is built from it.' : 'The spine is built once a film is chosen.'}</p>
            {job.status === 'awaiting_brief' && <a className="linkish" href={storyPath(job.id, 'brief')}>← the brief</a>}
          </div>
        </div>
        <div className="actions dock"><a className="secondary" href={storyPath(job.id, 'brief')}>← The brief</a></div>
      </section>
    )
  }

  const tl = job.map?.through_lines.find((t) => t.key === spine.through_line_key)
  const hook = spine.hook?.element_id ? index.get(spine.hook.element_id) ?? null : null
  const mvTitle = (num: number) => spine.movements.find((m) => m.n === num)?.title ?? `movement ${num}`
  const used = new Set(spine.movements.flatMap((m) => m.sources))

  return (
    <section className="step story-spine" data-story-spine>
      <div className="section-head">
        <h3>The spine</h3>
        <span className="eyebrow">{spine.movements.length} movements · {used.size} sources · {seconds(spine.length_seconds)} · {approachLabel(spine.approach_key)}</span>
      </div>
      <p className="lede">{tl ? <>The film holds one question open — <em>{tl.question}</em> — </> : null}told as {approachLabel(spine.approach_key).toLowerCase()} in {spine.movements.length} movements. Read the current left to right: each source enters where its tributary meets the line.</p>

      <Current job={job} spine={spine} />

      <div className="movements" data-movements>
        {spine.movements.map((m) => (
          <article key={m.n} className="panel movement" data-movement={m.n}>
            <span className="eyebrow eyebrow-accent">movement {m.n}{m.entry_of.length ? ` · enters here: ${m.entry_of.map((k) => docHandle(job, k)).join(', ')}` : ''}</span>
            <h4>{m.title}</h4>
            <p className="deliverable-line">{m.job}</p>
            <ValueTurnView vt={m.value_turn} />
            <p className="strip"><span className="strip-label">sources</span> {m.sources.length ? m.sources.map((k) => <span key={k} className="chip chip-flat" title={docTitle(job, k)}>{docHandle(job, k)}</span>) : '—'}</p>
            <ElementChips job={job} ids={m.element_ids} index={index} open={open} onToggle={toggle} />
            {m.narration_hint && (
              <div className="quotecard"><blockquote>{m.narration_hint}</blockquote><cite className="machine">narration hint — for the screenwriter, not the viewer</cite></div>
            )}
          </article>
        ))}
      </div>

      <div className="section-head"><h3>The devices</h3><span className="eyebrow">what the spine plants, hooks, holds open and resolves</span></div>
      <div className="devices" data-devices>
        <div className="panel device" data-device="motif">
          <span className="eyebrow eyebrow-accent">motif</span>
          <p className="deliverable-line">{spine.motif?.what || '—'}</p>
          {spine.motif?.what && <p className="strip"><span className="strip-label">plant</span> {mvTitle(spine.motif.plant_movement)} <span className="arrow">→</span> <span className="strip-label">payoff</span> {mvTitle(spine.motif.payoff_movement)}</p>}
          <ElementChips job={job} ids={spine.motif?.element_ids ?? []} index={index} open={open} onToggle={toggle} />
        </div>
        <div className="panel device" data-device="hook">
          <span className="eyebrow eyebrow-accent">hook</span>
          {hook ? <ElementRow el={hook.el} showDoc /> : <p className="hint">{spine.hook?.element_id ? `${spine.hook.element_id} is not in any profile.` : 'No hook named.'}</p>}
          {spine.hook?.why && <p className="tag telling-why">{spine.hook.why}</p>}
        </div>
        <div className="panel device" data-device="open-loop">
          <span className="eyebrow eyebrow-accent">open loop</span>
          <p className="deliverable-line">{spine.open_loop || '—'}</p>
        </div>
        <div className="panel device" data-device="verdict">
          <span className="eyebrow eyebrow-accent">verdict</span>
          <p className="deliverable-line">{spine.verdict || '—'}</p>
        </div>
        <div className="panel device" data-device="colour-script">
          <span className="eyebrow eyebrow-accent">colour script</span>
          <p className="deliverable-line">{spine.colour_script || '—'}</p>
        </div>
        <div className="panel device" data-device="musical-arc">
          <span className="eyebrow eyebrow-accent">musical arc</span>
          <p className="deliverable-line">{spine.musical_arc || '—'}</p>
        </div>
      </div>

      <div className="actions dock">
        <a className="secondary" href={storyPath(job.id, 'brief')}>← The brief</a>
        {job.handoff
          ? <a className="primary" href={storyPath(job.id, 'handoff')} data-next>Next: the handoff →</a>
          : <button className="primary" disabled data-next>Next: the handoff — after the spine</button>}
      </div>
    </section>
  )
}
