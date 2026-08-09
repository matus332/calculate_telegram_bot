import datetime

import psycopg
import pytest

import database

TEST_DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "finance_test",
    "user": "postgres",
    "password": "1234",
}


@pytest.fixture(autouse=True)
def test_db(monkeypatch):
    def test_connection():
        return psycopg.connect(**TEST_DB_CONFIG)

    monkeypatch.setattr(
        database,
        "get_connection",
        test_connection,
    )

    connection = test_connection()
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS expenses")
    cursor.execute("DROP TABLE IF EXISTS grn_card")
    cursor.execute("DROP TABLE IF EXISTS grn_cash")
    cursor.execute("DROP TABLE IF EXISTS dollars")
    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute("""
        CREATE TABLE users (
            user_id BIGINT PRIMARY KEY
        )
        """)

    cursor.execute("""
        CREATE TABLE dollars (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            type TEXT,
            amount INTEGER
        )
        """)

    cursor.execute("""
        CREATE TABLE grn_cash (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            type TEXT,
            amount INTEGER
        )
        """)

    cursor.execute("""
        CREATE TABLE grn_card (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            type TEXT,
            amount INTEGER
        )
        """)

    cursor.execute("""
        CREATE TABLE expenses (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            category TEXT,
            amount INTEGER,
            payment_method TEXT
        )
        """)

    connection.commit()
    connection.close()


def test_dollar_deposit_and_withdraw():
    user_id = 1

    database.add_user(user_id)
    database.deposit_dollar(user_id, 1000)

    assert database.get_dollar_balance(user_id) == 1000

    database.withdraw_dollar(user_id, 300)

    assert database.get_dollar_balance(user_id) == 700


def test_grn_cash_balance():
    user_id = 1

    database.add_user(user_id)
    database.deposit_grn_cash(user_id, 2000)
    database.withdraw_grn_cash(user_id, 500)

    assert database.get_grn_cash_balance(user_id) == 1500


def test_grn_card_balance():
    user_id = 1

    database.add_user(user_id)
    database.deposit_grn_card(user_id, 3000)
    database.withdraw_grn_card(user_id, 1200)

    assert database.get_grn_card_balance(user_id) == 1800


def test_balances_are_separated_by_user():
    database.add_user(1)
    database.add_user(2)

    database.deposit_grn_card(1, 1000)
    database.deposit_grn_card(2, 5000)

    assert database.get_grn_card_balance(1) == 1000
    assert database.get_grn_card_balance(2) == 5000


def test_add_expense():
    database.add_user(1)

    database.add_expense(
        user_id=1,
        amount=350,
        payment_method="card",
        category="products",
    )

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_id, category, amount, payment_method
        FROM expenses
        """)

    expense = cursor.fetchone()

    connection.close()

    assert expense == (1, "products", 350, "card")


def test_daily_report_groups_categories():
    user_id = 1
    date = datetime.date(2026, 8, 10)

    database.add_user(user_id)

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [
            (user_id, date, "products", 100, "card"),
            (user_id, date, "products", 250, "cash"),
            (user_id, date, "coffee", 80, "card"),
        ],
    )

    connection.commit()
    connection.close()

    report = database.daily_report_expenses(
        user_id,
        date,
    )

    assert dict(report) == {
        "products": 350,
        "coffee": 80,
    }


def test_daily_report_only_selected_date():
    user_id = 1

    database.add_user(user_id)

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [
            (
                user_id,
                datetime.date(2026, 8, 9),
                "products",
                1000,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 8, 10),
                "products",
                300,
                "card",
            ),
        ],
    )

    connection.commit()
    connection.close()

    report = database.daily_report_expenses(
        user_id,
        datetime.date(2026, 8, 10),
    )

    assert dict(report) == {
        "products": 300,
    }


def test_weekly_report_date_range():
    user_id = 1

    database.add_user(user_id)

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [
            (
                user_id,
                datetime.date(2026, 8, 2),
                "products",
                5000,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 8, 3),
                "products",
                100,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 8, 5),
                "products",
                200,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 8, 9),
                "coffee",
                50,
                "cash",
            ),
            (
                user_id,
                datetime.date(2026, 8, 10),
                "products",
                9000,
                "card",
            ),
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


def test_monthly_report():
    user_id = 1

    database.add_user(user_id)

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [
            (
                user_id,
                datetime.date(2026, 7, 31),
                "products",
                9000,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 8, 1),
                "products",
                100,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 8, 15),
                "products",
                200,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 8, 31),
                "coffee",
                50,
                "cash",
            ),
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


def test_yearly_report():
    user_id = 1

    database.add_user(user_id)

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT INTO expenses
        (user_id, date, category, amount, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """,
        [
            (
                user_id,
                datetime.date(2025, 12, 31),
                "products",
                9000,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 1, 1),
                "products",
                100,
                "card",
            ),
            (
                user_id,
                datetime.date(2026, 6, 15),
                "coffee",
                200,
                "cash",
            ),
            (
                user_id,
                datetime.date(2026, 12, 31),
                "products",
                300,
                "card",
            ),
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


def test_add_user_does_not_create_duplicates():
    database.add_user(123456)
    database.add_user(123456)

    users = database.get_all_users()

    assert users == [(123456,)]
