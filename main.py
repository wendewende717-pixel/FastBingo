import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class CustomWebAppHandler(SimpleHTTPRequestHandler):
    def init(self, *args, **kwargs):
        super().init(*args, directory="static", **kwargs)

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

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN", "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Fast Bingo Bot is running...")
    app.run_polling()

if name == "main":
    main()
