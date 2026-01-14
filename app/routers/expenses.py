from fastapi import APIRouter, HTTPException, status, Depends
from app.crud import create_expense, get_expense_by_id, get_all_expenses, update_expense, delete_expense
from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
import psycopg2
from app.database import get_connection


router = APIRouter()



@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense_route(expense: ExpenseCreate, conn = Depends(get_connection)) -> ExpenseResponse:
    """
    Create a new expense.
    
    Returns 201 Created on success.
    """
    try:
        return create_expense(expense, conn)
    except psycopg2.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")



@router.get("/", response_model=list[ExpenseResponse], status_code=status.HTTP_200_OK)
def get_all_expenses_route(conn = Depends(get_connection)) -> list[ExpenseResponse]:
    """
    Get all expenses.
    
    Returns 200 OK with a list of expenses.
    """
    try:
        return get_all_expenses(conn)
    except psycopg2.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")



@router.get("/{id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def get_expense_by_id_route(id: int, conn = Depends(get_connection)) -> ExpenseResponse:
    """
    Get a single expense by ID.
    
    Returns 200 OK if found, 404 Not Found if expense doesn't exist.
    """
    try:
        expense = get_expense_by_id(id, conn)
        if expense is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found")
        return expense
    except HTTPException:
        raise
    except psycopg2.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")



@router.put("/{id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def update_expense_route(id: int, expense: ExpenseUpdate, conn = Depends(get_connection)) -> ExpenseResponse:
    """
    Update an existing expense by ID.
    
    Returns 200 OK if updated successfully, 404 Not Found if expense doesn't exist.
    """
    try:
        updated_expense = update_expense(id, expense, conn)
        if updated_expense is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found")
        return updated_expense
    except HTTPException:
        raise
    except psycopg2.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_route(id: int, conn = Depends(get_connection)):
    """
    Delete an expense by ID.
    
    Returns 204 No Content if deleted successfully, 404 Not Found if expense doesn't exist.
    """
    try:
        deleted = delete_expense(id, conn)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found")
        # 204 No Content means no response body, so we return None explicitly
        return None
    except HTTPException:
        raise
    except psycopg2.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")