import os
import logging
import random
import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- SQLite Database setup ---
DB_NAME = "bingo_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT UNIQUE,
            account_id TEXT UNIQUE,
            balance REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_user_by_telegram_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, account_id, balance FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "phone": row[1], "account_id": row[2], "balance": row[3]}
    return None

def register_or_get_user(user_id, name, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check by phone number first to prevent duplicate accounts per phone
    cursor.execute("SELECT user_id, name, phone, account_id, balance FROM users WHERE phone = ?", (phone,))
    existing_phone = cursor.fetchone()
    
    if existing_phone:
        # If phone exists, update user_id in case Telegram account changed
        cursor.execute("UPDATE users SET user_id = ? WHERE phone = ?", (user_id, phone))
        conn.commit()
        conn.close()
        return {"name": existing_phone[1], "phone": existing_phone[2], "account_id": existing_phone[3], "balance": existing_phone[4]}, False

    # Generate unique FB-XXXX ID
    while True:
        custom_id = f"FB-{random.randint(1000, 9999)}"
        cursor.execute("SELECT 1 FROM users WHERE account_id = ?", (custom_id,))
        if not cursor.fetchone():
            break

    cursor.execute("INSERT INTO users (user_id, name, phone, account_id, balance) VALUES (?, ?, ?, ?, ?)",
                   (user_id, name, phone, custom_id, 0.0))
    conn.commit()
    conn.close()
    return {"name": name, "phone": phone, "account_id": custom_id, "balance": 0.0}, True

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    user_data = get_user_by_telegram_id(user_id)

    if not user_data:
        contact_keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("📲 ስልክ ቁጥር አጋራ (Share Contact)", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        msg = (
            f"ሰላም {first_name}! 👋\n\n"
            f"እንኳን ወደ **Fast Bingo NextGen Pro** በደህና መጡ! 🎲\n\n"
            f"የራሶትን ቋሚ የሂሳብ መለያ (**Account ID**) ለማግኘት እባክዎ ከታች ያለውን **'📲 ስልክ ቁጥር አጋራ'** የሚለውን አዝራር ይጫኑ።\n\n"
            f"*(ማሳሰቢያ፦ የስልክ ቁጥርዎ ለደህንነት እና ለቋሚ አካውንትዎ ብቻ ያገለግላል)*"
        )
        await update.message.reply_text(msg, reply_markup=contact_keyboard, parse_mode="Markdown")
    else:
        await show_main_menu(update, user_id, user_data)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        first_name = update.effective_user.first_name
        phone_number = update.message.contact.phone_number

        user_data, is_new = register_or_get_user(user_id, first_name, phone_number)

        if is_new:
            success_msg = f"🎉 **ምዝገባዎ በስኬት ተጠናቋል!**\n\n👤 **ስም:** {first_name}\n🆔 **የእርስዎ ቋሚ ID:** `{user_data['account_id']}`\n📱 **ስልክ:** {phone_number}"
        else:
            success_msg = f"🔄 **እንኳን ተመልሰው መጡ!**\n\nቀደም ሲል የተመዘገበ አካውንት አግኝተናል፦\n🆔 **የእርስዎ ID:** `{user_data['account_id']}`\n💰 **ቀሪ ሂሳብ:** {user_data['balance']} ብር"

        await update.message.reply_text(success_msg, parse_mode="Markdown")
        await show_main_menu(update, user_id, user_data)
    except Exception as e:
        logging.error(f"Error in contact handler: {e}")

async def show_main_menu(update: Update, user_id: int, user_data=None):
    if not user_data:
        user_data = get_user_by_telegram_id(user_id) or {"account_id": f"FB-{user_id}", "balance": 0.0}

    web_app_url = "https://my-fastbingo-app.onrender.com"

    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ተጫወት (Play)", web_app=WebAppInfo(url=web_app_url)), InlineKeyboardButton("📝 ምዝገባ", callback_data="reg")],
        [InlineKeyboardButton("💵 ቀሪ ሂሳብ (Balance)", callback_data="bal"), InlineKeyboardButton("💳 ብር መሙያ (Deposit)", callback_data="dep")],
        [InlineKeyboardButton("☎️ እገዛ (Support)", callback_data="sup"), InlineKeyboardButton("📖 መመሪያ (Instruction)", callback_data="inst")],
        [InlineKeyboardButton("🎁 ብር ማስተላለፊያ", callback_data="trans"), InlineKeyboardButton("🤑 ብር ማውጫ (Withdraw)", callback_data="with")],
        [InlineKeyboardButton("🔗 ጓደኛ ጋብዝ (Invite)", callback_data="inv"), InlineKeyboardButton("🔄 ቦነስ ቀይር", callback_data="bon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_txt = (
        f"👋 እንኳን ወደ **Fast Bingo NextGen Pro** በደህና መጡ!\n\n"
        f"🆔 **የእርስዎ ID:** `{user_data['account_id']}`\n"
        f"💰 **የአካውንትዎ ቀሪ ሂሳብ:** {user_data['balance']} ብር\n\n"
        f"ከታች ካሉት አማራጮች አንዱን ይምረጡ፦"
    )

    if update.message:
        await update.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = get_user_by_telegram_id(user_id) or {"account_id": f"FB-{user_id}", "balance": 0.0}

    data = query.data

    if data == "bal":
        await query.message.reply_text(f"💵 **የቀሪ ሂሳብ መረጃ**\n\n🆔 ID: `{user_data['account_id']}`\n💰 ቀሪ ሂሳብ: **{user_data['balance']} ብር**", parse_mode="Markdown")
    elif data == "dep":
        await query.message.reply_text("💳 **ብር መሙያ (Deposit)**\n\nበቴሌብር (Telebirr) ወይም ቻፓ (Chapa) ሂሳብዎን መሙላት ይችላሉ።\nለማስገባት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "with":
        await query.message.reply_text("🤑 **ብር ማውጫ (Withdraw)**\n\nዝቅተኛ የማውጫ መጠን: **50 ብር**\nለማውጣት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "sup":
        await query.message.reply_text("☎ **የደንበኞች እገዛ (Support)**\n\nለማንኛውም ጥያቄ ወይም አቤቱታ በቴሌግራም ያውሩን፦ @wende4366", parse_mode="Markdown")
    elif data == "inst":
        await query.message.reply_text("📖 **የጨዋታ መመሪያ (Instruction)**\n\n1. 'ቢንጎ ተጫወት' የሚለውን በመጫን ቦርዱን ይክፈቱ።\n2. ከ 1-600 ካርቴላዎች ውስጥ የሚፈልጉትን ይምረጡ።\n3. ቁጥሮች ሲጠሩ በራሱ ወይም በእጅዎ ይመልከቱ።\n4. ቀድመው ቢንጎ ሲሰሩ ያሸንፋሉ!", parse_mode="Markdown")
    elif data == "reg":
        await query.message.reply_text(f"📝 **የምዝገባ መረጃ**\n\nተመዝግበዋል! የቋሚ መለያ ቁጥርዎ: `{user_data['account_id']}` ነው::", parse_mode="Markdown")
    elif data == "trans":
        await query.message.reply_text("🎁 **ብር ማስተላለፊያ (Transfer)**\n\nለሌላ ተጫዋች ብር ለማስተላለፍ የያዙትን ID ያስገቡ፦", parse_mode="Markdown")
    elif data == "inv":
        await query.message.reply_text(f"🔗 **ጓደኛ ይጋብዙ**\n\nይህንን የጋበዛ ሊንክ ለጓደኞችዎ በመላክ ቦነስ ያግኙ፦\nhttps://t.me/FastBingoBot?start={user_data['account_id']}", parse_mode="Markdown")
    elif data == "bon":
        await query.message.reply_text("🔄 **ቦነስ መመንዘሪያ**\n\nያለዎት የቦነስ ነጥብ: **0 Points** (100 Points = 10 ብር)", parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        TOKEN = "8156382103:AAH..." # <--- የቦትህ Token

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Fast Bingo Bot with Permanent Database running...")
    app.run_polling()

if __name__ == "__main__":
    main()
