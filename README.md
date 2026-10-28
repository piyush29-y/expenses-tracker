# Personal Expense Tracker

A beginner-friendly command-line expense tracking application
built using Python, JSON file handling, and Matplotlib.

## Features

- Add, view, edit, and delete expenses
- Store expenses permanently in JSON files
- Set and update monthly budgets
- Calculate monthly spending and remaining budget
- Analyze category-wise expenses
- Display spending insights
- Generate pie, bar, and daily trend charts

## Requirements

- Python 3.10 or later
- Matplotlib

## Installation

Install the dependency:

    python -m pip install -r requirements.txt

## Run the application

From the project folder, run:

    python run_tracker.py

## Data storage

Expenses are saved in:

    data/expenses.json

Monthly budgets are saved in:

    data/budgets.json

Charts are saved in:

    charts/

The application creates the data folder and JSON files
automatically when it starts.

## Important

Keep backups of your JSON files. Do not manually delete
them if you want to preserve your expense history.