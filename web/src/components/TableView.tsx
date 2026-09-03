/* A table as a real table. Anchored cells wear a dotted gold underline; hover
   shows the quoted sentence, click pins it in the "on the record" panel
   beneath. The anchor is the API's verbatim quote — never our paraphrase. */
import { useState } from 'react'
import type { Anchor, DossierTable } from '../types'

export function TableView({ table, docTitles }: { table: DossierTable; docTitles?: Record<string, string> }) {
  const [pinned, setPinned] = useState<Anchor | null>(null)
  const anchors = table.rows.reduce((n, r) => n + r.cells.filter((c) => c.anchor).length, 0)
  return (
    <figure className="tablefig" data-table={table.key}>
      <figcaption>
        <span className="tablefig-caption">{table.caption}</span>
        <span className="eyebrow">{table.rows.length} rows · {anchors} anchored</span>
      </figcaption>
      <div className="table-scroll">
        <table className="desk-table">
          <thead>
            <tr>{table.columns.map((c, i) => <th key={i}>{c}</th>)}</tr>
          </thead>
          <tbody>
            {table.rows.map((row, ri) => (
              <tr key={ri}>
                {row.cells.map((cell, ci) => cell.anchor ? (
                  <td key={ci}>
                    <button type="button" className={`anchored${pinned === cell.anchor ? ' pinned' : ''}`}
                            title={cell.anchor.quote}
                            onClick={() => setPinned(pinned === cell.anchor ? null : cell.anchor!)}>
                      {cell.value}
                    </button>
                  </td>
                ) : <td key={ci}>{cell.value}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {pinned && (
        <div className="quotecard" data-anchor-pinned>
          <blockquote>“{pinned.quote}”</blockquote>
          <cite className="machine">on the record — {docTitles?.[pinned.doc_key] ?? pinned.doc_key}</cite>
        </div>
      )}
      {table.note && <p className="tablefig-note">{table.note}</p>}
    </figure>
  )
}
