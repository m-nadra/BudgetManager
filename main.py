import pyinputplus as pyip

print("""Budget Manager app.
Enter 1 to ...
Enter 2 to exit app.""")

while True:
    match pyip.inputNum("Enter number: "):
        case 1:
            pass
        case 2:
            break
        case _:
            print("Invalid input. Try again.")
