from fastapi import Depends
from app.database import get_connection
from app.services.expenses import ExpenseService

def get_expense_service(conn = Depends(get_connection)) -> ExpenseService:
    return ExpenseService(conn)

