from src.database import Account


def test_importFromDatabase():
    account = Account('Test Account', 1000, 1)
    account.addToDatabase()
    checkAccount = Account.importFromDatabase(1)
    assert checkAccount.name == 'Test Account'
    assert checkAccount.balance == 1000
    checkAccount.deleteFromDatabase()


def test_edit():
    account = Account('Test Account', 1000, 1)
    account.edit('New Name', 2000)
    assert account.name == 'New Name'
    assert account.balance == 2000


def test_updateBalance():
    account = Account('Test Account', 1000, 1)
    account.addToDatabase()
    Account.updateBalance(1, 500)
    checkAccount = Account.importFromDatabase(1)
    assert checkAccount.balance == 1500
    Account.updateBalance(1, -500)
    checkAccount = Account.importFromDatabase(1)
    assert checkAccount.balance == 1000
    checkAccount.deleteFromDatabase()


def test_getAll():
    account1 = Account('Test Account', 1000, 1)
    account1.addToDatabase()
    account2 = Account('Test Account 2', 2000, 2)
    account2.addToDatabase()
    accounts = Account.getAll()
    assert len(accounts) == 2
    assert accounts[0].name == 'Test Account'
    assert accounts[1].name == 'Test Account 2'
    account1 = Account.importFromDatabase(1)
    account1.deleteFromDatabase()
    account2 = Account.importFromDatabase(2)
    account2.deleteFromDatabase()


def test_transferMoney():
    source = Account('Test Account', 1000, 1)
    source.addToDatabase()
    destination = Account('Test Account 2', 2000, 2)
    destination.addToDatabase()
    Account.transferMoney(1, 2, 500)
    checkSource = Account.importFromDatabase(1)
    checkDestination = Account.importFromDatabase(2)
    assert checkSource.balance == 500
    assert checkDestination.balance == 2500
    checkSource.deleteFromDatabase()
    checkDestination.deleteFromDatabase()
