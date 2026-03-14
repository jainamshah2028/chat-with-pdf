"""Pytest configuration and fixtures for the test suite."""

import os
import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def mock_env_vars():
    """Fixture to provide mock environment variables."""
    env_vars = {
        "OPENAI_API_KEY": "test-key-12345",
        "DEFAULT_PROVIDER": "openai",
        "OPENAI_MODEL": "gpt-3.5-turbo",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        yield env_vars


@pytest.fixture
def mock_openai_client():
    """Fixture to provide a mocked OpenAI client."""
    with patch("config.OpenAI") as mock:
        mock.return_value = Mock()
        yield mock


@pytest.fixture
def sample_text():
    """Fixture providing sample text for testing."""
    return """
    This is a sample text for testing PDF processing.
    It contains multiple sentences and paragraphs.
    
    The quick brown fox jumps over the lazy dog.
    This is useful for testing text chunking and embedding.
    """


@pytest.fixture
def sample_chunks():
    """Fixture providing sample text chunks after processing."""
    return [
        "This is a sample text for testing PDF processing.",
        "It contains multiple sentences and paragraphs.",
        "The quick brown fox jumps over the lazy dog.",
        "This is useful for testing text chunking and embedding.",
    ]


@pytest.fixture
def mock_faiss_index():
    """Fixture to provide a mocked FAISS index."""
    with patch("langchain.vectorstores.FAISS") as mock:
        mock_instance = Mock()
        mock_instance.similarity_search.return_value = [
            Mock(page_content="Test chunk 1"),
            Mock(page_content="Test chunk 2"),
        ]
        mock.return_value = mock_instance
        yield mock
