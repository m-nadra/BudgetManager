"""Contains functions to interact with the database."""

from pydoc import classname
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


class Base:
    """Contains common fields and methods, which are inherited by all classes."""
    id = Column(Integer, primary_key=True, autoincrement=True)

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
    def importFromDatabase(cls, objectId: int) -> 'classname':
        """Import an object from the database.

        Args:
            objectId (int): The ID of object to import.

        Returns:
            classname: Object in database.
        """
        session = Session()
        try:
            importedObject = session.query(cls).get(objectId)
            if importedObject is None:
                raise ValueError
            return importedObject
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

    @staticmethod
    def updateBalance(accountId: int, balanceChange: float):
        """Update balance of the account.

        Args:
            accountId (int): ID of the account to update.
            balanceChange (float): Amount of money to add or subtract from the account.
            For adding money, use positive values.
            For subtracting money, use negative values.
        """
        session = Session()
        try:
            account = session.query(Account).filter_by(id=accountId).one()
            account.balance += balanceChange
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
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
            Account.updateBalance(sourceId, -amount)
            Account.updateBalance(destinationId, amount)
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
    accountId = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    date = Column(String, nullable=False)

    def __init__(self, name: str, amount: float, accountId: int, date: str, id: int = None) -> None:
        """Class constructor.

        Args:
            name (str): Name of the expense.
            amount (float): Amount of the expense.
            accountId (int): Account ID of the expense.
            date (str): Date of the expense.
            id (int, optional): Expense ID. Defaults to None. Database will assign it automatically.
        """
        self.id = id
        self.name = name
        self.amount = amount
        self.accountId = accountId
        self.date = date

    def edit(self) -> None:
        """Update the object in the database without changing account balance.
        To do this use Account.updateBalance() method.
        """
        session = Session()
        try:
            session.query(Expense).filter(Expense.id == self.id).update(
                {'name': self.name, 'amount': self.amount, 'date': self.date, 'accountId': self.accountId})
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()


class Income(Base):
    """Represents an income table in the database."""
    __tablename__ = 'incomes'
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    accountId = Column(Integer, ForeignKey('accounts.id'), nullable=False)
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
        self.accountId = accountId
        self.date = date

    def edit(self) -> None:
        """Update the income in the database without changing account balance.
        To do this use Account.updateBalance() method.
        """
        session = Session()
        try:
            session.query(Income).filter(Income.id == self.id).update(
                {'name': self.name, 'amount': self.amount, 'date': self.date, 'accountId': self.accountId})
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err
        finally:
            session.close()
