"Menu to interact with user using command line interface."
import datetime
import os
import pyinputplus as pyip
import database as db

os.system("cls")
while True:
    print("""\nBudget Manager app.
    Enter 1 to see your budget.
    Enter 2 to add account.
    Enter 3 to add expense.
    Enter 4 to see expenses.
    Enter 5 to add income.
    Enter 6 to see incomes.
    Enter 7 to transfer money between accounts.
    Enter 0 to exit app.""")
    match pyip.inputNum("Enter number: "):
        case 1:
            os.system("cls")
            print("Displaying budget")
            db.view_accounts()
            input("\nPress any key to back to the menu. ")
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
            date = input("Enter income date (dd-mm-yyyy): (blank for today) ")
            if date == "":
                date = datetime.datetime.now().strftime("%d-%m-%Y")

            db.view_accounts()
            account_id = pyip.inputInt("Enter account id: ")
            db.add_expense(name, amount, date, account_id)
        case 4:
            os.system("cls")
            print("Dispalaying expenses")
            db.view_expenses()
            input("\nPress any key to back to the menu. ")
        case 5:
            os.system("cls")
            print("Adding income")

            name = pyip.inputStr("Enter income name: ")
            amount = pyip.inputFloat("Enter income amount: ", min=0)
            date = input("Enter income date (dd-mm-yyyy): (blank for today) ")
            if date == "":
                date = datetime.datetime.now().strftime("%d-%m-%Y")

            db.view_accounts()
            account_id = pyip.inputInt("Enter account id: ")
            db.add_income(name, amount, date, account_id)
        case 6:
            os.system("cls")
            print("Displaying incomes")
            db.view_incomes()
            input("\nPress any key to back to the menu. ")
        case 7:
            os.system("cls")
            print("Transfering money between accounts")

            db.view_accounts()
            from_account_id = pyip.inputInt("Enter from account id: ")
            db.view_accounts()
            to_account_id = pyip.inputInt("Enter to account id: ")
            amount = pyip.inputFloat("Enter amount to transfer: ", min=0)
            db.transfer(from_account_id, to_account_id, amount)
        case 0:
            break
        case _:
            print("Invalid input. Try again.")
