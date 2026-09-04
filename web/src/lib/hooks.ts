/* Data hooks: the job snapshot (polled while it moves) and the event ledger
   (replayed from ?after=, then watched live). */
import { useCallback, useEffect, useRef, useState } from 'react'
import { api } from './api'
import type { DossierJob, RunEvent, StoryJob } from '../types'

const TERMINAL = new Set(['done', 'failed'])

export function useJob(id: string | null, pollMs = 2500) {
  const [job, setJob] = useState<DossierJob | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [tick, setTick] = useState(0)
  const reload = useCallback(() => setTick((t) => t + 1), [])
  useEffect(() => {
    if (!id) { setJob(null); return }
    let cancelled = false
    let timer: number | undefined
    const load = async () => {
      try {
        const j = await api.getJob(id)
        if (cancelled) return
        setJob(j)
        setError(null)
        if (!TERMINAL.has(j.status)) timer = window.setTimeout(load, pollMs)
      } catch (e) {
        if (cancelled) return
        setError(String((e as Error).message ?? e))
        timer = window.setTimeout(load, pollMs * 2)
      }
    }
    void load()
    return () => { cancelled = true; if (timer !== undefined) window.clearTimeout(timer) }
  }, [id, pollMs, tick])
  return { job, error, reload, setJob }
}

export function useEvents(id: string | null, live: boolean): RunEvent[] {
  const [events, setEvents] = useState<RunEvent[]>([])
  const lastSeq = useRef(0)
  useEffect(() => {
    setEvents([])
    lastSeq.current = 0
    if (!id) return
    let cancelled = false
    let stop: (() => void) | null = null
    const push = (batch: RunEvent[]) => {
      if (cancelled || !batch.length) return
      setEvents((prev) => {
        const seen = new Set(prev.map((e) => e.seq))
        const fresh = batch.filter((e) => !seen.has(e.seq))
        if (!fresh.length) return prev
        const next = [...prev, ...fresh].sort((a, b) => a.seq - b.seq)
        lastSeq.current = next[next.length - 1].seq
        return next
      })
    }
    api.events(id, 0).then((batch) => {
      push(batch)
      if (cancelled) return
      const terminal = batch.some((e) => e.kind === 'job_finished' || e.kind === 'job_failed')
      if (live && !terminal) {
        stop = api.watchEvents(id, batch.length ? batch[batch.length - 1].seq : 0, (e) => push([e]))
      }
    }).catch(() => { /* no ledger yet — the rail falls back to job status */ })
    return () => { cancelled = true; stop?.() }
  }, [id, live])
  return events
}

/* The story job snapshot — same rule as useJob: polled while it moves,
   left alone once it is handed off, stopped or cancelled. */
const STORY_TERMINAL = new Set(['done', 'failed', 'cancelled'])

export function useStoryJob(id: string | null, pollMs = 2500) {
  const [job, setJob] = useState<StoryJob | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [tick, setTick] = useState(0)
  const reload = useCallback(() => setTick((t) => t + 1), [])
  useEffect(() => {
    if (!id) { setJob(null); setError(null); return }
    let cancelled = false
    let timer: number | undefined
    const load = async () => {
      try {
        const j = await api.getStoryJob(id)
        if (cancelled) return
        setJob(j)
        setError(null)
        if (!STORY_TERMINAL.has(j.status)) timer = window.setTimeout(load, pollMs)
      } catch (e) {
        if (cancelled) return
        setError(String((e as Error).message ?? e))
        timer = window.setTimeout(load, pollMs * 2)
      }
    }
    void load()
    return () => { cancelled = true; if (timer !== undefined) window.clearTimeout(timer) }
  }, [id, pollMs, tick])
  return { job, error, reload, setJob }
}
