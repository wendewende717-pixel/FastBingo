cat << 'EOF' > main.py
import sqlite3
import random
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import threading

logging.basicConfig(level=logging.INFO)

TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss"
ADMIN_ID = 7390194019

# --- FASTAPI WEB SERVER ---
web_app = FastAPI()
web_app.mount("/static", StaticFiles(directory="static"), name="static")

@web_app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# --- TELEGRAM BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play Fast Bingo (Web App)", web_app=WebAppInfo(url="https://google.com"))
        ],
        [
            InlineKeyboardButton("💰 ባላንስ ማየት", callback_data="check_bal"),
            InlineKeyboardButton("📥 ገቢ (Deposit)", callback_data="dep")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **ሰላም {user.first_name}!**\n\n"
        "ወደ **Fast Bingo Pro WebApp** እንኳን በደህና መጡ! 🎯\n"
        "ታች ያለውን **'Play Fast Bingo'** የሚለውን ቁልፍ በመጫን በዘመናዊ ገፅ ይጫወቱ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def run_web():
    uvicorn.run(web_app, host="0.0.0.0", port=8000, log_level="warning")

def main():
    # Start Web Server in Background Thread
    threading.Thread(target=run_web, daemon=True).start()
    
    # Start Telegram Bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("🚀 Fast Bingo Pro WebApp Server & Bot በስኬት ስራ ጀምሯል (Port 8000)...")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF

python main.py
pkg install python clang make -y
pip install --upgrade pip
pip install fastapi uvicorn requests python-telegram-bot
python main.py
cat << 'EOF' > main.py
import sqlite3
import random
import logging
import http.server
import socketserver
import threading
import json
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss"
PORT = 8000

# --- NATIVE WEB SERVER (NO FASTAPI / UVICORN NEEDED) ---
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/static/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_web_server():
    handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🌐 Native WebApp Server running at http://localhost:{PORT}")
        httpd.serve_forever()

# --- TELEGRAM BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # WebApp Button Configuration
    # ለጊዜው በሙከራ ደረጃ Localhost/Google ወይም በNgrok Link ማገናኘት ይቻላል
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play Fast Bingo (Web App)", web_app=WebAppInfo(url="https://bingo-webapp-preview.loca.lt"))
        ],
        [
            InlineKeyboardButton("💰 ባላንስ ማየት", callback_data="check_bal"),
            InlineKeyboardButton("📥 ገቢ (Deposit)", callback_data="dep")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **ሰላም {user.first_name}!**\n\n"
        "ወደ **Fast Bingo Pro WebApp** እንኳን በደህና መጡ! 🎯\n"
        "ታች ያለውን **'Play Fast Bingo'** የሚለውን አዝራር በመጫን በዘመናዊ ገፅ ይጫወቱ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    # 1. Start Built-in Web Server in background thread
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    
    # 2. Start Telegram Bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("🚀 Fast Bingo Pro WebApp Server & Bot በስኬት ስራ ጀምሯል...")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF

python main.py
pkg install nodejs-lts -y
npm install -g localtunnel
lt --port 8000
pkg install cloudflared -y
cloudflared tunnel --url http://localhost:8000
pkg update && pkg upgrade -y
pkg install cloudflared -y
cloudflared tunnel --url http://localhost:8000
python main.py
cloudflared tunnel --url http://localhost:8000
# 1. የቦት ፋይሉን በራስ-ሰር መጻፍ
cat << 'EOF' > main.py
import sqlite3
import random
import logging
import http.server
import socketserver
import threading
import json
import re
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss"
PORT = 8000

# የቅርብ ጊዜውን URL ለማንበብ
def get_latest_url():
    try:
        with open("tunnel.log", "r") as f:
            content = f.read()
            urls = re.findall(r'https://[a-zA-Z0-0\-]+\.trycloudflare\.com', content)
            if urls:
                return urls[-1]
    except Exception:
        pass
    return "https://cho-march-accuracy-scoop.trycloudflare.com"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/static/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_web_server():
    handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    current_url = get_latest_url()
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play Fast Bingo (Web App)", web_app=WebAppInfo(url=current_url))
        ],
        [
            InlineKeyboardButton("💰 ባላንስ ማየት", callback_data="check_bal"),
            InlineKeyboardButton("📥 ገቢ (Deposit)", callback_data="dep")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **ሰላም {user.first_name}!**\n\n"
        "ወደ **Fast Bingo Pro WebApp** እንኳን በደህና መጡ! 🎯\n"
        "ታች ያለውን **'Play Fast Bingo'** የሚለውን አዝራር በመጫን በዘመናዊ ገፅ ይጫወቱ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("🚀 Fast Bingo Pro WebApp Server & Bot በስኬት ስራ ጀምሯል...")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF

# 2. ቦቱን ማስነሳት
python main.py
# 1. ከ Cloudflare log ላይ ትክክለኛውን URL መፈለግ
TUNNEL_URL=$(grep -o 'https://[a-zA-Z0-9-]*\.trycloudflare\.com' ~/.cloudflared/*.log 2>/dev/null | tail -n 1)
if [ -z "$TUNNEL_URL" ]; then     TUNNEL_URL=$(grep -o 'https://[a-zA-Z0-9-]*\.trycloudflare\.com' log.txt 2>/dev/null | tail -n 1); fi
echo "የተገኘው URL: $TUNNEL_URL"
# 2. main.py ፋይልን በስኬት መጻፍ
cat << EOF > main.py
import sqlite3
import random
import logging
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss"
PORT = 8000
WEBAPP_URL = "${TUNNEL_URL}"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/static/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_web_server():
    handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play Fast Bingo (Web App)", web_app=WebAppInfo(url=WEBAPP_URL))
        ],
        [
            InlineKeyboardButton("💰 ባላንስ ማየት", callback_data="check_bal"),
            InlineKeyboardButton("📥 ገቢ (Deposit)", callback_data="dep")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **ሰላም {user.first_name}!**\n\n"
        "ወደ **Fast Bingo Pro WebApp** እንኳን በደህና መጡ! 🎯\n"
        "ታች ያለውን **'Play Fast Bingo'** የሚለውን አዝራር በመጫን በዘመናዊ ገፅ ይጫወቱ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print(f"🚀 Fast Bingo Pro WebApp Server & Bot በስኬት ስራ ጀምሯል... URL: {WEBAPP_URL}")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF

# 3. ቦቱን ማስነሳት
python main.py
cat << 'EOF' > main.py
import sqlite3
import random
import logging
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss"
PORT = 8000
WEBAPP_URL = "https://cho-march-accuracy-scoop.trycloudflare.com"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/static/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_web_server():
    handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play Fast Bingo (Web App)", web_app=WebAppInfo(url=WEBAPP_URL))
        ],
        [
            InlineKeyboardButton("💰 ባላንስ ማየት", callback_data="check_bal"),
            InlineKeyboardButton("📥 ገቢ (Deposit)", callback_data="dep")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **ሰላም {user.first_name}!**\n\n"
        "ወደ **Fast Bingo Pro WebApp** እንኳን በደህና መጡ! 🎯\n"
        "ታች ያለውን **'Play Fast Bingo'** የሚለውን አዝራር በመጫን በዘመናዊ ገፅ ይጫወቱ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("🚀 Fast Bingo Pro WebApp Server & Bot በስኬት ስራ ጀምሯል...")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF

python main.py
# 1. ያሉትን ሂደቶች ማቆም
pkill -f cloudflared
pkill -f python
# 2. Cloudflare Tunnel ከበስተጀርባ ማስነሳት
cloudflared tunnel --url http://localhost:8000 > tunnel.log 2>&1 &
# 3. ሊንኩ እስኪፈጠር 5 ሰከንድ መጠበቅ
sleep 5
# 4. አዲሱን ሊንክ ከ log ውስጥ አውጥቶ main.py መጻፍ
TUNNEL_URL=$(grep -o 'https://[a-zA-Z0-9-]*\.trycloudflare\.com' tunnel.log | tail -n 1)
cat << EOF > main.py
import sqlite3
import random
import logging
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8234368672:AAHaTtqt08OpQQmrDDjknqtdhH66FeF5Oss"
PORT = 8000
WEBAPP_URL = "${TUNNEL_URL}"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/static/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_web_server():
    handler = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Play Fast Bingo (Web App)", web_app=WebAppInfo(url=WEBAPP_URL))
        ],
        [
            InlineKeyboardButton("💰 ባላንስ ማየት", callback_data="check_bal"),
            InlineKeyboardButton("📥 ገቢ (Deposit)", callback_data="dep")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 **ሰላም {user.first_name}!**\n\n"
        "ወደ **Fast Bingo Pro WebApp** እንኳን በደህና መጡ! 🎯\n"
        "ታች ያለውን **'Play Fast Bingo'** የሚለውን አዝራር በመጫን በዘመናዊ ገፅ ይጫወቱ።",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print(f"🚀 Fast Bingo Pro WebApp Server & Bot በስኬት ስራ ጀምሯል... URL: {WEBAPP_URL}")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF

# 5. ቦቱን ማስነሳት
python main.py
cloudflared tunnel --url http://localhost:8000
cd fast-bingo
python main.py
cd fast-bingo
git add .
git commit -m "Update WebApp UI"
git push
pkg update && pkg install git -y
ls
cd fast-bingo
git add .
git commit -m "Update WebApp UI"
git push
termux-change-repo
pkg update && pkg install git -y
git add .
git commit -m "Update WebApp UI"
git push
cd fast-bingo
git add .
git commit -m "Update WebApp UI"
git push
ls -a
git init
git add .
git commit -m "Update Fast Bingo WebApp UI"
git push
git config --global user.email "wende4366@gmail.com"
git config --global user.name "wende"
git remote add origin https://github.com/wende4366/fast-bingo.git
git add .
git commit -m "Update Fast Bingo WebApp UI"
git push -u origin main
git branch -M main
git push -u origin main
git remote set-url origin https://github.com/wendewende717-pixel/fast-bingo.git
git push -u origin main
git remote set-url origin https://github.com/wendewende717-pixel/FastBingo.git
git push -u origin main --force
cd FastBingo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
keyboard = [[
]]
reply_markup = InlineKeyboardMarkup(keyboard)
git add .
git commit -m "Update Telegram WebApp URL"
git push origin main
cd FastBingo
nano main.py
git add .
git commit -m "Update main.py with fixed WebApp URL"
git push origin main
cd FastBingo
nano main.py
git add .
git commit -m "Update main.py with live Render URL"
git push origin main
