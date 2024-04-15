"Menu to interact with user using command line interface."
import datetime
import os
import pyinputplus as pyip
import database as db


while True:
    print("""\nBudget Manager app.
    Enter 1 to see your budget.
    Enter 2 to add account.
    Enter 3 to add expense.
    Enter 4 to see expenses.
    Enter 0 to exit app.""")
    match pyip.inputNum("Enter number: "):
        case 1:
            os.system("cls")
            print("Displaying budget")
            db.view_accounts()
        case 2:
            os.system("cls")
            print("Adding new account")

            name = pyip.inputStr("Enter account name: ")
            amount = pyip.inputFloat("Enter account amount: ", min=0)
            db.add_account(name, amount)
        case 3:
            os.system("cls")
            print("Adding expense")

            name = pyip.inputStr("Enter expense name: ")
            amount = pyip.inputFloat("Enter expense amount: ", min=0)
            if date := input("Enter expense date (dd-mm-yyyy): (blank for today) ") == "":
                date = datetime.datetime.now().strftime("%d-%m-%Y")

            db.view_accounts()
            account_id = pyip.inputInt("Enter account id: ")
            db.add_expense(name, amount, date, account_id)
        case 4:
            os.system("cls")
            print("Dispalaying expenses")
            db.view_expenses()
        case 0:
            break
        case _:
            print("Invalid input. Try again.")
