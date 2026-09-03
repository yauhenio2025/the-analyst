/* Formatting helpers — amounts and counts in tabular mono. */
export const usd = (n: number | null | undefined, approx = false) =>
  n === null || n === undefined || Number.isNaN(n)
    ? '—' : `${approx ? '~' : ''}$${n < 10 ? n.toFixed(2) : n.toFixed(0)}`

export const tokens = (n: number | null | undefined) =>
  n === null || n === undefined ? '—'
    : n >= 1_000_000 ? `${(n / 1_000_000).toFixed(1)}M`
    : n >= 1000 ? `${(n / 1000).toFixed(n >= 100_000 ? 0 : 1)}K` : String(n)

export const duration = (ms: number | null | undefined) => {
  if (ms === null || ms === undefined) return '—'
  if (ms < 1000) return `${ms} ms`
  const s = Math.round(ms / 1000)
  if (s < 60) return `${s}s`
  const m = Math.floor(s / 60)
  return `${m}m ${String(s % 60).padStart(2, '0')}s`
}

export const minutes = (m: number | null | undefined) =>
  m === null || m === undefined ? '—' : `~${Math.round(m)} min`

export const dateShort = (iso: string) => {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleDateString(undefined, { day: 'numeric', month: 'short' })
}

export const timeShort = (iso: string) => {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

export const chars = (n: number | null | undefined) =>
  n === null || n === undefined ? '—' : `${n.toLocaleString()} chars`

export const engineName = (key: string) => key.replace(/_/g, ' ')

export const STATUS_LABEL: Record<string, string> = {
  queued: 'Queued',
  reconnaissance: 'Reading the documents',
  awaiting_brief: 'Brief ready — your choice',
  planning: 'Planning the analysis',
  analysis: 'Running the analysis',
  tables: 'Building the tables',
  figures: 'Drawing the figures',
  composing: 'Composing the dossier',
  done: 'Delivered',
  failed: 'Stopped',
}

export const statusLabel = (s: string | undefined | null) =>
  (s && STATUS_LABEL[s]) || s || '—'
