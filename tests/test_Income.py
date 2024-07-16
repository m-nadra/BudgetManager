import pytest
from src.database import Income, Account


@pytest.fixture
def setup():
    """Create two incomes and one account in the database."""
    Income.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()
    Income('Test Income', 100, 1, '2021-01-01')
    Income('Test Income 2', 200, 2, '2021-01-02')
    Account('Test Account', 1000, 1)
    yield
    Income.deleteAllFromDatabase()
    Account.deleteAllFromDatabase()


def test_importFromDatabase(setup) -> None:
    """Test importing income from the database."""
    income = Income.importFromDatabase(1)
    assert income.name == 'Test Income'
    assert income.amount == 100


def test_edit(setup) -> None:
    """Test if income is edited."""
    income = Income.importFromDatabase(1)
    income.edit("New Name", 200, 2, '2021-01-02')
    assert income.name == 'New Name'
    assert income.amount == 200
    assert income.accountId == 2
    assert income.date == '2021-01-02'


def test_getAll(setup) -> None:
    """Test if all incomes are fetched from the database."""
    incomes = Income.getAll()
    assert len(incomes) == 2
    assert incomes[0].name == 'Test Income'
    assert incomes[1].name == 'Test Income 2'
