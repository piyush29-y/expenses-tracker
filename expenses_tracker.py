import sqlite3 
from datetime import datetime

db = sqlite3.connect("expenses.db")
exp_cur = db.cursor()

exp_cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT, amount REAL, category TEXT, note TEXT)""")
exp_cur.execute("""CREATE TABLE IF NOT EXISTS budgets(
    month TEXT PRIMARY KEY, amount REAL)""")
db.commit()

#for add expense operation

class ExpenseTracker:
    def add_expense(self):
     while True:
        try:
            date = input("Date (YYYY-MM-DD, blank=today): ")
            date = date or datetime.today().strftime("%Y-%m-%d")
            datetime.strptime(date, "%Y-%m-%d")

            amount = float(input("Amount: "))
            category = input("Category: ").strip().title()
            note = input("Description: ")

            if amount <= 0 or not category:
                print("Invalid amount or category!")
                continue

            exp_cur.execute(
                "INSERT INTO expenses(date,amount,category,note) VALUES(?,?,?,?)",
                (date, amount, category, note)
            )
            db.commit()
            print("Expense added successfully!")

            again = input("Do you want to add another expense? (yes/no): ").lower().strip()

            if again != "yes":
                break

        except ValueError:
            print("Enter a valid date and amount. Please try again.")