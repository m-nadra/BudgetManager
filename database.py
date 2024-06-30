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


def get_all_accounts() -> list:
    """
    Execute SELECT query to view all accounts.

    Args:
        None

    Column order:
        [0] - id\n
        [1] - name\n
        [2] - balance

    Returns:
        list: A list of all accounts retrieved from the database.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id, name, printf("%.2f", balance) FROM accounts;')
    accounts = cursor.fetchall()

    cursor.close()
    connection.close()
    return accounts


def add_account(name: str, balance: float) -> None:
    """
    Add new account to the database.
    If account name already exists, raise an error.

    Args:
        name (str): Account name.
        balance (float): Account balance.
    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?);",
                       (name, balance))
    except Exception as exc:
        raise sqlite3.Error from exc

    connection.commit()
    cursor.close()
    connection.close()


def get_account(account_id: int) -> tuple:
    """
    Return single record from accounts table.

    Args:
        account_id (int): The ID of the account to get.

    Column order:
        [0] - Account ID\n
        [1] - Account name\n
        [2] - Account balance

    Returns:
        tuple: A single record from the accounts table.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM accounts WHERE id = ?;", (account_id,))
    account = cursor.fetchone()

    cursor.close()
    connection.close()
    return account


def edit_account(account_id: int, name: str, balance: float) -> None:
    """
    Execute UPDATE query to edit account.

    Args:
        account_id (int): The ID of the account to edit.
        name (str): The name of the account.
        balance (float): The balance of the account.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE accounts SET name = ?, balance = ? WHERE id = ?;",
                       (name, balance, account_id))
    except connection.Error:
        connection.rollback()
    connection.commit()
    cursor.close()
    connection.close()


def delete_account(account_id: int) -> None:
    """
    Execute DELETE query to delete account.

    Args:
        account_id (int): The ID of the account to delete.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM accounts WHERE id = ?;", (account_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def transfer_money(from_account_id: int, to_account_id: int, amount: float):
    """
    Execute UPDATE query to transfer money between accounts.

    Args:
        from_account_id (int): The ID of the account to transfer from.
        to_account_id (int): The ID of the account to transfer to.
        amount (float): The amount to transfer.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?;", (amount, from_account_id))
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?;", (amount, to_account_id))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def get_all_expenses() -> list:
    """
    Execute SELECT query to view all expenses.

    Args:
        None

    Column order:
        [0] - Expense name\n
        [1] - Expense amount\n
        [2] - Expense date\n
        [3] - Account name\n
        [4] - Expense ID

    Returns:
        list: A list of all expenses retrieved from the database.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT e.name, printf("%.2f", e.amount), e.date, a.name, e.id
        FROM expenses AS e
        JOIN accounts AS a
        ON a.id=e.account_id;
        """)
    expenses = cursor.fetchall()

    cursor.close()
    connection.close()
    return expenses


def add_expense(name: str, amount: float, date: str, account_id: int) -> None:
    """
    Adds an expenses table entry to the database 
    and reduces the account balance by the value of the expense.

    Args:
        name (str): The name of the expense.
        amount (float): The amount of the expense.
        date (str): The date of the expense.
        account_id (int): The ID of the account.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO expenses (name, amount, date, account_id) VALUES (?, ?, ?, ?);",
                       (name, amount, date, account_id))
        cursor.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?;", (amount, account_id))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def get_expense(expense_id: int) -> tuple:
    """
    Return single record from expenses table.

    Args:
        expense_id (int): The ID of the expense to get.

    Column order:
        [0] - Expense name\n
        [1] - Expense amount\n
        [2] - Expense date\n
        [3] - Account name\n
        [4] - Expense ID

    Returns:
        tuple: A single record from the expenses table.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT e.name, e.amount, e.date, a.name, e.id
        FROM expenses AS e
        JOIN accounts AS a
        ON a.id=e.account_id WHERE e.id = ?;
        """, (expense_id,))
    expense = cursor.fetchone()

    cursor.close()
    connection.close()
    return expense


def edit_expense(name: str, amount: float, date: str, account_id: int, expense_id: int) -> None:
    """
    Execute UPDATE query to edit expense.

    Args:
        name (str): The name of the expense.
        amount (float): The amount of the expense.
        date (str): The date of the expense.
        account_id (int): The ID of the account.
        expense_id (int): The ID of the expense.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE expenses
            SET name = ?, amount = ?, date = ?, account_id = ?
            WHERE id = ?;
            """, (name, amount, date, account_id, expense_id))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def delete_expense(expense_id: int) -> None:
    """
    Delete expense from the database without changing account balance.

    Args:
        expense_id (int): The ID of the expense to delete.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM expenses WHERE id = ?;", (expense_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def undo_expense(expense_id: int) -> None:
    """
    Remove the expense from the database and add the refund to the account balance.

    Args:
        expense_id (int): The ID of the expense to undo.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + (SELECT amount FROM expenses WHERE id = ?)
            WHERE id = (SELECT account_id FROM expenses WHERE id = ?);
            """, (expense_id, expense_id))
        cursor.execute("DELETE FROM expenses WHERE id = ?;", (expense_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def get_all_incomes() -> list:
    """
    Execute SELECT query to view all incomes.

    Column order:
        [0] - Income name\n
        [1] - Income amount\n
        [2] - Income date\n
        [3] - Account name\n
        [4] - Income ID

    Returns:
        list: A list of all incomes retrieved from the database.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT i.name, printf("%.2f", i.amount), i.date, a.name, i.id
        FROM incomes AS i
        JOIN accounts AS a
        ON a.id=i.account_id; """)
    incomes = cursor.fetchall()

    cursor.close()
    connection.close()
    return incomes


def add_income(name: str, amount: float, date: str, account_id: int):
    """
    Adds an entry to the incomes table in the database 
    and increases the account balance by the value of income.

    Args:
        name (str): The name of the income.
        amount (float): The amount of the income.
        date (str): The date of the income.
        account_id (int): The ID of the account.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO incomes (name, amount, date, account_id) VALUES (?, ?, ?, ?);",
                       (name, amount, date, account_id))
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?;", (amount, account_id))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def get_income(income_id: int) -> tuple:
    """
    Return single record from incomes table.

    Column order:
        [0] - Income name\n
        [1] - Income amount\n
        [2] - Income date\n
        [3] - Account name\n
        [4] - Income ID

    Returns:
        tuple: A single record from the incomes table.
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
    """
    Execute UPDATE query to edit income.

    Args:
        name (str): The name of the income.
        amount (float): The amount of the income.
        date (str): The date of the income.
        account_id (int): The ID of the account.
        income_id (int): The ID of the income.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        balance_change = float(get_income(income_id)[1]) - float(amount)
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - ?
            WHERE id = (SELECT account_id FROM incomes WHERE id = ?);
            """, (balance_change, income_id))
        cursor.execute(
            "UPDATE incomes SET name = ?, amount = ?, date = ?, account_id = ? WHERE id = ?;",
            (name, amount, date, account_id, income_id))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def delete_income(income_id: int) -> None:
    """
    Execute DELETE query to delete income without changing account balance.

    Args:
        income_id (int): The ID of the income to delete.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM incomes WHERE id = ?;", (income_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()


def undo_income(income_id: int) -> None:
    """
    Remove income from the database and subtract the income amount from the account balance.

    Args:
        income_id (int): The ID of the income to undo.

    Returns:
        None
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - (SELECT amount FROM incomes WHERE id = ?)
            WHERE id = (SELECT account_id FROM incomes WHERE id = ?);
            """, (income_id, income_id))
        cursor.execute("DELETE FROM incomes WHERE id = ?;", (income_id,))
    except connection.Error:
        connection.rollback()

    connection.commit()
    cursor.close()
    connection.close()
