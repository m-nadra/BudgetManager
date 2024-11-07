import pytest
from BudgetManager.database import Expense, Account


@pytest.fixture
def setup():
    """Create testing data."""
    Expense.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()
    Account('Test Account', 1000, 1)
    Account('Test Account 2', 2000, 2)
    Expense('Test Expense', 100, 1, '2021-01-01', 1)
    Account.updateBalance(1, -100)
    Expense('Test Expense 2', 200, 2, '2021-01-02', 2)
    Account.updateBalance(2, -200)
    yield
    Expense.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()


def test_importFromDatabase(setup) -> None:
    """Test importing expense from the database."""
    expense = Expense.importFromDatabase(1)
    assert expense.name == 'Test Expense'
    assert expense.amount == 100


def test_edit(setup) -> None:
    """Test if expense is edited and account balance is updated."""
    expense = Expense.importFromDatabase(1)
    account = Account.importFromDatabase(1)
    assert account.balance == 900
    assert expense.name == 'Test Expense'

    expense.edit("New Name", 200, 2, '2021-01-02')
    assert expense.name == 'New Name'
    assert expense.amount == 200
    assert expense.accountId == 2
    assert expense.date == '2021-01-02'

    Account.updateBalance(1, 100)
    Account.updateBalance(2, -200)
    account = Account.importFromDatabase(2)
    assert account.balance == 1600


def test_getAll(setup) -> None:
    """Test if all expenses are fetched from the database."""
    expenses = Expense.getAll()
    assert len(expenses) == 2
    assert expenses[0].name == 'Test Expense'
    assert expenses[1].name == 'Test Expense 2'
