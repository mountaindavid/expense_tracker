"""
Unit tests for Pydantic expense models.

Tests validation logic, field constraints, and model creation.
"""

import pytest
from decimal import Decimal
from datetime import date, datetime, timedelta
from pydantic import ValidationError

from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate


class TestExpenseCreate:
    """Tests for ExpenseCreate model - request validation"""

    def test_create_valid_expense(self):
        """Test creating expense with valid data"""
        expense = ExpenseCreate(
            amount=Decimal("100.50"), category="Food", description="Lunch", date=date(2024, 1, 15)
        )

        assert expense.amount == Decimal("100.50")
        assert expense.category == "Food"
        assert expense.description == "Lunch"
        assert expense.date == date(2024, 1, 15)

    def test_create_expense_without_description(self):
        """Test creating expense without optional description"""
        expense = ExpenseCreate(
            amount=Decimal("50.00"), category="Transport", date=date(2024, 1, 15)
        )

        assert expense.description is None
        assert expense.amount == Decimal("50.00")

    def test_create_expense_negative_amount_raises_error(self):
        """Test that negative amount raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(amount=Decimal("-10.00"), category="Food", date=date(2024, 1, 15))

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_zero_amount_raises_error(self):
        """Test that zero amount raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(amount=Decimal("0.00"), category="Food", date=date(2024, 1, 15))

        errors = exc_info.value.errors()
        assert any(error["msg"] == "Input should be greater than 0" for error in errors)
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_create_expense_empty_category_raises_error(self):
        """Test that empty category raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(amount=Decimal("100.00"), category="", date=date(2024, 1, 15))

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("category",) for error in errors)

    def test_create_expense_category_too_long_raises_error(self):
        """Test that category longer than 100 chars raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.00"),
                category="A" * 101,  # 101 characters
                date=date(2024, 1, 15),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("category",) for error in errors)

    def test_create_expense_future_date_raises_error(self):
        """Test that future date raises ValidationError"""
        future_date = date.today() + timedelta(days=1)

        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(amount=Decimal("100.00"), category="Food", date=future_date)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("date",) for error in errors)

    def test_create_expense_today_date_valid(self):
        """Test that today's date is valid"""
        expense = ExpenseCreate(amount=Decimal("100.00"), category="Food", date=date.today())

        assert expense.date == date.today()

    def test_create_expense_description_too_long_raises_error(self):
        """Test that description longer than 255 chars raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.00"),
                category="Food",
                description="A" * 256,  # 256 characters
                date=date(2024, 1, 15),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("description",) for error in errors)

    def test_create_expense_amount_too_many_decimal_places(self):
        """Test that amount with more than 2 decimal places raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.999"),  # 3 decimal places
                category="Food",
                date=date(2024, 1, 15),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_create_expense_amount_string_raises_error(self):
        """Test that string instead of number for amount raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount="abc", category="Food", date=date(2024, 1, 15)  # String instead of number
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_create_expense_amount_none_raises_error(self):
        """Test that None for required amount field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=None, category="Food", date=date(2024, 1, 15)  # None for required field
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_create_expense_amount_missing_raises_error(self):
        """Test that missing required amount field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                # amount field is missing
                category="Food",
                date=date(2024, 1, 15),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_create_expense_category_none_raises_error(self):
        """Test that None for required category field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.00"),
                category=None,  # None for required field
                date=date(2024, 1, 15),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("category",) for error in errors)

    def test_create_expense_category_missing_raises_error(self):
        """Test that missing required category field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.00"),
                # category field is missing
                date=date(2024, 1, 15),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("category",) for error in errors)

    def test_create_expense_date_string_raises_error(self):
        """Test that string instead of date for date field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.00"),
                category="Food",
                date="2024.01.15",  # String instead of date object
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("date",) for error in errors)

    def test_create_expense_date_none_raises_error(self):
        """Test that None for required date field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.00"), category="Food", date=None  # None for required field
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("date",) for error in errors)

    def test_create_expense_date_missing_raises_error(self):
        """Test that missing required date field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("100.00"),
                category="Food",
                # date field is missing
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("date",) for error in errors)

    def test_create_expense_amount_integer_converts_to_decimal(self):
        """Test that integer is automatically converted to Decimal by Pydantic"""
        # Pydantic automatically converts int to Decimal
        expense = ExpenseCreate(
            amount=100, category="Food", date=date(2024, 1, 15)  # int is converted to Decimal(100)
        )
        assert expense.amount == Decimal("100")
        assert isinstance(expense.amount, Decimal)

    def test_create_expense_amount_string_number_converts_to_decimal(self):
        """Test that string number is automatically converted to Decimal by Pydantic"""
        # Pydantic automatically converts valid string number to Decimal
        expense = ExpenseCreate(
            amount="100.50",  # String number is converted to Decimal
            category="Food",
            date=date(2024, 1, 15),
        )
        assert expense.amount == Decimal("100.50")
        assert isinstance(expense.amount, Decimal)

    def test_create_expense_amount_too_many_digits_raises_error(self):
        """Test that amount with more than 10 digits raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("12345678901"),  # 11 digits, max_digits=10
                category="Food",
                date=date(2024, 1, 15),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_create_expense_category_exact_max_length_valid(self):
        """Test that category with exactly 100 characters is valid"""
        expense = ExpenseCreate(
            amount=Decimal("100.00"),
            category="A" * 100,  # Exactly 100 characters (boundary value)
            date=date(2024, 1, 15),
        )
        assert len(expense.category) == 100

    def test_create_expense_description_exact_max_length_valid(self):
        """Test that description with exactly 255 characters is valid"""
        expense = ExpenseCreate(
            amount=Decimal("100.00"),
            category="Food",
            description="A" * 255,  # Exactly 255 characters (boundary value)
            date=date(2024, 1, 15),
        )
        assert len(expense.description) == 255

    def test_create_expense_description_none_explicit(self):
        """Test that description can be explicitly set to None"""
        expense = ExpenseCreate(
            amount=Decimal("100.00"),
            category="Food",
            description=None,  # Explicitly None
            date=date(2024, 1, 15),
        )
        assert expense.description is None

    def test_create_expense_multiple_errors_at_once(self):
        """Test that multiple validation errors are reported together"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseCreate(
                amount=Decimal("-10.00"),  # Negative
                category="",  # Empty string
                date=date.today() + timedelta(days=1),  # Future date
            )

        errors = exc_info.value.errors()
        error_locations = [error["loc"] for error in errors]
        # Check that all three errors are present
        assert ("amount",) in error_locations
        assert ("category",) in error_locations
        assert ("date",) in error_locations

    def test_create_expense_with_invalid_category_input_raises_error(self):
        """Test that invalid category input raises ValidationError"""
        with pytest.raises(ValidationError) as exc_error:
            ExpenseCreate(amount=Decimal(0.01), category=123, date=date(2024, 1, 15))
        errors = exc_error.value.errors()
        assert any(error["loc"] == ("category",) for error in errors)


class TestExpenseResponse:
    """Tests for ExpenseResponse model - response with id and timestamps"""

    def test_create_valid_expense_response(self):
        """Test creating expense response with all fields"""
        expense = ExpenseResponse(
            id=1,
            amount=Decimal("100.50"),
            category="Food",
            description="Lunch",
            date=date(2024, 1, 15),
            created_at=datetime(2024, 1, 15, 10, 30, 0),
            updated_at=datetime(2024, 1, 15, 10, 30, 0),
        )

        assert expense.id == 1
        assert expense.amount == Decimal("100.50")
        assert expense.created_at == datetime(2024, 1, 15, 10, 30, 0)
        assert expense.updated_at == datetime(2024, 1, 15, 10, 30, 0)

    def test_expense_response_inherits_base_validation(self):
        """Test that ExpenseResponse inherits validation from ExpenseBase"""
        # Should fail because amount is negative
        with pytest.raises(ValidationError):
            ExpenseResponse(
                id=1,
                amount=Decimal("-10.00"),
                category="Food",
                date=date(2024, 1, 15),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_expense_response_id_missing_raises_error(self):
        """Test that missing required id field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseResponse(
                # id field is missing
                amount=Decimal("100.00"),
                category="Food",
                date=date(2024, 1, 15),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("id",) for error in errors)

    def test_expense_response_id_none_raises_error(self):
        """Test that None for required id field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseResponse(
                id=None,  # None for required field
                amount=Decimal("100.00"),
                category="Food",
                date=date(2024, 1, 15),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("id",) for error in errors)

    def test_expense_response_id_string_raises_error(self):
        """Test that string instead of int for id raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseResponse(
                id="abc",  # String instead of int
                amount=Decimal("100.00"),
                category="Food",
                date=date(2024, 1, 15),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("id",) for error in errors)

    def test_expense_response_created_at_missing_raises_error(self):
        """Test that missing required created_at field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseResponse(
                id=1,
                amount=Decimal("100.00"),
                category="Food",
                date=date(2024, 1, 15),
                # created_at field is missing
                updated_at=datetime.now(),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("created_at",) for error in errors)

    def test_expense_response_updated_at_missing_raises_error(self):
        """Test that missing required updated_at field raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseResponse(
                id=1,
                amount=Decimal("100.00"),
                category="Food",
                date=date(2024, 1, 15),
                created_at=datetime.now(),
                # updated_at field is missing
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("updated_at",) for error in errors)

    def test_expense_response_datetime_string_raises_error(self):
        """Test that string instead of datetime for timestamps raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseResponse(
                id=1,
                amount=Decimal("100.00"),
                category="Food",
                date=date(2024, 1, 15),
                created_at="20240115 10:30:00",  # String instead of date
                updated_at=datetime.now(),
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("created_at",) for error in errors)


class TestExpenseUpdate:
    """Tests for ExpenseUpdate model - partial updates with optional fields"""

    def test_create_empty_update(self):
        """Test creating update with all fields None (valid - no changes)"""
        update = ExpenseUpdate()

        assert update.amount is None
        assert update.category is None
        assert update.description is None
        assert update.date is None

    def test_create_partial_update_amount_only(self):
        """Test updating only amount"""
        update = ExpenseUpdate(amount=Decimal("200.00"))

        assert update.amount == Decimal("200.00")
        assert update.category is None
        assert update.description is None
        assert update.date is None

    def test_create_partial_update_category_only(self):
        """Test updating only category"""
        update = ExpenseUpdate(category="Entertainment")

        assert update.category == "Entertainment"
        assert update.amount is None

    def test_create_partial_update_multiple_fields(self):
        """Test updating multiple fields at once"""
        update = ExpenseUpdate(
            amount=Decimal("150.00"), category="Transport", description="Taxi ride"
        )

        assert update.amount == Decimal("150.00")
        assert update.category == "Transport"
        assert update.description == "Taxi ride"
        assert update.date is None

    def test_update_negative_amount_raises_error(self):
        """Test that negative amount in update raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseUpdate(amount=Decimal("-10.00"))

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_update_zero_amount_raises_error(self):
        """Test that zero amount in update raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseUpdate(amount=Decimal("0.00"))

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_update_empty_category_raises_error(self):
        """Test that empty category in update raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseUpdate(category="")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("category",) for error in errors)

    def test_update_future_date_raises_error(self):
        """Test that future date in update raises ValidationError"""
        future_date = date.today() + timedelta(days=1)

        with pytest.raises(ValidationError) as exc_info:
            ExpenseUpdate(date=future_date)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("date",) for error in errors)

    def test_update_today_date_valid(self):
        """Test that today's date in update is valid"""
        update = ExpenseUpdate(date=date.today())

        assert update.date == date.today()

    def test_update_none_date_valid(self):
        """Test that None date in update is valid (no update)"""
        update = ExpenseUpdate(date=None)

        assert update.date is None

    def test_update_amount_string_raises_error(self):
        """Test that string instead of number for amount in update raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseUpdate(amount="abc")  # String instead of number

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_update_amount_string_number_converts_to_decimal(self):
        """Test that string number is automatically converted to Decimal in update"""
        update = ExpenseUpdate(amount="200.50")  # String number is converted
        assert update.amount == Decimal("200.50")
        assert isinstance(update.amount, Decimal)

    def test_update_date_string_raises_error(self):
        """Test that string instead of date for date in update raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseUpdate(date="20240115")  # String instead of date

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("date",) for error in errors)

    def test_update_category_none_valid(self):
        """Test that None for optional category in update is valid"""
        update = ExpenseUpdate(category=None)  # None for optional field
        assert update.category is None

    def test_update_description_none_valid(self):
        """Test that None for optional description in update is valid"""
        update = ExpenseUpdate(description=None)  # None for optional field
        assert update.description is None

    def test_update_amount_too_many_digits_raises_error(self):
        """Test that amount with more than 10 digits in update raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseUpdate(amount=Decimal("12345678901"))  # 11 digits

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("amount",) for error in errors)

    def test_update_category_exact_max_length_valid(self):
        """Test that category with exactly 100 characters in update is valid"""
        update = ExpenseUpdate(category="A" * 100)  # Exactly 100 characters
        assert len(update.category) == 100

    def test_update_description_exact_max_length_valid(self):
        """Test that description with exactly 255 characters in update is valid"""
        update = ExpenseUpdate(description="A" * 255)  # Exactly 255 characters
        assert len(update.description) == 255
