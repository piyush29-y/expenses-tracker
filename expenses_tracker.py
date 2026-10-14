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