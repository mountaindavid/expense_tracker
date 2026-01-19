from fastapi import APIRouter, HTTPException, status, Depends
from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expenses import DatabaseError, ExpenseService
from app.dependencies import get_expense_service

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense_route(
    expense: ExpenseCreate, service: ExpenseService = Depends(get_expense_service)
) -> ExpenseResponse:
    """
    Create a new expense.

    Returns 201 Created on success.
    """
    try:
        return service.create(expense)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=list[ExpenseResponse], status_code=status.HTTP_200_OK)
def get_all_expenses_route(
    service: ExpenseService = Depends(get_expense_service),
) -> list[ExpenseResponse]:
    """
    Get all expenses.

    Returns 200 OK with a list of expenses.
    """
    try:
        return service.get_all()
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def get_expense_by_id_route(
    id: int, service: ExpenseService = Depends(get_expense_service)
) -> ExpenseResponse:
    """
    Get a single expense by ID.

    Returns 200 OK if found, 404 Not Found if expense doesn't exist.
    """
    try:
        expense = service.get_by_id(id)
        if expense is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found"
            )
        return expense
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
def update_expense_route(
    id: int, expense: ExpenseUpdate, service: ExpenseService = Depends(get_expense_service)
) -> ExpenseResponse:
    """
    Update an existing expense by ID.

    Returns 200 OK if updated successfully, 404 Not Found if expense doesn't exist.
    """
    try:
        updated_expense = service.update(id, expense)
        if updated_expense is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found"
            )
        return updated_expense
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_route(id: int, service: ExpenseService = Depends(get_expense_service)):
    """
    Delete an expense by ID.

    Returns 204 No Content if deleted successfully, 404 Not Found if expense doesn't exist.
    """
    try:
        deleted = service.delete(id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found"
            )
        # 204 No Content means no response body, so we return None explicitly
        return None
    except HTTPException:
        raise
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
