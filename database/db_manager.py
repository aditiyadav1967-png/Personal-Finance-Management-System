import sqlite3
import os
from activity.activity_logger import ActivityLogger

class DatabaseManager:
    def __init__(self, db_name="finance.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', db_name)
        self.create_tables()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    type TEXT,
                    description TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    category TEXT,
                    limit_amount REAL,
                    UNIQUE(user_id, category),
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()

    def register_user(self, username, password):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
        
        if user:
            return user['id']
        return None

    def add_transaction(self, user_id, date, category, amount, trans_type, description, username="Unknown"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (user_id, date, category, amount, type, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, date, category, amount, trans_type, description))
            conn.commit()
        
        # Initialize logger specifically for this user
        logger = ActivityLogger(username=username)
        logger.log_transaction(username, trans_type, category, amount, description)

    def get_transactions(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC, id DESC", (user_id,))
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def set_budget(self, user_id, category, limit_amount, username="Unknown"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)
                ON CONFLICT(user_id, category) DO UPDATE SET limit_amount = ?
            ''', (user_id, category, limit_amount, limit_amount))
            conn.commit()

    def get_budgets(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category, limit_amount FROM budgets WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
        return {row['category']: row['limit_amount'] for row in rows}