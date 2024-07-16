import pytest
from src.database import Income, Account


@pytest.fixture
def setup():
    Income.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()
    income1 = Income('Test Income', 100, 1, '2021-01-01')
    income1.addToDatabase()
    income2 = Income('Test Income 2', 200, 2, '2021-01-02')
    income2.addToDatabase()
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
    income.edit("New Name", 200, 2, '2021-01-02')
    assert income.name == 'New Name'
    assert income.amount == 200
    assert income.accountId == 2
    assert income.date == '2021-01-02'


def test_getAll(setup):
    incomes = Income.getAll()
    assert len(incomes) == 2
    assert incomes[0].name == 'Test Income'
    assert incomes[1].name == 'Test Income 2'
