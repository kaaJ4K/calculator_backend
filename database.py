import sqlite3
from datetime import datetime


DATABASE = "calculator.db"


def get_connection():

    return sqlite3.connect(DATABASE)



def init_database():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        expression TEXT NOT NULL,

        result TEXT NOT NULL,

        created_at TEXT NOT NULL

    )
    """)


    conn.commit()

    conn.close()



def save_history(expression, result):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO history
        (expression, result, created_at)

        VALUES (?, ?, ?)
        """,
        (
            expression,
            str(result),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )


    conn.commit()

    conn.close()



def get_history():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id, expression, result, created_at
        FROM history
        ORDER BY id DESC
        """
    )


    rows = cursor.fetchall()


    conn.close()


    history = []


    for row in rows:

        history.append({

            "id": row[0],

            "expression": row[1],

            "result": row[2],

            "created_at": row[3]

        })


    return history



def delete_history(history_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM history WHERE id=?",
        (history_id,)
    )


    conn.commit()


    deleted = cursor.rowcount


    conn.close()


    return deleted