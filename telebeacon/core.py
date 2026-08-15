from datetime import datetime

from telebeacon.telegram_client import TelegramClient

client = TelegramClient()


def send_telegram_message(message: str) -> None:
    if not client.configured:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # noqa: DTZ005
    full_message = f"[{timestamp}] {message}"
    client.send_message(full_message)
