import sqlite3

def init_db():
    conn = sqlite3.connect("bingo_database.db")
    cursor = conn.cursor()
    
    # 1. Permanent User Accounts (ቋሚ Telegram User ID)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            phone_number TEXT UNIQUE,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. Game Sessions History (ልዩ Game ID እና 20% ኮሚሽን የተቆረጠበት ደራሽ)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            game_id TEXT PRIMARY KEY,
            room_price REAL,
            total_cartelas INTEGER,
            total_players INTEGER,
            derash_amount REAL,
            winner_user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Fast Bingo SQLite Database initialized successfully!")
