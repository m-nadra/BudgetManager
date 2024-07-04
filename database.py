"Contains functions to interact with the database."

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


class Base:
    def deleteFromDatabase(self) -> None:
        "Delete object from the database."
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


engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base(cls=Base)
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
        "Add object to the database."
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
        "Add object to the database."
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
        """
        Create an Income object from the database.

        Args:
            incomeId (int): The ID of the income to import.

        Returns: 
            Income object
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
        """
        Execute UPDATE query to edit income.

        Args:
            name (str): The name of the income.
            amount (float): The amount of the income.
            date (str): The date of the income.
            account_id (int): The ID of the account.

        Returns:
            None
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

    @staticmethod
    def getAll() -> list:
        """
        Return list of all incomes from the database.

        Columns in the table: id, name, amount, account_id, date
        """
        session = Session()
        incomes = session.query(Income).all()
        session.close()
        return incomes

    def deleteFromDatabaseAndUpdateAccountBalance(self):
        """
        Remove income from the database and subtract the income amount from the account balance.

        Args:
            income_id (int): The ID of the income to undo.

        Returns:
            None
        """
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
