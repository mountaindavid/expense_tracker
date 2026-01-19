"""
Pytest fixtures for unit tests.
"""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_cursor():
    """Create a mock cursor for database operations"""
    return Mock()


@pytest.fixture
def mock_context_manager(mock_cursor):
    """Create a mock context manager for cursor (with conn.cursor() as cursor:)"""
    mock_context_manager = Mock()
    mock_context_manager.__enter__ = Mock(return_value=mock_cursor)
    mock_context_manager.__exit__ = Mock(return_value=None)
    return mock_context_manager


@pytest.fixture
def mock_conn(mock_context_manager):
    """Create a mock database connection with cursor context manager"""
    mock_conn = Mock()
    mock_conn.cursor.return_value = mock_context_manager
    return mock_conn
