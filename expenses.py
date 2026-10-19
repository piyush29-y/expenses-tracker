from datetime import date
from decimal import Decimal,InvalidOperation
from expenses_tracker.storage import execute,fetch_all,fetch_one
def validate_amount(amount):
    try:
        amount = Decimal(amount)
    except InvalidOperation:
        raise ValueError("Amount must be a valid decimal number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return amount
def validate_date(expense_date):
    try:
        parsed_date = date.fromisoformat(str(expense_date)).strip()
    except  (ValueError, TypeError):
        raise ValueError("Date must be in YYYY-MM-DD Format.")
    if not isinstance(expense_date, date):
        raise ValueError("Date must be a valid date object.")
    if expense_date > date.today():
        raise ValueError("Date cannot be in the future.")
    return expense_date
def validate_category(category):
    if not isinstance(category,str) or not category.strip():
        raise ValueError("Category must be a non-empty string.")
    return category.strip()
def get_all_expenses():
    return fetch_all()
def get_expense(expense_id):
    pass
def update_expense(expense_id,amount,category,expense_date,description):
    existing =get_expense(expense_id)
    if not existing:
        raise ValueError("Expense with the given ID does not match")
    amount = validate_amount(amount)
    category = validate_category(category)
    expense_date = validate_date(expense_date)
    result = execute((str(amount),category,str(expense_date),description,int(expense_id)))
    return  result.rowcount > 0
def delete_expense(expense_id):
    existing = get_expense(expense_id)
    if not existing:
        raise ValueError("Expense with the given ID does not match")
    result =execute((
        "Delete from expenses where id =?",int(expense_id),),)
    return result.rowcount >0