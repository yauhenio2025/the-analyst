# Logical Translation Matrix

| Current host field | analyzer-v2 source field(s) | Transform / derivation rule | Gap status |
| --- | --- | --- | --- |
| `concept` | concept packet header | Copy packet concept name | covered |
| `analysis_type` | launch mode | Constant `logical` | covered |
| `framework` | workflow/chain provenance | Constant `Logical Structure Analysis` | covered |
| `argument_inventory[]` | raw logical chain outputs across formalization / chain / quote / synthesis stages | Extract per-argument records with source, quote, logical form, unstated premises, concept role | covered via template |
| `argument_chains[]` | chain-building / taxonomy / synthesis outputs | Normalize sequences, dependencies, ultimate conclusion, visualization, optional taxonomy fields | covered via template |
| `causal_architecture` | causal-mechanisms outputs | Normalize cause/effect claims, mechanism detail, intervention claims | covered via template |
| `conditional_web` | conditional-web outputs | Normalize antecedent/consequent/biconditional/nested conditional uses | covered via template |
| `argumentative_weight` | argumentative-weight outputs | Normalize load-bearing / supporting / defensive / illustrative groupings | covered via template |
| `logical_vulnerabilities[]` | vulnerability-analysis outputs | Normalize vulnerability type, description, challenge, severity, argument linkage | covered via template |
| `textual_shifts[]` | cross-text-comparison outputs | Normalize change type and comparison analysis across ordered sources | covered via template |
| `synthesis.argument_density` | synthesis output + inventory counts | Preserve or derive count / count-like summary | covered via template |
| `synthesis.logical_centrality` | synthesis summary + weight/vulnerability posture | Normalize to `core|important|peripheral` | covered via template |
| `synthesis.causal_weight` | causal architecture + synthesis summary | Normalize to `heavy|moderate|light` | covered via template |
| `synthesis.strongest_arguments[]` | synthesis + weight outputs | Select strongest argument ids | covered via template |
| `synthesis.weakest_arguments[]` | synthesis + vulnerability outputs | Select weakest argument ids | covered via template |
| `synthesis.vulnerability_summary` | vulnerability-analysis + synthesis prose | Summarize major weaknesses | covered via template |
| `synthesis.overall_assessment` | synthesis output | Preserve overall assessment | covered via template |

Scrutiny dependencies:
- `argument_inventory[].id`
- `argument_inventory[].source`
- `argument_inventory[].quote`
- `argument_inventory[].logical_form.premises`
- `argument_inventory[].logical_form.conclusion`
- `argument_inventory[].logical_form.argument_type`
- `argument_inventory[].unstated_premises`
- `argument_inventory[].concept_role`

Notes:
- Contract validation must cover the full `LogicalAnalysis` contract, including non-tabbed fields such as `conditional_web`, `argumentative_weight`, and `textual_shifts`.
- Scrutiny acceptance requires that the host-local scrutiny path reads only this translated logical result, not any old local-runtime-only fields.
