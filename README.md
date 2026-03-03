# telebeacon

[![CI](https://github.com/SneachChea/telebeacon/actions/workflows/ci.yml/badge.svg)](https://github.com/SneachChea/telebeacon/actions/workflows/ci.yml)

Minimal helper package for sending Telegram notifications from Python code.

## Features

- Send timestamped messages to a Telegram chat.
- Decorate functions to notify on start, success, and failure.
- Includes tests and CI checks (`ruff`, `mypy`, `pytest`).

## Installation

```bash
python -m pip install .
```

For development (tests and tooling):

```bash
python -m pip install -e .[dev]
```

## Configuration

Set the required environment variables:

```bash
export TELEGRAM_BOT_TOKEN="<your-bot-token>"
export TELEGRAM_CHAT_ID="<your-chat-id>"
```

You can also use a `.env` file and load it with `python-dotenv`.

## Usage

Send a message directly:

```python
from telebeacon.core import send_telegram_message

send_telegram_message("Deployment started")
```

Use the decorator:

```python
from telebeacon.notify_telegram import notify_telegram


@notify_telegram
def run_job() -> None:
 print("running...")
```

## Development

Run tests:

```bash
pytest -q
```

Run pre-commit hooks locally:

```bash
pre-commit run -a -v
```

## CI

GitHub Actions workflow in `.github/workflows/ci.yml` runs:

- Format/lint checks with `ruff`.
- Test suite with `pytest`.
