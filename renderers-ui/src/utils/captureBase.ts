type CaptureSelection = Record<string, unknown>;

export interface PackageCaptureBaseRuntime {
  onCapture: (selection: CaptureSelection) => void;
  sourceViewKey?: string;
  sourceType?: string;
  captureJobId?: string;
  captureEntityId?: string;
}

interface PackageCaptureSelectionBaseParams {
  titleSegments: string[];
  entityId?: string;
}

type CaptureConfig = Record<string, unknown>;

function asString(value: unknown): string | undefined {
  return typeof value === 'string' ? value : undefined;
}

export function resolvePackageCaptureBaseRuntime(
  config: CaptureConfig,
): PackageCaptureBaseRuntime | null {
  if (config._captureMode !== true) return null;

  const onCapture = typeof config._onCapture === 'function'
    ? config._onCapture as PackageCaptureBaseRuntime['onCapture']
    : undefined;

  if (!onCapture) return null;

  return {
    onCapture,
    sourceViewKey: asString(config._captureViewKey),
    sourceType: asString(config._captureSourceType),
    captureJobId: asString(config._captureJobId),
    captureEntityId: asString(config._captureEntityId),
  };
}

export function buildPackageCaptureSelectionBase(
  runtime: PackageCaptureBaseRuntime,
  params: PackageCaptureSelectionBaseParams,
): CaptureSelection {
  return {
    source_view_key: runtime.sourceViewKey || '',
    source_type: runtime.sourceType || 'analysis',
    context_title: [runtime.sourceViewKey || 'Analysis', ...params.titleSegments].join(' > '),
    entity_id: params.entityId !== undefined
      ? params.entityId
      : (runtime.captureEntityId || runtime.captureJobId || ''),
  };
}
