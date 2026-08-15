import os

import requests

TELEGRAM_API_URL = "https://api.telegram.org"
REQUEST_TIMEOUT_SECONDS = 10


class TelegramClient:
    def __init__(
        self,
        token: str | None = None,
        chat_id: str | None = None,
        parse_mode: str | None = "Markdown",
    ):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.parse_mode = parse_mode
        self.configured = bool(self.token and self.chat_id)

    def send_message(self, message: str) -> None:
        if not self.configured:
            return
        assert self.token is not None and self.chat_id is not None

        url = f"{TELEGRAM_API_URL}/bot{self.token}/sendMessage"
        payload: dict[str, str] = {
            "chat_id": self.chat_id,
            "text": message,
        }
        if self.parse_mode is not None:
            payload["parse_mode"] = self.parse_mode
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        if not response.ok:
            raise RuntimeError(
                f"Failed to send message: {response.text}. "
                f"Check that the bot token and chat id are valid, and that the "
                f"message does not contain unescaped {self.parse_mode} characters."
            )
