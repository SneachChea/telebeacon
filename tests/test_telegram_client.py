"""Unit tests for telebeacon.telegram_client."""

import pytest

from telebeacon.telegram_client import TELEGRAM_API_URL, TelegramClient
import telebeacon.telegram_client as telegram_client_module


def test_init_reads_token_and_chat_id_from_env(monkeypatch) -> None:
    """Constructor should read credentials from environment variables."""

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token123")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "chat456")

    client = TelegramClient()

    assert client.token == "token123"
    assert client.chat_id == "chat456"


def test_init_marks_unconfigured_when_credentials_missing(monkeypatch) -> None:
    """Constructor should not raise but remain unconfigured when env vars are missing."""

    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    client = TelegramClient()

    assert client.configured is False


def test_init_marks_configured_when_credentials_present(monkeypatch) -> None:
    """Constructor should mark client as configured when both credentials are present."""

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token123")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "chat456")

    client = TelegramClient()

    assert client.configured is True


def test_send_message_noop_when_not_configured(monkeypatch) -> None:
    """send_message should do nothing when client is not configured."""

    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    called = False

    class FakeResponse:
        ok = True
        text = ""

    def fake_post(url: str, json: dict[str, str]) -> FakeResponse:
        nonlocal called
        _ = (url, json)
        called = True
        return FakeResponse()

    monkeypatch.setattr(telegram_client_module.requests, "post", fake_post)
    client = TelegramClient(token=None, chat_id=None)

    client.send_message("hello")

    assert called is False


def test_send_message_posts_expected_payload(monkeypatch) -> None:
    """send_message should call Telegram API with expected URL and payload."""

    captured: dict[str, object] = {}

    class FakeResponse:
        ok = True
        text = ""

    def fake_post(url: str, json: dict[str, str]) -> FakeResponse:
        captured["url"] = url
        captured["json"] = json
        return FakeResponse()

    monkeypatch.setattr(telegram_client_module.requests, "post", fake_post)
    client = TelegramClient(token="token123", chat_id="chat456")

    client.send_message("hello")

    assert captured["url"] == f"{TELEGRAM_API_URL}/bottoken123/sendMessage"
    assert captured["json"] == {
        "chat_id": "chat456",
        "text": "hello",
        "parse_mode": "Markdown",
    }


def test_send_message_raises_on_failed_response(monkeypatch) -> None:
    """send_message should raise when Telegram API response is not OK."""

    class FakeResponse:
        ok = False
        text = "bad request"

    def fake_post(url: str, json: dict[str, str]) -> FakeResponse:
        _ = (url, json)
        return FakeResponse()

    monkeypatch.setattr(telegram_client_module.requests, "post", fake_post)
    client = TelegramClient(token="token123", chat_id="chat456")

    with pytest.raises(Exception, match="Failed to send message: bad request"):
        client.send_message("hello")
