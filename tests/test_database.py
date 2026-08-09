import datetime
import sqlite3

import pytest

import database


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_finance.db"

    real_connect = sqlite3.connect

    connection = real_connect(db_path)
    cursor = connection.cursor()

    cursor.executescript(
        """
        CREATE TABLE dollars (
            user_id INTEGER,
            date TEXT,
            type TEXT,
            amount INTEGER
        );

        CREATE TABLE grn_cash (
            user_id INTEGER,
            date TEXT,
            type TEXT,
            amount INTEGER
        );

        CREATE TABLE grn_card (
            user_id INTEGER,
            date TEXT,
            type TEXT,
            amount INTEGER
        );

        CREATE TABLE expenses (
            user_id INTEGER,
            date TEXT,
            category TEXT,
            amount INTEGER,
            payment_method TEXT
        );

        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY
        );
        """
    )

    connection.commit()
    connection.close()

    monkeypatch.setattr(
        database.sqlite3,
        "connect",
        lambda _: real_connect(db_path),
    )

    return db_path

def test_dollar_deposit_and_withdraw(test_db):
    user_id = 1

    database.deposit_dollar(user_id, 1000)

    assert database.get_dollar_balance(user_id) == 1000

    database.withdraw_dollar(user_id, 300)

    assert database.get_dollar_balance(user_id) == 700

def test_grn_cash_balance(test_db):
    user_id = 1

    database.deposit_grn_cash(user_id, 2000)
    database.withdraw_grn_cash(user_id, 500)

    assert database.get_grn_cash_balance(user_id) == 1500

def test_grn_card_balance(test_db):
    user_id = 1

    database.deposit_grn_card(user_id, 3000)
    database.withdraw_grn_card(user_id, 1200)

    assert database.get_grn_card_balance(user_id) == 1800

def test_balances_are_separated_by_user(test_db):
    database.deposit_grn_card(1, 1000)
    database.deposit_grn_card(2, 5000)

    assert database.get_grn_card_balance(1) == 1000
    assert database.get_grn_card_balance(2) == 5000

def test_add_expense(test_db):
    database.add_expense(
        user_id=1,
        amount=350,
        payment_method="card",
        category="products",
    )

    connection = database.sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id, category, amount, payment_method
        FROM expenses
        """
    )

    expense = cursor.fetchone()
    connection.close()

    assert expense == (1, "products", 350, "card")

def test_daily_report_groups_categories(test_db):
    user_id = 1
    date = datetime.date(2026, 8, 9)

    connection = database.sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (user_id, date.isoformat(), "products", 100, "card"),
            (user_id, date.isoformat(), "products", 250, "cash"),
            (user_id, date.isoformat(), "coffee", 80, "card"),
        ],
    )

    connection.commit()
    connection.close()

    report = database.daily_report_expenses(user_id, date)

    assert dict(report) == {
        "products": 350,
        "coffee": 80,
    }

def test_daily_report_only_selected_date(test_db):
    user_id = 1

    connection = database.sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (user_id, "2026-08-08", "products", 1000, "card"),
            (user_id, "2026-08-09", "products", 300, "card"),
        ],
    )

    connection.commit()
    connection.close()

    report = database.daily_report_expenses(
        user_id,
        datetime.date(2026, 8, 9),
    )

    assert dict(report) == {
        "products": 300,
    }

def test_weekly_report_date_range(test_db):
    user_id = 1

    connection = database.sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            # До недели — не должен попасть
            (user_id, "2026-08-02", "products", 5000, "card"),

            # Наша неделя
            (user_id, "2026-08-03", "products", 100, "card"),
            (user_id, "2026-08-05", "products", 200, "card"),
            (user_id, "2026-08-09", "coffee", 50, "cash"),

            # После недели — не должен попасть
            (user_id, "2026-08-10", "products", 9000, "card"),
        ],
    )

    connection.commit()
    connection.close()

    report = database.weekly_report_expenses(
        user_id,
        datetime.date(2026, 8, 3),
        datetime.date(2026, 8, 9),
    )

    assert dict(report) == {
        "products": 300,
        "coffee": 50,
    }

def test_monthly_report(test_db):
    user_id = 1

    connection = database.sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (user_id, "2026-07-31", "products", 9000, "card"),
            (user_id, "2026-08-01", "products", 100, "card"),
            (user_id, "2026-08-15", "products", 200, "card"),
            (user_id, "2026-08-31", "coffee", 50, "cash"),
        ],
    )

    connection.commit()
    connection.close()

    report = database.monthly_report_expenses(
        user_id,
        datetime.date(2026, 8, 1),
        datetime.date(2026, 8, 31),
    )

    assert dict(report) == {
        "products": 300,
        "coffee": 50,
    }

def test_yearly_report(test_db):
    user_id = 1

    connection = database.sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (user_id, "2025-12-31", "products", 9000, "card"),
            (user_id, "2026-01-01", "products", 100, "card"),
            (user_id, "2026-06-15", "coffee", 200, "cash"),
            (user_id, "2026-12-31", "products", 300, "card"),
        ],
    )

    connection.commit()
    connection.close()

    report = database.yearly_report_expenses(
        user_id,
        datetime.date(2026, 1, 1),
        datetime.date(2026, 12, 31),
    )

    assert dict(report) == {
        "products": 400,
        "coffee": 200,
    }

def test_add_user_does_not_create_duplicates(test_db):
    database.add_user(123456)
    database.add_user(123456)

    users = database.get_all_users()

    assert users == [(123456,)]