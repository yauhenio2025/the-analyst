# Inferential Translation Matrix

| Current host field | analyzer-v2 source field(s) | Transform / derivation rule | Gap status |
| --- | --- | --- | --- |
| `concept` | concept packet header | Copy packet concept name | covered |
| `analysis_type` | launch mode | Constant `inferential` | covered |
| `framework` | workflow/engine provenance | Constant `Brandomian Inferential Role Analysis` | covered |
| `the_deceptively_simple.surface_presentation` | inferential prose + schema focus on core idea presentation | Extract how the concept looks straightforward on the surface | covered via template |
| `the_deceptively_simple.hidden_weight` | inferential prose + downstream commitments | Extract what inferential burden is hidden behind the surface framing | covered via template |
| `the_deceptively_simple.key_quotes[]` | source-labelled pass outputs | Extract direct quotes plus source labels and brief analysis | covered via template |
| `commitment_cascade.commitment_relations[]` | `what_youre_signing_up_for`, `commitment_chains`, prose passes | Assemble endorsement → immediate/downstream/practical commitment relations | covered via template |
| `commitment_cascade.hidden_commitments[]` | hidden/implicit commitment discussion in prose | Extract hidden commitments with explanation/evidence | covered via template |
| `incompatibility_map.incompatibility_relations[]` | `either_or_choices`, `unresolved_tensions`, `relationship_graph` | Normalize conflicts into concept/concept incompatibility relations | covered via template |
| `incompatibility_map.unstable_combinations` | prose synthesis of conflicting commitments | Summarize unstable combinations in prose | covered via template |
| `tensions.unresolved_tensions[]` | `unresolved_tensions`, `perspectival_gaps`, `performative_contradictions` | Normalize unresolved tensions and supporting evidence | covered via template |
| `tensions.intellectual_fault_lines` | prose synthesis of contradictions and fault lines | Summarize fault lines | covered via template |
| `practical_stakes.obligations[]` | `real_world_implications`, package/practical prose | Extract obligation-like upshots | covered via template |
| `practical_stakes.prohibitions[]` | `either_or_choices`, incompatibility prose | Extract prohibitions / foreclosed actions | covered via template |
| `practical_stakes.affected_decisions[]` | `real_world_implications`, `how_the_conversation_shifts` | Extract decision domains affected by the concept | covered via template |
| `practical_stakes.normative_entanglements` | practical / normative prose | Summarize normative entanglements | covered via template |
| `commitment_packages[]` | `package_deals` | Normalize package name / core commitments / incompatibilities / endorsers | covered via template |
| `synthesis.inferential_definition` | packet + prose summary | Produce concise inferential definition | covered via template |
| `synthesis.centrality_score` | key-idea centrality + prose weighting | Normalize to 0-1 numeric score | covered via template |
| `synthesis.stability_score` | tension/incompatibility landscape | Normalize to 0-1 numeric score | covered via template |
| `synthesis.most_consequential_commitment` | commitment cascade / implications | Select most consequential commitment | covered via template |
| `synthesis.key_revelation` | overall inferential synthesis | Produce concise key revelation | covered via template |

Notes:
- This translation is an assembly/normalization step from analyzer-v2 graph/schema-plus-prose output into the 7-section Critic host contract.
- Source-facing labels must remain exactly the source titles carried in the by-ref packet.
