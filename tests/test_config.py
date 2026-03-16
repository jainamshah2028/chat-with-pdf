"""Unit tests for the config module."""

import os
# Import config - adjust path if needed
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import AppConfig, Config, Themes


class TestAppConfigInitialization:
    """Test AppConfig class initialization."""

    def test_appconfig_class_exists(self):
        """Test that AppConfig class exists."""
        assert AppConfig is not None

    def test_config_alias_exists(self):
        """Test that Config alias exists for backward compatibility."""
        assert Config is AppConfig

    def test_appconfig_has_openai_models(self):
        """Test AppConfig has OpenAI models configured."""
        assert hasattr(AppConfig, "OPENAI_MODELS")
        assert "GPT-3.5 Turbo" in AppConfig.OPENAI_MODELS
        assert "GPT-4" in AppConfig.OPENAI_MODELS

    def test_appconfig_has_ollama_models(self):
        """Test AppConfig has Ollama models configured."""
        assert hasattr(AppConfig, "OLLAMA_MODELS")
        assert "Llama 2" in AppConfig.OLLAMA_MODELS

    def test_appconfig_has_huggingface_models(self):
        """Test AppConfig has HuggingFace embedding models."""
        assert hasattr(AppConfig, "HUGGINGFACE_EMBEDDING_MODELS")
        assert "All MiniLM L6 v2 (Fast)" in AppConfig.HUGGINGFACE_EMBEDDING_MODELS


class TestAppConfigMethods:
    """Test AppConfig class methods."""

    def test_appconfig_ensure_directories_method(self):
        """Test AppConfig has ensure_directories method."""
        assert hasattr(AppConfig, "ensure_directories")
        assert callable(AppConfig.ensure_directories)

    def test_appconfig_get_openai_key_method(self):
        """Test AppConfig has get_openai_key method."""
        assert hasattr(AppConfig, "get_openai_key")
        assert callable(AppConfig.get_openai_key)

    def test_appconfig_set_openai_key_method(self):
        """Test AppConfig has set_openai_key method."""
        assert hasattr(AppConfig, "set_openai_key")
        assert callable(AppConfig.set_openai_key)

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-12345"}, clear=False)
    def test_get_openai_key_returns_value(self):
        """Test getting OpenAI key from environment."""
        key = AppConfig.get_openai_key()
        assert key == "test-key-12345"

    def test_get_openai_key_returns_none_when_not_set(self):
        """Test get_openai_key returns None when not set."""
        with patch.dict(os.environ, {}, clear=True):
            key = AppConfig.get_openai_key()
            assert key is None

    def test_set_openai_key_updates_environment(self):
        """Test setting OpenAI key."""
        AppConfig.set_openai_key("new-test-key")
        assert os.getenv("OPENAI_API_KEY") == "new-test-key"


class TestAppConfigSettings:
    """Test AppConfig settings."""

    def test_supported_formats(self):
        """Test supported file formats are defined."""
        assert hasattr(AppConfig, "SUPPORTED_FORMATS")
        assert "pdf" in AppConfig.SUPPORTED_FORMATS

    def test_max_file_size(self):
        """Test max file size is set."""
        assert hasattr(AppConfig, "MAX_FILE_SIZE_MB")
        assert AppConfig.MAX_FILE_SIZE_MB > 0

    def test_chunk_size_defaults(self):
        """Test chunk size defaults are set."""
        assert hasattr(AppConfig, "DEFAULT_CHUNK_SIZE")
        assert AppConfig.DEFAULT_CHUNK_SIZE > 0


class TestThemesConfiguration:
    """Test theme configurations."""

    def test_themes_class_exists(self):
        """Test that Themes class exists."""
        assert Themes is not None

    def test_default_theme_exists(self):
        """Test default theme is defined."""
        assert hasattr(Themes, "DEFAULT")
        assert "primary_color" in Themes.DEFAULT

    def test_dark_theme_exists(self):
        """Test dark theme is defined."""
        assert hasattr(Themes, "DARK")
        assert "primary_color" in Themes.DARK

    def test_blue_theme_exists(self):
        """Test blue theme is defined."""
        assert hasattr(Themes, "BLUE")
        assert "primary_color" in Themes.BLUE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
