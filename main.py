import pyinputplus as pyip
import database as db

print("""Budget Manager app.
Enter 1 to see your budget.
Enter 2 to add account.
Enter 3 to add expense.
Enter 0 to exit app.""")

while True:
    match pyip.inputNum("Enter number: "):
        case 1:
            db.view_accounts()
        case 2:
            account_name = pyip.inputStr("Enter account name: ")
            account_amount = pyip.inputFloat("Enter account amount: ", min=0)
            db.add_account(account_name, account_amount)
        case 3:
            expense_name = pyip.inputStr("Enter expense name: ")
            expense_amount = pyip.inputFloat("Enter expense amount: ", min=0)
            db.view_accounts()
            account_id = pyip.inputInt("Enter account id: ")
            db.add_expense(expense_name, expense_amount, account_id)
        case 0:
            break
        case _:
            print("Invalid input. Try again.")
