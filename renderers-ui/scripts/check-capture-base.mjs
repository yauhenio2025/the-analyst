import assert from 'node:assert/strict';

const captureBaseModule = new URL('../dist/utils/captureBase.js', import.meta.url);
const {
  resolvePackageCaptureBaseRuntime,
  buildPackageCaptureSelectionBase,
} = await import(captureBaseModule);

function noop() {}

assert.equal(
  resolvePackageCaptureBaseRuntime({
    _captureMode: false,
    _onCapture: noop,
  }),
  null,
  'resolver should fail closed when capture mode is off',
);

assert.equal(
  resolvePackageCaptureBaseRuntime({
    _captureMode: true,
    _onCapture: 'not-a-function',
  }),
  null,
  'resolver should fail closed when onCapture is not a function',
);

const rawRuntime = resolvePackageCaptureBaseRuntime({
  _captureMode: true,
  _onCapture: noop,
  _captureViewKey: '',
  _captureSourceType: '',
  _captureJobId: '',
  _captureEntityId: '',
});

assert.ok(rawRuntime, 'resolver should return a runtime when capture mode is on and onCapture is valid');
assert.equal(rawRuntime.sourceViewKey, '', 'resolver should preserve raw empty-string view keys');
assert.equal(rawRuntime.sourceType, '', 'resolver should preserve raw empty-string source types');
assert.equal(rawRuntime.captureJobId, '', 'resolver should preserve raw empty-string capture job ids');
assert.equal(rawRuntime.captureEntityId, '', 'resolver should preserve raw empty-string capture entity ids');

const defaultRuntime = resolvePackageCaptureBaseRuntime({
  _captureMode: true,
  _onCapture: noop,
});

assert.ok(defaultRuntime, 'resolver should return a defaultable runtime when only the hard gate passes');
assert.deepEqual(
  buildPackageCaptureSelectionBase(defaultRuntime, {
    titleSegments: ['Section'],
  }),
  {
    source_view_key: '',
    source_type: 'analysis',
    context_title: 'Analysis > Section',
    entity_id: '',
  },
  'builder should apply package defaults when view key, source type, and identity are absent',
);

const builderRuntime = resolvePackageCaptureBaseRuntime({
  _captureMode: true,
  _onCapture: noop,
  _captureViewKey: 'view_key',
  _captureSourceType: 'analysis',
  _captureJobId: 'job-1',
  _captureEntityId: 'entity-1',
});

assert.deepEqual(
  buildPackageCaptureSelectionBase(
    builderRuntime,
    {
      titleSegments: ['', 'Card Title'],
    },
  ),
  {
    source_view_key: 'view_key',
    source_type: 'analysis',
    context_title: 'view_key >  > Card Title',
    entity_id: 'entity-1',
  },
  'builder should preserve the package > title convention without filtering empty segments',
);

assert.deepEqual(
  buildPackageCaptureSelectionBase(
    builderRuntime,
    {
      titleSegments: ['Card Title'],
    },
  ),
  {
    source_view_key: 'view_key',
    source_type: 'analysis',
    context_title: 'view_key > Card Title',
    entity_id: 'entity-1',
  },
  'builder should preserve the 2-segment builder pattern used by sub-renderers without parent sections',
);

assert.deepEqual(
  buildPackageCaptureSelectionBase(
    builderRuntime,
    {
      titleSegments: ['Section Title', 'Card Title'],
    },
  ),
  {
    source_view_key: 'view_key',
    source_type: 'analysis',
    context_title: 'view_key > Section Title > Card Title',
    entity_id: 'entity-1',
  },
  'builder should preserve the 3-segment builder pattern used by parent-section sub-renderers',
);

assert.deepEqual(
  buildPackageCaptureSelectionBase(
    builderRuntime,
    {
      titleSegments: ['Section Title', 'Group Name', 'Move Title'],
    },
  ),
  {
    source_view_key: 'view_key',
    source_type: 'analysis',
    context_title: 'view_key > Section Title > Group Name > Move Title',
    entity_id: 'entity-1',
  },
  'builder should preserve the deeper 4-segment builder pattern used by grouped sub-renderers',
);

assert.equal(
  buildPackageCaptureSelectionBase(
    resolvePackageCaptureBaseRuntime({
      _captureMode: true,
      _onCapture: noop,
      _captureJobId: 'job-2',
      _captureEntityId: 'entity-2',
    }),
    {
      titleSegments: ['Card'],
      entityId: '',
    },
  ).entity_id,
  '',
  'builder should honor an explicit entityId whenever it is defined, even if empty',
);

assert.equal(
  buildPackageCaptureSelectionBase(
    resolvePackageCaptureBaseRuntime({
      _captureMode: true,
      _onCapture: noop,
      _captureJobId: 'job-3',
    }),
    {
      titleSegments: ['Card'],
    },
  ).entity_id,
  'job-3',
  'builder should fall back to captureJobId when no entityId is supplied and no captureEntityId exists',
);

console.log('capture-base verification passed');
