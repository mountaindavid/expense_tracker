from app.models import ExpenseCreate, ExpenseResponse, ExpenseUpdate
import psycopg2


def create_expense(expense: ExpenseCreate, conn: psycopg2.extensions.connection) -> ExpenseResponse:
    """
    Create a new expense in the database

    Args:
        expense: ExpenseCreate model with validated data
        conn: psycopg2 connection object
    Returns:
        ExpenseResponse with id and timestamps from database

    Raises:
        psycopg2.Error: If database operation fails
    """

    try:
        with conn.cursor() as cursor:
            # Create a new expense in the database
            sql = """INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s) RETURNING *"""
            # Execute the SQL statement
            cursor.execute(
                sql, (expense.amount, expense.category, expense.description, expense.date)
            )
            # Fetch the new expense
            row = cursor.fetchone()
            # Commit the transaction
            conn.commit()
            # Return the new expense
            return ExpenseResponse(
                id=row[0],
                amount=row[1],
                category=row[2],
                description=row[3],
                date=row[4],
                created_at=row[5],
                updated_at=row[6],
            )
    except psycopg2.Error:
        conn.rollback()
        raise


def get_expense_by_id(
    expense_id: int, conn: psycopg2.extensions.connection
) -> ExpenseResponse | None:
    """
    Get an expense from the database

    Args:
        expense_id: The ID of the expense to get
        conn: psycopg2 connection object

    Returns:
        ExpenseResponse with the expense data

    Raises:
        psycopg2.Error: If database operation fails
    """
    try:
        with conn.cursor() as cursor:
            sql = """SELECT * FROM expenses WHERE id = %s"""
            cursor.execute(sql, (expense_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return ExpenseResponse(
                id=row[0],
                amount=row[1],
                category=row[2],
                description=row[3],
                date=row[4],
                created_at=row[5],
                updated_at=row[6],
            )
    except psycopg2.Error:
        raise


def get_all_expenses(conn: psycopg2.extensions.connection) -> list[ExpenseResponse]:
    """
    Get all expenses from the database

    Args:
        conn: psycopg2 connection object

    Returns:
        List of ExpenseResponse objects (empty list if none found)

    Raises:
        psycopg2.Error: If database operation fails
    """
    try:
        with conn.cursor() as cursor:
            sql = """SELECT * FROM expenses ORDER BY date DESC"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                ExpenseResponse(
                    id=row[0],
                    amount=row[1],
                    category=row[2],
                    description=row[3],
                    date=row[4],
                    created_at=row[5],
                    updated_at=row[6],
                )
                for row in rows
            ]
    except psycopg2.Error:
        raise


def update_expense(
    expense_id: int, expense: ExpenseUpdate, conn: psycopg2.extensions.connection
) -> ExpenseResponse | None:
    """
    Update an expense in the database (partial update supported)

    Args:
        expense_id: ID of expense to update
        expense: ExpenseUpdate with fields to update (None = don't update)
        conn: psycopg2 connection object

    Returns:
        ExpenseResponse with updated data if found, None if not found

    Raises:
        psycopg2.Error: If database operation fails
    """
    try:
        with conn.cursor() as cursor:
            # Build dynamic SET clause for partial updates
            update_fields = []
            params = []

            if expense.amount is not None:
                update_fields.append("amount = %s")
                params.append(expense.amount)

            if expense.category is not None:
                update_fields.append("category = %s")
                params.append(expense.category)

            if expense.description is not None:
                update_fields.append("description = %s")
                params.append(expense.description)

            if expense.date is not None:
                update_fields.append("date = %s")
                params.append(expense.date)

            # Check if anything to update
            if not update_fields:
                return get_expense_by_id(expense_id, conn)  # No changes, return current

            # Always update timestamp
            update_fields.append("updated_at = CURRENT_TIMESTAMP")

            # Build SQL
            set_clause = ", ".join(update_fields)
            params.append(expense_id)
            sql = f"UPDATE expenses SET {set_clause} WHERE id = %s RETURNING *"

            cursor.execute(sql, tuple(params))
            row = cursor.fetchone()

            # Check if expense exists
            if row is None:
                return None

            conn.commit()

            return ExpenseResponse(
                id=row[0],
                amount=row[1],
                category=row[2],
                description=row[3],
                date=row[4],
                created_at=row[5],
                updated_at=row[6],
            )

    except psycopg2.Error:
        conn.rollback()
        raise


def delete_expense(id: int, conn: psycopg2.extensions.connection) -> bool:
    """
    Delete an expense from the database

    Args:
        id: The ID of the expense to delete
        conn: psycopg2 connection object

    Returns:
        True if the expense was deleted, False otherwise

    Raises:
        psycopg2.Error: If database operation fails
    """
    try:
        with conn.cursor() as cursor:
            sql = """DELETE FROM expenses WHERE id = %s RETURNING *"""
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row is None:
                return False

            conn.commit()
            return True

    except psycopg2.Error:
        conn.rollback()
        raise
