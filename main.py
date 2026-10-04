import os
import json
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
                balance REAL DEFAULT 50.0,
                bonus_points INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                type TEXT,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                           (user_id, first_name, username, 50.0))
            conn.commit()
            row = (user_id, 50.0, 0)
        conn.close()
        return row
    except Exception as e:
        logging.error(f"Error in get_or_create_user: {e}")
        return (user_id, 50.0, 0)

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

    logo_path = "logo.jpg"
    
    if os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as photo_file:
                await update.message.reply_photo(
                    photo=photo_file,
                    caption=caption_text,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            return
        except Exception as e:
            logging.error(f"Error sending local photo: {e}")

    await update.message.reply_text(
        text=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/api/get_profile":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_id = data.get("user_id")
            first_name = data.get("first_name", "ተጫዋች")
            username = data.get("username", "")

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if row is None:
                cursor.execute("INSERT INTO users (user_id, username, first_name, balance) VALUES (?, ?, ?, ?)",
                               (user_id, username, first_name, 50.0))
                conn.commit()
                balance = 50.0
            else:
                balance = row[0]

            conn.close()

            response = {"status": "success", "user_id": user_id, "balance": balance}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif parsed_path.path == "/api/buy_card":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            user_id = data.get("user_id")
            room_price = float(data.get("room_price", 0))

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if row and row[0] >= room_price:
                new_balance = row[0] - room_price
                cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
                cursor.execute("INSERT INTO transactions (user_id, amount, type, description) VALUES (?, ?, ?, ?)",
                               (user_id, room_price, "ENTRY_FEE", f"{room_price} ETB ክፍል መግቢያ"))
                conn.commit()
                conn.close()

                response = {"status": "success", "new_balance": new_balance, "message": "ካርድ በተሳካ ሁኔታ ተገዝቷል!"}
            else:
                conn.close()
                response = {"status": "error", "message": "በቂ ቀሪ ሂሳብ የሎትም! እባክዎን አስቀድመው ብር ያስገቡ።"}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_POST()

def run_http_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
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
