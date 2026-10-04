import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
    first_name = user.first_name if user else "ተጫዋች"
    
    inline_keyboard = [
        [InlineKeyboardButton("🎯 Fast Bingo ጀምር (Play Now)", web_app={"url": WEBAPP_URL})],
        [InlineKeyboardButton("📢 ቻናል (Channel)", url="https://t.me/FastBingoApp")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    
    caption = (
        f"ሰላም {first_name}! 👋\n\n"
        f"እንኳን ወደ **Fast Bingo** በሰላም መጡ! 🎲\n\n"
        f"ከታች ያለውን **'Fast Bingo ጀምር'** የሚለውን ቁልፍ ተጭነው መጫወት ይጀምሩ።"
    )
    
    await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()
    
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN is missing!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Bot is starting...")
    # drop_pending_updates=True የተጋጩ ግንኙነቶችን በራሱ ያጸዳል
    application.run_polling(drop_pending_updates=True, close_loop=False)

if __name__ == "__main__":
    main()
