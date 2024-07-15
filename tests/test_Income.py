import pytest
from src.database import Income, Account


@pytest.fixture
def setup():
    Income.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()
    expense1 = Income('Test Income', 100, 1, '2021-01-01')
    expense1.addToDatabase()
    expense2 = Income('Test Income 2', 200, 2, '2021-01-02')
    expense2.addToDatabase()
    account = Account('Test Account', 1000, 1)
    account.addToDatabase()
    yield
    Income.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()


def test_importFromDatabase(setup):
    income = Income.importFromDatabase(1)
    assert income.name == 'Test Income'
    assert income.amount == 100


def test_edit(setup):
    income = Income.importFromDatabase(1)
    income.name = 'New Name'
    income.amount = 200
    income.accountId = 2
    income.date = '2021-01-02'
    income.edit()
    checkIncome = Income.importFromDatabase(1)
    assert checkIncome.name == 'New Name'
    assert checkIncome.amount == 200
    assert checkIncome.accountId == 2
    assert checkIncome.date == '2021-01-02'


def test_getAll(setup):
    incomes = Income.getAll()
    assert len(incomes) == 2
    assert incomes[0].name == 'Test Income'
    assert incomes[1].name == 'Test Income 2'
