"""An optional method-owned output ceiling, propagated through retries/fallbacks."""
from contextlib import contextmanager
from contextvars import ContextVar

_LIMIT = ContextVar('method_output_token_limit', default=None)


def current():
    return _LIMIT.get()


@contextmanager
def limit(tokens):
    previous = current()
    effective = min(previous, tokens) if previous and tokens else previous or tokens
    token = _LIMIT.set(effective)
    try:
        yield
    finally:
        _LIMIT.reset(token)
