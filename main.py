import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://my-fastbingo-app.onrender.com")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run_http_server():
    port = int(os.environ.get("PORT", 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, QuietHTTPRequestHandler)
    print(f"HTTP WebApp server running on port {port}...")
    httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name if user else "Wende"
    
    inline_keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ተጫወት (Play Bingo)", web_app=WebAppInfo(url=WEBAPP_URL))],
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
            InlineKeyboardButton("☎️ እገዛ (Support)", url="https://t.me/FastBingoApp")
        ],
        [
            InlineKeyboardButton("🔗 ጓደኛ ጋብዝ (Invite)", callback_data="invite"),
            InlineKeyboardButton("🔄 ቦት መንከባከቢያ", callback_data="refresh")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    
    caption = (
        f"🔥 **እንኳን ወደ Fast Bingo NextGen Pro በደህና መጡ!**\n\n"
        f"ሰላም {first_name} 👋\n"
        f"በኢትዮጵያ የመጀመሪያው እና ዘመናዊው የኦንላይን የቢንጎ ጨዋታ መድረክ ላይ ይገኛሉ።\n\n"
        f"🎯 **ለመጫወት፦** ከታች የሚገኘውን '**🎮 ቢንጎ ተጫወት**' የሚለውን ቁልፍ ይጫኑ።\n"
        f"💰 **የአካውንትዎ መረጃ፦** '**👤 ፕሮፋይል / ቀሪ ሂሳብ**' የሚለውን በመጫን ይመልከቱ።"
    )
    
    await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()
    
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN is missing!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Fast Bingo Pro Bot is starting...")
    application.run_polling(drop_pending_updates=True, close_loop=False)

if __name__ == "__main__":
    main()
