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


def test_init_raises_when_credentials_missing(monkeypatch) -> None:
    """Constructor should raise when token/chat id are not provided."""

    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    with pytest.raises(ValueError, match="must be provided"):
        TelegramClient()


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
