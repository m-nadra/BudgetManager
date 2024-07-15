"""Contains functions to interact with the database."""

from pydoc import classname
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.exc import IntegrityError


class RecordNotFound(Exception):
    """Raised when a record is not found in the database."""
    pass


class RecordAlreadyExists(Exception):
    """Raised when a record already exists in the database. Raises only for unique fields."""
    pass


class dbConnection:
    """Context manager for database connection. It is used to create a session object."""

    def __init__(self):
        self.engine = create_engine('sqlite:///data.db')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def __enter__(self):
        return self.Session()

    def __exit__(self, type, value, traceback):
        self.Session().close()


class Base(DeclarativeBase):
    """Contains common fields and methods, which are inherited by all classes."""
    id = Column(Integer, primary_key=True, autoincrement=True)

    def addToDatabase(self) -> None:
        """Add object to the database."""
        with dbConnection() as session:
            try:
                session.add(self)
                session.commit()
            except IntegrityError:
                session.rollback()
                raise RecordAlreadyExists

    def deleteFromDatabase(self) -> None:
        """Delete object from the database.

        Raises:
            RecordNotFound: Raise when the object is not found in the database.
        """
        with dbConnection() as session:
            session.query(self.__class__).filter(
                self.__class__.id == self.id).delete()
            session.commit()

    @classmethod
    def importFromDatabase(cls, objectId: int) -> 'classname':
        """Import object from the database by ID.

        Args:
            objectId (int): id of the object to import.

        Raises:
            RecordNotFound: If the object is not found in the database.

        Returns:
            classname: Imported object.
        """
        with dbConnection() as session:
            importedObject = session.get(cls, objectId)
            if importedObject is None:
                raise RecordNotFound
            return importedObject

    @classmethod
    def getAll(cls) -> list:
        """Get all records from the table.

        Returns:
            list: Table records.
        """
        with dbConnection() as session:
            return session.query(cls).all()

    @classmethod
    def deleteAllFromDatabase(cls) -> None:
        """Delete all records from the table."""
        with dbConnection() as session:
            session.query(cls).delete()
            session.commit()


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
        """Update object data and record in the database.

        Args:
            name (str): New name of the account.
            balance (float): New balance of the account.
        """
        with dbConnection() as session:
            try:
                session.query(Account).filter(Account.id == self.id).update(
                    {'name': name, 'balance': balance})
                session.commit()
                self.name = name
                self.balance = balance
            except IntegrityError:
                session.rollback()
                raise RecordAlreadyExists
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def updateBalance(accountId, balanceChange: float):
        """This method upadate the balance ONLY in the database. After using this method
        you have to import the object again to get the updated balance. 
        Use it only when you are not gonna create object otherwise use edit() method.

        Args:
            balanceChange (float): Amount of money to add or subtract from the account.
            For adding money, use positive values. For subtracting money, use negative values.

        Raises:
            RecordNotFound: If the account is not found in the database.
        """
        with dbConnection() as session:
            account = Account.importFromDatabase(accountId)
            account.balance += balanceChange

            try:
                session.query(Account).filter(
                    Account.id == account.id).update({'balance': account.balance})
                session.commit()
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def transferMoney(sourceId: int, destinationId: int, amount: float) -> None:
        """Transfer money between accounts.

        Args:
            sourceId (int): ID of account to transfer money from.
            destinationId (int): ID of account to transfer money to.
            amount (float): Amount of money to transfer.
        """
        with dbConnection() as session:
            try:
                Account.updateBalance(sourceId, -amount)
                Account.updateBalance(destinationId, amount)
                session.commit()
            except Exception:
                session.rollback()
                raise


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


class Income(Base):
    """Represents an expense table in the database."""
    __tablename__ = 'incomes'
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
            session.query(Income).filter(Income.id == self.id).update(
                {'name': self.name, 'amount': self.amount, 'date': self.date, 'accountId': self.accountId})
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise err


engine = create_engine('sqlite:///data.db', echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
