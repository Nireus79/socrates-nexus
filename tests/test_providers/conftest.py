"""Fixtures for provider tests."""

import sys
from unittest.mock import Mock, AsyncMock, MagicMock
import pytest


@pytest.fixture(autouse=True)
def mock_provider_packages():
    """Mock provider packages if not installed."""
    # Store original modules
    original_modules = {}

    # Mock openai package
    if "openai" not in sys.modules:
        original_modules["openai"] = sys.modules.get("openai")
        mock_openai = Mock()
        mock_openai.OpenAI = Mock()
        mock_openai.AsyncOpenAI = Mock()
        sys.modules["openai"] = mock_openai

    # Mock anthropic package
    if "anthropic" not in sys.modules:
        original_modules["anthropic"] = sys.modules.get("anthropic")
        mock_anthropic = Mock()
        mock_anthropic.Anthropic = Mock()
        mock_anthropic.AsyncAnthropic = Mock()
        sys.modules["anthropic"] = mock_anthropic

    # Mock google.generativeai package
    if "google" not in sys.modules:
        original_modules["google"] = sys.modules.get("google")
        mock_google = MagicMock()
        sys.modules["google"] = mock_google

    if "google.generativeai" not in sys.modules:
        original_modules["google.generativeai"] = sys.modules.get("google.generativeai")
        mock_genai = Mock()
        mock_genai.configure = Mock()
        mock_genai.GenerativeModel = Mock()
        sys.modules["google.generativeai"] = mock_genai
        # Also set it on the google module
        sys.modules["google"].generativeai = mock_genai

    # Mock ollama package
    if "ollama" not in sys.modules:
        original_modules["ollama"] = sys.modules.get("ollama")
        mock_ollama = Mock()
        mock_ollama.Client = Mock()
        mock_ollama.AsyncClient = Mock()
        sys.modules["ollama"] = mock_ollama

    yield

    # Clean up after tests - restore original modules or remove mocks
    for mod in ["openai", "anthropic", "google", "google.generativeai", "ollama"]:
        if mod in original_modules:
            if original_modules[mod] is None:
                # Module wasn't there before, remove it
                if mod in sys.modules:
                    del sys.modules[mod]
            # else: restore original (but usually we added it, so this won't happen)
