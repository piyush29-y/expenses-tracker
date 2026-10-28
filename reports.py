#report.py
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path
from storage import load_expenses
from budgets import get_monthly_budget

BASE_DIR = Path(__file__).resolve().parent
CHART_FOLDER = BASE_DIR / "charts"

def get_month_expenses(month):
    return [
        item for item in load_expenses()
        if item["date"].startswith(month)]

def monthly_summary(month):
    expenses = get_month_expenses(month)
    count = len(expenses)
    total = sum(float(item["amount"]) for item in expenses)
    return count, total 

def category_analysis(month):
    expenses = get_month_expenses(month)
    totals = {}
    for item in expenses:
        category = item["category"]
        amount = float(item["amount"])
        totals[category] = totals.get(category, 0) + amount
    return sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True)

def spending_insights(month):
    count, total = monthly_summary(month)
    budget = get_monthly_budget(month)
    categories = category_analysis(month)
    print(f"\nSPENDING INSIGHTS - {month}")
    print(f"Total spending: ₹{total:.2f}")
    print(f"Number of expenses: {count}")

    if budget > 0:
        remaining = budget - total
        print(f"Monthly budget: ₹{budget:.2f}")
        print(f"Budget remaining: ₹{remaining:.2f}")

        if remaining < 0:
            print(f"Warning: You exceeded your budget by ₹{-remaining:.2f}!")
        elif remaining == 0:
            print("You have used your entire budget.")
        else:
            print(f"Budget used: {(total / budget) * 100:.1f}%")
    else:
        print("No budget set for this month.")

    if categories:
        highest_category, highest_amount = categories[0]
        print(f"Highest spending category: {highest_category} "
            f"(₹{highest_amount:.2f})")

        if len(categories) > 1:
            lowest_category, lowest_amount = categories[-1]
            print(
                f"Lowest spending category: {lowest_category} "
                f"(₹{lowest_amount:.2f})")

    if count == 0:
        print("No expenses recorded for this month.")

def generate_charts(month):
    categories = category_analysis(month)
    daily_totals = {}
    for item in get_month_expenses(month):
        expense_date = item["date"]
        daily_totals[expense_date] = (
            daily_totals.get(expense_date, 0)
            + float(item["amount"]))

    if not categories:
        print("No expenses available to create charts.")
        return

    CHART_FOLDER.mkdir(parents=True, exist_ok=True)

    names = [item[0] for item in categories]#pie chart
    amounts = [item[1] for item in categories]

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=names, autopct="%1.1f%%")
    plt.title(f"Category-wise Expenses - {month}")
    plt.tight_layout()
    plt.savefig(CHART_FOLDER / "category_pie.png")
    plt.close()

    plt.figure(figsize=(8, 6))#bar chart
    plt.bar(names, amounts)
    plt.title(f"Expenses by Category - {month}")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_FOLDER / "category_bar.png")
    plt.close()

    dates = sorted(daily_totals)#daily spend
    daily_amounts = [daily_totals[day] for day in dates]

    plt.figure(figsize=(9, 6))
    plt.plot(dates, daily_amounts, marker="o")
    plt.title(f"Daily Spending Trend - {month}")
    plt.xlabel("Date")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_FOLDER / "monthly_trend.png")
    plt.close()

    print(f"Charts saved successfully in: {CHART_FOLDER}")