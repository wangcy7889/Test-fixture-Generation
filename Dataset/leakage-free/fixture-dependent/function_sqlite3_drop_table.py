import sqlite3

def drop_table_if_exists(conn, table_name):
    if not isinstance(conn, sqlite3.Connection):
        raise AttributeError()
    try:
        with conn:
            conn.execute(f"DROP TABLE {table_name}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {e}")
