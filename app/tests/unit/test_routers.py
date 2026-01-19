"""
Unit tests for FastAPI expense routers.

Tests HTTP endpoints, status codes, response models, and error handling.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from decimal import Decimal
from datetime import date, datetime

from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expenses import ExpenseService, DatabaseError
from app.app import app

# Import dependency function after app is imported to avoid circular imports
from app.dependencies import get_expense_service


@pytest.fixture(autouse=True)
def cleanup_dependencies():
    """Clean up dependency overrides after each test"""
    yield
    app.dependency_overrides.clear()


class TestCreateExpenseRoute:
    """Tests for POST /expenses endpoint"""
    
    def test_create_expense_success(self):
        """Test successful expense creation returns 201 Created"""
        # Arrange: Create mock service and response
        mock_service = Mock(spec=ExpenseService)
        expected_response = ExpenseResponse(
            id=1,
            amount=Decimal("100.00"),
            category="Food",
            description="Lunch",
            date=date(2024, 1, 15),
            created_at=datetime(2024, 1, 15, 10, 0),
            updated_at=datetime(2024, 1, 15, 10, 0)
        )
        mock_service.create.return_value = expected_response
        
        # Override dependency
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.post(
            "/expenses/",
            json={
                "amount": "100.00",
                "category": "Food",
                "description": "Lunch",
                "date": "2024-01-15"
            }
        )
        
        # Assert: Check HTTP response
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["amount"] == "100.00"
        assert response.json()["category"] == "Food"
        assert response.json()["description"] == "Lunch"
        assert response.json()["date"] == "2024-01-15"
        
        # Assert: Check service was called correctly
        mock_service.create.assert_called_once()
        call_args = mock_service.create.call_args[0][0]
        assert isinstance(call_args, ExpenseCreate)
        assert call_args.amount == Decimal("100.00")
    
    def test_create_expense_database_error(self):
        """Test that database error returns 500 Internal Server Error"""
        # Arrange: Mock service raises DatabaseError
        mock_service = Mock(spec=ExpenseService)
        mock_service.create.side_effect = DatabaseError("Database connection failed")
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.post(
            "/expenses/",
            json={
                "amount": "100.00",
                "category": "Food",
                "description": "Lunch",
                "date": "2024-01-15"
            }
        )
        
        # Assert: Check error response
        assert response.status_code == 500
        assert "Database connection failed" in response.json()["detail"]


class TestGetAllExpensesRoute:
    """Tests for GET /expenses endpoint"""
    
    def test_get_all_expenses_success(self):
        """Test successful retrieval returns 200 OK with list"""
        # Arrange: Mock service returns list
        mock_service = Mock(spec=ExpenseService)
        expected_responses = [
            ExpenseResponse(
                id=1,
                amount=Decimal("100.00"),
                category="Food",
                description="Lunch",
                date=date(2024, 1, 15),
                created_at=datetime(2024, 1, 15, 10, 0),
                updated_at=datetime(2024, 1, 15, 10, 0)
            ),
            ExpenseResponse(
                id=2,
                amount=Decimal("200.00"),
                category="Transport",
                description="Bus",
                date=date(2024, 1, 16),
                created_at=datetime(2024, 1, 16, 10, 0),
                updated_at=datetime(2024, 1, 16, 10, 0)
            )
        ]
        mock_service.get_all.return_value = expected_responses
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.get("/expenses/")
        
        # Assert: Check HTTP response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2
        
        # Assert: Check service was called
        mock_service.get_all.assert_called_once()
    
    def test_get_all_expenses_empty(self):
        """Test that empty list returns 200 OK with empty array"""
        # Arrange: Mock service returns empty list
        mock_service = Mock(spec=ExpenseService)
        mock_service.get_all.return_value = []
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.get("/expenses/")
        
        # Assert: Check HTTP response
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_expenses_database_error(self):
        """Test that database error returns 500 Internal Server Error"""
        # Arrange: Mock service raises DatabaseError
        mock_service = Mock(spec=ExpenseService)
        mock_service.get_all.side_effect = DatabaseError("Database error")
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.get("/expenses/")
        
        # Assert: Check error response
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]


class TestGetExpenseByIdRoute:
    """Tests for GET /expenses/{id} endpoint"""
    
    def test_get_expense_by_id_success(self):
        """Test successful retrieval returns 200 OK"""
        # Arrange: Mock service returns expense
        mock_service = Mock(spec=ExpenseService)
        expected_response = ExpenseResponse(
            id=1,
            amount=Decimal("100.00"),
            category="Food",
            description="Lunch",
            date=date(2024, 1, 15),
            created_at=datetime(2024, 1, 15, 10, 0),
            updated_at=datetime(2024, 1, 15, 10, 0)
        )
        mock_service.get_by_id.return_value = expected_response
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.get("/expenses/1")
        
        # Assert: Check HTTP response
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["amount"] == "100.00"
        
        # Assert: Check service was called with correct id
        mock_service.get_by_id.assert_called_once_with(1)
    
    def test_get_expense_by_id_not_found(self):
        """Test that not found returns 404 Not Found"""
        # Arrange: Mock service returns None
        mock_service = Mock(spec=ExpenseService)
        mock_service.get_by_id.return_value = None
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.get("/expenses/999")
        
        # Assert: Check error response
        assert response.status_code == 404
        assert "Expense with id 999 not found" in response.json()["detail"]
        
        # Cleanup
        app.dependency_overrides.clear()
    
    def test_get_expense_by_id_database_error(self):
        """Test that database error returns 500 Internal Server Error"""
        # Arrange: Mock service raises DatabaseError
        mock_service = Mock(spec=ExpenseService)
        mock_service.get_by_id.side_effect = DatabaseError("Database error")
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.get("/expenses/1")
        
        # Assert: Check error response
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]


class TestUpdateExpenseRoute:
    """Tests for PUT /expenses/{id} endpoint"""
    
    def test_update_expense_success(self):
        """Test successful update returns 200 OK"""
        # Arrange: Mock service returns updated expense
        mock_service = Mock(spec=ExpenseService)
        expected_response = ExpenseResponse(
            id=1,
            amount=Decimal("150.00"),
            category="Food",
            description="Dinner",
            date=date(2024, 1, 16),
            created_at=datetime(2024, 1, 15, 10, 0),
            updated_at=datetime(2024, 1, 16, 10, 0)
        )
        mock_service.update.return_value = expected_response
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.put(
            "/expenses/1",
            json={
                "amount": "150.00",
                "category": "Food",
                "description": "Dinner",
                "date": "2024-01-16"
            }
        )
        
        # Assert: Check HTTP response
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["amount"] == "150.00"
        
        # Assert: Check service was called correctly
        mock_service.update.assert_called_once()
        call_id = mock_service.update.call_args[0][0]
        call_expense = mock_service.update.call_args[0][1]
        assert call_id == 1
        assert isinstance(call_expense, ExpenseUpdate)
    
    def test_update_expense_partial(self):
        """Test partial update works correctly"""
        # Arrange: Mock service returns updated expense
        mock_service = Mock(spec=ExpenseService)
        expected_response = ExpenseResponse(
            id=1,
            amount=Decimal("100.00"),
            category="Transport",
            description="Lunch",
            date=date(2024, 1, 15),
            created_at=datetime(2024, 1, 15, 10, 0),
            updated_at=datetime(2024, 1, 15, 11, 0)
        )
        mock_service.update.return_value = expected_response
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request with only category
        client = TestClient(app)
        response = client.put(
            "/expenses/1",
            json={"category": "Transport"}
        )
        
        # Assert: Check HTTP response
        assert response.status_code == 200
        assert response.json()["category"] == "Transport"
    
    def test_update_expense_not_found(self):
        """Test that not found returns 404 Not Found"""
        # Arrange: Mock service returns None
        mock_service = Mock(spec=ExpenseService)
        mock_service.update.return_value = None
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.put(
            "/expenses/999",
            json={"amount": "150.00"}
        )
        
        # Assert: Check error response
        assert response.status_code == 404
        assert "Expense with id 999 not found" in response.json()["detail"]
        
        # Cleanup
        app.dependency_overrides.clear()
    
    def test_update_expense_database_error(self):
        """Test that database error returns 500 Internal Server Error"""
        # Arrange: Mock service raises DatabaseError
        mock_service = Mock(spec=ExpenseService)
        mock_service.update.side_effect = DatabaseError("Database error")
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.put(
            "/expenses/1",
            json={"amount": "150.00"}
        )
        
        # Assert: Check error response
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]


class TestDeleteExpenseRoute:
    """Tests for DELETE /expenses/{id} endpoint"""
    
    def test_delete_expense_success(self):
        """Test successful deletion returns 204 No Content"""
        # Arrange: Mock service returns True
        mock_service = Mock(spec=ExpenseService)
        mock_service.delete.return_value = True
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.delete("/expenses/1")
        
        # Assert: Check HTTP response
        assert response.status_code == 204
        assert response.content == b""  # 204 No Content has no body
        
        # Assert: Check service was called with correct id
        mock_service.delete.assert_called_once_with(1)
    
    def test_delete_expense_not_found(self):
        """Test that not found returns 404 Not Found"""
        # Arrange: Mock service returns False
        mock_service = Mock(spec=ExpenseService)
        mock_service.delete.return_value = False
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.delete("/expenses/999")
        
        # Assert: Check error response
        assert response.status_code == 404
        assert "Expense with id 999 not found" in response.json()["detail"]
        
        # Cleanup
        app.dependency_overrides.clear()
    
    def test_delete_expense_database_error(self):
        """Test that database error returns 500 Internal Server Error"""
        # Arrange: Mock service raises DatabaseError
        mock_service = Mock(spec=ExpenseService)
        mock_service.delete.side_effect = DatabaseError("Database error")
        
        app.dependency_overrides[get_expense_service] = lambda: mock_service
        
        # Act: Make HTTP request
        client = TestClient(app)
        response = client.delete("/expenses/1")
        
        # Assert: Check error response
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]
