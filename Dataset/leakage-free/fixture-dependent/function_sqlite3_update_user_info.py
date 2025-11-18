import sqlite3

def update_user_info(db_path, user_id, new_name=None, new_age=None, new_gender=None):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        update_fields = []
        values = []

        if new_name is not None:
            update_fields.append("name = ?")
            values.append(new_name)
        if new_age is not None:
            update_fields.append("age = ?")
            values.append(new_age)
        if new_gender is not None:
            update_fields.append("gender = ?")
            values.append(new_gender)

        if not update_fields:
            return False


        update_statement = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        values.append(user_id)


        cursor.execute(update_statement, tuple(values))
        conn.commit()


        return cursor.rowcount > 0

    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error: {e}")

