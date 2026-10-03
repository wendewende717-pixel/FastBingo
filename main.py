import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

def get_webapp_url():
    try:
        if os.path.exists("tunnel.log"):
            with open("tunnel.log", "r") as f:
                for line in f:
                    if "trycloudflare.com" in line:
                        parts = line.split()
                        for part in parts:
                            if "https://" in part and "trycloudflare.com" in part:
                                return part.strip()
    except Exception as e:
        logging.error(f"Error reading tunnel URL: {e}")
    return os.getenv("WEBAPP_URL", "https://example.com")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = get_webapp_url()
    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ጨዋታ ጀምር (Play Bingo)", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton("📢 ቻናል ይቀላቀሉ", url="https://t.me/your_channel"),
         InlineKeyboardButton("👥 የቴሌግራም ቡድን", url="https://t.me/your_group")],
        [InlineKeyboardButton("ℹ️ ስለ ቦቱ / እርዳታ", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 **እንኳን ወደ Fast Bingo በሰላም መጡ!**\n\n"
        "ለመጫወት ከታች ያለውን **'🎮 ቢንጎ ጨዋታ ጀምር'** የሚለውን ቁልፍ ይጫኑ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def run_http_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logging.info("Starting HTTP server on port 8000...")
    httpd.serve_forever()

def main():
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    logging.info("Starting Telegram Bot...")
    app.run_polling()

if __name__ == "__main__":
    main()
