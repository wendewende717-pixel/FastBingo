import os
import logging
import asyncio
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
    # ትክክለኛው የ Render አድራሻህ
    web_app_url = "https://my-fastbingo-app.onrender.com"
    
    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ጨዋታ ጀምር", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "ሰላም! እንኳን ወደ Fast Bingo NextGen Pro በደህና መጡ! 🎲\nከታች ያለውን አዝራር ተጭነው ይጫወቱ።", 
        reply_markup=reply_markup
    )

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        # እዚህ ጋር በ BotFather የሰጠህን Token አስገባ
        TOKEN = "8156382103:AAH..." # <--- የቦትህን Token እዚህ ጻፍ!

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Fast Bingo Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
