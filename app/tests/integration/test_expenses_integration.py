"""
Integration tests for expense operations.

Tests the full stack: Router → Service → CRUD → Database
Uses a real test database to verify actual SQL queries and data persistence.
"""

import pytest
from decimal import Decimal
from datetime import date, datetime

from app.models import ExpenseCreate, ExpenseUpdate
from app.services.expenses import ExpenseService, DatabaseError


class TestExpenseServiceIntegration:
    """Integration tests for ExpenseService with real database"""

    def test_create_expense_integration(self, expense_service):
        """Test creating expense through full stack"""
        expense_data = ExpenseCreate(
            amount=Decimal("100.50"), category="Food", description="Lunch", date=date(2024, 1, 15)
        )

        result = expense_service.create(expense_data)

        assert result.id is not None
        assert result.amount == Decimal("100.50")
        assert result.category == "Food"
        assert result.description == "Lunch"
        assert result.date == date(2024, 1, 15)
        assert isinstance(result.created_at, datetime)
        assert isinstance(result.updated_at, datetime)

    def test_get_expense_by_id_integration(self, expense_service):
        """Test retrieving expense by ID through full stack"""
        # Create expense first
        expense_data = ExpenseCreate(
            amount=Decimal("200.00"),
            category="Transport",
            description="Bus ticket",
            date=date(2024, 1, 16),
        )
        created = expense_service.create(expense_data)

        # Retrieve it
        result = expense_service.get_by_id(created.id)

        assert result is not None
        assert result.id == created.id
        assert result.amount == Decimal("200.00")
        assert result.category == "Transport"

    def test_get_expense_by_id_not_found_integration(self, expense_service):
        """Test retrieving non-existent expense"""
        result = expense_service.get_by_id(99999)

        assert result is None

    def test_get_all_expenses_integration(self, expense_service):
        """Test retrieving all expenses through full stack"""
        # Create multiple expenses
        expense1 = ExpenseCreate(amount=Decimal("50.00"), category="Food", date=date(2024, 1, 15))
        expense2 = ExpenseCreate(
            amount=Decimal("75.00"), category="Transport", date=date(2024, 1, 16)
        )

        expense_service.create(expense1)
        expense_service.create(expense2)

        # Get all
        results = expense_service.get_all()

        assert len(results) >= 2
        assert all(expense.id is not None for expense in results)
        assert all(expense.amount > 0 for expense in results)

    def test_update_expense_integration(self, expense_service):
        """Test updating expense through full stack"""
        # Create expense
        expense_data = ExpenseCreate(
            amount=Decimal("100.00"), category="Food", description="Lunch", date=date(2024, 1, 15)
        )
        created = expense_service.create(expense_data)

        # Update it
        update_data = ExpenseUpdate(amount=Decimal("150.00"), description="Dinner")
        updated = expense_service.update(created.id, update_data)

        assert updated is not None
        assert updated.id == created.id
        assert updated.amount == Decimal("150.00")
        assert updated.category == "Food"  # Unchanged
        assert updated.description == "Dinner"  # Changed

    def test_update_expense_not_found_integration(self, expense_service):
        """Test updating non-existent expense"""
        update_data = ExpenseUpdate(amount=Decimal("150.00"))
        result = expense_service.update(99999, update_data)

        assert result is None

    def test_delete_expense_integration(self, expense_service):
        """Test deleting expense through full stack"""
        # Create expense
        expense_data = ExpenseCreate(
            amount=Decimal("100.00"), category="Food", date=date(2024, 1, 15)
        )
        created = expense_service.create(expense_data)

        # Delete it
        deleted = expense_service.delete(created.id)

        assert deleted is True

        # Verify it's gone
        result = expense_service.get_by_id(created.id)
        assert result is None

    def test_delete_expense_not_found_integration(self, expense_service):
        """Test deleting non-existent expense"""
        result = expense_service.delete(99999)

        assert result is False

    def test_full_crud_workflow_integration(self, expense_service):
        """Test complete CRUD workflow"""
        # Create
        expense_data = ExpenseCreate(
            amount=Decimal("100.00"), category="Food", description="Lunch", date=date(2024, 1, 15)
        )
        created = expense_service.create(expense_data)
        assert created.id is not None

        # Read
        retrieved = expense_service.get_by_id(created.id)
        assert retrieved is not None
        assert retrieved.amount == Decimal("100.00")

        # Update
        update_data = ExpenseUpdate(amount=Decimal("150.00"))
        updated = expense_service.update(created.id, update_data)
        assert updated.amount == Decimal("150.00")

        # Verify update persisted
        retrieved_after_update = expense_service.get_by_id(created.id)
        assert retrieved_after_update.amount == Decimal("150.00")

        # Delete
        deleted = expense_service.delete(created.id)
        assert deleted is True

        # Verify deletion
        final_check = expense_service.get_by_id(created.id)
        assert final_check is None
