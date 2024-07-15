import pytest
from src.database import Account
from src.database import RecordAlreadyExists


@pytest.fixture
def setup():
    Account.deleteAllFromDatabase()
    account1 = Account('Test Account', 1000, 1)
    account1.addToDatabase()
    account2 = Account('Test Account 2', 2000, 2)
    account2.addToDatabase()
    try:
        account3 = Account('Test Account', 3000, 3)
        account3.addToDatabase()
    except RecordAlreadyExists:
        pass
    yield
    Account.deleteAllFromDatabase()


def test_importFromDatabase(setup):
    account = Account.importFromDatabase(1)
    assert account.name == 'Test Account'
    assert account.balance == 1000


def test_edit(setup):
    account = Account.importFromDatabase(1)
    account.edit('New Name', 2000)
    assert account.name == 'New Name'
    assert account.balance == 2000


def test_updateBalance(setup):
    Account.updateBalance(1, 500)
    checkAccount = Account.importFromDatabase(1)
    assert checkAccount.balance == 1500
    Account.updateBalance(1, -500)
    checkAccount = Account.importFromDatabase(1)
    assert checkAccount.balance == 1000


def test_getAll(setup):
    accounts = Account.getAll()
    assert len(accounts) == 2
    assert accounts[0].name == 'Test Account'
    assert accounts[1].name == 'Test Account 2'


def test_transferMoney(setup):
    Account.transferMoney(1, 2, 500)
    sourceAccount = Account.importFromDatabase(1)
    destinationAccount = Account.importFromDatabase(2)
    assert sourceAccount.balance == 500
    assert destinationAccount.balance == 2500
