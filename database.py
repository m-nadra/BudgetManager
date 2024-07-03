"Contains functions to interact with the database."
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    balance = Column(Float, nullable=False)

    def __init__(self, name, balance, id=None):
        self.id = id
        self.name = name
        self.balance = balance

    def addToDatabase(self) -> None:
        """
        Add new account to the database.
        If account name already exists, raise an error.
        """
        session = Session()
        try:
            session.add(self)
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def edit(self, name: str, balance: float) -> None:
        """
        Execute UPDATE query to edit account.

        Args:
            account_id (int): The ID of the account to edit.
            name (str): The name of the account.
            balance (float): The balance of the account.

        Returns:
            None
        """
        session = Session()
        if self.name != name:  # Prevent blocking query when name is not changed
            self.name = name
        self.balance = balance
        try:
            session.query(Account).filter(Account.id == self.id).update(
                {'name': self.name, 'balance': self.balance})
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def deleteFromDatabase(self) -> None:
        """
        Delete account with the given ID from the database.
        """
        session = Session()
        try:
            account = session.query(Account).filter(
                Account.id == self.id).one()
            if account is None:
                raise ValueError
            session.delete(account)
            session.commit()
        finally:
            session.close()

    @classmethod
    def importFromDatabase(cls, accountId: int) -> 'Account':
        """
        Create an Account object from the database.

        Args:
            accountId (int): The ID of the account to import.

        Returns: 
            Account object
        """
        session = Session()
        try:
            account = session.query(Account).filter_by(
                id=accountId).one_or_none()
            if account is None:
                raise ValueError
            return cls(account.name, account.balance, account.id)
        finally:
            session.close()

    @staticmethod
    def getAll() -> list:
        """
        Return list of all accounts from the database.

        Columns in the table: id, name, balance
        """
        session = Session()
        accounts = session.query(Account).all()
        session.close()
        return accounts

    @staticmethod
    def transferMoney(sourceId: int, destinationId: int, amount: float):
        """
        Execute UPDATE query to transfer money between accounts.

        Args:
            from_account_id (int): The ID of the account to transfer from.
            to_account_id (int): The ID of the account to transfer to.
            amount (float): The amount to transfer.

        Returns:
            None
        """
        session = Session()
        try:
            source_account = session.query(
                Account).filter_by(id=sourceId).one()
            destination_account = session.query(
                Account).filter_by(id=destinationId).one()

            source_account.balance -= float(amount)
            destination_account.balance += float(amount)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    date = Column(String, nullable=False)

    def __init__(self, name, amount, account_id, date, id=None):
        self.id = id
        self.name = name
        self.amount = amount
        self.account_id = account_id
        self.date = date

    def addToDatabase(self) -> None:
        "Add new expense to the database."
        session = Session()
        try:
            session.add(self)
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def edit(self, name: str, amount: float, date: str, account_id: int) -> None:
        """
        Execute UPDATE query to edit expense.

        Args:
            name (str): The name of the expense.
            amount (float): The amount of the expense.
            date (str): The date of the expense.
            account_id (int): The ID of the account.

        Returns:
            None
        """
        session = Session()
        self.name = name
        self.amount = amount
        self.date = date
        self.account_id = account_id
        try:
            session.query(Expense).filter(Expense.id == self.id).update(
                {'name': self.name, 'amount': self.amount, 'date': self.date, 'account_id': self.account_id})
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def deleteFromDatabase(self) -> None:
        "Delete expense with the given ID from the database."
        session = Session()
        try:
            expense = session.query(Expense).filter(
                Expense.id == self.id).one()
            if expense is None:
                raise ValueError
            session.delete(expense)
            session.commit()
        finally:
            session.close()

    def deleteFromDatabaseAndUpdateAccountBalance(self) -> None:
        """
        Remove the expense from the database and add the refund to the account balance.

        Args:
            expense_id (int): The ID of the expense to undo.

        Returns:
            None
        """
        session = Session()
        account = Account.importFromDatabase(self.account_id)
        try:
            account.balance += self.amount
            account.edit(account.name, account.balance)
            self.deleteFromDatabase()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def importFromDatabase(self, expenseId: int) -> 'Expense':
        """
        Create an Expense object from the database.

        Args:
            expenseId (int): The ID of the expense to import.

        Returns: 
            Expense object
        """
        session = Session()
        try:
            expense = session.query(Expense).filter_by(
                id=expenseId).one_or_none()
            if expense is None:
                raise ValueError
            return Expense(expense.name, expense.amount, expense.account_id, expense.date, expense.id)
        finally:
            session.close()

    @staticmethod
    def getAll() -> list:
        """
        Return list of all expenses from the database.

        Columns in the table: id, name, amount, account_id, date
        """
        session = Session()
        expenses = session.query(Expense).all()
        session.close()
        return expenses


class Income(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    date = Column(Date, nullable=False)


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
