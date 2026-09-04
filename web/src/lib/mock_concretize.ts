/* Mock fixtures for the concretization passes (spine → cross-check), spliced into
   the the house replay by ./mock.ts: two more stage-B phases on the rail, the spine
   the desk planned against, and the findings ledger with fates. */
import type { CrossCheckVerdict, DossierSpine, Finding, RunEvent } from '../types'

type Mirror = { phase: string; phase_number: number; kind?: string }
export type ScriptEvent = Partial<RunEvent> & { stage: 'A' | 'B'; at_ms: number; mirror?: Mirror }

export const SPINE: DossierSpine = {
  round: 1,
  read: {
    plain_summary: 'the house has said its AI programme has three fields — client, product, money. Read against the five levels a move can be read on, the three sit at or below the product; the fourth field, the house codes, is the one nobody has named. The dossier says: pitch above the stack, on the fourth field, before Wednesday.',
    buried_crux: 'The commitments phase carries the decision the reader needs but never states it: accepting the three-field sentence commits the CEO to a stack he does not own. It hides in phase 2, pass 3.',
    readers: [{ type: 'the CEO\'s chief of staff', mode: 'reads the summary and one table', wants: 'the sentence to say on Wednesday and what it commits us to' }],
    strands: [{ name: 'the three-field sentence', carried_by: ['4.1', 'table t1'], accidental: false, note: 'returns in every section' }],
    prose_to_table: ['the five levels a move can be read against, with the reset scored on each'],
    table_to_prose: [],
    figures_earned: ['one reset read against five levels'],
    figures_dropped: ['a timeline of the turnaround — decoration; the dates are in the prose'],
    cumulative_direction: 'toward the fourth field; the counter-evidence (the programme is real and funded) needs its own bounded paragraph in section 2',
    form_capacity: 'five sections and two tables; not more',
  },
  thesis: 'the house\'s AI programme is real but sits below the house codes, and the fourth field is where a house is won or lost.',
  reader_question: 'What do I say on Wednesday, and what does it commit us to?',
  handle: 'Pitch above the stack.',
  through_line: 'the three-field sentence from the Capital Markets Day',
  summary_job: 'the finding and what it commits the house to',
  conclusion_job: 'the one sentence for Wednesday and the question to ask after it',
  sections: [
    { key: 'where_the_house_stands', heading: 'Where the house stands', claim: 'the house enters the meeting at the low point of its cycle with a new external CEO who names his turnarounds.', reader_needs_next: 'what the CEO has already said about AI', evidence_kind: 'chronology', table: { intent: 'the situation on the record', row_unit: 'one row = one dated fact', columns: ['Fact', 'Date', 'Source'], carries_claims: ['low point', 'external CEO'] }, figure: null, anchors_planned: [{ doc_key: 'house', quote: 'over-distribution and low cultural relevance' }], feeds: ['three_fields'] },
    { key: 'three_fields', heading: 'Three fields, and the missing fourth', claim: 'The three fields the CEO named all sit at or below the product level, leaving the house codes unaddressed.', reader_needs_next: 'why the fourth field is where a house is won', evidence_kind: 'mechanism', table: null, figure: { primitive: 'layering', visual_format: 'conceptual_layers', picture_shows: 'five levels stacked, the three fields shaded at the bottom two, the fourth field empty', caption_says: 'The programme is real; it lives below the codes.', why_a_picture: 'the reader must see the gap in the stack' }, anchors_planned: [{ doc_key: 'house', quote: 'follow the client, follow the product, follow the money' }], feeds: ['the_reset'] },
    { key: 'the_reset', heading: 'One reset, read against five levels', claim: 'The store-network reset from 600 to 450 is a product-level move dressed as a house-level one.', reader_needs_next: 'where the framing could misfire', evidence_kind: 'case_comparison', table: { intent: 'the reset scored on each level', row_unit: 'one row = one level', columns: ['Level', 'What the reset does', 'What it leaves'], carries_claims: ['product-level move'] }, figure: { primitive: 'comparative_positioning', visual_format: 'quadrant_chart', picture_shows: 'the reset placed against scope and depth', caption_says: 'A deep cut at a shallow level.', why_a_picture: 'a position is seen, not read' }, anchors_planned: [{ doc_key: 'paper', quote: 'a reading, not a verdict' }], feeds: ['misfire'] },
    { key: 'misfire', heading: 'Where the framing could misfire', claim: 'Saying "use AI" to a marketing-native CEO in pre-results mode reads as a vendor pitch.', reader_needs_next: 'the sentence to say instead', evidence_kind: 'implication', table: null, figure: null, anchors_planned: [{ doc_key: 'house', quote: 'Reconthe house' }], feeds: ['wednesday'] },
    { key: 'wednesday', heading: 'The sentence for Wednesday', claim: 'The pitch that lands is the fourth field named in the CEO\'s own vocabulary, with one house code as the proof.', reader_needs_next: 'nothing — this is the decision', evidence_kind: 'implication', table: null, figure: null, anchors_planned: [{ doc_key: 'paper', quote: 'house codes' }], feeds: [] },
  ],
  exhibits_budget: { tables: 3, figures: 2 },
  notes: ['section three_fields: figure spec dropped by code (over the budget of 2)'],
}

export const FINDINGS: Finding[] = [
  { id: 'fnd-a1', kind: 'caption_carries_number', where: { figure_key: 'f2', section_key: 'the_reset' }, quote: 'One reset read against five levels — store network 600 → 450', note: 'The picture\'s caption carries a number; the caption says what to take from the picture, never the figures. Cure: rewrite it without the number.', affordance: 'rewrite_caption', realization: 'A deep cut at a shallow level.', recommended: true, source: 'clamp', round: 1, status: 'resolved', fates: [{ round: 1, fate: 'executed', rationale: 'caption rewritten by code', by: 'code' }] },
  { id: 'fnd-b2', kind: 'anchor_fragment', where: { section_key: 'three_fields', anchor_n: 2 }, quote: 'The programme is real: a Chief AI Officer, Google partnerships, and Gucci named as the group\'s official AI laboratory.', note: 'The anchor for claim 2 only matched as a cut-off prefix; the reader would see a fragment. The claim is left unfootnoted. Cure: re-anchor it to the whole sentence.', affordance: 'reanchor_claim', realization: null, recommended: true, source: 'wall', round: 0, status: 'open', fates: [{ round: 1, fate: 'persists', rationale: 'the page still carries the claim without its footnote', by: 'judge' }] },
  { id: 'fnd-c3', kind: 'caption_restates_text', where: { section_key: 'three_fields', figure_key: 'f1', paragraph_index: 2 }, quote: 'The three fields all sit at or below the product level.', note: 'The paragraph beside the picture says what the caption says; the reader reads it twice. Cure: cut the sentence and argue from the picture.', affordance: 'rewrite_paragraph', realization: 'Read against the five levels, the programme lives below the codes — which is exactly where a vendor would put it.', recommended: true, source: 'judge', round: 1, status: 'open', fates: [] },
]

export const CROSSCHECK: CrossCheckVerdict = {
  round: 1, hangs_together: false, judged: true, clamps: 1, findings_minted: 2, realized: ['fnd-a1'],
  summary: 'The dossier argues one thing and the exhibits carry it; one caption carried a number (fixed), one anchor is a fragment, and one paragraph repeats its picture\'s caption.',
  what_changed: null,
}

/* extra stage-B events: the spine between the analysis and the tables, the cross-check between the draft and delivery */
export const EXTRA_EVENTS: ScriptEvent[] = [
  { stage: 'B', at_ms: 22420, kind: 'phase_started', phase: 'spine', detail: 'Deciding what the dossier argues before a word is written: one claim per section, and the table or diagram each claim needs.',
    narrator: 'Deciding what the dossier argues — five sections, each with one claim; two tables and one diagram commissioned by the argument, not by a dial.' },
  { stage: 'B', at_ms: 22460, kind: 'call_started', phase: 'spine', model: 'claude-sonnet-4-6', detail: 'composition read + spine: ~38,000 input tokens (std context)', input_tokens: 38000,
    prompt_excerpt: 'ANGLE (the chosen deliverable): The fourth field\nAUDIENCE: executive …\nEXHIBITS BUDGET (ceiling): 3 tables, 2 diagrams.' },
  { stage: 'B', at_ms: 22540, kind: 'call_finished', phase: 'spine', model: 'claude-sonnet-4-6', input_tokens: 38210, output_tokens: 2840, cost_usd: 0.157, duration_ms: 58000,
    detail: 'composition read + spine: 38,210 in / 2,840 out, $0.157, 58s', output_excerpt: '{"read": {"plain_summary": "the house has said its AI programme has three fields …' },
  { stage: 'B', at_ms: 22560, kind: 'artifact', phase: 'spine', detail: 'spine: the house\'s AI programme is real but sits below the house codes, and the fourth field is where a house is won or lost.',
    payload_json: '{"kind":"spine","sections":5,"tables":2,"figures":1}' },
  { stage: 'B', at_ms: 22580, kind: 'phase_finished', phase: 'spine', duration_ms: 160000, detail: 'spine done in 160s — 5 sections, 2 tables + 1 diagram commissioned' },
  { stage: 'B', at_ms: 45420, kind: 'phase_started', phase: 'crosscheck', detail: 'Reading the dossier as one thing — do the pictures show what the text argues, do the rows match the claims, is anything asserted that nothing backs.',
    narrator: 'Reading the dossier as one thing — the pictures, the rows and the prose against the spine.' },
  { stage: 'B', at_ms: 45440, kind: 'note', phase: 'crosscheck', detail: 'clamp: caption_carries_number at {"figure_key": "f2", "section_key": "the_reset"} — The picture\'s caption carries a number' },
  { stage: 'B', at_ms: 45460, kind: 'call_started', phase: 'crosscheck', model: 'claude-sonnet-4-6', detail: 'cross-check verdict (2 pictures shown): ~14,000 input tokens (std context), 2 image(s)', input_tokens: 14000 },
  { stage: 'B', at_ms: 45520, kind: 'call_finished', phase: 'crosscheck', model: 'claude-sonnet-4-6', input_tokens: 14380, output_tokens: 1210, cost_usd: 0.061, duration_ms: 41000,
    detail: 'cross-check verdict: 14,380 in / 1,210 out, $0.061, 41s', output_excerpt: '{"hangs_together": false, "summary": "The dossier argues one thing and the exhibits carry it; …' },
  { stage: 'B', at_ms: 45540, kind: 'note', phase: 'crosscheck', detail: 'realize: caption of f2 rewritten without its number' },
  { stage: 'B', at_ms: 45550, kind: 'narration', phase: 'crosscheck', narrator: 'Reading the dossier as one thing — 3 findings (1 by arithmetic); acted on 1. Still open: anchor fragment, caption restates text.' },
  { stage: 'B', at_ms: 45560, kind: 'artifact', phase: 'crosscheck', detail: 'cross-check: The dossier argues one thing and the exhibits carry it; one caption carried a number (fixed), one anchor is a fragment, and one paragraph repeats its picture\'s caption.',
    payload_json: '{"kind":"crosscheck","findings_minted":2,"clamps":1,"realized":["fnd-a1"]}' },
  { stage: 'B', at_ms: 45580, kind: 'phase_finished', phase: 'crosscheck', duration_ms: 49000, detail: 'crosscheck done in 49s — findings recorded: 3 minted (1 by code), 1 acted on' },
]
