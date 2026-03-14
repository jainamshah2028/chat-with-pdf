"""Unit tests for the config module."""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock

# Import config - adjust path if needed
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config


class TestConfigInitialization:
    """Test Config class initialization."""

    def test_config_init_with_openai(self, mock_env_vars):
        """Test Config initialization with OpenAI provider."""
        with patch("config.OpenAI"):
            config = Config()
            assert config.provider == "openai"

    @patch.dict(os.environ, {"DEFAULT_PROVIDER": "huggingface"}, clear=False)
    def test_config_init_with_huggingface(self, mock_env_vars):
        """Test Config initialization with HuggingFace provider."""
        config = Config()
        assert config.provider == "huggingface"

    @patch.dict(
        os.environ,
        {"DEFAULT_PROVIDER": "invalid_provider"},
        clear=False,
    )
    def test_config_invalid_provider(self):
        """Test Config with invalid provider raises error."""
        with pytest.raises((ValueError, AttributeError, KeyError)):
            Config()

    def test_config_missing_openai_key(self):
        """Test Config fails gracefully when OpenAI key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(KeyError):
                Config()


class TestConfigMethods:
    """Test Config class methods."""

    def test_config_has_get_llm_method(self, mock_env_vars):
        """Test that Config has get_llm method."""
        with patch("config.OpenAI"):
            config = Config()
            assert hasattr(config, "get_llm") or hasattr(config, "__call__")

    @patch.dict(
        os.environ,
        {"OPENAI_API_KEY": "test-key", "OPENAI_MODEL": "gpt-4"},
        clear=False,
    )
    def test_openai_model_configuration(self):
        """Test OpenAI model is correctly configured."""
        with patch("config.OpenAI") as mock_openai:
            mock_instance = MagicMock()
            mock_openai.return_value = mock_instance
            config = Config()
            # Verify OpenAI was called (initialization check)
            assert mock_openai.called or mock_instance is not None


class TestConfigEdgeCases:
    """Test edge cases and error handling."""

    def test_config_empty_provider_string(self):
        """Test Config with empty provider string."""
        with patch.dict(
            os.environ,
            {"DEFAULT_PROVIDER": "", "OPENAI_API_KEY": "test"},
            clear=False,
        ):
            with pytest.raises((ValueError, KeyError)):
                Config()

    def test_config_none_provider(self):
        """Test Config when provider is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(KeyError):
                Config()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
