/* A tiny Markdown-to-HTML renderer for section prose (paragraphs, headings,
   emphasis, lists, inline code). Sections may also arrive as HTML — then we
   render that. Kept small on purpose: the composed dossier is the API's. */
import { useMemo } from 'react'

function esc(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

function inline(s: string) {
  return esc(s)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*(?!\*)(.+?)\*(?!\*)/g, '$1<em>$2</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
}

export function mdToHtml(md: string): string {
  const out: string[] = []
  const blocks = md.replace(/\r/g, '').split(/\n{2,}/)
  for (const raw of blocks) {
    const b = raw.trim()
    if (!b) continue
    const h = b.match(/^(#{1,4})\s+(.*)$/)
    if (h) { out.push(`<h${h[1].length + 1}>${inline(h[2])}</h${h[1].length + 1}>`); continue }
    if (/^([-*]\s+.*\n?)+$/.test(b)) {
      out.push(`<ul>${b.split('\n').map((l) => `<li>${inline(l.replace(/^[-*]\s+/, ''))}</li>`).join('')}</ul>`)
      continue
    }
    if (/^(\d+[.)]\s+.*\n?)+$/.test(b)) {
      out.push(`<ol>${b.split('\n').map((l) => `<li>${inline(l.replace(/^\d+[.)]\s+/, ''))}</li>`).join('')}</ol>`)
      continue
    }
    if (b.startsWith('>')) {
      out.push(`<blockquote>${inline(b.replace(/^>\s?/gm, ''))}</blockquote>`)
      continue
    }
    out.push(`<p>${inline(b).replace(/\n/g, '<br/>')}</p>`)
  }
  return out.join('\n')
}

export function Md({ md, html, className }: { md?: string | null; html?: string | null; className?: string }) {
  const body = useMemo(() => html ?? (md ? mdToHtml(md) : ''), [md, html])
  return <div className={`prose${className ? ` ${className}` : ''}`} dangerouslySetInnerHTML={{ __html: body }} />
}
