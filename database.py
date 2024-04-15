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
                FOREIGN KEY (account_id) REFERENCES accounts(id))""")

setup_connection.commit()
setup_cursor.close()
setup_connection.close()


def view_accounts() -> None:
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM accounts;")
    for row in cursor.fetchall():
        print(
            f"Account id: {row[0]}, name: {row[1]}, amount: {format(row[2], '.2f')}")

    cursor.close()
    connection.close()


def add_account(account_name: str, account_amount: float) -> None:
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO accounts (name, amount) VALUES (?, ?);",
                   (account_name, account_amount))

    connection.commit()
    cursor.close()
    connection.close()


def add_expense(expense_name: str, expense_amount: float, account_id: int) -> None:
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO expenses (name, amount, account_id) VALUES (?, ?, ?);",
                       (expense_name, expense_amount, account_id))
        cursor.execute(
            "UPDATE accounts SET amount = amount - ? WHERE id = ?;", (expense_amount, account_id))
    except connection.Error:
        print("Error occurred. Rolling back changes.")
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def view_expenses() -> None:
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """SELECT e.name, e.amount, a.name 
        FROM expenses AS e
        JOIN accounts AS a
        ON a.id = e.account_id;""")
    for row in cursor.fetchall():
        print(
            f"Expense: {row[0]}, amount: {format(row[1], '.2f')}, account id: {row[2]}")

    cursor.close()
    connection.close()
