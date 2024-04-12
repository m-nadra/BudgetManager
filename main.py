import pyinputplus as pyip
import database as db

print("""Budget Manager app.
Enter 1 to see your budget.
Enter 2 to add account.
Enter 0 to exit app.""")

while True:
    match pyip.inputNum("Enter number: "):
        case 1:
            db.execute("view_budget")
        case 2:
            db.execute("add_account")
        case 0:
            break
        case _:
            print("Invalid input. Try again.")
