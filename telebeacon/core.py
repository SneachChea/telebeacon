from datetime import datetime
from telebeacon.telegram_client import TelegramClient

_client = None


def _get_client() -> TelegramClient:
    global _client
    if _client is None:
        _client = TelegramClient()
    return _client


def send_telegram_message(message: str) -> None:
    client = _get_client()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    client.send_message(full_message)
