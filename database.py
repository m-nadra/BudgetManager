import sqlite3


def execute(user_input):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS budget (
                   id INTEGER PRIMARY KEY, 
                   name TEXT, 
                   amount REAL)""")

    match user_input:
        case "add_account":
            data = (input("Enter name: "), float(input("Enter amount: ")))
            cursor.execute("INSERT INTO budget (name, amount) VALUES (?, ?);", data)
        case "view_budget":
            cursor.execute("SELECT name, amount FROM budget;")
            for row in cursor.fetchall():
                print(f"Account name: {row[0]}, amount: {row[1]}") 
        case _:
            pass

    connection.commit()
    cursor.close()
    connection.close()
