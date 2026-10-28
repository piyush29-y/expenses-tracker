#expenses.py
from storage import load_expenses, save_expenses

def add_expense(date, amount, category, note):
    expenses = load_expenses()

    next_id = max(
        (int(item["id"]) for item in expenses),
        default=0) + 1

    expense = {
        "id": next_id,
        "date": date,
        "amount": round(float(amount), 2),
        "category": category.strip(),
        "note": note.strip()
    }
    expenses.append(expense)
    save_expenses(expenses)
    return next_id

def get_expenses():
    expenses = load_expenses()
    return sorted(
        expenses,
        key=lambda item: (item["date"], int(item["id"])),
        reverse=True
    )
def get_expense(expense_id):
    for item in load_expenses():
        if int(item["id"]) == int(expense_id):
            return item
    return None

def update_expense(expense_id, date, amount, category, note):
    expenses = load_expenses()
    for item in expenses:
        if int(item["id"]) == int(expense_id):
            item["date"] = date
            item["amount"] = round(float(amount), 2)
            item["category"] = category.strip()
            item["note"] = note.strip()
            save_expenses(expenses)
            return True
    return False

def delete_expense(expense_id):
    expenses = load_expenses()
    updated_expenses = [
        item for item in expenses
        if int(item["id"]) != int(expense_id)
    ]
    if len(updated_expenses) == len(expenses):
        return False
    save_expenses(updated_expenses)
    return True