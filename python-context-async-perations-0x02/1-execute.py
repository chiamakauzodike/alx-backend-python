import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # return query results to the with-block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                print(f"[ERROR] {exc_val}")
            self.conn.close()
            print("[INFO] Database connection closed.")

# Usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    print("[RESULTS]", results)
