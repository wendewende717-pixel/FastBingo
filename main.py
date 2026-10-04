import os
import asyncio
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://my-fastbingo-app.onrender.com")

# --- Simple HTTP Server for Render Port Binding ---
def run_http_server():
    port = int(os.getenv("PORT", 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"HTTP Web Server running on port {port}...")
    httpd.serve_forever()

# --- Telegram Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    
    keyboard = [
        [InlineKeyboardButton("🎯 Fast Bingo ጀምር (Play Now)", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📢 ቻናል (Channel)", url="https://t.me/A_ToolsX")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"ሰላም {user_first_name}! 👋\n\nወደ **Fast Bingo NextGen Pro** እንኳን በደህና መጡ! 🎲\n\nታች ያለውን **'Fast Bingo ጀምር'** የሚለውን በተን በመጫን መጫወት መጀመር ይችላሉ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    # 1. Start Web HTTP Server in separate Thread
    threading.Thread(target=run_http_server, daemon=True).start()

    # 2. Run Telegram Bot
    if TOKEN:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        print("Telegram Bot is running...")
        app.run_polling()
    else:
        print("Warning: BOT_TOKEN environment variable not set. Running Web Server only.")
        import time
        while True:
            time.sleep(3600)

if __name__ == "__main__":
    main()
