import sqlite3


def get_user_name(db_connection, user_id):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else "None"
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {e}")
