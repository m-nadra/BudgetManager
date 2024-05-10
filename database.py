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


def add_account(name: str, amount: float):
    "Execute INSERT query to add new account."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO accounts (name, amount) VALUES (?, ?);",
                       (name, amount))
        print("Account added.")
    except connection.Error:
        print("Error occurred. Account not added.")

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
        print("Expense saved.")
    except connection.Error:
        print("Error occurred. Expense not added.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def view_expenses() -> list:
    "Execute SELECT query to view all expenses."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT e.name, e.amount, e.date, a.name
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
            "UPDATE accounts SET amount = amount + ? WHERE id = ?;", (amount, account_id))
        print("Income saved.")
    except connection.Error:
        print("Error occurred. Income not added.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def view_incomes() -> list:
    "Execute SELECT query to view all incomes."
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT i.name, i.amount, i.date, a.name
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
