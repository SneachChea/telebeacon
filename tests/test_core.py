"""Unit tests for telebeacon.core."""

from datetime import datetime

from telebeacon import core


class DummyClient:
    """Simple test double that records sent messages."""

    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def send_message(self, message: str) -> None:
        self.sent_messages.append(message)


def test_get_client_caches_single_instance(monkeypatch) -> None:
    """_get_client should instantiate TelegramClient only once."""

    created: list[object] = []

    class FakeTelegramClient:
        def __init__(self) -> None:
            created.append(object())

    monkeypatch.setattr(core, "TelegramClient", FakeTelegramClient)

    first = core._get_client()
    second = core._get_client()

    assert first is second
    assert len(created) == 1


def test_send_telegram_message_adds_timestamp(monkeypatch) -> None:
    """send_telegram_message should prefix the outgoing message with a timestamp."""

    fixed_time = datetime(2026, 3, 3, 12, 0, 0)

    class FixedDateTime:
        @classmethod
        def now(cls) -> datetime:
            return fixed_time

    dummy_client = DummyClient()
    monkeypatch.setattr(core, "datetime", FixedDateTime)
    monkeypatch.setattr(core, "_get_client", lambda: dummy_client)

    core.send_telegram_message("hello")

    assert dummy_client.sent_messages == ["🕒 [2026-03-03 12:00:00]\nhello"]
