import os
import logging
import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----------------------------------------------------
# DATABASE SETUP (SQLite)
# ----------------------------------------------------
DB_NAME = "fast_bingo.db"

def init_sqlite_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            balance REAL DEFAULT 10.0,
            bonus_points INTEGER DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_or_create_user(user_id, first_name, username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, balance, bonus_points FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if row is None:
        initial_balance = 10.0
        cursor.execute(
            "INSERT INTO users (user_id, first_name, username, balance) VALUES (?, ?, ?, ?)",
            (user_id, first_name, username, initial_balance)
        )
        conn.commit()
        conn.close()
        return {"balance": initial_balance, "bonus_points": 0, "is_new": True}
    else:
        conn.close()
        return {"balance": row[1], "bonus_points": row[2], "is_new": False}

# Initialize Database
init_sqlite_db()

# ----------------------------------------------------
# WEB SERVER FOR WEBAPP
# ----------------------------------------------------
class CustomWebAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

def run_http_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), CustomWebAppHandler)
    print(f"Serving WebApp on port {port}...")
    server.serve_forever()

# ----------------------------------------------------
# TELEGRAM BOT HANDLERS
# ----------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name if user.first_name else "ተጫዋች"
    username = user.username if user.username else ""
    
    # Save/Retrieve from DB
    user_data = get_or_create_user(user.id, first_name, username)
    
    web_app_url = "https://my-fastbingo-app.onrender.com"

    # የቅድሙ 9 በተኖች በምስሉ ላይ እንደነበረው (1 Full Width + 8 Grid Buttons)
    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ተጫወት (Play Bingo)", web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton("👤 ፕሮፋይል / ቀሪ ሂሳብ", callback_data="bal"), InlineKeyboardButton("💳 ብር መሙያ (Deposit)", callback_data="dep")],
        [InlineKeyboardButton("🤑 ብር ማውጫ (Withdraw)", callback_data="with"), InlineKeyboardButton("🎁 ብር ማስተላለፊያ", callback_data="trans")],
        [InlineKeyboardButton("📖 መመሪያ (Instruction)", callback_data="inst"), InlineKeyboardButton("☎️ እገዛ (Support)", callback_data="sup")],
        [InlineKeyboardButton("🔗 ጓደኛ ጋብዝ (Invite)", callback_data="inv"), InlineKeyboardButton("🔄 ቦነስ መመንዘሪያ", callback_data="bon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bonus_msg = "\n🎉 **የ 10 ETB ነፃ የመመዝገቢያ ቦነስ ተጨምሮልዎታል!**\n" if user_data["is_new"] else ""

    welcome_txt = (
        f"🔥 **እንኳን ወደ Fast Bingo NextGen Pro በደህና መጡ!**\n\n"
        f"ሰላም **{first_name}** 👋{bonus_msg}\n"
        f"በኢትዮጵያ የመጀመሪያው እና ዘመናዊው የኦንላይን የቢንጎ ጨዋታ መድረክ ላይ ይገኛሉ።\n\n"
        f"🎯 **ለመጫወት፦** ከታች የሚገኘውን **'🎮 ቢንጎ ተጫወት'** የሚለውን ቁልፍ ይጫኑ።\n"
        f"💰 **የአካውንትዎ መረጃ፦** **'👤 ፕሮፋይል / ቀሪ ሂሳብ'** የሚለውን በመጫን ይመልከቱ።"
    )

    photo_path = "static/logo.png"

    try:
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo_file,
                    caption=welcome_txt,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
        else:
            await update.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to send photo: {e}")
        await update.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    account_id = f"FB-{user.id}"
    first_name = user.first_name if user.first_name else "ተጫዋች"
    username = user.username if user.username else ""

    # Fetch live user data from Database
    user_data = get_or_create_user(user.id, first_name, username)

    data = query.data

    if data == "bal":
        profile_txt = (
            f"👤 **የተጫዋች ፕሮፋይል መረጃ**\n\n"
            f"▫️ **ስም:** {first_name}\n"
            f"▫️ **ቋሚ ID:** `{account_id}`\n"
            f"💵 **ቀሪ ሂሳብ:** **{user_data['balance']:.2f} ETB**\n"
            f"🎁 **የቦነስ ነጥብ:** **{user_data['bonus_points']} Points**\n\n"
            f"*(አካውንትዎ ላይ ብር ለመሙላት '💳 ብር መሙያ' የሚለውን ይጠቀሙ)*"
        )
        await query.message.reply_text(profile_txt, parse_mode="Markdown")
    elif data == "dep":
        await query.message.reply_text("💳 **ብር መሙያ (Deposit)**\n\nበቴሌብር (Telebirr) ወይም ቻፓ (Chapa) ሂሳብዎን መሙላት ይችላሉ።\nለማስገባት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "with":
        await query.message.reply_text("🤑 **ብር ማውጫ (Withdraw)**\n\nዝቅተኛ የማውጫ መጠን: **50 ብር**\nለማውጣት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "sup":
        await query.message.reply_text("☎️ **የደንበኞች እገዛ (Support)**\n\nለማንኛውም ጥያቄ ወይም አቤቱታ በቴሌግራም ያውሩን፦ @wende4366", parse_mode="Markdown")
    elif data == "inst":
        await query.message.reply_text("📖 **የጨዋታ መመሪያ (Instruction)**\n\n1. 'ቢንጎ ተጫወት' የሚለውን በመጫን ቦርዱን ይክፈቱ።\n2. ከ 1-600 ካርቴላዎች ውስጥ የሚፈልጉትን ይምረጡ።\n3. ቁጥሮች ሲጠሩ በራሱ ወይም በእጅዎ ይመልከቱ።\n4. ቀድመው ቢንጎ ሲሰሩ ያሸንፋሉ!", parse_mode="Markdown")
    elif data == "trans":
        await query.message.reply_text("🎁 **ብር ማስተላለፊያ (Transfer)**\n\nለሌላ ተጫዋች ብር ለማስተላለፍ የያዙትን ID ያስገቡ፦", parse_mode="Markdown")
    elif data == "inv":
        await query.message.reply_text(f"🔗 **ጓደኛ ይጋብዙ**\n\nይህንን የጋበዛ ሊንክ ለጓደኞችዎ በመላክ ቦነስ ያግኙ፦\nhttps://t.me/FastBingoBot?start={account_id}", parse_mode="Markdown")
    elif data == "bon":
        await query.message.reply_text("🔄 **ቦነስ መመንዘሪያ**\n\nያለዎት የቦነስ ነጥብ: **0 Points** (100 Points = 10 ብር)", parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Fast Bingo Bot running smoothly...")
    app.run_polling()

if __name__ == "__main__":
    main()
