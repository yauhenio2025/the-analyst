"""An OpenRouter stream that ends without a finish_reason is a fragment: the backend raises so the runner retries (2026-09-05)."""
from types import SimpleNamespace

import pytest

from src.llm.backends import OpenRouterBackend


def _chunk(text=None, finish=None, usage=None):
    return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=text), finish_reason=finish)], usage=usage)


def _backend(chunks, monkeypatch):
    b = OpenRouterBackend("openrouter/openai/gpt-5.6-sol")
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kw: iter(chunks))))
    monkeypatch.setattr(b, "_get_client", lambda: client)
    return b


def test_stream_without_finish_reason_is_treated_as_truncated(monkeypatch):
    b = _backend([_chunk("The reading begins "), _chunk("and then the stream dies")], monkeypatch)
    with pytest.raises(RuntimeError, match="without a finish_reason"):
        b.execute_streaming(system_prompt="s", user_message="u", max_tokens=1000, label="t")


def test_stream_with_stop_completes_and_length_is_marked_partial(monkeypatch):
    usage = SimpleNamespace(prompt_tokens=10, completion_tokens=5)
    b = _backend([_chunk("A whole answer. "), _chunk("Done.", finish="stop", usage=usage)], monkeypatch)
    r = b.execute_streaming(system_prompt="s", user_message="u", max_tokens=1000, label="t")
    assert r.content == "A whole answer. Done." and not r.partial and r.input_tokens == 10
    b2 = _backend([_chunk("Cut at the cap"), _chunk(None, finish="length")], monkeypatch)
    r2 = b2.execute_streaming(system_prompt="s", user_message="u", max_tokens=1000, label="t")
    assert r2.content == "Cut at the cap" and r2.partial and r2.connection_error == "finish_reason=length"
