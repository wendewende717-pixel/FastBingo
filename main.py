import os
import logging
import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
DB_NAME = "fast_bingo.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                balance REAL DEFAULT 0.0,
                bonus_points INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("SQLite Database initialized successfully.")
    except Exception as e:
        logging.error(f"Database init error: {e}")

def get_or_create_user(user_id, first_name, username):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, balance, bonus_points FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO users (user_id, first_name, username, balance) VALUES (?, ?, ?, ?)",
                           (user_id, first_name, username, 0.0))
            conn.commit()
            row = (user_id, 0.0, 0)
        conn.close()
        return row
    except Exception as e:
        logging.error(f"Error in get_or_create_user: {e}")
        return (user_id, 0.0, 0)

def get_webapp_url():
    return os.getenv("WEBAPP_URL", "https://my-fastbingo-app.onrender.com")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_or_create_user(user.id, user.first_name, user.username)
    
    url = get_webapp_url()
    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ጨዋታ ጀምር (Play Bingo)", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton("📢 ቻናል ይቀላቀሉ", url="https://t.me/your_channel"),
         InlineKeyboardButton("👥 የቴሌግራም ቡድን", url="https://t.me/your_group")],
        [InlineKeyboardButton("ℹ️ ስለ ቦቱ / እርዳታ", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **እንኳን ወደ Fast Bingo በሰላም መጡ {user.first_name}!**\n\n"
        "ለመጫወት ከታች ያለውን **'🎮 ቢንጎ ጨዋታ ጀምር'** የሚለውን ቁልፍ ይጫኑ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def run_http_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logging.info("Starting HTTP server on port 8000...")
    httpd.serve_forever()

def main():
    init_db()
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    logging.info("Starting Telegram Bot...")
    app.run_polling()

if __name__ == "__main__":
    main()
