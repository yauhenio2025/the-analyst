/* The library — your dossiers, grouped Today / This week / Earlier, and the
   paste-and-go box above them: one paste (or an exemplar bundle), three
   dials, one button that says what happens next. */
import { Fragment, useEffect, useState } from 'react'
import { api, type UploadedBundle, MOCK } from '../lib/api'
import { dateShort, usd } from '../lib/format'
import { dossierPath, navigate } from '../router'
import { StatusChip } from '../components/StatusChip'
import { OutcomeButton } from '../components/OutcomeButton'
import type { Audience, Depth, Exemplar, JobListEntry, SourceSpec } from '../types'

const STEP_NAMES = ['', 'Your documents', 'The brief', 'The draft', 'Your dossier']

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
  const [depth, setDepth] = useState<Depth>('medium')
  const [figures, setFigures] = useState(2)
  const [audience, setAudience] = useState<Audience>('executive')
  const [autopilot, setAutopilot] = useState(false)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    api.listJobs().then(setEntries).catch((e) => setError(String((e as Error).message ?? e)))
    api.exemplars().then((x) => { setExemplars(x); if (x.length && !exemplar) setExemplar(x[0].key) })
      .catch(() => setExemplars([]))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const todayStr = new Date().toDateString()
  const isToday = (e: JobListEntry) => new Date(e.created_at).toDateString() === todayStr
  const isWeek = (e: JobListEntry) => !isToday(e) && Date.now() - Date.parse(e.created_at) < 7 * 86400e3
  const groups = entries === null ? [] : [
    { label: 'Today', rows: entries.filter(isToday) },
    { label: 'This week', rows: entries.filter(isWeek) },
    { label: 'Earlier', rows: entries.filter((e) => !isToday(e) && !isWeek(e)) },
  ]

  const ready = mode === 'paste' ? text.trim().length >= 200 : mode === 'upload' ? (files.length > 0 || uploaded !== null) : exemplar !== null
  const chosenExemplar = exemplars.find((x) => x.key === exemplar)

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
      const res = await api.createJob({
        sources, audience, depth,
        output: { text: true, tables: true, figures, video: false },
        autopilot,
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
          <p className="lede">Paste the text or pick a bundle. It reads first, then proposes three ways to tell it; you choose before anything more is spent. Every model call is recorded and priced.</p>
        </div>
        <div className="quotecard">
          <blockquote>The read is a reading, not a verdict.</blockquote>
          <cite className="machine">the rule every dossier is written under — stated in the brief, checked on the console.</cite>
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

        <div className="dials">
          <label className="field">
            <span className="field-label">Depth</span>
            <select value={depth} onChange={(e) => setDepth(e.target.value as Depth)} data-dial="depth">
              <option value="simple">Simple — one pass, fast</option>
              <option value="medium">Medium — two passes per engine</option>
              <option value="advanced">Advanced — full passes, slow</option>
            </select>
          </label>
          <label className="field">
            <span className="field-label">Figures</span>
            <select value={figures} onChange={(e) => setFigures(Number(e.target.value))} data-dial="figures">
              {[0, 1, 2, 3, 4].map((n) => <option key={n} value={n}>{n === 0 ? 'None' : n}</option>)}
            </select>
          </label>
          <label className="field">
            <span className="field-label">Written for</span>
            <select value={audience} onChange={(e) => setAudience(e.target.value as Audience)} data-dial="audience">
              <option value="executive">An executive</option>
              <option value="analyst">An analyst</option>
              <option value="researcher">A researcher</option>
            </select>
          </label>
          <label className="field toggle">
            <span className="field-label">Autopilot</span>
            <span className="toggle-row">
              <input type="checkbox" checked={autopilot} onChange={(e) => setAutopilot(e.target.checked)} data-dial="autopilot" />
              <span className="hint">{autopilot ? 'the desk chooses the brief and keeps going' : 'off — you choose the brief'}</span>
            </span>
          </label>
        </div>

        <div className="actions dock">
          <OutcomeButton verb="Start" object={autopilot ? '· the desk chooses the brief' : "· you'll review the brief first"}
                         disabled={!ready || busy} onClick={start} data-start
                         effect={autopilot ? 'It reads, picks the recommended telling, and writes straight through. You can stop it at any step.'
                           : 'It reads the documents and proposes three tellings. Nothing more is spent until you choose one.'} />
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
