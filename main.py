import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. Static WebApp Server Setup (Serves static/index.html)
class WebAppHandler(SimpleHTTPRequestHandler):
    def init(self, *args, **kwargs):
        super().init(*args, directory="static", **kwargs)

def run_http_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), WebAppHandler)
    print(f"Serving WebApp on port {port}...")
    server.serve_forever()

# 2. Telegram Bot Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Live Render WebApp Link
    web_app_url = "https://fastbingo.onrender.com"
    
    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ጨዋታ ጀምር", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    user_first_name = update.effective_user.first_name
    welcome_msg = (
        f"ሰላም {user_first_name}! 👋\n\n"
        f"እንኳን ወደ Fast Bingo NextGen Pro በደህና መጡ! 🎲\n"
        f"ከታች ያለውን አዝራር ተጭነው ጨዋታውን ይጀምሩ።"
    )
    
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode="Markdown")

# 3. Main Application Entry Point
def main():
    # Start HTTP Static WebApp Server in a background thread
    threading.Thread(target=run_http_server, daemon=True).start()

    # Telegram Bot Token (ከመቀየርህ በፊት ያንተን Bot Token እዚህ አስገባ)
    TOKEN = os.environ.get("BOT_TOKEN", "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss")

    # Build and run python-telegram-bot
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Fast Bingo Bot is running...")
    app.run_polling()

if name == "main":
    main()
