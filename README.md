# telebeacon

[![CI](https://github.com/SneachChea/telebeacon/actions/workflows/ci.yml/badge.svg)](https://github.com/SneachChea/telebeacon/actions/workflows/ci.yml)

Minimal helper package for sending Telegram notifications from Python code.

## Features

- Send timestamped messages to a Telegram chat.
- Decorate functions to notify on start, success, and failure.
- Includes tests and CI checks (`ruff`, `mypy`, `pytest`).

## Installation

```bash
pip install telebeacon
```

For development (tests and tooling):

```bash
python -m pip install -e .[dev]
```

## Configuration

The package requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to be configured. You can set them in three ways:

1. **OS level**: Set them in your shell session or environment (e.g., `export` or `set`).
   ```bash
   export TELEGRAM_BOT_TOKEN="<your-bot-token>"
   export TELEGRAM_CHAT_ID="<your-chat-id>"
   ```
2. **Via `.env` file**: Use `python-dotenv` in your project to load them from a `.env` file. This is the most common approach for libraries installed via pip.
3. **Automatic lookup**: `telebeacon` functions and decorators automatically look for `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in your environment.

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
