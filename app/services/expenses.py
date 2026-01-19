from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
import psycopg2
from app.crud import (
    create_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
)


class ExpenseService:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    def create(self, expense: ExpenseCreate) -> ExpenseResponse:
        try:
            return create_expense(expense, self.conn)
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def get_all(self) -> list[ExpenseResponse]:
        """
        Get all expenses.

        Raises:
            DatabaseError: If database operation fails (technical error)
        """
        try:
            return get_all_expenses(self.conn)
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def get_by_id(self, expense_id: int) -> ExpenseResponse:
        """
        Get expense by ID.

        Raises:
            ExpenseNotFoundError: If expense doesn't exist (business error)
            DatabaseError: If database operation fails (technical error)
        """
        try:
            expense = get_expense_by_id(expense_id, self.conn)
            if expense is None:
                raise ExpenseNotFoundError(f"Expense with id {expense_id} not found")
            return expense
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def update(self, expense_id: int, expense: ExpenseUpdate) -> ExpenseResponse:
        """
        Update an expense.

        Raises:
            ExpenseNotFoundError: If expense doesn't exist (business error)
            DatabaseError: If database operation fails (technical error)
        """
        try:
            updated_expense = update_expense(expense_id, expense, self.conn)
            if updated_expense is None:
                raise ExpenseNotFoundError(f"Expense with id {expense_id} not found")
            return updated_expense
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def delete(self, expense_id: int) -> None:
        """
        Delete an expense.

        Raises:
            ExpenseNotFoundError: If expense doesn't exist (business error)
            DatabaseError: If database operation fails (technical error)
        """
        try:
            deleted = delete_expense(expense_id, self.conn)
            if not deleted:
                raise ExpenseNotFoundError(f"Expense with id {expense_id} not found")
            return None
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")


class DatabaseError(Exception):
    """Technical database error - should be converted to 500"""

    pass


class ExpenseNotFoundError(Exception):
    """Business error - expense not found - should be converted to 404"""

    pass
