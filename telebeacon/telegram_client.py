import os
import requests
from dotenv import load_dotenv


TELEGRAM_API_URL = "https://api.telegram.org"


class TelegramClient:
    def __init__(self, token: str | None = None, chat_id: str | None = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        if not self.token or not self.chat_id:
            raise ValueError("Telegram bot token and chat ID must be provided")

    def send_message(self, message: str) -> None:
        url = f"{TELEGRAM_API_URL}/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(url, json=payload)
        if not response.ok:
            raise Exception(f"Failed to send message: {response.text}")


if __name__ == "__main__":
    load_dotenv()
    client = TelegramClient()
    client.send_message("Hello from TelegramClient!")
