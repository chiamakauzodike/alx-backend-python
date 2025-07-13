import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # This will be assigned to the variable in the `with` statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                print(f"[ERROR] Exception occurred: {exc_val}")
            self.conn.close()
            print("[INFO] Database connection closed.")

# Use the custom context manager to execute a query
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("[RESULTS]", results)
