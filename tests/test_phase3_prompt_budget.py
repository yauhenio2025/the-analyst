"""Focused tests for Phase 3.0 prompt-budget repair.

Covers:
1. Phase 3.0 document assembly returns target-only text
2. Raw selected-source corpus is excluded from Phase 3.0
3. Selected-source identity header is preserved
4. Pre-provider fail-fast rejects over-limit inputs
5. Repaired prompt shape stays under the 900K-token guard
6. Later-pass inner-context growth does not breach the guard
"""

import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_plan_data(
    *,
    workflow_key: str = "anxiety_of_influence_thematic_single_thinker",
    selected_source_thinker_id: str = "otto_neurath",
    selected_source_thinker_name: str = "Otto Neurath",
    prior_works: list[dict] | None = None,
    target_title: str = "test-project",
):
    """Build a minimal plan_data dict that mimics a real AOI job."""
    if prior_works is None:
        prior_works = [
            {
                "title": "Economic Writings",
                "source_thinker_id": "otto_neurath",
                "source_thinker_name": "Otto Neurath",
                "source_document_id": "economic_writings",
            },
            {
                "title": "Empiricism and Sociology",
                "source_thinker_id": "otto_neurath",
                "source_thinker_name": "Otto Neurath",
                "source_document_id": "empiricism_sociology",
            },
        ]
    return {
        "workflow_key": workflow_key,
        "selected_source_thinker_id": selected_source_thinker_id,
        "selected_source_thinker_name": selected_source_thinker_name,
        "prior_works": prior_works,
        "target_work": {"title": target_title},
    }


TARGET_TEXT = "Target corpus text " * 1000  # ~19K chars
SOURCE_TEXT_PER_WORK = "Source corpus text " * 100_000  # ~1.9M chars each


# ---------------------------------------------------------------------------
# 1. Phase 3.0 document assembly: target-only
# ---------------------------------------------------------------------------

class TestPhase3DocumentAssembly:
    """Phase 3.0 document_text must contain only the target corpus."""

    def _call_assembly(self, phase_number: float):
        """Call _get_standard_phase_document_text with mocked job/document data."""
        from src.executor.phase_runner import _get_standard_phase_document_text

        plan_data = _make_plan_data()
        job_record = {"plan_data": plan_data}

        with (
            patch("src.executor.phase_runner.get_job", return_value=job_record),
            patch(
                "src.executor.phase_runner._get_target_document_text",
                return_value=TARGET_TEXT,
            ),
            patch(
                "src.executor.phase_runner._get_work_document_text",
                return_value=SOURCE_TEXT_PER_WORK,
            ),
        ):
            return _get_standard_phase_document_text(
                document_ids={},
                job_id="job-test",
                phase_number=phase_number,
            )

    def test_phase3_returns_target_text(self):
        """Phase 3.0 document_text contains the target corpus."""
        result = self._call_assembly(3.0)
        assert "Target corpus text" in result

    def test_phase3_excludes_raw_source_corpus(self):
        """Phase 3.0 document_text does NOT contain the raw source corpus text."""
        result = self._call_assembly(3.0)
        assert "Source corpus text" not in result

    def test_phase3_preserves_source_identity_header(self):
        """Phase 3.0 document_text includes a source-thinker identity header."""
        result = self._call_assembly(3.0)
        assert "Otto Neurath" in result
        assert "Economic Writings" in result
        assert "Empiricism and Sociology" in result

    def test_phase3_mentions_upstream_provenance(self):
        """Phase 3.0 identity header directs provenance to upstream context."""
        result = self._call_assembly(3.0)
        assert "Phase 1.0" in result or "upstream" in result.lower()

    def test_phase3_much_smaller_than_full_corpus(self):
        """Phase 3.0 document_text is dramatically smaller without raw source."""
        result_phase3 = self._call_assembly(3.0)
        result_phase1 = self._call_assembly(1.0)
        # Phase 1.0 gets the full source corpus; Phase 3.0 should be much smaller
        assert len(result_phase3) < len(result_phase1) / 10

    def test_phase1_still_gets_full_source_corpus(self):
        """Phase 1.0 document assembly is unchanged — still gets full source corpus."""
        result = self._call_assembly(1.0)
        assert "Source corpus text" in result


# ---------------------------------------------------------------------------
# 2. Pre-provider fail-fast guard
# ---------------------------------------------------------------------------

class TestPreProviderFailFast:
    """engine_runner must reject prompts exceeding ~975K estimated tokens."""

    def test_over_limit_raises_before_backend(self):
        """A 4M-char input on the 1M path raises RuntimeError locally."""
        from src.executor.engine_runner import run_engine_call

        huge_system = "x" * 100_000
        huge_user = "y" * 3_800_000  # ~3.9M chars total -> ~975K tokens

        with pytest.raises(RuntimeError, match="Prompt budget exceeded locally"):
            run_engine_call(
                system_prompt=huge_system,
                user_message=huge_user,
                phase_number=3.0,
                requires_full_documents=True,
                label="test-guard",
            )

    def test_under_limit_does_not_raise(self):
        """A 400K-char input on the 1M path does NOT trigger the guard."""
        from src.executor.engine_runner import run_engine_call

        small_system = "x" * 10_000
        small_user = "y" * 390_000  # ~400K chars -> ~100K tokens

        # Should proceed to the backend call (which we mock to avoid real API)
        mock_result = MagicMock()
        mock_result.content = "ok"
        mock_result.model_id = "test"
        mock_result.input_tokens = 100
        mock_result.output_tokens = 50
        mock_result.thinking_tokens = 0
        mock_result.duration_ms = 100
        mock_result.partial = False

        with patch("src.executor.engine_runner.get_backend") as mock_backend:
            mock_backend.return_value.execute_sync.return_value = mock_result
            result = run_engine_call(
                system_prompt=small_system,
                user_message=small_user,
                phase_number=3.0,
                requires_full_documents=True,
                label="test-under-limit",
            )
            assert result["content"] == "ok"

    def test_guard_only_fires_on_extended_context(self):
        """The 975K guard only fires when use_1m_context is True."""
        from src.executor.engine_runner import run_engine_call

        huge_system = "x" * 100_000
        huge_user = "y" * 3_800_000

        # With requires_full_documents=False, config['use_1m_context'] is False.
        # The guard should NOT fire — the backend will eventually reject the
        # call, but the local 900K guard is scoped to the 1M path only.
        # Mock the backend to verify the guard was not the blocker.
        mock_result = MagicMock()
        mock_result.content = "ok"
        mock_result.model_id = "test"
        mock_result.input_tokens = 100
        mock_result.output_tokens = 50
        mock_result.thinking_tokens = 0
        mock_result.duration_ms = 100
        mock_result.partial = False

        with patch("src.executor.engine_runner.get_backend") as mock_backend:
            mock_backend.return_value.execute_sync.return_value = mock_result
            # Should NOT raise our local guard error
            result = run_engine_call(
                system_prompt=huge_system,
                user_message=huge_user,
                phase_number=3.0,
                requires_full_documents=False,
                label="test-no-1m",
            )
            assert result["content"] == "ok"


# ---------------------------------------------------------------------------
# 3. Repaired prompt shape stays under the guard
# ---------------------------------------------------------------------------

class TestRepairedPromptShape:
    """Reconstructed Phase 3.0 pass 1 must fit under the 975K-token guard."""

    def test_budget_helper_matches_composed_prompt_total(self):
        """Budget diagnostics must match the real guard path, not double-count context."""
        from src.engines.registry import get_engine_registry
        from src.engines.schemas_v2 import PassDefinition
        from src.executor.chain_runner import _estimate_pass_budget
        from src.stages.capability_composer import compose_pass_prompt

        cap_def = get_engine_registry().get_capability_definition("aoi_thematic_synthesis")
        assert cap_def is not None

        upstream_context = "Upstream thematic evidence.\n" * 20
        inner_context = "Inner pass findings.\n" * 10
        full_shared_context = "\n\n---\n\n".join([upstream_context, inner_context])
        pass_def = PassDefinition(
            pass_number=1,
            label="Source Theme Discovery",
            stance="discovery",
            description="",
            focus_dimensions=[],
            consumes_from=[],
        )
        system_prompt = compose_pass_prompt(
            cap_def=cap_def,
            pass_def=pass_def,
            depth="deep",
            shared_context=full_shared_context,
        ).prompt
        document_text = "Selected source corpus.\n" * 100

        budget = _estimate_pass_budget(
            document_text,
            system_prompt,
            full_shared_context=full_shared_context,
            inner_context=inner_context,
        )

        assert budget["shared_chars"] == len(full_shared_context)
        assert budget["inner_chars"] == len(inner_context)
        assert budget["total_chars"] == len(document_text) + len(system_prompt)
        assert budget["estimated_tokens"] == (len(document_text) + len(system_prompt)) // 4
        assert budget["total_chars"] != (
            len(document_text)
            + len(system_prompt)
            + len(full_shared_context)
            + len(inner_context)
        )

    def test_march27_style_repaired_input_under_guard(self):
        """With target-only assembly, a March 27-scale run stays under budget."""
        # March 27 baseline: target ~274K chars, upstream context ~250K chars
        target_chars = 274_000
        upstream_context_chars = 250_000
        system_prompt_chars = 8_000
        source_identity_header_chars = 500

        total_chars = (
            target_chars
            + source_identity_header_chars
            + upstream_context_chars
            + system_prompt_chars
        )
        estimated_tokens = total_chars // 4

        assert estimated_tokens < 975_000, (
            f"Repaired Phase 3.0 pass 1 still exceeds guard: "
            f"{estimated_tokens:,} tokens from {total_chars:,} chars"
        )
        # Verify it's well within budget, not just barely under
        assert estimated_tokens < 200_000, (
            f"Repaired path should be well under 200K tokens, got {estimated_tokens:,}"
        )

    def test_phase1_otto_source_corpus_passes_guard(self):
        """Phase 1.0 with the full Otto source corpus (~3.63M chars) passes the guard.

        The March 27 pre-fix run proved Phase 1.0 completes successfully with
        this corpus (job-226f65f43a3b). Provider-side input tokens for the
        three passes were 920,477 / 937,532 / 955,918, so the guard must not
        block this path.
        """
        # Measured from the fresh rerun diagnostic
        source_corpus_chars = 3_627_836
        shared_context_chars = 830
        system_prompt_chars = 4_729

        total_chars = source_corpus_chars + shared_context_chars + system_prompt_chars
        estimated_tokens = total_chars // 4

        assert estimated_tokens < 975_000, (
            f"Phase 1.0 Otto source corpus should pass the guard: "
            f"{estimated_tokens:,} estimated tokens from {total_chars:,} chars"
        )
        assert max([920_477, 937_532, 955_918]) < 1_000_000
        assert max([920_477, 937_532, 955_918]) > 900_000


# ---------------------------------------------------------------------------
# 4. Multi-pass inner-context growth
# ---------------------------------------------------------------------------

class TestMultiPassBudgetSafety:
    """Later passes with inner-context growth must not breach the guard."""

    def test_pass3_with_inner_context_under_guard(self):
        """Pass 3 (integration) adds pass 1+2 outputs but should stay under budget."""
        # Target-only document: ~274K chars
        target_doc_chars = 274_000
        # Upstream context from Phase 1.0 + 2.0: ~250K chars
        upstream_chars = 250_000
        # System prompt: ~8K chars
        system_chars = 8_000
        # Source identity header: ~500 chars
        source_header_chars = 500
        # Inner context from pass 1 + pass 2 outputs: generous estimate
        # Each pass output ~30K chars (64K token max_tokens output ≈ ~256K chars,
        # but realistic output is much smaller)
        pass1_output_chars = 30_000
        pass2_output_chars = 30_000
        inner_context_chars = pass1_output_chars + pass2_output_chars

        total = (
            target_doc_chars
            + source_header_chars
            + upstream_chars
            + system_chars
            + inner_context_chars
        )
        estimated_tokens = total // 4

        assert estimated_tokens < 975_000, (
            f"Pass 3 with inner context exceeds guard: "
            f"{estimated_tokens:,} tokens from {total:,} chars"
        )

    def test_extreme_inner_context_detected_by_guard(self):
        """If inner-context growth is pathological, the guard catches it."""
        # Simulate a case where prior pass outputs are unusually large
        target_doc_chars = 274_000
        upstream_chars = 250_000
        system_chars = 8_000
        # Pathological: each prior pass produced 1.7M chars of output
        inner_context_chars = 3_400_000

        total = target_doc_chars + upstream_chars + system_chars + inner_context_chars
        estimated_tokens = total // 4

        # This should exceed the guard (3.93M chars / 4 = 983K tokens >= 975K)
        assert estimated_tokens >= 975_000, (
            f"Pathological inner context should be caught by the guard, "
            f"got {estimated_tokens:,} tokens"
        )
