from flask import Flask, render_template
import database as db

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/accounts')
def accounts():
    return render_template('accounts.html', accounts=db.view_accounts())


@app.route('/expenses')
def expenses():
    return render_template('expenses.html', expenses=db.view_expenses())


@app.route('/incomes')
def incomes():
    return render_template('incomes.html', incomes=db.view_incomes())


if __name__ == '__main__':
    app.run(debug=True)
