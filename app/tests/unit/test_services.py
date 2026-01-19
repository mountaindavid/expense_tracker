"""
Unit tests for ExpenseService.

Tests business logic layer that wraps CRUD operations and handles database errors.
"""

import pytest
from unittest.mock import patch
from decimal import Decimal
from datetime import date, datetime
import psycopg2

from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expenses import ExpenseService, DatabaseError


class TestExpenseServiceCreate:
    """Tests for ExpenseService.create method"""

    def test_create_success(self, mock_conn):
        """Test successful expense creation"""
        expense_data = ExpenseCreate(
            amount=Decimal("100.00"), category="Food", description="Lunch", date=date(2024, 1, 15)
        )
        expected_response = ExpenseResponse(
            id=1,
            amount=Decimal("100.00"),
            category="Food",
            description="Lunch",
            date=date(2024, 1, 15),
            created_at=datetime(2024, 1, 15, 10, 0),
            updated_at=datetime(2024, 1, 15, 10, 0),
        )

        with patch(
            "app.services.expenses.create_expense", return_value=expected_response
        ) as mock_create:
            service = ExpenseService(mock_conn)
            result = service.create(expense_data)

            assert result == expected_response
            mock_create.assert_called_once_with(expense_data, mock_conn)

    def test_create_database_error(self, mock_conn):
        """Test that psycopg2.Error is converted to DatabaseError"""
        expense_data = ExpenseCreate(
            amount=Decimal("100.00"), category="Food", date=date(2024, 1, 15)
        )

        with patch("app.services.expenses.create_expense", side_effect=psycopg2.Error("DB error")):
            service = ExpenseService(mock_conn)
            with pytest.raises(DatabaseError) as exc_info:
                service.create(expense_data)
            assert "Database error: DB error" in str(exc_info.value)


class TestExpenseServiceGetAll:
    """Tests for ExpenseService.get_all method"""

    def test_get_all_success(self, mock_conn):
        """Test successful retrieval of all expenses"""
        expected_responses = [
            ExpenseResponse(
                id=1,
                amount=Decimal("100.00"),
                category="Food",
                description="Lunch",
                date=date(2024, 1, 15),
                created_at=datetime(2024, 1, 15, 10, 0),
                updated_at=datetime(2024, 1, 15, 10, 0),
            ),
            ExpenseResponse(
                id=2,
                amount=Decimal("200.00"),
                category="Transport",
                description="Bus",
                date=date(2024, 1, 16),
                created_at=datetime(2024, 1, 16, 10, 0),
                updated_at=datetime(2024, 1, 16, 10, 0),
            ),
        ]

        with patch(
            "app.services.expenses.get_all_expenses", return_value=expected_responses
        ) as mock_get_all:
            service = ExpenseService(mock_conn)
            result = service.get_all()

            assert result == expected_responses
            mock_get_all.assert_called_once_with(mock_conn)

    def test_get_all_database_error(self, mock_conn):
        """Test that psycopg2.Error is converted to DatabaseError"""
        with patch(
            "app.services.expenses.get_all_expenses", side_effect=psycopg2.Error("DB error")
        ):
            service = ExpenseService(mock_conn)
            with pytest.raises(DatabaseError) as exc_info:
                service.get_all()
            assert "Database error: DB error" in str(exc_info.value)


class TestExpenseServiceGetById:
    """Tests for ExpenseService.get_by_id method"""

    def test_get_by_id_success(self, mock_conn):
        """Test successful retrieval by ID"""
        expected_response = ExpenseResponse(
            id=1,
            amount=Decimal("100.00"),
            category="Food",
            description="Lunch",
            date=date(2024, 1, 15),
            created_at=datetime(2024, 1, 15, 10, 0),
            updated_at=datetime(2024, 1, 15, 10, 0),
        )

        with patch(
            "app.services.expenses.get_expense_by_id", return_value=expected_response
        ) as mock_get_by_id:
            service = ExpenseService(mock_conn)
            result = service.get_by_id(1)

            assert result == expected_response
            mock_get_by_id.assert_called_once_with(1, mock_conn)

    def test_get_by_id_not_found(self, mock_conn):
        """Test that None is returned when expense not found"""
        with patch("app.services.expenses.get_expense_by_id", return_value=None):
            service = ExpenseService(mock_conn)
            result = service.get_by_id(999)

            assert result is None

    def test_get_by_id_database_error(self, mock_conn):
        """Test that psycopg2.Error is converted to DatabaseError"""
        with patch(
            "app.services.expenses.get_expense_by_id", side_effect=psycopg2.Error("DB error")
        ):
            service = ExpenseService(mock_conn)
            with pytest.raises(DatabaseError) as exc_info:
                service.get_by_id(1)
            assert "Database error: DB error" in str(exc_info.value)


class TestExpenseServiceUpdate:
    """Tests for ExpenseService.update method"""

    def test_update_success(self, mock_conn):
        """Test successful expense update"""
        expense_update = ExpenseUpdate(amount=Decimal("150.00"), category="Food")
        expected_response = ExpenseResponse(
            id=1,
            amount=Decimal("150.00"),
            category="Food",
            description="Lunch",
            date=date(2024, 1, 15),
            created_at=datetime(2024, 1, 15, 10, 0),
            updated_at=datetime(2024, 1, 16, 10, 0),
        )

        with patch(
            "app.services.expenses.update_expense", return_value=expected_response
        ) as mock_update:
            service = ExpenseService(mock_conn)
            result = service.update(1, expense_update)

            assert result == expected_response
            mock_update.assert_called_once_with(1, expense_update, mock_conn)

    def test_update_not_found(self, mock_conn):
        """Test that None is returned when expense not found"""
        expense_update = ExpenseUpdate(amount=Decimal("150.00"))

        with patch("app.services.expenses.update_expense", return_value=None):
            service = ExpenseService(mock_conn)
            result = service.update(999, expense_update)

            assert result is None

    def test_update_database_error(self, mock_conn):
        """Test that psycopg2.Error is converted to DatabaseError"""
        expense_update = ExpenseUpdate(amount=Decimal("150.00"))

        with patch("app.services.expenses.update_expense", side_effect=psycopg2.Error("DB error")):
            service = ExpenseService(mock_conn)
            with pytest.raises(DatabaseError) as exc_info:
                service.update(1, expense_update)
            assert "Database error: DB error" in str(exc_info.value)


class TestExpenseServiceDelete:
    """Tests for ExpenseService.delete method"""

    def test_delete_success(self, mock_conn):
        """Test successful expense deletion"""
        with patch("app.services.expenses.delete_expense", return_value=True) as mock_delete:
            service = ExpenseService(mock_conn)
            result = service.delete(1)

            assert result is True
            mock_delete.assert_called_once_with(1, mock_conn)

    def test_delete_not_found(self, mock_conn):
        """Test that False is returned when expense not found"""
        with patch("app.services.expenses.delete_expense", return_value=False):
            service = ExpenseService(mock_conn)
            result = service.delete(999)

            assert result is False

    def test_delete_database_error(self, mock_conn):
        """Test that psycopg2.Error is converted to DatabaseError"""
        with patch("app.services.expenses.delete_expense", side_effect=psycopg2.Error("DB error")):
            service = ExpenseService(mock_conn)
            with pytest.raises(DatabaseError) as exc_info:
                service.delete(1)
            assert "Database error: DB error" in str(exc_info.value)
