"""
This module contains the Flask application for a budget manager.

The application provides routes for managing accounts, expenses, and incomes.
It uses a database module to interact with the underlying database.

Routes:
- '/' : Renders the main page.
- '/accounts' : Handles the accounts route.
- '/add_account' : Renders the 'add_account.html' template.
- '/edit_account/<int:account_id>' : Handles the edit account route.
- '/delete_account/<int:account_id>' : Handles the delete account route.
- '/transfer_money' : Handles the transfer money route.
- '/expenses' : Handles the expenses route.
- '/add_expense' : Renders the 'add_expense.html' template.
- '/edit_expense/<int:expense_id>' : Handles the edit expense route.
- '/delete_expense/<int:expense_id>' : Handles the delete expense route.
- '/undo_expense/<int:expense_id>' : Undo an expense by its ID.
- '/incomes' : Handles the incomes route.
- '/add_income' : Renders the 'add_income.html' template.
- '/edit_income/<int:income_id>' : Handles the edit income route.
- '/delete_income/<int:income_id>' : Handles the delete income route.
- '/undo_income/<int:income_id>' : Undo an income by its ID.
"""

from flask import Flask, render_template, request, redirect, url_for
import database as db

app = Flask(__name__)


@app.route('/')
def main():
    """
    Renders the main page.

    Returns:
        str: The rendered template.
    """
    return render_template('main.html')


@app.route('/accounts', methods=['GET', 'POST'])
def accounts() -> str:
    """
    Handles the accounts route.

    If the request method is 'POST', it adds a new account to the database
    using the account name and balance provided in the form data.

    Returns the rendered 'accounts.html' template with the accounts data
    retrieved from the database. If an exception occurs, it returns the
    'accounts.html' template without any accounts data.

    Returns:
        str: The rendered 'accounts.html' template as a string.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        balance = request.form.get('balance')
        try:
            account = db.Account(name, balance)
            account.addToDatabase()
        except db.IntegrityError:
            message = 'Account already exists! Accounts must have unique names.'
            return render_template('add_account.html', message=message)
    try:
        return render_template('accounts.html', accounts=db.Account.getAll())
    except db.sqlite3.Error:
        return render_template('accounts.html')


@app.route('/add_account')
def add_account() -> str:
    """
    Renders the 'add_account.html' template.

    Returns:
        str: The rendered template.
    """
    return render_template('add_account.html')


@app.route('/edit_account/<int:account_id>', methods=['GET', 'POST'])
def edit_account(account_id: int) -> str:
    """
    Handles the edit account route.

    If the request method is 'GET', it renders the 'edit_account.html' template
    with the account data retrieved from the database.

    If the request method is 'POST', it updates the account in the database
    with the new name and balance provided in the form data.

    Returns the rendered 'accounts.html' template with the updated accounts data
    retrieved from the database.

    Args:
        account_id (int): The ID of the account to be edited.

    Returns:
        str: The rendered 'accounts.html' template as a string.
    """
    if request.method == 'GET':
        return render_template('edit_account.html', account=db.Account.importFromDatabase(account_id))
    name = request.form.get('name')
    balance = request.form.get('balance')
    account = db.Account.importFromDatabase(account_id)
    try:
        account.edit(name, balance)
    except db.sqlite3.Error:
        message = 'Account already exists! Accounts must have unique names.'
        return render_template('edit_account.html', account=db.Account.importFromDatabase(account_id), message=message)
    return render_template('accounts.html', accounts=db.Account.getAll())


@app.route('/delete_account/<int:account_id>')
def delete_account(account_id: int) -> str:
    """
    Handles the delete account route.

    Deletes the account with the specified ID from the database.

    Returns the rendered 'accounts.html' template with the updated accounts data
    retrieved from the database.

    Args:
        account_id (int): The ID of the account to be deleted.

    Returns:
        str: The rendered 'accounts.html' template as a string.
    """
    account = db.Account.importFromDatabase(account_id)
    account.deleteFromDatabase()
    return render_template('accounts.html', accounts=db.Account.getAll())


@app.route('/transfer_money', methods=['GET', 'POST'])
def transfer_money() -> str:
    """
    Handles the transfer money route.
    After transferring money, it returns the rendered 'accounts.html' template.

    Args:
        None

    Returns:
        str: The rendered 'accounts.html' template, if method is POST.
        str: The rendered 'transfer_money.html' template, if method is GET.
    """
    if request.method == 'GET':
        return render_template('transfer_money.html', accounts=db.Account.getAll())

    sourceId = request.form.get('from_account')
    destinationId = request.form.get('to_account')
    amount = request.form.get('amount')
    db.Account.transferMoney(sourceId, destinationId, amount)
    return render_template('accounts.html', accounts=db.Account.getAll())


@app.route('/expenses', methods=['GET'])
def expenses() -> str:
    """
    Handles the expenses route.

    If the request method is 'POST', it adds a new expense to the database
    using the expense name, amount, date, and account ID provided in the form data.

    Returns the rendered 'expenses.html' template with the expenses data
    retrieved from the database. If an exception occurs, it returns the
    'expenses.html' template without any expenses data.

    Returns:
        str: The rendered 'expenses.html' template as a string.
    """
    try:
        return render_template('expenses.html', expenses=db.Expense.getAll(), accounts=db.Account.getAll())
    except db.sqlite3.OperationalError:
        return render_template('expenses.html')


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense() -> str:
    """
    Renders the 'Expense.add.html' template.

    Returns:
        str: The rendered template.
    """
    if request.method == 'GET':
        return render_template('add_expense.html', accounts=db.Account.getAll())
    name = request.form.get('name')
    amount = request.form.get('amount')
    account_id = request.form.get('account')
    date = request.form.get('date')
    expense = db.Expense(name, amount, account_id, date)
    expense.addToDatabase()
    return redirect(url_for('expenses'))


@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id: int) -> str:
    """
    Handles the edit expense route.

    If the request method is 'GET', it renders the 'edit_expense.html' template
    with the expense data retrieved from the database.

    If the request method is 'POST', it updates the expense in the database
    with the new name, amount, date, and account ID provided in the form data.

    Returns the rendered 'expenses.html' template with the updated expenses data
    retrieved from the database.

    Args:
        expense_id (int): The ID of the expense to be edited.

    Returns:
        str: The rendered 'expenses.html' template as a string.
    """
    if request.method == 'GET':
        return render_template('edit_expense.html', expense=db.Expense.importFromDatabase(expense_id),
                               accounts=db.Account.getAll())
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    account_id = request.form.get('account')
    expense = db.Expense.importFromDatabase(expense_id)
    expense.edit(name, amount, date, account_id)
    return redirect(url_for('expenses'))


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id: int) -> str:
    """
    Handles the delete expense route.

    Deletes the expense with the specified ID from the database.

    Returns the rendered 'expenses.html' template with the updated expenses data
    retrieved from the database.

    Args:
        expense_id (int): The ID of the expense to be deleted.

    Returns:
        str: The rendered 'expenses.html' template as a string.
    """
    expense = db.Expense.importFromDatabase(expense_id)
    expense.deleteFromDatabase()
    return redirect(url_for('expenses'))


@app.route('/undo_expense/<int:expense_id>', methods=['GET', 'POST'])
def undo_expense(expense_id: int) -> str:
    """
    Undo an expense by its ID. Update account balance to previous state.

    Parameters:
    - expense_id (int): The ID of the expense to be undone.

    Returns:
    - str: The rendered 'expenses.html' template.

    """
    expense = db.Expense.importFromDatabase(expense_id)
    expense.deleteFromDatabaseAndUpdateAccountBalance()
    return render_template('expenses.html', expenses=db.Expense.getAll())


@app.route('/incomes', methods=['GET', 'POST'])
def incomes() -> str:
    """
    Handles the incomes route.

    If the request method is 'POST', it adds a new income to the database
    using the income name, amount, date, and account ID provided in the form data.

    Returns the rendered 'incomes.html' template with the incomes data
    retrieved from the database. If an exception occurs, it returns the
    'incomes.html' template without any income data.

    Returns:
        str: The rendered 'incomes.html' template as a string.
    """
    if request.method == 'POST':
        income_name = request.form.get('name')
        income_amount = request.form.get('amount')
        income_date = request.form.get('date')
        income_account = request.form.get('account')
        db.add_income(income_name, income_amount, income_date, income_account)
    try:
        return render_template('incomes.html', incomes=db.get_all_incomes())
    except db.sqlite3.OperationalError:
        return render_template('incomes.html')


@app.route('/add_income')
def add_income() -> str:
    """
    Renders the 'add_income.html' template.

    Returns:
        str: The rendered template.
    """
    return render_template('add_income.html', accounts=db.Account.getAll())


@app.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
def edit_income(income_id: int) -> str:
    """
    Handles the edit income route.

    If the request method is 'GET', it renders the 'edit_income.html' template
    with the income data retrieved from the database.

    If the request method is 'POST', it updates the income in the database
    with the new name, amount, date, and account ID provided in the form data.

    Returns the rendered 'incomes.html' template with the updated incomes data
    retrieved from the database.

    Args:
        income_id (int): The ID of the income to be edited.

    Returns:
        str: The rendered 'incomes.html' template as a string.
    """
    if request.method == 'GET':
        return render_template('edit_income.html', income=db.get_income(income_id),
                               accounts=db.Account.getAll())
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    account_id = request.form.get('account')
    db.edit_income(name, amount, date, account_id, income_id)
    return render_template('incomes.html', incomes=db.get_all_incomes())


@app.route('/delete_income/<int:income_id>')
def delete_income(income_id: int) -> str:
    """
    Handles the delete income route.

    Deletes the income with the specified ID from the database.

    Returns the rendered 'incomes.html' template with the updated incomes data
    retrieved from the database.

    Args:
        income_id (int): The ID of the income to be deleted.

    Returns:
        str: The rendered 'incomes.html' template as a string.
    """
    db.delete_income(income_id)
    return render_template('incomes.html', incomes=db.get_all_incomes())


@app.route('/undo_income/<int:income_id>', methods=['GET', 'POST'])
def undo_income(income_id: int) -> str:
    """
    Undo an income by its ID. Update account balance to previous state.

    Parameters:
    - income_id (int): The ID of the income to be undone.

    Returns:
    - str: The rendered 'incomes.html' template.

    """
    db.undo_income(income_id)
    return render_template('incomes.html', incomes=db.get_all_incomes())


if __name__ == '__main__':
    app.run(debug=True)
