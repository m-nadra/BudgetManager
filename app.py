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
- '/expenses' : Handles the expenses route.
- '/add_expense' : Renders the 'add_expense.html' template.
- '/edit_expense/<int:expense_id>' : Handles the edit expense route.
- '/delete_expense/<int:expense_id>' : Handles the delete expense route.
- '/incomes' : Handles the incomes route.
- '/add_income' : Renders the 'add_income.html' template.
- '/edit_income/<int:income_id>' : Handles the edit income route.
- '/delete_income/<int:income_id>' : Handles the delete income route.
"""

from flask import Flask, render_template, request
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
        account_name = request.form.get('name')
        account_balance = request.form.get('balance')
        db.add_account(account_name, account_balance)
    try:
        return render_template('accounts.html', accounts=db.view_accounts())
    except db.sqlite3.OperationalError:
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
        return render_template('edit_account.html', account=db.get_account(account_id))
    name = request.form.get('name')
    balance = request.form.get('balance')
    db.edit_account(account_id, name, balance)
    return render_template('accounts.html', accounts=db.view_accounts())


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
    db.delete_account(account_id)
    return render_template('accounts.html', accounts=db.view_accounts())


@app.route('/expenses', methods=['GET', 'POST'])
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
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        date = request.form.get('date')
        account_id = request.form.get('account')
        db.add_expense(name, amount, date, account_id)
    try:
        return render_template('expenses.html', expenses=db.view_expenses())
    except db.sqlite3.OperationalError:
        return render_template('expenses.html')


@app.route('/add_expense')
def add_expense() -> str:
    """
    Renders the 'add_expense.html' template.

    Returns:
        str: The rendered template.
    """
    return render_template('add_expense.html', accounts=db.view_accounts())


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
        return render_template('edit_expense.html', expense=db.get_expense(expense_id),
                               accounts=db.view_accounts())
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    account_id = request.form.get('account')
    db.edit_expense(name, amount, date, account_id, expense_id)
    return render_template('expenses.html', expenses=db.view_expenses())


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
    db.delete_expense(expense_id)
    return render_template('expenses.html', expenses=db.view_expenses())


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
        return render_template('incomes.html', incomes=db.view_incomes())
    except db.sqlite3.OperationalError:
        return render_template('incomes.html')


@app.route('/add_income')
def add_income() -> str:
    """
    Renders the 'add_income.html' template.

    Returns:
        str: The rendered template.
    """
    return render_template('add_income.html', accounts=db.view_accounts())


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
                               accounts=db.view_accounts())
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    account_id = request.form.get('account')
    db.edit_income(name, amount, date, account_id, income_id)
    return render_template('incomes.html', incomes=db.view_incomes())


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
    return render_template('incomes.html', incomes=db.view_incomes())


if __name__ == '__main__':
    app.run(debug=True)
