import re
import logging
import http.server
import socketserver
import threading
import database
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# ዳታቤዙን ሰርቨሩ ሲነሳ ማስጀመር
database.init_db()

TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss"
PORT = 8000

def get_url():
    try:
        with open("tunnel.log", "r") as f:
            urls = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', f.read())
            if urls:
                return urls[-1]
    except Exception:
        pass
    return ""

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/static/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_web_server():
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # ተጫዋቹን ዳታቤዝ ውስጥ መመዝገብ / ማረጋገጥ
    db_user = database.get_or_create_user(
        telegram_id=user.id,
        username=user.username or "",
        first_name=user.first_name or ""
    )
    
    current_url = get_url()
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play Fast Bingo (Web App)", web_app=WebAppInfo(url=current_url))
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **ሰላም {user.first_name}!**\n\n"
        f"ወደ **Fast Bingo NextGen Pro** እንኳን በደህና መጡ! 🎯\n"
        f"💳 ያሎት ቀሪ ሂሳብ: **{db_user['balance']} ETB**\n\n"
        "ታች ያለውን **'Play Fast Bingo'** የሚለውን አዝራር በመጫን ይጫወቱ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    threading.Thread(target=run_web_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 Fast Bingo Bot ከዳታቤዝ ጋር ተያይዞ በስኬት ተነስቷል!")
    app.run_polling()

if __name__ == '__main__':
    main()
