/* OutcomeButton — Wirecut's outcome contract, reduced to what this desk
   needs: "verb object · ~$x · ~y min · effect". The visible grammar and the
   data attributes stay identical so a census can read every spend. */
import type { ButtonHTMLAttributes } from 'react'

export interface OutcomeProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'children'> {
  verb: string
  object: string
  amount?: string | null
  minutes?: string | null
  effect?: string
  primary?: boolean
}

export function OutcomeButton({ verb, object, amount, minutes, effect, primary = true,
                                className, type = 'button', ...rest }: OutcomeProps) {
  return (
    <span className="outcome-unit">
      <button {...rest} type={type}
              className={`outcome-contract ${primary ? 'primary' : 'secondary'}${className ? ` ${className}` : ''}`}
              data-consequential="true"
              data-outcome-action={`${verb} ${object}`}
              data-outcome-usd={amount ?? undefined}>
        <span className="outcome-action">
          <span className="outcome-verb">{verb}</span>{' '}
          <span className="outcome-object">{object}</span>
        </span>
        {amount && <span className="outcome-amt">{amount}</span>}
        {minutes && <span className="outcome-amt outcome-min">{minutes}</span>}
      </button>
      {effect && <span className="outcome-subline">{effect}</span>}
    </span>
  )
}
