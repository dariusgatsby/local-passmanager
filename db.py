import sqlite3
import os
HOSTNAME = os.getlogin()
DB_FILE = f"/home/{HOSTNAME}/.localpwm/pw.db"
def connect(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        result = func(conn, cur, *args, **kwargs)
        cur.close()
        conn.close()
        return result
    return wrapper

@connect
def create_table(conn, cur):
    cur.execute("CREATE TABLE passwords (website, username, password, created_at)")

@connect
def add_PW_to_table(conn, cur, data):
    cur.execute("INSERT INTO passwords VALUES(?, ?, ?, ?)", data)
    conn.commit()

@connect
def get_notebook_names(conn, cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    for table in tables:
        print(f"* {table[0]}")

@connect
def view_pws(conn, cur):
    for row in cur.execute(f"SELECT * FROM passwords"):
        if len(row) == 0:
            print("Table empty")
            return None
        print(row)

@connect
def view_sites(conn, cur):
    for row in cur.execute(f"SELECT website FROM passwords"):
        if len(row) == 0:
            print("Table empty")
            return None
        print(row)

@connect
def select_pw(conn, cur, website):
    res = cur.execute(f"SELECT password FROM passwords WHERE website='{website}'")
    pw = res.fetchone()
    print(pw)

@connect
def notebook_exists(conn, cur, name):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
    result = cur.fetchone()
    return result

if __name__ == "__main__":
    pass

