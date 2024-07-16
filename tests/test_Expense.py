import pytest
from src.database import Expense, Account


@pytest.fixture
def setup():
    Expense.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()
    Expense('Test Expense', 100, 1, '2021-01-01')
    Expense('Test Expense 2', 200, 2, '2021-01-02')
    Account('Test Account', 1000, 1)
    yield
    Expense.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()


def test_importFromDatabase(setup):
    expense = Expense.importFromDatabase(1)
    assert expense.name == 'Test Expense'
    assert expense.amount == 100


def test_edit(setup):
    expense = Expense.importFromDatabase(1)
    expense.edit("New Name", 200, 2, '2021-01-02')
    assert expense.name == 'New Name'
    assert expense.amount == 200
    assert expense.accountId == 2
    assert expense.date == '2021-01-02'


def test_getAll(setup):
    expenses = Expense.getAll()
    assert len(expenses) == 2
    assert expenses[0].name == 'Test Expense'
    assert expenses[1].name == 'Test Expense 2'
