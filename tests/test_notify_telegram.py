"""Unit tests for the notify_telegram decorator."""

import pytest

import telebeacon.notify_telegram as notify_module
from telebeacon.notify_telegram import notify_telegram


def test_notify_telegram_success_sends_start_and_finish(monkeypatch) -> None:
    """Decorator should send start and success messages with duration."""

    messages: list[str] = []
    perf_values = iter([10.0, 11.5])

    monkeypatch.setattr(notify_module, "send_telegram_message", messages.append)
    monkeypatch.setattr(notify_module.time, "perf_counter", lambda: next(perf_values))

    @notify_telegram
    def add(x: int, y: int) -> int:
        return x + y

    result = add(1, 2)

    assert result == 3
    assert len(messages) == 2
    assert "started" in messages[0]
    assert "finished successfully" in messages[1]
    assert "1.50s" in messages[1]


def test_notify_telegram_failure_sends_start_and_error(monkeypatch) -> None:
    """Decorator should send failure notification and re-raise the exception."""

    messages: list[str] = []
    perf_values = iter([20.0, 20.75])

    monkeypatch.setattr(notify_module, "send_telegram_message", messages.append)
    monkeypatch.setattr(notify_module.time, "perf_counter", lambda: next(perf_values))

    @notify_telegram
    def boom() -> None:
        raise RuntimeError("failure")

    with pytest.raises(RuntimeError, match="failure"):
        boom()

    assert len(messages) == 2
    assert "started" in messages[0]
    assert "failed (RuntimeError)" in messages[1]
    assert "0.75s" in messages[1]


def test_notify_telegram_preserves_metadata(monkeypatch) -> None:
    """Decorator should preserve wrapped function metadata via functools.wraps."""

    monkeypatch.setattr(notify_module, "send_telegram_message", lambda _: None)

    @notify_telegram
    def sample() -> str:
        """Sample function docstring."""
        return "ok"

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Sample function docstring."
