"Contains functions to interact with the database."
import sqlite3

setup_connection = sqlite3.connect('data.db')
setup_cursor = setup_connection.cursor()

setup_cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL)""")

setup_cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                account_id INTEGER NOT NULL,
                date DATE,
                FOREIGN KEY (account_id) REFERENCES accounts(id))""")

setup_connection.commit()
setup_cursor.close()
setup_connection.close()


def view_accounts():
    "Execute SELECT query to view all accounts."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM accounts;")
    for row in cursor.fetchall():
        print(
            f"Account id: {row[0]}, name: {row[1]}, amount: {format(row[2], '.2f')}")

    cursor.close()
    connection.close()


def add_account(name: str, amount: float):
    "Execute INSERT query to add new account."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO accounts (name, amount) VALUES (?, ?);",
                   (name, amount))

    connection.commit()
    cursor.close()
    connection.close()


def add_expense(name: str, amount: float, date: str, account_id: int):
    "Execute INSERT query to add new expense and UPDATE query to update account amount."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO expenses (name, amount, date, account_id) VALUES (?, ?, ?, ?);",
                       (name, amount, date, account_id))
        cursor.execute(
            "UPDATE accounts SET amount = amount - ? WHERE id = ?;", (amount, account_id))
    except connection.Error:
        print("Error occurred. Rolling back changes.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def view_expenses():
    "Execute SELECT query to view all expenses."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT e.name, e.amount, e.expense_date, a.name
        FROM expenses AS e
        JOIN accounts AS a
        ON a.id=e.account_id; """)
    for row in cursor.fetchall():
        print(f"Expense: {row[0]}, amount: {format(row[1], '.2f')},"
              "date: {row[2]}, account: {row[3]}")

    cursor.close()
    connection.close()
