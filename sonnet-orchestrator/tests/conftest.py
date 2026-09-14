"""Shared session fixtures: the compiled lexicon (loaded once) and Settings."""
from __future__ import annotations

from pathlib import Path

import pytest

from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.lexicon import Lexicon


@pytest.fixture(scope="session")
def settings():
    return load_settings()


@pytest.fixture(scope="session")
def lexicon(settings):
    return Lexicon(Path(settings.cmudict_path))
