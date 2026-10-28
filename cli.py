#cli.Py
from datetime import date, datetime
from storage import initialize_storage
from budgets import BudgetManager, get_monthly_budget
from expenses import(add_expense,get_expenses,get_expense,update_expense,delete_expense)
from reports import(monthly_summary,category_analysis,spending_insights,generate_charts)

class ExpenseTracker(BudgetManager):
    def add_expense_menu(self):
        while True:
            try:
                amount = float(input("Enter amount: ₹"))

                if not 0 < amount < float("inf"):
                    print("Amount must be finite and greater than zero.")
                    continue

                category = input("Enter category: ").strip()

                if not category:
                    print("Category cannot be empty.")
                    continue

                expense_date = input(f"Enter date (YYYY-MM-DD) [{date.today()}]: ").strip() or str(date.today())

                datetime.strptime(expense_date, "%Y-%m-%d")

                note = input("Enter description: ").strip()

                expense_id = add_expense(expense_date, amount, category, note)

                print(f"Expense added successfully! ID: {expense_id}")

            except ValueError:
                print("Enter a valid amount or date.")
                continue

            if input("Add another expense? (y/n): ").strip().lower() != "y":
                break

    def view_expenses(self):
        expenses = get_expenses()

        if not expenses:
            print("No expenses found.")
            return

        print("\nID | Date | Amount | Category | Description")
        print("-" * 65)

        for item in expenses:
            print(
                f"{item['id']} | {item['date']} | "
                f"₹{item['amount']:.2f} | "
                f"{item['category']} | {item['note']}")

    def edit_expense(self):
        try:
            expense_id = int(input("Enter expense ID to edit: "))
            old = get_expense(expense_id)

            if not old:
                print("Expense not found.")
                return

            print("Press Enter to keep an existing value.")
            print("For description, enter - to clear it.")

            amount_text = input(f"Amount [{old['amount']}]: ").strip()
            category_text = input(f"Category [{old['category']}]: ").strip()
            date_text = input(f"Date [{old['date']}]: ").strip()
            note_text = input(f"Description [{old['note']}]: ").strip()
            amount = (float(amount_text) if amount_text else old["amount"])
            category = category_text or old["category"]
            expense_date = date_text or old["date"]

            if note_text == "-":
                note = ""
            elif note_text:
                note = note_text
            else:
                note = old["note"]

            if not 0 < amount < float("inf"):
                print("Amount must be finite and greater than zero.")
                return
            if not category:
                print("Category cannot be empty.")
                return

            datetime.strptime(expense_date, "%Y-%m-%d")
            success = update_expense(expense_id,expense_date,amount,category,note)

            if success:
                print("Expense updated successfully!")
            else:
                print("Expense not found.")

        except ValueError:
            print("Invalid ID, amount, or date.")

    def delete_expense_menu(self):
        try:
            expense_id = int(input("Enter expense ID to delete: "))
            old = get_expense(expense_id)
            if not old:
                print("Expense not found.")
                return
            print(
                f"Expense: {old['date']} | "
                f"₹{old['amount']:.2f} | {old['category']}"
            )
            confirm = input("Are you sure you want to delete it? (y/n): ").strip().lower()
            if confirm != "y":
                print("Deletion cancelled.")
                return
            if delete_expense(expense_id):
                print("Expense deleted successfully!")
            else:
                print("Expense not found.")
        except ValueError:
            print("Enter a valid numeric ID.")

    def check_budget(self, month):
        budget = self.get_budget(month)
        _, total = monthly_summary(month)
        remaining = budget - total

        print(f"\nBUDGET STATUS - {month}")
        print(f"Monthly budget: ₹{budget:.2f}")
        print(f"Total expenses: ₹{total:.2f}")

        if budget <= 0:
            print("No budget set for this month.")
            return

        print(f"Budget remaining: ₹{remaining:.2f}")

        if remaining < 0:
            print(f"Warning: Budget exceeded by ₹{-remaining:.2f}!")
        elif remaining == 0:
            print("You have used your entire budget.")
        else:
            print(f"Budget used: {(total / budget) * 100:.1f}%")

    def show_monthly_summary(self, month):
        count, total = monthly_summary(month)
        budget = self.get_budget(month)

        print(f"\nMONTHLY SUMMARY - {month}")
        print(f"Number of expenses: {count}")
        print(f"Total spending: ₹{total:.2f}")

        if budget > 0:
            print(f"Monthly budget: ₹{budget:.2f}")
            print(f"Budget remaining: ₹{budget - total:.2f}")
        else:
            print("No budget set for this month.")

    def show_category_analysis(self, month):
        categories = category_analysis(month)

        if not categories:
            print("No expenses found for this month.")
            return

        total = sum(amount for _, amount in categories)

        print(f"\nCATEGORY-WISE ANALYSIS - {month}")

        for category, amount in categories:
            percentage = (amount / total * 100) if total else 0

            print(f"{category}: ₹{amount:.2f} "
                f"({percentage:.1f}%)")

    def dashboard(self):
        default_month = date.today().strftime("%Y-%m")
        month = input(f"Enter month (YYYY-MM) [{default_month}]: ").strip() or default_month

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month. Use YYYY-MM, for example 2026-10.")
            return

        while True:
            print(f"\nDASHBOARD - {month}")
            print("a. Check Budget Status")
            print("b. Monthly Summary")
            print("c. Category-wise Analysis")
            print("d. Spending Insights")
            print("e. Generate Charts")
            print("f. Change Month")
            print("g. Back to Main Menu")

            choice = input("Choose an option: ").strip().lower()
            if choice == "a":
                self.check_budget(month)
            elif choice == "b":
                self.show_monthly_summary(month)
            elif choice == "c":
                self.show_category_analysis(month)
            elif choice == "d":
                spending_insights(month)
            elif choice == "e":
                generate_charts(month)
            elif choice == "f":
                new_month = input("Enter month (YYYY-MM): ").strip()
                try:
                    datetime.strptime(new_month, "%Y-%m")
                    month = new_month
                except ValueError:
                    print("Invalid month format.")
            elif choice == "g":
                break
            else:
                print("Invalid choice.")

    def run(self):
        month = date.today().strftime("%Y-%m")

        print("\n")
        print("      PERSONAL EXPENSE TRACKER")
        print("=" * 35)

        budget = self.get_budget(month)
        if budget > 0:
            print(f"Current monthly budget: ₹{budget:.2f}")

            if input("Update budget? (y/n): ").strip().lower() == "y":
                self.set_budget(month)
        else:
            print(f"No budget set for {month}.")
            self.set_budget(month)

        while True:
            print("\n-----------MAIN MENU-----------")
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. Edit Expense")
            print("4. Delete Expense")
            print("5. Dashboard")
            print("6. Set or Update Monthly Budget")
            print("7. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.add_expense_menu()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.edit_expense()
            elif choice == "4":
                self.delete_expense_menu()
            elif choice == "5":
                self.dashboard()
            elif choice == "6":
                budget_month = input(
                    "Enter budget month (YYYY-MM) "
                    f"[{date.today().strftime('%Y-%m')}]: "
                ).strip() or date.today().strftime("%Y-%m")

                try:
                    datetime.strptime(budget_month, "%Y-%m")
                    self.set_budget(budget_month)
                except ValueError:
                    print("Invalid month. Use YYYY-MM.")
            elif choice == "7":
                print("Thank you for using Expense Tracker!")
                break
            else:
                print("Invalid choice. Please choose 1 to 7.")

def run_cli():
    initialize_storage()
    ExpenseTracker().run()

if __name__ == "__main__":
    run_cli()