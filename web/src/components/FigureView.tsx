import { usd } from '../lib/format'
import type { DossierFigure } from '../types'

export function FigureView({ figure, index }: { figure: DossierFigure; index: number }) {
  return (
    <figure className="figfig" data-figure={figure.key}>
      <img src={figure.url} alt={figure.caption} loading="lazy" />
      <figcaption>
        <span className="figfig-caption">Figure {index} — {figure.caption}</span>
        <span className="machine">
          {figure.provider ?? 'image'}{figure.cost_usd !== undefined ? ` · ${usd(figure.cost_usd)}` : ''}
          {figure.figure_id ? ` · ${figure.figure_id}` : ''}
        </span>
      </figcaption>
    </figure>
  )
}
