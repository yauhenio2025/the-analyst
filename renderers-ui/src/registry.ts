import type { RendererComponent } from './types';
import { AccordionRenderer } from './renderers/AccordionRenderer';
import { CardGridRenderer } from './renderers/CardGridRenderer';
import { CardRenderer } from './renderers/CardRenderer';
import { ProseRenderer } from './renderers/ProseRenderer';
import { TableRenderer } from './renderers/TableRenderer';
import { StatSummaryRenderer } from './renderers/StatSummaryRenderer';
import { RawJsonRenderer } from './renderers/RawJsonRenderer';

export const DEFAULT_TYPE_RENDERERS: Record<string, RendererComponent> = {
  prose: ProseRenderer,
  raw_json: RawJsonRenderer,
  card_grid: CardGridRenderer,
  accordion: AccordionRenderer,
  table: TableRenderer,
  stat_summary: StatSummaryRenderer,
  card: CardRenderer,
  // Existing consumer compatibility alias.
  timeline: CardGridRenderer,
};

export function resolveDefaultRenderer(rendererType: string): RendererComponent | null {
  return DEFAULT_TYPE_RENDERERS[rendererType] ?? null;
}

export function hasDefaultRenderer(rendererType: string): boolean {
  return resolveDefaultRenderer(rendererType) !== null;
}
