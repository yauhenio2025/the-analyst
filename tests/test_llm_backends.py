from src.llm.backends import AnthropicBackend


def test_anthropic_thinking_config_uses_budget_tokens():
    assert AnthropicBackend._thinking_config("high", 48_000) == {
        "type": "enabled",
        "budget_tokens": 16_384,
    }


def test_anthropic_thinking_config_clamps_to_available_max_tokens():
    assert AnthropicBackend._thinking_config("high", 3_000) == {
        "type": "enabled",
        "budget_tokens": 1_976,
    }


def test_anthropic_thinking_config_skips_when_max_tokens_too_small():
    assert AnthropicBackend._thinking_config("high", 1_500) is None
