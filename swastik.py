import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

DB_NAME = "sfm_peis.db"

# -------------------- DATABASE SETUP --------------------
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    monthly_income REAL,
    savings_goal REAL
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    budget REAL
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS income(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    source TEXT,
    date TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    note TEXT,
    date TEXT
)""")

conn.commit()

# -------------------- USER MODULE --------------------
def create_user():
    name = input("Enter your name: ")
    income = float(input("Enter your monthly income: "))
    goal = float(input("Enter your monthly savings goal: "))
    cur.execute(
        "INSERT INTO users(name, monthly_income, savings_goal) VALUES(?,?,?)",
        (name, income, goal)
    )
    conn.commit()
    print("User profile created!\n")

# -------------------- CATEGORY MODULE --------------------
def add_category():
    name = input("Category name: ")
    budget = float(input("Monthly budget for this category: "))
    try:
        cur.execute(
            "INSERT INTO categories(name, budget) VALUES(?,?)",
            (name, budget)
        )
        conn.commit()
        print("Category added.\n")
    except:
        print("Category already exists.\n")

# -------------------- INCOME MODULE --------------------
def add_income():
    amount = float(input("Income amount: "))
    source = input("Source (Salary/Freelance/etc): ")
    date = datetime.now().strftime("%Y-%m-%d")

    cur.execute(
        "INSERT INTO income(amount, source, date) VALUES(?,?,?)",
        (amount, source, date)
    )
    conn.commit()
    print("Income recorded.\n")

# -------------------- EXPENSE MODULE --------------------
def add_expense():
    amount = float(input("Expense amount: "))
    category = input("Category: ")
    note = input("Note: ")
    date = datetime.now().strftime("%Y-%m-%d")

    cur.execute(
        "INSERT INTO expenses(amount, category, note, date) VALUES(?,?,?,?)",
        (amount, category, note, date)
    )
    conn.commit()
    print("Expense added.\n")

# -------------------- BUDGET MODULE --------------------
def check_budget():
    cur.execute("SELECT name, budget FROM categories")
    categories = cur.fetchall()

    print("\n--- Budget Status ---")
    for name, budget in categories:
        cur.execute(
            "SELECT SUM(amount) FROM expenses WHERE category=?",
            (name,)
        )
        spent = cur.fetchone()[0] or 0

        print(f"{name}: Spent {spent} / Budget {budget}")
        if spent > budget:
            print("⚠ Budget exceeded!")
    print()

# -------------------- ANALYTICS MODULE --------------------
def analytics():
    cur.execute("SELECT SUM(amount) FROM income")
    total_income = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cur.fetchone()[0] or 0

    print("\n--- Financial Summary ---")
    print(f"Total Income  : {total_income}")
    print(f"Total Expense : {total_expense}")
    print(f"Savings       : {total_income - total_expense}")

    cur.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC LIMIT 1
    """)

    top = cur.fetchone()
    if top:
        print(f"Highest Spending Category: {top[0]} ({top[1]})")
    print()

# -------------------- PIE CHART MODULE --------------------
def show_expense_piechart():
    print("\nGenerating Expense Pie Chart...")

    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    data = cur.fetchall()

    if not data:
        print("No expense data available.\n")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(7,7))
    plt.pie(amounts, labels=categories,
            autopct='%1.1f%%', startangle=90)

    plt.title("Expense Distribution by Category")
    plt.axis('equal')
    plt.show()

# -------------------- BAR GRAPH MODULE --------------------
def show_expense_bargraph():
    print("\nGenerating Expense Bar Graph...")

    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    data = cur.fetchall()

    if not data:
        print("No expense data available.\n")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(8,6))
    plt.bar(categories, amounts)

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# -------------------- MAIN MENU --------------------
def menu():
    while True:
        print("====== SFM-PEIS MENU ======")
        print("1. Create User Profile")
        print("2. Add Category")
        print("3. Add Income")
        print("4. Add Expense")
        print("5. Check Budget Status")
        print("6. View Financial Analytics")
        print("7. Show Expense Pie Chart")
        print("8. Show Expense Bar Graph")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            add_category()
        elif choice == "3":
            add_income()
        elif choice == "4":
            add_expense()
        elif choice == "5":
            check_budget()
        elif choice == "6":
            analytics()
        elif choice == "7":
            show_expense_piechart()
        elif choice == "8":
            show_expense_bargraph()
        elif choice == "9":
            print("Exiting... Stay financially smart!")
            break
        else:
            print("Invalid choice\n")

menu()
conn.close()
