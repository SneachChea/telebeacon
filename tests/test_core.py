"""Unit tests for telebeacon.core."""

from datetime import UTC, datetime

from telebeacon import core


class DummyClient:
    """Simple test double that records sent messages."""

    def __init__(self) -> None:
        self.configured = True
        self.sent_messages: list[str] = []

    def send_message(self, message: str) -> None:
        self.sent_messages.append(message)


def test_send_telegram_message_adds_timestamp(monkeypatch) -> None:
    """send_telegram_message should prefix the outgoing message with a timestamp."""

    fixed_time = datetime(2026, 3, 3, 12, 0, 0, tzinfo=UTC)

    class FixedDateTime:
        UTC = UTC

        @classmethod
        def now(cls, tz=None) -> datetime:
            return fixed_time

    dummy_client = DummyClient()
    monkeypatch.setattr(core, "datetime", FixedDateTime)
    monkeypatch.setattr(core, "client", dummy_client)

    core.send_telegram_message("hello")

    assert dummy_client.sent_messages == ["[2026-03-03 12:00:00] hello"]


def test_send_telegram_message_skips_when_client_unconfigured(monkeypatch) -> None:
    """send_telegram_message should return without sending when client is unconfigured."""

    class UnconfiguredClient:
        configured = False

        def send_message(self, message: str) -> None:
            raise AssertionError(f"send_message should not be called: {message}")

    monkeypatch.setattr(core, "client", UnconfiguredClient())

    core.send_telegram_message("hello")
