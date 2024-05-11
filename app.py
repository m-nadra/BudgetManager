from flask import Flask, render_template, request
import database as db

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        account_name = request.form.get('name')
        account_balance = request.form.get('balance')
        db.add_account(account_name, account_balance)
    return render_template('accounts.html', accounts=db.view_accounts())


@app.route('/add_account')
def add_account():
    return render_template('add_account.html')


@app.route('/incomes', methods=['GET', 'POST'])
def incomes():
    if request.method == 'POST':
        income_name = request.form.get('name')
        income_amount = request.form.get('amount')
        income_date = request.form.get('date')
        income_account = request.form.get('account')
        db.add_income(income_name, income_amount, income_date, income_account)
    return render_template('incomes.html', incomes=db.view_incomes())


@app.route('/add_income')
def add_income():
    return render_template('add_income.html', accounts=db.view_accounts())


@app.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
def edit_income(income_id):
    if request.method == 'GET':
        return render_template('edit_income.html', income=db.get_income(income_id), accounts=db.view_accounts())
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    account_id = request.form.get('account')
    db.edit_income(name, amount, date, account_id, income_id)
    return render_template('incomes.html', incomes=db.view_incomes())


@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')
        date = request.form.get('date')
        account_id = request.form.get('account')
        db.add_expense(name, amount, date, account_id)
    return render_template('expenses.html', expenses=db.view_expenses())


@app.route('/add_expense')
def add_expense():
    return render_template('add_expense.html', accounts=db.view_accounts())


@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if request.method == 'GET':
        return render_template('edit_expense.html', expense=db.get_expense(expense_id), accounts=db.view_accounts())
    name = request.form.get('name')
    amount = request.form.get('amount')
    date = request.form.get('date')
    account_id = request.form.get('account')
    db.edit_expense(name, amount, date, account_id, expense_id)
    return render_template('expenses.html', expenses=db.view_expenses())


@app.route('/delete_income/<int:income_id>', methods=['GET', 'POST'])
def delete_income(income_id):
    db.delete_income(income_id)
    return render_template('incomes.html', incomes=db.view_incomes())


@app.route('/delete_expense/<int:expense_id>', methods=['GET', 'POST'])
def delete_expense(expense_id):
    db.delete_expense(expense_id)
    return render_template('expenses.html', expenses=db.view_expenses())


if __name__ == '__main__':
    app.run(debug=True)
