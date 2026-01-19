from fastapi import APIRouter, HTTPException, status, Depends
from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expenses import DatabaseError, ExpenseNotFoundError, ExpenseService
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
        # Technical error -> HTTP 500
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
        return service.get_by_id(id)
    except ExpenseNotFoundError as e:
        # Business error -> HTTP 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        # Technical error -> HTTP 500
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
        return service.update(id, expense)
    except ExpenseNotFoundError as e:
        # Business error -> HTTP 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        # Technical error -> HTTP 500
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_route(id: int, service: ExpenseService = Depends(get_expense_service)):
    """
    Delete an expense by ID.

    Returns 204 No Content if deleted successfully, 404 Not Found if expense doesn't exist.
    """
    try:
        service.delete(id)
        return None
    except ExpenseNotFoundError as e:
        # Business error -> HTTP 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        # Technical error -> HTTP 500
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
