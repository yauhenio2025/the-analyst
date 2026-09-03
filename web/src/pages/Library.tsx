/* The library — your dossiers, grouped Today / This week / Earlier, and the
   go box above them: one paste (or files, or an exemplar bundle), the use box
   ("What will you use this dossier for?"), who it is written for, the lane
   (propose deliverables · I'll pick the analysis · let the material decide),
   an advanced fold, one button that says what happens next (design §C6). */
import { Fragment, useEffect, useState } from 'react'
import { api, type UploadedBundle, MOCK } from '../lib/api'
import { dateShort, usd } from '../lib/format'
import { dossierPath, navigate } from '../router'
import { StatusChip } from '../components/StatusChip'
import { OutcomeButton } from '../components/OutcomeButton'
import { CatalogPicker, type PickedStep } from '../components/CatalogPicker'
import { USE_KINDS, type Audience, type Catalog, type Depth, type Entry, type Exemplar, type JobListEntry, type SourceSpec, type UseKind } from '../types'

const STEP_NAMES = ['', 'Your documents', 'The brief', 'The draft', 'Your dossier']

const LANES: { key: Entry; label: string; hint: string; start: string; effect: string }[] = [
  { key: 'use', label: 'Tell me what you’ll use it for', hint: 'the desk proposes three deliverables, one recommended', start: '· you’ll choose a deliverable',
    effect: 'It reads the documents and proposes three deliverables — what you get, what you will understand, what you will be able to do. Nothing more is spent until you choose one.' },
  { key: 'chosen', label: 'I know the analysis I want', hint: 'pick the engines from the purpose-first catalog', start: '· your path, then the brief',
    effect: 'It reads the documents, then writes the one deliverable your path yields — and one alternative the desk would propose. You confirm before anything more is spent.' },
  { key: 'material', label: 'Let the material decide', hint: 'the desk chooses and explains why', start: '· the desk chooses and explains',
    effect: 'It reads, proposes three deliverables, picks the one the material carries best, records why, and writes straight through. You can stop it at any step.' },
]

export function Library() {
  const [entries, setEntries] = useState<JobListEntry[] | null>(null)
  const [exemplars, setExemplars] = useState<Exemplar[]>([])
  const [error, setError] = useState<string | null>(null)
  const [mode, setMode] = useState<'paste' | 'exemplar' | 'upload'>('paste')
  const [files, setFiles] = useState<File[]>([])
  const [uploaded, setUploaded] = useState<UploadedBundle | null>(null)
  const [uploading, setUploading] = useState(false)
  const [text, setText] = useState('')
  const [title, setTitle] = useState('')
  const [exemplar, setExemplar] = useState<string | null>(null)
  // the use box
  const [intent, setIntent] = useState('')
  const [useKind, setUseKind] = useState<UseKind | null>(null)
  const [occasion, setOccasion] = useState('')
  const [whoReads, setWhoReads] = useState('')
  const [decision, setDecision] = useState('')
  // written for + lane
  const [audience, setAudience] = useState<Audience>('executive')
  const [lane, setLane] = useState<Entry>('use')
  const [steps, setSteps] = useState<PickedStep[]>([])
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [catalogKey, setCatalogKey] = useState('')
  const [catalogError, setCatalogError] = useState<string | null>(null)
  // advanced
  const [depth, setDepth] = useState<Depth>('medium')
  const [figures, setFigures] = useState(2)
  const [plates, setPlates] = useState(0)
  const [spendCap, setSpendCap] = useState('')
  const [imageProvider, setImageProvider] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    api.listJobs().then(setEntries).catch((e) => setError(String((e as Error).message ?? e)))
    api.exemplars().then((x) => { setExemplars(x); if (x.length && !exemplar) setExemplar(x[0].key) })
      .catch(() => setExemplars([]))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const chosenExemplar = exemplars.find((x) => x.key === exemplar)
  const corpusChars = mode === 'paste' ? text.length : mode === 'upload' ? (uploaded?.chars ?? files.reduce((n, f) => n + f.size, 0)) : (chosenExemplar?.chars ?? 0)
  const nDocs = mode === 'paste' ? 1 : mode === 'upload' ? (uploaded?.n_docs ?? Math.max(1, files.length)) : (chosenExemplar?.n_docs ?? 1)
  useEffect(() => {
    if (lane !== 'chosen') return
    const key = `${audience}:${Math.round(corpusChars / 5000)}:${nDocs}`
    if (key === catalogKey) return
    setCatalogKey(key)
    setCatalogError(null)
    api.catalog(audience, corpusChars || null, nDocs).then(setCatalog).catch((e) => setCatalogError(String((e as Error).message ?? e)))
  }, [lane, audience, corpusChars, nDocs, catalogKey])

  const todayStr = new Date().toDateString()
  const isToday = (e: JobListEntry) => new Date(e.created_at).toDateString() === todayStr
  const isWeek = (e: JobListEntry) => !isToday(e) && Date.now() - Date.parse(e.created_at) < 7 * 86400e3
  const groups = entries === null ? [] : [
    { label: 'Today', rows: entries.filter(isToday) },
    { label: 'This week', rows: entries.filter(isWeek) },
    { label: 'Earlier', rows: entries.filter((e) => !isToday(e) && !isWeek(e)) },
  ]

  const sourceReady = mode === 'paste' ? text.trim().length >= 200 : mode === 'upload' ? (files.length > 0 || uploaded !== null) : exemplar !== null
  const ready = sourceReady && (lane !== 'chosen' || steps.length > 0)
  const laneDef = LANES.find((l) => l.key === lane)!

  const start = async () => {
    if (!ready || busy) return
    setBusy(true)
    setError(null)
    let sources: SourceSpec[]
    try {
      if (mode === 'paste') {
        sources = [{ kind: 'paste', title: title.trim() || text.trim().split(/\n|(?<=[.!?])\s/)[0].slice(0, 80), text }]
      } else if (mode === 'upload') {
        let b = uploaded
        if (!b) {
          setUploading(true)
          b = await api.uploadBundle(files, title.trim() || undefined)
          setUploaded(b)
          setUploading(false)
        }
        sources = [{ kind: 'exemplar', key: b.name ?? b.key }]
      } else {
        sources = [{ kind: 'exemplar', key: exemplar! }]
      }
      const useFrame = (useKind || occasion.trim() || whoReads.trim() || decision.trim())
        ? { use_kind: useKind, occasion: occasion.trim() || null, who_reads: whoReads.trim() || null, decision: decision.trim() || null } : null
      const cap = Number(spendCap)
      const res = await api.createJob({
        sources, audience, depth,
        intent: intent.trim() || undefined,
        output: { text: true, tables: true, figures, plates, video: false },
        entry: lane, autopilot: lane === 'material',
        use_frame: useFrame,
        path: lane === 'chosen' ? { steps } : undefined,
        spend_cap_usd: spendCap && Number.isFinite(cap) && cap > 0 ? cap : undefined,
        image_provider: imageProvider || undefined,
      })
      navigate(dossierPath(res.job_id, 'sources'))
    } catch (e) {
      setError(String((e as Error).message ?? e))
      setBusy(false)
      setUploading(false)
    }
  }

  const stepOf = (e: JobListEntry) => STEP_NAMES[e.step] ?? `Step ${e.step}`
  const landing = (e: JobListEntry) =>
    e.status === 'done' ? 'dossier' : e.status === 'awaiting_brief' ? 'brief'
      : e.step >= 3 ? 'draft' : 'sources'

  return (
    <section className="library">
      <div className="intro">
        <div>
          <span className="eyebrow">The desk · <b>document in, dossier out</b></span>
          <h2 className="display">Give it the documents. It writes the dossier — text, tables, figures — and shows its work.</h2>
          <p className="lede">Paste the text or pick a bundle, say what you will use the dossier for. It reads first, then proposes three deliverables — what you will understand and be able to do — and you choose before anything more is spent. Every model call is recorded and priced.</p>
        </div>
        <div className="quotecard">
          <blockquote>Focus on the deliverables and what they will change in your action.</blockquote>
          <cite className="machine">the rule every brief is written under — stated on each card, checked by code.</cite>
        </div>
      </div>

      <div className="panel gobox" data-gobox>
        <div className="gobox-tabs" role="tablist">
          <button role="tab" aria-selected={mode === 'paste'} className={`mode-btn${mode === 'paste' ? ' on' : ''}`} onClick={() => setMode('paste')}>Paste text</button>
          <button role="tab" aria-selected={mode === 'upload'} className={`mode-btn${mode === 'upload' ? ' on' : ''}`} onClick={() => setMode('upload')}>Upload files</button>
          <button role="tab" aria-selected={mode === 'exemplar'} className={`mode-btn${mode === 'exemplar' ? ' on' : ''}`} onClick={() => setMode('exemplar')}>Use an exemplar bundle</button>
          <span className="mode-hint machine">{mode === 'paste'
            ? (text.trim().length < 200 ? `${text.trim().length} / 200 characters to start` : `${text.trim().length.toLocaleString()} characters`)
            : mode === 'upload'
              ? (uploaded ? `${uploaded.n_docs} documents · ${uploaded.chars.toLocaleString()} characters` : files.length ? `${files.length} file${files.length === 1 ? '' : 's'} · ${(files.reduce((n, f) => n + f.size, 0) / 1024 / 1024).toFixed(1)} MB` : 'pick pdf, md or txt files')
              : chosenExemplar ? `${chosenExemplar.n_docs} documents · ${chosenExemplar.chars.toLocaleString()} characters` : 'pick a bundle'}</span>
        </div>

        {mode === 'paste' ? (
          <div className="gobox-paste">
            <label className="field">
              <span className="field-label">The document</span>
              <textarea rows={8} value={text} placeholder="Paste the whole text, exactly as written. The dossier is built only from what is in it."
                        onChange={(e) => setText(e.target.value)} data-paste />
            </label>
            <label className="field field-inline">
              <span className="field-label">Title <span className="hint">optional</span></span>
              <input value={title} placeholder="What should the library call it?" onChange={(e) => setTitle(e.target.value)} />
            </label>
          </div>
        ) : mode === 'upload' ? (
          <div className="gobox-paste" data-upload>
            <label className="field">
              <span className="field-label">The files <span className="hint">pdf · md · txt — several make one bundle</span></span>
              <input type="file" multiple accept=".pdf,.md,.markdown,.txt,.text,application/pdf,text/markdown,text/plain"
                     onChange={(e) => { setFiles(Array.from(e.target.files ?? [])); setUploaded(null) }} data-files />
            </label>
            {files.length > 0 && (
              <ul className="upload-list machine">
                {files.map((f) => (
                  <li key={f.name + f.size}>{f.name} <span className="hint">· {(f.size / 1024).toFixed(0)} KB</span>
                    {uploaded?.documents.find((d) => d.filename === f.name) && <span className="chip-mini on">read · {uploaded.documents.find((d) => d.filename === f.name)!.char_count.toLocaleString()} chars</span>}
                  </li>
                ))}
              </ul>
            )}
            <label className="field field-inline">
              <span className="field-label">Bundle title <span className="hint">optional</span></span>
              <input value={title} placeholder="What should the library call this bundle?" onChange={(e) => setTitle(e.target.value)} />
            </label>
            <p className="hint">The text is extracted on the server and kept as one bundle with a header per document — the same shape a stacks export has. Scanned PDFs without a text layer are refused.</p>
            {uploading && <p className="hint">Reading the files…</p>}
          </div>
        ) : (
          <div className="choices" role="radiogroup" data-exemplars>
            {exemplars.length === 0 && <p className="hint">No exemplar bundles served.</p>}
            {exemplars.map((x) => (
              <button key={x.key} type="button" role="radio" aria-checked={exemplar === x.key}
                      className={`move${exemplar === x.key ? ' selected' : ''}`} onClick={() => setExemplar(x.key)}>
                <span className="phase">bundle · {x.n_docs} {x.n_docs === 1 ? 'document' : 'documents'}</span>
                <h4>{x.title}</h4>
                <p className="tag">{x.description}</p>
                <span className={`chip-mini${exemplar === x.key ? ' on' : ''}`}>chosen</span>
              </button>
            ))}
          </div>
        )}

        <div className="usebox" data-usebox>
          <label className="field">
            <span className="field-label">What will you use this dossier for? <span className="hint">the brief is written around it</span></span>
            <textarea rows={2} value={intent} placeholder="e.g. Decide which sustainability claims go into the Q4 campaign — and where a journalist would attack them."
                      onChange={(e) => setIntent(e.target.value)} data-intent />
          </label>
          <div className="use-chips" role="radiogroup" aria-label="use">
            {USE_KINDS.map((u) => (
              <button key={u.key} type="button" role="radio" aria-checked={useKind === u.key} title={u.hint}
                      className={`use-chip-btn${useKind === u.key ? ' on' : ''}`} onClick={() => setUseKind(useKind === u.key ? null : u.key)} data-use-kind={u.key}>{u.label}</button>
            ))}
          </div>
          {useKind && (
            <div className="dials use-details" data-use-details>
              <label className="field"><span className="field-label">Occasion <span className="hint">optional</span></span>
                <input value={occasion} placeholder="campaign planning, Q4" onChange={(e) => setOccasion(e.target.value)} /></label>
              <label className="field"><span className="field-label">Who reads it <span className="hint">optional</span></span>
                <input value={whoReads} placeholder="brand president + comms" onChange={(e) => setWhoReads(e.target.value)} /></label>
              <label className="field"><span className="field-label">Decision due <span className="hint">optional</span></span>
                <input value={decision} placeholder="which claims go into the Q4 campaign" onChange={(e) => setDecision(e.target.value)} /></label>
            </div>
          )}
        </div>

        <div className="dials lanebox">
          <label className="field">
            <span className="field-label">Written for</span>
            <select value={audience} onChange={(e) => setAudience(e.target.value as Audience)} data-dial="audience">
              <option value="executive">An executive</option>
              <option value="analyst">An analyst</option>
              <option value="researcher">A researcher</option>
            </select>
          </label>
          <div className="field lane-field">
            <span className="field-label">How the brief is made</span>
            <div className="lanes" role="radiogroup" data-lanes>
              {LANES.map((l) => (
                <label key={l.key} className={`lane${lane === l.key ? ' on' : ''}`} data-lane={l.key}>
                  <input type="radio" name="lane" value={l.key} checked={lane === l.key} onChange={() => setLane(l.key)} />
                  <span><b>{l.label}</b><span className="hint"> — {l.hint}</span></span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {lane === 'chosen' && (
          <div className="gobox-picker" data-lane-picker>
            <CatalogPicker catalog={catalog} loading={!catalog && !catalogError} error={catalogError} steps={steps} onChange={setSteps} />
          </div>
        )}

        <details className="advanced" data-advanced>
          <summary className="eyebrow">advanced · depth preference, figures, plates, spend cap, image provider</summary>
          <div className="dials">
            <label className="field">
              <span className="field-label">Depth preference</span>
              <select value={depth} onChange={(e) => setDepth(e.target.value as Depth)} data-dial="depth">
                <option value="simple">Simple — one pass, fast</option>
                <option value="medium">Medium — two or three engines</option>
                <option value="advanced">Advanced — full passes, slow</option>
              </select>
              <span className="hint">a preference; each card carries its own weight and price</span>
            </label>
            <label className="field">
              <span className="field-label">Figures</span>
              <select value={figures} onChange={(e) => setFigures(Number(e.target.value))} data-dial="figures">
                {[0, 1, 2, 3, 4].map((n) => <option key={n} value={n}>{n === 0 ? 'None' : n}</option>)}
              </select>
            </label>
            <label className="field">
              <span className="field-label">Plates <span className="hint">whole-page 4K diagrams</span></span>
              <select value={plates} onChange={(e) => setPlates(Number(e.target.value))} data-dial="plates">
                {[0, 1, 2].map((n) => <option key={n} value={n}>{n === 0 ? 'None' : n}</option>)}
              </select>
            </label>
            <label className="field">
              <span className="field-label">Spend cap <span className="hint">USD, optional</span></span>
              <input inputMode="decimal" value={spendCap} placeholder="none" onChange={(e) => setSpendCap(e.target.value)} data-dial="spend-cap" />
            </label>
            <label className="field">
              <span className="field-label">Image provider <span className="hint">optional</span></span>
              <select value={imageProvider} onChange={(e) => setImageProvider(e.target.value)} data-dial="image-provider">
                <option value="">default</option>
                <option value="gemini_pro">gemini_pro</option>
                <option value="gemini_flash">gemini_flash</option>
                <option value="seedream_5_pro">seedream_5_pro</option>
                <option value="qwen_image_2_pro">qwen_image_2_pro</option>
              </select>
            </label>
          </div>
        </details>

        <div className="actions dock">
          <OutcomeButton verb="Start" object={laneDef.start} disabled={!ready || busy} onClick={start} data-start effect={laneDef.effect} />
          {busy && <span className="machine">starting…</span>}
          {MOCK && <span className="chip chip-flat" title="Fixture replay — no server">mock</span>}
        </div>
      </div>

      {error && <div className="error-box" title={error}>{error}</div>}

      <div className="section-head">
        <h3>Your dossiers</h3>
        {entries && entries.length > 0 && <span className="eyebrow">{entries.length} on the shelf</span>}
      </div>
      {entries === null && !error && <div className="spinner" />}
      {entries && entries.length === 0 && (
        <div className="sheet"><p className="empty-line">Nothing yet. Paste a document above and start.</p></div>
      )}
      {entries && entries.length > 0 && (
        <div className="sheet" data-shelf>
          {groups.map((g) => g.rows.length > 0 && (
            <Fragment key={g.label}>
              <div className="act-rule">{g.label}</div>
              {g.rows.map((e) => (
                <a key={e.id} className="slate-row" href={dossierPath(e.id, landing(e))} data-shelf-row>
                  <div className="slate-main">
                    <span className="title">{e.title}</span>
                    <span className="meta machine">{dateShort(e.created_at)} · step {e.step} · {stepOf(e)}</span>
                  </div>
                  <div className="row-badges">
                    <StatusChip status={e.status} />
                    <span className="amt">{usd(e.totals?.cost_usd ?? 0)}</span>
                  </div>
                </a>
              ))}
            </Fragment>
          ))}
        </div>
      )}
    </section>
  )
}
