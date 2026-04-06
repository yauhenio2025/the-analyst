from pathlib import Path
import sys
import time

import pytest

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if root_str in sys.path:
    sys.path.remove(root_str)
sys.path.insert(0, root_str)

from src.llm.backends import _execute_with_hard_timeout


def test_execute_with_hard_timeout_returns_value():
    result = _execute_with_hard_timeout(
        lambda: "ok",
        timeout_seconds=1,
        label="unit-test",
    )
    assert result == "ok"


def test_execute_with_hard_timeout_raises_without_blocking_forever():
    start = time.monotonic()

    def _hang():
        time.sleep(1.0)
        return "late"

    with pytest.raises(TimeoutError, match="hard timeout"):
        _execute_with_hard_timeout(
            _hang,
            timeout_seconds=0.01,
            label="unit-test",
        )

    assert time.monotonic() - start < 0.2
