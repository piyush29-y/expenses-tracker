from storage import load_budgets, save_budgets
def save_budget(month, amount):
    budgets = load_budgets()
    budgets[month] = round(float(amount), 2)
    save_budgets(budgets)

def get_monthly_budget(month):
    budgets = load_budgets()
    return float(budgets.get(month, 0))

class BudgetManager:
    def set_budget(self, month):
        while True:
            try:
                amount = float(input("Enter monthly budget: ₹"))

                if not 0 < amount < float("inf"):
                    print("Budget must be a finite amount greater than zero.")
                    continue

                save_budget(month, amount)
                print(f"Budget for {month} saved successfully!")
                break

            except ValueError:
                print("Enter a valid positive budget amount.")

    def get_budget(self, month):
        return get_monthly_budget(month)