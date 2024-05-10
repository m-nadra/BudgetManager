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


@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        expense_name = request.form.get('name')
        expense_amount = request.form.get('amount')
        expense_date = request.form.get('date')
        expense_account = request.form.get('account')
        db.add_expense(expense_name, expense_amount,
                       expense_date, expense_account)
    return render_template('expenses.html', expenses=db.view_expenses())


@app.route('/incomes', methods=['GET', 'POST'])
def incomes():
    if request.method == 'POST':
        income_name = request.form.get('name')
        income_amount = request.form.get('amount')
        income_date = request.form.get('date')
        income_account = request.form.get('account')
        print(income_name, income_amount, income_date, income_account)
        db.add_income(income_name, income_amount, income_date, income_account)
    return render_template('incomes.html', incomes=db.view_incomes())


@app.route('/add_account')
def add_account():
    return render_template('add_account.html')


@app.route('/add_income')
def add_income():
    return render_template('add_income.html', accounts=db.view_accounts())


@app.route('/add_expense')
def add_expense():
    return render_template('add_expense.html', accounts=db.view_accounts())


if __name__ == '__main__':
    app.run(debug=True)
