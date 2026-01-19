import pytest
from decimal import Decimal
from datetime import date, datetime
from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.crud.expenses import create_expense, get_expense_by_id, get_all_expenses, update_expense, delete_expense
import psycopg2

class TestCreateExpense:
    '''Test the create_expense function'''
    def test_create_expense_success(self, mock_conn, mock_cursor):
        '''Test that the create_expense function returns a valid ExpenseResponse'''
        mock_cursor.fetchone.return_value = (1, Decimal("100.00"), "Food", "Lunch", date(2024, 1, 15), datetime.now(), datetime.now())
        expense = create_expense(ExpenseCreate(amount=Decimal("100.00"), category="Food", description="Lunch", date=date(2024, 1, 15)), mock_conn)
        # Assert: Check result
        assert isinstance(expense, ExpenseResponse)
        assert expense.id == 1
        assert expense.amount == Decimal("100.00")
        assert expense.category == "Food"
        assert expense.description == "Lunch"
        assert expense.date == date(2024, 1, 15)
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s) RETURNING *",
            (Decimal("100.00"), "Food", "Lunch", date(2024, 1, 15))
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.rollback.assert_not_called()

    def test_create_expense_failure(self, mock_conn, mock_cursor):
        '''Test that the create_expense function raises an error if the database operation fails'''
        # Setup error on execute() - this is where database errors occur
        mock_cursor.execute.side_effect = psycopg2.Error("Database error")
        with pytest.raises(psycopg2.Error):
            create_expense(ExpenseCreate(amount=Decimal("100.00"), category="Food", description="Lunch", date=date(2024, 1, 15)), mock_conn)
        mock_conn.rollback.assert_called_once()


class TestGetExpenseById:
    '''Test the get_expense_by_id function'''
    def test_get_expense_by_id_success(self, mock_conn, mock_cursor):
        '''Test that the get_expense_by_id function returns a valid ExpenseResponse'''
        mock_cursor.fetchone.return_value = (1, Decimal("100.00"), "Food", "Lunch", date(2024, 1, 15), datetime.now(), datetime.now())
        expense = get_expense_by_id(1, mock_conn)
        # Assert: Check result
        assert isinstance(expense, ExpenseResponse)
        assert expense.id == 1
        assert expense.amount == Decimal("100.00")
        assert expense.category == "Food"
        assert expense.description == "Lunch"
        assert expense.date == date(2024, 1, 15)
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM expenses WHERE id = %s",
            (1,)
        )
        mock_cursor.fetchone.assert_called_once()

    def test_get_expense_by_id_not_found(self, mock_conn, mock_cursor):
        '''Test that the get_expense_by_id function returns None when expense is not found'''
        mock_cursor.fetchone.return_value = None
        expense = get_expense_by_id(999, mock_conn)
        # Assert: Check result
        assert expense is None
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM expenses WHERE id = %s",
            (999,)
        )
        mock_cursor.fetchone.assert_called_once()

    def test_get_expense_by_id_failure(self, mock_conn, mock_cursor):
        '''Test that the get_expense_by_id function raises an error if the database operation fails'''
        # Setup error on execute() - this is where database errors occur
        mock_cursor.execute.side_effect = psycopg2.Error("Database error")
        with pytest.raises(psycopg2.Error):
            get_expense_by_id(1, mock_conn)
        # Note: get_expense_by_id does NOT call rollback, it only re-raises the error


class TestGetAllExpenses:
    '''Test the get_all_expenses function'''
    def test_get_all_expenses_success(self, mock_conn, mock_cursor):
        '''Test that the get_all_expenses function returns a list of ExpenseResponse objects'''
        mock_cursor.fetchall.return_value = [
            (1, Decimal("100.00"), "Food", "Lunch", date(2024, 1, 15), datetime.now(), datetime.now()),
            (2, Decimal("200.00"), "Transport", "Bus", date(2024, 1, 16), datetime.now(), datetime.now()),
        ]
        expenses = get_all_expenses(mock_conn)
        # Assert: Check result
        assert isinstance(expenses, list)
        assert len(expenses) == 2
        assert isinstance(expenses[0], ExpenseResponse)
        assert isinstance(expenses[1], ExpenseResponse)
        assert expenses[0].id == 1
        assert expenses[0].amount == Decimal("100.00")
        assert expenses[0].category == "Food"
        assert expenses[0].description == "Lunch"
        assert expenses[0].date == date(2024, 1, 15)
        assert expenses[1].id == 2
        assert expenses[1].amount == Decimal("200.00")
        assert expenses[1].category == "Transport"
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once_with("SELECT * FROM expenses ORDER BY date DESC")
        mock_cursor.fetchall.assert_called_once()

    def test_get_all_expenses_empty(self, mock_conn, mock_cursor):
        '''Test that the get_all_expenses function returns empty list when no expenses exist'''
        mock_cursor.fetchall.return_value = []
        expenses = get_all_expenses(mock_conn)
        # Assert: Check result
        assert isinstance(expenses, list)
        assert expenses == []
        assert len(expenses) == 0
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once_with("SELECT * FROM expenses ORDER BY date DESC")
        mock_cursor.fetchall.assert_called_once()

    def test_get_all_expenses_failure(self, mock_conn, mock_cursor):
        '''Test that the get_all_expenses function raises an error if the database operation fails'''
        # Setup error on execute() - this is where database errors occur
        mock_cursor.execute.side_effect = psycopg2.Error("Database error")
        with pytest.raises(psycopg2.Error):
            get_all_expenses(mock_conn)
        # Note: get_all_expenses does NOT call rollback, it only re-raises the error


class TestUpdateExpense:
    '''Test the update_expense function'''
    def test_update_expense_success(self, mock_conn, mock_cursor):
        '''Test that the update_expense function returns updated ExpenseResponse'''
        mock_cursor.fetchone.return_value = (1, Decimal("150.00"), "Food", "Dinner", date(2024, 1, 16), datetime.now(), datetime.now())
        expense_update = ExpenseUpdate(amount=Decimal("150.00"), category="Food", description="Dinner", date=date(2024, 1, 16))
        expense = update_expense(1, expense_update, mock_conn)
        # Assert: Check result
        assert isinstance(expense, ExpenseResponse)
        assert expense.id == 1
        assert expense.amount == Decimal("150.00")
        assert expense.category == "Food"
        assert expense.description == "Dinner"
        assert expense.date == date(2024, 1, 16)
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.rollback.assert_not_called()

    def test_update_expense_partial(self, mock_conn, mock_cursor):
        '''Test that the update_expense function supports partial updates'''
        mock_cursor.fetchone.return_value = (1, Decimal("100.00"), "Transport", "Lunch", date(2024, 1, 15), datetime.now(), datetime.now())
        expense_update = ExpenseUpdate(category="Transport")
        expense = update_expense(1, expense_update, mock_conn)
        # Assert: Check result
        assert isinstance(expense, ExpenseResponse)
        assert expense.id == 1
        assert expense.category == "Transport"
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_called_once()

    def test_update_expense_not_found(self, mock_conn, mock_cursor):
        '''Test that the update_expense function returns None when expense is not found'''
        mock_cursor.fetchone.return_value = None
        expense_update = ExpenseUpdate(amount=Decimal("150.00"))
        expense = update_expense(999, expense_update, mock_conn)
        # Assert: Check result
        assert expense is None
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_not_called()

    def test_update_expense_empty_update(self, mock_conn, mock_cursor):
        '''Test that the update_expense function returns current expense when all fields are None'''
        mock_cursor.fetchone.return_value = (1, Decimal("100.00"), "Food", "Lunch", date(2024, 1, 15), datetime.now(), datetime.now())
        expense_update = ExpenseUpdate()
        expense = update_expense(1, expense_update, mock_conn)
        # Assert: Check result - should return current expense via get_expense_by_id
        assert isinstance(expense, ExpenseResponse)
        assert expense.id == 1
        assert expense.amount == Decimal("100.00")
        # Note: When all fields are None, update_expense calls get_expense_by_id internally
        # So we need to setup get_expense_by_id mock, but it's simpler to just check the result

    def test_update_expense_failure(self, mock_conn, mock_cursor):
        '''Test that the update_expense function raises an error if the database operation fails'''
        mock_cursor.execute.side_effect = psycopg2.Error("Database error")
        expense_update = ExpenseUpdate(amount=Decimal("150.00"))
        with pytest.raises(psycopg2.Error):
            update_expense(1, expense_update, mock_conn)
        mock_conn.rollback.assert_called_once()


class TestDeleteExpense:
    '''Test the delete_expense function'''
    def test_delete_expense_success(self, mock_conn, mock_cursor):
        '''Test that the delete_expense function returns True when expense is deleted'''
        mock_cursor.fetchone.return_value = (1, Decimal("100.00"), "Food", "Lunch", date(2024, 1, 15), datetime.now(), datetime.now())
        result = delete_expense(1, mock_conn)
        # Assert: Check result
        assert result is True
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM expenses WHERE id = %s RETURNING *",
            (1,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.rollback.assert_not_called()

    def test_delete_expense_not_found(self, mock_conn, mock_cursor):
        '''Test that the delete_expense function returns False when expense is not found'''
        mock_cursor.fetchone.return_value = None
        result = delete_expense(999, mock_conn)
        # Assert: Check result
        assert result is False
        # Assert: Check database calls
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM expenses WHERE id = %s RETURNING *",
            (999,)
        )
        mock_cursor.fetchone.assert_called_once()
        mock_conn.commit.assert_not_called()

    def test_delete_expense_failure(self, mock_conn, mock_cursor):
        '''Test that the delete_expense function raises an error if the database operation fails'''
        mock_cursor.execute.side_effect = psycopg2.Error("Database error")
        with pytest.raises(psycopg2.Error):
            delete_expense(1, mock_conn)
        mock_conn.rollback.assert_called_once()