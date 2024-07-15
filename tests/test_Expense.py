import pytest
from src.database import Income, Account


@pytest.fixture
def setup():
    expense1 = Income('Test Expense', 100, 1, '2021-01-01')
    expense1.addToDatabase()
    expense2 = Income('Test Expense 2', 200, 2, '2021-01-02')
    expense2.addToDatabase()
    account = Account('Test Account', 1000, 1)
    account.addToDatabase()
    yield
    Income.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()


def test_importFromDatabase(setup):
    expense = Income.importFromDatabase(1)
    assert expense.name == 'Test Expense'
    assert expense.amount == 100


def test_edit(setup):
    expense = Income.importFromDatabase(1)
    expense.name = 'New Name'
    expense.amount = 200
    expense.accountId = 2
    expense.date = '2021-01-02'
    expense.edit()
    checkExpense = Income.importFromDatabase(1)
    assert checkExpense.name == 'New Name'
    assert checkExpense.amount == 200
    assert checkExpense.accountId == 2
    assert checkExpense.date == '2021-01-02'


def test_getAll(setup):
    expenses = Income.getAll()
    assert len(expenses) == 2
    assert expenses[0].name == 'Test Expense'
    assert expenses[1].name == 'Test Expense 2'
