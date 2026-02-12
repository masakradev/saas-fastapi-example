from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.core.db import get_async_engine, get_async_session


class TestGetAsyncEngine:
    """Tests for get_async_engine function."""

    @patch("app.core.db.create_async_engine")
    @patch("app.core.db.settings")
    def test_returns_engine(
        self, mock_settings: MagicMock, mock_create_engine: MagicMock
    ) -> None:
        """Test that get_async_engine returns an engine."""
        mock_settings.SQLALCHEMY_DATABASE_URI.return_value = "postgresql+asyncpg://test"
        mock_create_engine.return_value = MagicMock(spec=AsyncEngine)

        result = get_async_engine()

        assert result is not None
        mock_create_engine.assert_called_once()

    @patch("app.core.db.create_async_engine")
    @patch("app.core.db.settings")
    def test_raises_on_error(
        self, mock_settings: MagicMock, mock_create_engine: MagicMock
    ) -> None:
        """Test that SQLAlchemyError is re-raised."""
        mock_settings.SQLALCHEMY_DATABASE_URI.return_value = "postgresql+asyncpg://test"
        mock_create_engine.side_effect = SQLAlchemyError("Connection failed")

        with pytest.raises(SQLAlchemyError):
            get_async_engine()


class TestGetAsyncSession:
    """Tests for get_async_session function."""

    @pytest.mark.anyio
    @patch("app.core.db.get_async_engine")
    @patch("app.core.db.async_sessionmaker")
    async def test_yields_session(
        self, mock_sessionmaker: MagicMock, mock_engine: MagicMock
    ) -> None:
        """Test that get_async_session yields a session."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_session
        mock_context.__aexit__.return_value = None
        mock_sessionmaker.return_value.return_value = mock_context

        async for session in get_async_session():
            assert session == mock_session

    @pytest.mark.anyio
    @patch("app.core.db.get_async_engine")
    @patch("app.core.db.async_sessionmaker")
    async def test_configures_sessionmaker(
        self, mock_sessionmaker: MagicMock, mock_engine: MagicMock
    ) -> None:
        """Test that sessionmaker is configured correctly."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_session
        mock_context.__aexit__.return_value = None
        mock_sessionmaker.return_value.return_value = mock_context

        async for _ in get_async_session():
            pass

        mock_sessionmaker.assert_called_once_with(
            bind=mock_engine.return_value,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )
