/* A chip is a FACT, not a button. Tone follows the recorded status. */
import { statusLabel } from '../lib/format'
import type { DossierStatus } from '../types'

export function toneOf(status: DossierStatus | string | null | undefined): 'ok' | 'neg' | 'live' | 'wait' | 'flat' {
  if (status === 'done') return 'ok'
  if (status === 'failed' || status === 'cancelled') return 'neg'
  if (status === 'awaiting_brief') return 'wait'
  if (status === 'queued') return 'flat'
  return 'live'
}

export function StatusChip({ status, label }: { status: DossierStatus | string | null | undefined; label?: string }) {
  const tone = toneOf(status)
  return (
    <span className={`chip chip-${tone}`} data-status={status ?? ''}>
      {tone === 'live' && <span className="pip pip-running" aria-hidden="true" />}
      {label ?? statusLabel(status)}
    </span>
  )
}
