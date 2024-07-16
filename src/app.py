"""
This module contains the Flask application for a budget manager.

The application provides routes for managing accounts, expenses, and incomes.
It uses a database module to interact with the underlying database.
"""

from flask import Flask, render_template, request, redirect, url_for
from database import Account, Expense, Income
from database import RecordAlreadyExists

app = Flask(__name__)


@app.route('/')
def main():
    """
    Renders the main page.

    Returns:
        str: The rendered template.
    """
    return render_template('main.html')


@app.route('/accounts', methods=['GET'])
def accounts() -> str:
    """Render 'accounts.html' template."""
    accounts = Account.getAll()
    return render_template('accounts.html', accounts=accounts)


@app.route('/addAccount', methods=['GET'])
def renderAddAccountSite() -> str:
    "Renders the 'add_account.html' template."
    return render_template('add_account.html')


@app.route('/addAccount', methods=['POST'])
def addAccount() -> str:
    """Add account to database and redirect to 'accounts' route.
    If an exception occurs, return 'add_account.html' template with a message.
    """
    name = request.form.get('name')
    balance = request.form.get('balance')
    try:
        Account(name, balance)
    except RecordAlreadyExists:
        message = 'Account already exists! Accounts must have unique names.'
        return render_template('add_account.html', message=message)
    return redirect(url_for('accounts'))


@app.route('/editAccount/<int:accountId>', methods=['GET'])
def renderEditAccountSite(accountId: int) -> str:
    "Render 'edit_account.html' template."
    account = Account.importFromDatabase(accountId)
    return render_template('edit_account.html', account=account)


@app.route('/editAccount/<int:accountId>', methods=['POST'])
def editAccount(accountId: int) -> str:
    """Edit account by its ID. Redirect to 'accounts' route.
    If an exception occurs, return 'edit_account.html' template with a message.
    """
    try:
        name = request.form.get('name')
        balance = request.form.get('balance')
        account = Account.importFromDatabase(accountId)
        account.edit(name, balance)
    except RecordAlreadyExists:
        message = 'Account already exists! Accounts must have unique names.'
        return render_template('edit_account.html', account=Account.importFromDatabase(accountId), message=message)
    return redirect(url_for('accounts'))


@app.route('/deleteAccount/<int:accountId>', methods=['GET'])
def deleteAccount(accountId: int) -> str:
    "Delete account by its ID. Redirect to 'accounts' route."
    account = Account.importFromDatabase(accountId)
    account.deleteFromDatabase()
    return redirect(url_for('accounts'))


@app.route('/transferMoney', methods=['GET'])
def renderTransferMoneySite() -> str:
    "Render 'transfer_money.html' template."
    accounts = Account.getAll()
    return render_template('transfer_money.html', accounts=accounts)


@app.route('/transferMoney/', methods=['POST'])
def transferMoney() -> str:
    "Transfer money between accounts. Redirect to 'accounts' route."
    sourceId = request.form.get('from_account')
    destinationId = request.form.get('to_account')
    amount = float(request.form.get('amount'))
    Account.transferMoney(sourceId, destinationId, amount)
    return redirect(url_for('accounts'))


@app.route('/expenses', methods=['GET'])
def expenses() -> str:
    "Render 'expenses.html' template. If an exception occurs, return 'expenses.html' template without any expenses data."
    expensesList = Expense.getAll()
    accountsList = Account.getAll()
    return render_template('expenses.html', expenses=expensesList, accounts=accountsList)


@app.route('/addExpense', methods=['GET'])
def renderAddExpenseSite() -> str:
    "Render 'add_expense.html' template."
    return render_template('add_expense.html', accounts=Account.getAll())


@app.route('/addExpense', methods=['POST'])
def addExpense() -> str:
    "Add expense to database and redirect to 'expenses' route."
    name = request.form.get('name')
    amount = request.form.get('amount')
    account_id = request.form.get('account')
    date = request.form.get('date')
    Expense(name, amount, account_id, date)
    Account.updateBalance(account_id, -float(amount))
    return redirect(url_for('expenses'))


@app.route('/editExpense/<int:expenseId>', methods=['GET'])
def renderEditExpenseSite(expenseId: int) -> str:
    "Render 'edit_expense.html' template."
    expense = Expense.importFromDatabase(expenseId)
    accounts = Account.getAll()
    return render_template('edit_expense.html', expense=expense, accounts=accounts)


@app.route('/editExpense/<int:expenseId>', methods=['POST'])
def editExpense(expenseId: int) -> str:
    "Edit expense by its ID. Redirect to 'expenses' route."
    expense = Expense.importFromDatabase(expenseId)
    newName = request.form.get('name')
    newDate = request.form.get('date')
    newAccountId = request.form.get('account')
    newAmount = float(request.form.get('amount'))

    if expense.accountId != newAccountId:
        Account.updateBalance(expense.accountId, float(expense.amount))
        Account.updateBalance(newAccountId, -float(expense.amount))
    balanceChange = float(expense.amount) - newAmount
    Account.updateBalance(newAccountId, balanceChange)

    expense.edit(newName, newAmount, newAccountId, newDate)
    return redirect(url_for('expenses'))


@app.route('/deleteExpense/<int:expenseId>', methods=['GET'])
def deleteExpense(expenseId: int) -> str:
    "Delete expense by its ID. Redirect to 'expenses' route."
    expense = Expense.importFromDatabase(expenseId)
    expense.deleteFromDatabase()
    return redirect(url_for('expenses'))


@app.route('/undoExpense/<int:expenseId>', methods=['GET'])
def deleteExpenseFromDatabaseAndUpdateAccountBalance(expenseId: int) -> str:
    "Delete expense by its ID and update account balance. Redirect to 'expenses' route."
    expense = Expense.importFromDatabase(expenseId)
    Account.updateBalance(expense.accountId, float(expense.amount))
    expense.deleteFromDatabase()
    return redirect(url_for('expenses'))


@app.route('/incomes', methods=['GET'])
def incomes() -> str:
    """Render 'incomes.html' template. If an exception occurs, 
    return 'incomes.html' template without any incomes data."""
    incomesList = Income.getAll()
    accountsList = Account.getAll()
    return render_template('incomes.html', incomes=incomesList, accounts=accountsList)


@app.route('/addIncome', methods=['GET'])
def renderAddIncomeSite() -> str:
    "Render 'add_income.html' template."
    accountsList = Account.getAll()
    return render_template('add_income.html', accounts=accountsList)


@app.route('/addIncome', methods=['POST'])
def addIncome() -> str:
    "Get data from form, add income to database and redirect to 'incomes' route."
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    accountId = request.form.get('account')
    Income(name, amount, accountId, date)
    Account.updateBalance(accountId, float(amount))
    return redirect(url_for('incomes'))


@app.route('/editIncome/<int:incomeId>', methods=['GET'])
def renderEditIncomeSite(incomeId: int) -> str:
    "Render 'edit_income.html' template."
    income = Income.importFromDatabase(incomeId)
    accouts = Account.getAll()
    return render_template('edit_income.html', income=income, accounts=accouts)


@app.route('/editIncome/<int:incomeId>', methods=['POST'])
def editIncome(incomeId: int) -> str:
    "Update income by its ID. Redirect to 'incomes' route."
    income = Income.importFromDatabase(incomeId)
    newName = request.form.get('name')
    newDate = request.form.get('date')
    newAmount = float(request.form.get('amount'))
    newAccountId = request.form.get('account')

    if income.accountId != newAccountId:
        Account.updateBalance(income.accountId, -float(income.amount))
        Account.updateBalance(newAccountId, float(income.amount))
    balanceChange = newAmount - float(income.amount)
    Account.updateBalance(newAccountId, balanceChange)

    income.edit(newName, newAmount, newAccountId, newDate)
    return redirect(url_for('incomes'))


@app.route('/deleteIncomeFromDatabase/<int:incomeId>', methods=['GET'])
def deleteIncomeFromDatabase(incomeId: int) -> str:
    "Delete income by its ID. Redirect to 'incomes' route."
    income = Income.importFromDatabase(incomeId)
    income.deleteFromDatabase()
    return redirect(url_for('incomes'))


@app.route('/deleteIncomeFromDatabaseAndUpdateAccountBalance/<int:incomeId>', methods=['GET'])
def deleteIncomeFromDatabaseAndUpdateAccountBalance(incomeId: int) -> str:
    "Delete income by its ID and update account balance. Redirect to 'incomes' route."
    income = Income.importFromDatabase(incomeId)
    Account.updateBalance(income.accountId, -float(income.amount))
    income.deleteFromDatabase()
    return redirect(url_for('incomes'))


if __name__ == '__main__':
    app.run(debug=True)
