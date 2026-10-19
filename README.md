# Personal Expense Tracker
A beginner-friendly Python command-line application for managing
personal expenses and monthly budgets.

## Features
- Add, view, edit, and delete expenses
- Store expenses and budgets in SQLite
- Set and update monthly budgets
- Check spending and remaining budget
- Daily, weekly, and monthly summaries
- Category-wise totals and percentages
- Rule-based spending insights
- Monthly dashboard
- Generate pie, bar, and spending trend charts

## Excluded Features
- Monthly income
- Search and filter
- Graphical user interface
- Web dashboard

## Requirements
- Python 3.10 or later
- Matplotlib

## Setup
Open a terminal in the project folder.
Create a virtual environment:
    python -m venv .venv
Activate it on Windows Command Prompt:
    .venv\Scripts\activate.ps1

Install dependencies:
    python -m pip install -r requirements.txt

## Run the Application
    python run_tracker.py

## Database
The database is stored at:
    data/expenses.db

## Charts
Generated images are stored in:
    charts/
The chart files are generated for the month selected by the user.
