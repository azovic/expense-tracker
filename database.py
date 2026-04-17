import sqlite3


DB_NAME = "finance.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_methods (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_name TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        expense_date TEXT NOT NULL,
        description TEXT,
        category_id INTEGER NOT NULL,
        payment_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(category_id),
        FOREIGN KEY (payment_id) REFERENCES payment_methods(payment_id)
    )
    """)

    conn.commit()
    conn.close()


def add_category(category_name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO categories (category_name) VALUES (?)",
            (category_name,)
        )
        conn.commit()
        print("Category added successfully.")
    except sqlite3.IntegrityError:
        print("This category already exists.")
    finally:
        conn.close()


def add_payment_method(payment_name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO payment_methods (payment_name) VALUES (?)",
            (payment_name,)
        )
        conn.commit()
        print("Payment method added successfully.")
    except sqlite3.IntegrityError:
        print("This payment method already exists.")
    finally:
        conn.close()


def get_categories():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT category_id, category_name FROM categories")
    categories = cursor.fetchall()

    conn.close()
    return categories


def get_payment_methods():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT payment_id, payment_name FROM payment_methods")
    methods = cursor.fetchall()

    conn.close()
    return methods


def add_expense(amount, expense_date, description, category_id, payment_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses (amount, expense_date, description, category_id, payment_id)
    VALUES (?, ?, ?, ?, ?)
    """, (amount, expense_date, description, category_id, payment_id))

    conn.commit()
    conn.close()
    print("Expense added successfully.")


def list_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT e.expense_id, e.amount, e.expense_date, e.description,
           c.category_name, p.payment_name
    FROM expenses e
    JOIN categories c ON e.category_id = c.category_id
    JOIN payment_methods p ON e.payment_id = p.payment_id
    ORDER BY e.expense_date DESC
    """)

    expenses = cursor.fetchall()
    conn.close()
    return expenses


def get_total_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses")
    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_expenses_by_category():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.category_name, IFNULL(SUM(e.amount), 0)
    FROM categories c
    LEFT JOIN expenses e ON c.category_id = e.category_id
    GROUP BY c.category_name
    ORDER BY 2 DESC
    """)

    results = cursor.fetchall()
    conn.close()
    return results


def get_expenses_by_payment_method():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.payment_name, IFNULL(SUM(e.amount), 0)
    FROM payment_methods p
    LEFT JOIN expenses e ON p.payment_id = e.payment_id
    GROUP BY p.payment_name
    ORDER BY 2 DESC
    """)

    results = cursor.fetchall()
    conn.close()
    return results

def delete_expense(expense_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE expense_id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    print("Expense deleted successfully.")

def delete_expense(expense_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))

    conn.commit()
    conn.close()


def expense_exists(expense_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM expenses WHERE expense_id = ?", (expense_id,))
    result = cursor.fetchone()

    conn.close()
    return result is not None    