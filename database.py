import sqlite3

DB_NAME = "fast_bingo.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            type TEXT,
            amount REAL,
            status TEXT DEFAULT 'PENDING',
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            room_price REAL,
            win_amount REAL DEFAULT 0.0,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_or_create_user(telegram_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT INTO users (telegram_id, username, first_name, balance) VALUES (?, ?, ?, ?)",
            (telegram_id, username, first_name, 0.0)
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cursor.fetchone()
    conn.close()
    return dict(user)

def update_balance(telegram_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Fast Bingo Database በስኬት ተዘጋጅቷል!")
