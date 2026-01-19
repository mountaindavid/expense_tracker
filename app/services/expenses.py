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
        try:
            return get_all_expenses(self.conn)
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def get_by_id(self, expense_id: int) -> ExpenseResponse | None:
        try:
            return get_expense_by_id(expense_id, self.conn)
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def update(self, expense_id: int, expense: ExpenseUpdate) -> ExpenseResponse | None:
        try:
            return update_expense(expense_id, expense, self.conn)
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")

    def delete(self, expense_id: int) -> bool:
        try:
            return delete_expense(expense_id, self.conn)
        except psycopg2.Error as e:
            raise DatabaseError(f"Database error: {str(e)}")


class DatabaseError(Exception):
    pass
