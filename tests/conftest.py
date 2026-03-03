"""Shared pytest fixtures for telebeacon tests."""

from collections.abc import Generator

import pytest

from telebeacon import core


@pytest.fixture(autouse=True)
def reset_client_cache() -> Generator[None, None, None]:
    """Reset the module-level Telegram client cache between tests."""
    core._client = None
    yield
    core._client = None
