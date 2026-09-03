import { engineName } from '../lib/format'

export function EngineChips({ engines }: { engines: string[] }) {
  return (
    <span className="engchips">
      {engines.map((e) => <span key={e} className="engchip" title={e}>{engineName(e)}</span>)}
    </span>
  )
}

export function Eyebrow({ children, accent }: { children: React.ReactNode; accent?: boolean }) {
  return <span className={`eyebrow${accent ? ' eyebrow-accent' : ''}`}>{children}</span>
}
