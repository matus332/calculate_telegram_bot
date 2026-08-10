from database import get_connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dollars (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            type TEXT,
            amount INTEGER
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS grn_cash (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            type TEXT,
            amount INTEGER
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS grn_card (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            type TEXT,
            amount INTEGER
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            user_id BIGINT REFERENCES users(user_id),
            date DATE,
            category TEXT,
            amount INTEGER,
            payment_method TEXT
        )
        """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()