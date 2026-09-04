/* The "on the record" strip — the house's fact tiles: a serif number, a small
   label beneath. Every number rendered here is a recorded fact. */
export interface RecordTile { num: string; label: string; title?: string }

export function Record({ tiles, columns }: { tiles: RecordTile[]; columns?: number }) {
  return (
    <div className="record" style={columns ? { gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` } : undefined}>
      {tiles.map((t, i) => (
        <div key={i} title={t.title}>
          <div className="num">{t.num}</div>
          <div className="lbl">{t.label}</div>
        </div>
      ))}
    </div>
  )
}
