import os
import logging
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ከተጠቃሚዎች መረጃ ጊዜያዊ ማከማቻ (In-Memory Database)
USER_DATABASE = {}

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

    # ተጠቃሚው ቀድሞ ካልተመዘገበ ስልኩን እንዲያጋራ መጠየቅ
    if user_id not in USER_DATABASE:
        contact_keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("📲 Share Contact (ስልክ ቁጥር አጋራ)", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        msg = (
            f"ሰላም {first_name}! 👋\n\n"
            f"እንኳን ወደ **Fast Bingo NextGen Pro** በደህና መጡ! 🎲\n\n"
            f"ጨዋታውን ለመጀመርና የራሶትን ልዩ **Account ID** ለማግኘት እባክዎ ከታች ያለውን **'📲 Share Contact'** አዝራር ይጫኑ።"
        )
        await update.message.reply_text(msg, reply_markup=contact_keyboard, parse_mode="Markdown")
    else:
        # ከተመዘገበ ዋናውን Dashboard ማሳየት
        await show_main_menu(update, user_id)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    phone_number = update.message.contact.phone_number

    # ለተጠቃሚው ልዩ Account ID ማመንጨት (ለምሳሌ FB-7842)
    custom_id = f"FB-{random.randint(1000, 9999)}"
    USER_DATABASE[user_id] = {
        "name": first_name,
        "phone": phone_number,
        "account_id": custom_id,
        "balance": 0.0
    }

    success_msg = f"🎉 **ምዝገባው ተሳክቷል!**\n\n👤 ስም: {first_name}\n🆔 Account ID: `{custom_id}`\n📱 ስልክ: {phone_number}"
    await update.message.reply_text(success_msg, parse_mode="Markdown")
    
    # ወደ ዋናው ሜኑ መውሰድ
    await show_main_menu(update, user_id)

async def show_main_menu(update: Update, user_id: int):
    user_data = USER_DATABASE.get(user_id, {"account_id": f"FB-{user_id}", "balance": 0.0})
    web_app_url = "https://my-fastbingo-app.onrender.com"

    keyboard = [
        [InlineKeyboardButton("🎮 Play Bingo (ተጫወት)", web_app=WebAppInfo(url=web_app_url)), InlineKeyboardButton("📝 Register", callback_data="reg")],
        [InlineKeyboardButton("💵 Check Balance", callback_data="bal"), InlineKeyboardButton("💳 Deposit", callback_data="dep")],
        [InlineKeyboardButton("☎️ Contact Support", callback_data="sup"), InlineKeyboardButton("📖 Instruction", callback_data="inst")],
        [InlineKeyboardButton("🎁 Transfer", callback_data="trans"), InlineKeyboardButton("🤑 Withdraw", callback_data="with")],
        [InlineKeyboardButton("🔗 Invite Friends", callback_data="inv"), InlineKeyboardButton("🔄 Convert Bonus", callback_data="bon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_txt = (
        f"👋 Welcome to **Fast Bingo**!\n"
        f"🆔 **Your ID:** `{user_data['account_id']}`\n"
        f"💰 **Balance:** {user_data['balance']} ETB\n\n"
        f"Choose an Option below."
    )
    await update.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        TOKEN = "8156382103:AAH..." # <--- የቦትህን Token እዚህ ጋር ተካው

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("Fast Bingo Bot with Registration is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
