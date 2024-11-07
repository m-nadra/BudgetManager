import pytest
from BudgetManager.database import Account
from BudgetManager.database import RecordAlreadyExists, RecordNotFound


@pytest.fixture
def setup():
    """Create test accounts in the database."""
    Account.deleteAllFromDatabase()
    Account('Test Account', 1000, 1)
    Account('Test Account 2', 2000, 2)
    yield
    Account.deleteAllFromDatabase()


def test_addAndDelete(setup):
    """Test adding and deleting records from the database."""
    account = Account('Test Account 3', 3000, 3)
    account.addToDatabase()
    account = Account.importFromDatabase(3)
    account.deleteFromDatabase()


def test_addToDatabaseUnwantedRecords(setup):
    """Test unwanted records in the database."""
    try:
        # Test for account with not unique name
        Account('Test Account', 3000, 3)
    except RecordAlreadyExists:
        pass
    try:
        # Test for account with existing id
        Account('Test Account', 3000, 1)
    except RecordAlreadyExists:
        pass


def test_importFromDatabase(setup):
    """Test importFromDatabase method for existing and non-existing records."""
    account = Account.importFromDatabase(1)
    assert account.name == 'Test Account'
    assert account.balance == 1000
    try:
        Account.importFromDatabase(3)
    except RecordNotFound:
        pass


def test_edit(setup):
    """Test edit method for existing and non-existing records."""
    account = Account.importFromDatabase(1)
    account.edit('New Name', 2000)
    assert account.name == 'New Name'
    assert account.balance == 2000
    try:
        # Account with the same name shouldn't be added
        account.edit('Test Account 2', 1000)
    except RecordAlreadyExists:
        # If record already exists, the account should not be updated
        assert account.name == 'New Name'
        assert account.balance == 2000


def test_updateBalance(setup):
    """Test updateBalance method for adding and substracting money from the account. Test for non-existing account."""
    Account.updateBalance(1, 500)
    checkAccount = Account.importFromDatabase(1)
    assert checkAccount.balance == 1500
    Account.updateBalance(1, -500)
    checkAccount = Account.importFromDatabase(1)
    assert checkAccount.balance == 1000
    try:
        Account.updateBalance(3, 500)
    except RecordNotFound:
        pass


def test_getAll(setup):
    """Test getAll method for getting all records from the database."""
    accounts = Account.getAll()
    assert len(accounts) == 2
    assert accounts[0].name == 'Test Account'
    assert accounts[1].name == 'Test Account 2'


def test_transferMoney(setup):
    """Test transferMoney method for transferring money between accounts. Test for non-existing account."""
    Account.transferMoney(1, 2, 500)
    sourceAccount = Account.importFromDatabase(1)
    destinationAccount = Account.importFromDatabase(2)
    assert sourceAccount.balance == 500
    assert destinationAccount.balance == 2500
    try:
        Account.transferMoney(5, 2, 600)
    except RecordNotFound:
        pass
