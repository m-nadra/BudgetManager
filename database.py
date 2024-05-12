"Contains functions to interact with the database."
import sqlite3

setup_connection = sqlite3.connect('data.db')
setup_cursor = setup_connection.cursor()

setup_cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                balance REAL NOT NULL)""")

setup_cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                account_id INTEGER NOT NULL,
                date DATE,
                FOREIGN KEY (account_id) REFERENCES accounts(id))""")

setup_cursor.execute("""CREATE TABLE IF NOT EXISTS incomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                account_id INTEGER NOT NULL,
                date DATE,
                FOREIGN KEY (account_id) REFERENCES accounts(id))""")

setup_connection.commit()
setup_cursor.close()
setup_connection.close()


def view_accounts() -> list:
    "Execute SELECT query to view all accounts."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM accounts;")
    accounts = cursor.fetchall()

    cursor.close()
    connection.close()
    return accounts


def add_account(name: str, balance: float):
    "Execute INSERT query to add new account."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?);",
                       (name, balance))
        print("Account added.")
    except Exception as exc:
        print("Error occurred. Account not added.")
        raise sqlite3.Error from exc

    connection.commit()
    cursor.close()
    connection.close()


def add_expense(name: str, amount: float, date: str, account_id: int) -> None:
    "Execute INSERT query to add new expense and UPDATE query to update account amount."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO expenses (name, amount, date, account_id) VALUES (?, ?, ?, ?);",
                       (name, amount, date, account_id))
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?;", (amount, account_id))
        print("Expense saved.")
    except connection.Error:
        print("Error occurred. Expense not added.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def view_expenses() -> list:
    """Execute SELECT query to view all expenses.
        Column order:
        [0] - Expense name
        [1] - Expense amount
        [2] - Expense date
        [3] - Account name
        [4] - Expense ID
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT e.name, e.amount, e.date, a.name, e.id
        FROM expenses AS e
        JOIN accounts AS a
        ON a.id=e.account_id; """)
    expenses = cursor.fetchall()

    cursor.close()
    connection.close()
    return expenses


def add_income(name: str, amount: float, date: str, account_id: int):
    "Execute INSERT query to add new income."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO incomes (name, amount, date, account_id) VALUES (?, ?, ?, ?);",
                       (name, amount, date, account_id))
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?;", (amount, account_id))
        print("Income saved.")
    except connection.Error:
        print("Error occurred. Income not added.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def view_incomes() -> list:
    """Execute SELECT query to view all incomes.
        Column order:
        [0] - Income name
        [1] - Income amount
        [2] - Income date
        [3] - Account name
        [4] - Income ID
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT i.name, i.amount, i.date, a.name, i.id
        FROM incomes AS i
        JOIN accounts AS a
        ON a.id=i.account_id; """)
    incomes = cursor.fetchall()

    cursor.close()
    connection.close()
    return incomes


def transfer(from_account_id: int, to_account_id: int, amount: float):
    "Execute UPDATE query to transfer money between accounts."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE accounts SET amount = amount - ? WHERE id = ?;", (amount, from_account_id))
        cursor.execute(
            "UPDATE accounts SET amount = amount + ? WHERE id = ?;", (amount, to_account_id))
        print("Transfer completed.")
    except connection.Error:
        print("Error occurred. Transfer not completed.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def get_expense(expense_id: int) -> tuple:
    """Return single record from expenses table.
        Column order:
        [0] - Expense name
        [1] - Expense amount
        [2] - Expense date
        [3] - Account name
        [4] - Expense ID
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT e.name, e.amount, e.date, a.name, e.id
        FROM expenses AS e
        JOIN accounts AS a
        ON a.id=e.account_id WHERE e.id = ?;""", (expense_id,))
    expense = cursor.fetchone()

    cursor.close()
    connection.close()
    return expense


def edit_expense(name: str, amount: float, date: str, account_id: int, expense_id: int) -> None:
    "Execute UPDATE query to edit expense."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE expenses SET name = ?, amount = ?, date = ?, account_id = ? WHERE id = ?;",
            (name, amount, date, account_id, expense_id))
        print("Expense updated.")
    except connection.Error:
        print("Error occurred. Expense not updated.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def delete_expense(expense_id: int) -> None:
    "Execute DELETE query to delete expense."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM expenses WHERE id = ?;", (expense_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def get_income(income_id: int) -> tuple:
    """Return single record from incomes table.
        Column order:
        [0] - Income name
        [1] - Income amount
        [2] - Income date
        [3] - Account name
        [4] - Income ID
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT i.name, i.amount, i.date, a.name, i.id
        FROM incomes AS i
        JOIN accounts AS a
        ON a.id=i.account_id WHERE i.id = ?;""", (income_id,))
    income = cursor.fetchone()

    cursor.close()
    connection.close()
    return income


def edit_income(name: str, amount: float, date: str, account_id: int, income_id: int) -> None:
    "Execute UPDATE query to edit income."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE incomes SET name = ?, amount = ?, date = ?, account_id = ? WHERE id = ?;",
            (name, amount, date, account_id, income_id))
        print("Income updated.")
    except connection.Error:
        print("Error occurred. Income not updated.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def delete_income(income_id: int) -> None:
    "Execute DELETE query to delete income."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM incomes WHERE id = ?;", (income_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def delete_account(account_id: int) -> None:
    "Execute DELETE query to delete account."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM accounts WHERE id = ?;", (account_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def get_account(account_id: int) -> tuple:
    "Return single record from accounts table."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM accounts WHERE id = ?;", (account_id,))
    account = cursor.fetchone()

    cursor.close()
    connection.close()
    return account


def edit_account(account_id: int, name: str, balance: float) -> None:
    "Execute UPDATE query to edit account."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE accounts SET name = ?, balance = ? WHERE id = ?;",
                       (name, balance, account_id))
    except connection.Error:
        print("Error occurred. Account not updated.")
        connection.rollback()
    connection.commit()
    cursor.close()
    connection.close()


def undo_expense(expense_id: int) -> None:
    "Execute UPDATE query to undo expense."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            """UPDATE accounts
                SET balance = balance + (SELECT amount FROM expenses WHERE id = ?)
                WHERE id = (SELECT account_id FROM expenses WHERE id = ?);""",
            (expense_id, expense_id))
        cursor.execute("DELETE FROM expenses WHERE id = ?;", (expense_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def undo_income(income_id: int) -> None:
    "Execute UPDATE query to undo income."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            """UPDATE accounts
                SET balance = balance - (SELECT amount FROM incomes WHERE id = ?)
                WHERE id = (SELECT account_id FROM incomes WHERE id = ?);""",
            (income_id, income_id))
        cursor.execute("DELETE FROM incomes WHERE id = ?;", (income_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()
