#storage.Py
import json
from pathlib import Path
# Find the folder 
BASE_DIR = Path(__file__).resolve().parent
DATA_FOLDER = BASE_DIR / "data" 
EXPENSES_FILE = DATA_FOLDER / "expenses.json"
BUDGETS_FILE = DATA_FOLDER / "budgets.json"

def read_json(file_path, default_value):
    if not file_path.exists():
        return default_value
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return default_value if data is None else data

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {file_path}. "
            "Please back up and repair the file."
        ) from error

def write_json(file_path, data):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_expenses():
    data = read_json(EXPENSES_FILE, [])

    if not isinstance(data, list):
        raise ValueError(
            "expenses.json must contain a JSON list."
        )
    return data

def save_expenses(expenses):
    write_json(EXPENSES_FILE, expenses)

def load_budgets():
    data = read_json(BUDGETS_FILE, {})

    if not isinstance(data, dict):
        raise ValueError("budgets.json must contain a JSON object.")
    return data

def save_budgets(budgets):
    write_json(BUDGETS_FILE, budgets)

def initialize_storage():
    """Create missing data files without replacing existing ones."""
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    if not EXPENSES_FILE.exists():
        save_expenses([])

    if not BUDGETS_FILE.exists():
        save_budgets({})