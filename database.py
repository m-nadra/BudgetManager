"""Contains functions to interact with the database."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


class Base:
    """Contains common fields and methods, which are inherited by all classes."""
    id = Column(Integer, primary_key=True, autoincrement=True)

    def deleteFromDatabase(self) -> None:
        """Delete object from the database."""
        session = Session()
        try:
            objectToDelete = session.query(self.__class__).filter(
                self.__class__.id == self.id).one()
            if objectToDelete is None:
                raise ValueError
            session.delete(objectToDelete)
            session.commit()
        finally:
            session.close()

    @classmethod
    def getAll(cls) -> list:
        """Get all records from the table.

        Returns:
            list: Table records.
        """
        session = Session()
        records = session.query(cls).all()
        session.close()
        return records


engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base(cls=Base)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Account(Base):
    """Represents an account table in the database."""
    __tablename__ = 'accounts'
    name = Column(String, nullable=False, unique=True)
    balance = Column(Float, nullable=False)

    def __init__(self, name: str, balance: float, id: int = None) -> None:
        """Class constructor

        Args:
            name (str): Name of the account.
            balance (float): Amount of money in the account.
            id (int, optional): Account ID. Defaults to None. Database will assign it automatically.
        """
        self.id = id
        self.name = name
        self.balance = balance

    def addToDatabase(self) -> None:
        """Add object to the database."""
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
        """Update the account in the database.

        Args:
            name (str): New name of the account.
            balance (float): New balance of the account.
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

    @classmethod
    def importFromDatabase(cls, accountId: int) -> 'Account':
        """Create an Account object from the database.

        Args:
            accountId (int): ID of the account to import.

        Returns:
            Account: Object of the account.
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
    def transferMoney(sourceId: int, destinationId: int, amount: float) -> None:
        """Transfer money between accounts.

        Args:
            sourceId (int): ID of account to transfer money from.
            destinationId (int): ID of account to transfer money to.
            amount (float): Amount of money to transfer.
        """
        session = Session()
        try:
            sourceAccount = session.query(
                Account).filter_by(id=sourceId).one()
            destinationAccount = session.query(
                Account).filter_by(id=destinationId).one()
            sourceAccount.balance -= float(amount)
            destinationAccount.balance += float(amount)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class Expense(Base):
    """Represents an expense table in the database."""
    __tablename__ = 'expenses'
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    date = Column(String, nullable=False)

    def __init__(self, name: str, amount: float, account_id: int, date: str, id: int = None) -> None:
        """Class constructor.

        Args:
            name (str): Name of the expense.
            amount (float): Amount of the expense.
            account_id (int): Account ID of the expense.
            date (str): Date of the expense.
            id (int, optional): Expense ID. Defaults to None. Database will assign it automatically.
        """
        self.id = id
        self.name = name
        self.amount = amount
        self.account_id = account_id
        self.date = date

    def addToDatabase(self) -> None:
        """Add object to the database."""
        session = Session()
        try:
            account = Account.importFromDatabase(self.account_id)
            account.balance -= float(self.amount)
            account.edit(account.name, account.balance)
            session.add(self)
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def edit(self, name: str, amount: float, date: str, account_id: int) -> None:
        """Update the expense in the database.
        :param name: New name of the expense.
        :param amount: New amount of the expense.
        :param date: New date of the expense.
        :param account_id: Account ID of the expense.
        """
        session = Session()
        try:
            account = Account.importFromDatabase(self.account_id)
            account.balance += float(self.amount) - float(amount)
            account.edit(account.name, account.balance)
            session.query(Expense).filter(Expense.id == self.id).update(
                {'name': name, 'amount': amount, 'date': date, 'account_id': account_id})
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def deleteFromDatabaseAndUpdateAccountBalance(self) -> None:
        """Remove expense from the database and update account balance."""
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
        """Create an Expense object from the database.
        :param expenseId: The ID of the expense to import.
        :return: Expense object
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


class Income(Base):
    """Represents an income table in the database."""
    __tablename__ = 'incomes'
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    date = Column(String, nullable=False)

    def __init__(self, name: str, amount: float, accountId: int, date: str, id: int = None) -> None:
        """Class constructor

        Args:
            name (str): Name of the income,
            amount (float): Amount of the income,
            accountId (int): Account ID of the income,
            date (str): Date of the income,
            id (int, optional): Income ID. Defaults to None. Database will assign it automatically.
        """
        self.id = id
        self.name = name
        self.amount = amount
        self.account_id = accountId
        self.date = date

    def addToDatabase(self) -> None:
        """Add object to the database."""
        session = Session()
        try:
            account = Account.importFromDatabase(self.account_id)
            account.balance += float(self.amount)
            session.add(self)
            account.edit(account.name, account.balance)
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    @classmethod
    def importFromDatabase(cls, incomeId: int) -> 'Income':
        """Create an Income object from the database.

        Args:
            incomeId (int): The ID of the income to import.

        Returns:
            Income: Object of the income.
        """
        session = Session()
        try:
            income = session.query(Income).filter_by(
                id=incomeId).one_or_none()
            if income is None:
                raise ValueError
            return cls(income.name, income.amount, income.account_id, income.date, income.id)
        finally:
            session.close()

    def edit(self, name: str, amount: float, date: str, account_id: int) -> None:
        """Update the income in the database.

        Args:
            name (str): The name of the income.
            amount (float): The amount of the income.
            date (str): The date of the income.
            account_id (int): The ID of the account.
        """
        session = Session()
        try:
            account = Account.importFromDatabase(self.account_id)
            account.balance -= self.amount - float(amount)
            account.edit(account.name, account.balance)
            session.query(Income).filter(Income.id == self.id).update(
                {'name': name, 'amount': amount, 'date': date, 'account_id': account_id})
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def deleteFromDatabaseAndUpdateAccountBalance(self) -> None:
        """Remove income from the database and update account balance."""
        session = Session()
        account = Account.importFromDatabase(self.account_id)
        try:
            account.balance -= self.amount
            account.edit(account.name, account.balance)
            self.deleteFromDatabase()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
