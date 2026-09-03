/* Hand-rolled pushState router (lifted from Wirecut's router.ts): the URL
   is truth. App derives the page from the parsed Route; components navigate
   by writing a new URL, never by mutating view state. */
import { useMemo, useSyncExternalStore } from 'react'

export type StepSlug = 'sources' | 'brief' | 'draft' | 'dossier'
export const STEP_SLUGS: StepSlug[] = ['sources', 'brief', 'draft', 'dossier']

export type Route =
  | { kind: 'library' }
  | { kind: 'dossier'; id: string; step: StepSlug; item: string | null }
  | { kind: 'plates'; id: string }
  | { kind: 'console'; id: string; node: string | null; exec: boolean }

export function parseRoute(url: string): Route {
  const [pathname, search] = url.split('?')
  const parts = pathname.split('/').filter(Boolean)
  const q = new URLSearchParams(search ?? '')
  if (parts.length === 0) return { kind: 'library' }
  if (parts[0] === 'd' && parts[1] && parts[2] === 'plates') return { kind: 'plates', id: parts[1] }
  if (parts[0] === 'd' && parts[1]) {
    const step = (STEP_SLUGS as string[]).includes(parts[2] ?? '')
      ? (parts[2] as StepSlug) : 'sources'
    return { kind: 'dossier', id: parts[1], step, item: q.get('item') }
  }
  if (parts[0] === 'console' && parts[1]) {
    return { kind: 'console', id: parts[1], node: q.get('node'),
             exec: q.get('view') === 'executive' }
  }
  return { kind: 'library' }
}

export const dossierPath = (id: string, step: StepSlug, query = '') =>
  `/d/${id}/${step}${query}`
export const consolePath = (id: string, query = '') => `/console/${id}${query}`
export const platesPath = (id: string) => `/d/${id}/plates`

type Listener = () => void
const listeners = new Set<Listener>()
const emit = () => { for (const l of listeners) l() }

export const currentUrl = () => window.location.pathname + window.location.search

export function navigate(path: string, opts: { replace?: boolean } = {}) {
  if (currentUrl() !== path) {
    window.history[opts.replace ? 'replaceState' : 'pushState'](null, '', path)
  }
  emit()
}

function subscribe(listener: Listener): () => void {
  listeners.add(listener)
  return () => { listeners.delete(listener) }
}

window.addEventListener('popstate', emit)

/* Delegated interception: every same-app <a href> IS the navigation, so
   middle-click and copy-link keep working. Downloads and external/API
   URLs keep browser behaviour. */
document.addEventListener('click', (e) => {
  if (e.defaultPrevented || e.button !== 0
      || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
  const anchor = (e.target as Element | null)?.closest?.('a')
  if (!anchor || anchor.target || anchor.hasAttribute('download')) return
  const href = anchor.getAttribute('href')
  if (!href || !href.startsWith('/') || href.startsWith('/v1/')) return
  e.preventDefault()
  navigate(href)
})

export function useRoute(): Route {
  const url = useSyncExternalStore(subscribe, currentUrl)
  return useMemo(() => parseRoute(url), [url])
}
