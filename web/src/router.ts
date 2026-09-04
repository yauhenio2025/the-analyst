/* Hand-rolled pushState router (lifted from Wirecut's router.ts): the URL
   is truth. App derives the page from the parsed Route; components navigate
   by writing a new URL, never by mutating view state. */
import { useMemo, useSyncExternalStore } from 'react'

export type StepSlug = 'sources' | 'brief' | 'draft' | 'dossier'
export const STEP_SLUGS: StepSlug[] = ['sources', 'brief', 'draft', 'dossier']

/* the story desk: six stations, each its own URL */
export type StoryStepSlug = 'sources' | 'reading' | 'map' | 'brief' | 'spine' | 'handoff'
export const STORY_STEP_SLUGS: StoryStepSlug[] = ['sources', 'reading', 'map', 'brief', 'spine', 'handoff']

/* the library has two desks: dossiers, and films for Wirecut */
export type Desk = 'dossier' | 'film'

export type Route =
  | { kind: 'library'; desk: Desk }
  | { kind: 'dossier'; id: string; step: StepSlug; item: string | null }
  | { kind: 'story'; id: string; step: StoryStepSlug | null; element: string | null }
  | { kind: 'plates'; id: string }
  | { kind: 'console'; id: string; node: string | null; exec: boolean }

export function parseRoute(url: string): Route {
  const [pathname, search] = url.split('?')
  const parts = pathname.split('/').filter(Boolean)
  const q = new URLSearchParams(search ?? '')
  const library: Route = { kind: 'library', desk: q.get('desk') === 'film' ? 'film' : 'dossier' }
  if (parts.length === 0) return library
  if (parts[0] === 'd' && parts[1] && parts[2] === 'plates') return { kind: 'plates', id: parts[1] }
  if (parts[0] === 'd' && parts[1]) {
    const step = (STEP_SLUGS as string[]).includes(parts[2] ?? '')
      ? (parts[2] as StepSlug) : 'sources'
    return { kind: 'dossier', id: parts[1], step, item: q.get('item') }
  }
  if (parts[0] === 's' && parts[1]) {
    const step = (STORY_STEP_SLUGS as string[]).includes(parts[2] ?? '')
      ? (parts[2] as StoryStepSlug) : null
    return { kind: 'story', id: parts[1], step, element: q.get('element') }
  }
  if (parts[0] === 'console' && parts[1]) {
    return { kind: 'console', id: parts[1], node: q.get('node'),
             exec: q.get('view') === 'executive' }
  }
  return library
}

export const dossierPath = (id: string, step: StepSlug, query = '') =>
  `/d/${id}/${step}${query}`
export const consolePath = (id: string, query = '') => `/console/${id}${query}`
export const platesPath = (id: string) => `/d/${id}/plates`
export const storyPath = (id: string, step: StoryStepSlug, query = '') =>
  `/s/${id}/${step}${query}`
/** the film without a station: lands on the furthest station the job has reached */
export const storyHome = (id: string) => `/s/${id}`
export const libraryPath = (desk: Desk = 'dossier') => desk === 'film' ? '/?desk=film' : '/'
/** a story id is minted as story-<hex> by the server (src/story/schemas.py) */
export const isStoryId = (id: string) => id.startsWith('story-')

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
