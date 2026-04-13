# Note: Admitted Concept Operator Surface Residual Ambiguity Inventory

Date: 2026-04-12
Context:
- `communications/MEMO_2026-04-11_close_read_admitted_concept_operator_surface_and_thin_host_simplification_scope.md`

This is the short Phase 1 inventory for the admitted concept normalization tranche.

## Confirmed Already-Live

- analyzer-v2 exact and latest translated-artifact authority works for fresh `logical` and `inferential` jobs
- the-critic admitted concept readback is analyzer-v2-backed and project-scoped
- analyzer-mgmt job pages already render the concept artifact card on `Result Boundary` after hydration

## Residual Ambiguities Worth Normalizing

### 1. analyzer-mgmt job page state can still be ambiguous during load

- the concept artifact truth is fetched separately from generic presenter/result state
- on fresh jobs, the page can sit in a skeleton or generic `preparing` state before the concept artifact card resolves
- this makes the operator truth real but not yet maximally explicit

Normalization target:
- explicit concept-artifact loading state
- explicit note when generic Result Boundary state lags the validated concept artifact truth

### 2. the-critic cache law was implicit in code, not explicit in docs

- deployed code already behaves as a read-through, non-authoritative cache
- that law needed to be frozen in documentation to prevent future drift

Normalization target:
- explicit cache-law documentation
- explicit note that admitted concept modes do not fall back to local semantic recomposition

### 3. legacy translator helpers still exist and can be misread

- `analyzer_v2_recomposition.py` still exists in the-critic
- deployed admitted concept paths no longer import it
- without an explicit note, it is easy to misread this module as still authoritative

Normalization target:
- mark the module as legacy/test-only for the admitted live seam
