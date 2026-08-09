import datetime
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# Dollar
def get_dollar_balance(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN type = 'deposit' THEN amount WHEN type = 'withdraw' THEN -amount END) FROM dollars WHERE user_id = %s",
        (user_id,),
    )
    operation = cursor.fetchone()
    connection.close()
    return operation[0]


def deposit_dollar(user_id, deposit):
    date = datetime.date.today()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO dollars (user_id, date, type, amount)" "VALUES (%s, %s, %s, %s)",
        (user_id, date, "deposit", deposit),
    )
    connection.commit()
    connection.close()


def withdraw_dollar(user_id, withdraw):
    date = datetime.date.today()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO dollars (user_id, date, type, amount)" "VALUES (%s, %s, %s, %s)",
        (user_id, date, "withdraw", withdraw),
    )
    connection.commit()
    connection.close()


# GRN CASH
def get_grn_cash_balance(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN type = 'deposit' THEN amount WHEN type = 'withdraw' THEN -amount END) FROM grn_cash WHERE user_id = %s",
        (user_id,),
    )
    operation = cursor.fetchone()
    connection.close()
    return operation[0]


def deposit_grn_cash(user_id, deposit):
    date = datetime.date.today()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_cash (user_id, date, type, amount)" "VALUES (%s, %s, %s, %s)",
        (user_id, date, "deposit", deposit),
    )
    connection.commit()
    connection.close()


def withdraw_grn_cash(user_id, withdraw):
    date = datetime.date.today()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_cash (user_id, date, type, amount)" "VALUES (%s, %s, %s, %s)",
        (user_id, date, "withdraw", withdraw),
    )
    connection.commit()
    connection.close()


# GRN CARD
def get_grn_card_balance(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN type = 'deposit' THEN amount WHEN type = 'withdraw' THEN -amount END) FROM grn_card WHERE user_id = %s",
        (user_id,),
    )
    operation = cursor.fetchone()
    connection.close()
    return operation[0]


def deposit_grn_card(user_id, deposit):
    date = datetime.date.today()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_card (user_id, date, type, amount)" "VALUES (%s, %s, %s, %s)",
        (user_id, date, "deposit", deposit),
    )
    connection.commit()
    connection.close()


def withdraw_grn_card(user_id, withdraw):
    date = datetime.date.today()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO grn_card (user_id, date, type, amount)" "VALUES (%s, %s, %s, %s)",
        (user_id, date, "withdraw", withdraw),
    )
    connection.commit()
    connection.close()


# --------------------------------------------


def add_expense(user_id, amount, payment_method, category):
    date = datetime.date.today()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, date, category, amount, payment_method) "
        "VALUES (%s, %s, %s, %s, %s)",
        (user_id, date, category, amount, payment_method),
    )
    connection.commit()
    connection.close()


# -------------------------------------------------


def daily_report_expenses(user_id, date):

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = %s AND date = %s GROUP BY category",
        (user_id, date),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses


def weekly_report_expenses(user_id, start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = %s AND date BETWEEN %s AND %s GROUP BY category",
        (user_id, start_date, end_date),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses


def monthly_report_expenses(user_id, start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = %s AND date BETWEEN %s AND %s GROUP BY category",
        (user_id, start_date, end_date),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses


def yearly_report_expenses(user_id, start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = %s AND date BETWEEN %s AND %s GROUP BY category",
        (user_id, start_date, end_date),
    )
    expenses = cursor.fetchall()
    connection.close()
    return expenses


def add_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (user_id) VALUES (%s) " "ON CONFLICT (user_id) DO NOTHING",
        (user_id,),
    )
    connection.commit()
    connection.close()


def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    connection.close()
    return users
