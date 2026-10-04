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
        [InlineKeyboardButton("🎮 ቢንጎ ተጫወት (Play Bingo)", web_app=WebAppInfo(url=url))],
        [
            InlineKeyboardButton("👤 ፕሮፋይል / ቀሪ ሂሳብ", callback_data="profile"),
            InlineKeyboardButton("💳 ብር መሙያ (Deposit)", callback_data="deposit")
        ],
        [
            InlineKeyboardButton("🤑 ብር ማውጫ (Withdraw)", callback_data="withdraw"),
            InlineKeyboardButton("🎁 ብር ማስተላለፊያ", callback_data="transfer")
        ],
        [
            InlineKeyboardButton("📖 መመሪያ (Instruction)", callback_data="instruction"),
            InlineKeyboardButton("☎️ እገዛ (Support)", callback_data="support")
        ],
        [
            InlineKeyboardButton("🔗 ጓደኛ ጋብዝ (Invite)", callback_data="invite"),
            InlineKeyboardButton("🔄 ቦነስ መንኮራኩር", callback_data="spin")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption_text = (
        f"🔥 **እንኳን ወደ Fast Bingo NextGen Pro በደህና መጡ!**\n\n"
        f"ሰላም {user.first_name} 👋\n"
        f"በኢትዮጵያ የመጀመሪያው እና ዘመናዊው የኦንላይን የቢንጎ ጨዋታ መድረክ ላይ ይገኛሉ።\n\n"
        f"🎯 **ለመጫወት:-** ከታች የሚገኘውን '🎮 ቢንጎ ተጫወት' የሚለውን ቁልፍ ይጫኑ።\n"
        f"💰 **የአካውንትዎ መረጃ:-** '👤 ፕሮፋይል / ቀሪ ሂሳብ' የሚለውን በመጫን ይመልከቱ።"
    )

    # ቴሌግራም ላይ ባነሩ በትክክል እንዲታይ የሚሰራ ምስል
    banner_url = "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=800"

    try:
        await update.message.reply_photo(
            photo=banner_url,
            caption=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        await update.message.reply_text(
            text=caption_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def run_http_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

def main():
    init_db()
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
