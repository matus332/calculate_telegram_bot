import datetime
import sqlite3

# Dollar
def get_dollar_balance(user_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN type = 'deposit' THEN amount WHEN type = 'withdraw' THEN -amount END) FROM dollars WHERE user_id = ?",
        (user_id,),
    )
    operation = cursor.fetchone()
    connection.close()
    return operation[0]


def deposit_dollar(user_id, deposit):
    date = datetime.date.today()
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO dollars (user_id, date, type, amount)" "VALUES (?, ?, ?, ?)",
        (user_id, date.isoformat(), "deposit", deposit),
    )
    connection.commit()
    connection.close()


def withdraw_dollar(user_id, withdraw):
    date = datetime.date.today()
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO dollars (user_id, date, type, amount)" "VALUES (?, ?, ?, ?)",
        (user_id, date.isoformat(), "withdraw", withdraw),
    )
    connection.commit()
    connection.close()


# GRN CASH
def get_grn_cash_balance(user_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN type = 'deposit' THEN amount WHEN type = 'withdraw' THEN -amount END) FROM grn_cash WHERE user_id = ?",
        (user_id,),
    )
    operation = cursor.fetchone()
    connection.close()
    return operation[0]


def deposit_grn_cash(user_id, deposit):
    date = datetime.date.today()
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_cash (user_id, date, type, amount)" "VALUES (?, ?, ?, ?)",
        (user_id, date.isoformat(), "deposit", deposit),
    )
    connection.commit()
    connection.close()


def withdraw_grn_cash(user_id, withdraw):
    date = datetime.date.today()
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_cash (user_id, date, type, amount)" "VALUES (?, ?, ?, ?)",
        (user_id, date.isoformat(), "withdraw", withdraw),
    )
    connection.commit()
    connection.close()


# GRN CARD
def get_grn_card_balance(user_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN type = 'deposit' THEN amount WHEN type = 'withdraw' THEN -amount END) FROM grn_card WHERE user_id = ?",
        (user_id,),
    )
    operation = cursor.fetchone()
    connection.close()
    return operation[0]


def deposit_grn_card(user_id, deposit):
    date = datetime.date.today()
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_card (user_id, date, type, amount)" "VALUES (?, ?, ?, ?)",
        (user_id, date.isoformat(), "deposit", deposit),
    )
    connection.commit()
    connection.close()


def withdraw_grn_card(user_id, withdraw):
    date = datetime.date.today()
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_card (user_id, date, type, amount)" "VALUES (?, ?, ?, ?)",
        (user_id, date.isoformat(), "withdraw", withdraw),
    )
    connection.commit()
    connection.close()


# --------------------------------------------


def add_expense(user_id, amount, payment_method, category):
    date = datetime.date.today()
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, date, category, amount, payment_method) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, date.isoformat(), category, amount, payment_method),
    )
    connection.commit()
    connection.close()


#-------------------------------------------------

def daily_report_expenses(user_id, date):

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND date = ? GROUP BY category",
        (user_id, date.isoformat()),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses

def weekly_report_expenses(user_id, start_date, end_date):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ? GROUP BY category",
        (user_id, start_date.isoformat(), end_date.isoformat()),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses

def monthly_report_expenses(user_id, start_date, end_date):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ? GROUP BY category",
        (user_id, start_date.isoformat(), end_date.isoformat()),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses

def yearly_report_expenses(user_id, start_date, end_date):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ? GROUP BY category",
        (user_id, start_date.isoformat(), end_date.isoformat()),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses

def add_user(user_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,),
    )
    connection.commit()
    connection.close()

def get_all_users():
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    connection.close()
    return users