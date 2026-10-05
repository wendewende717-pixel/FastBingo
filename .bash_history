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
cd FastBingo
git checkout main
nano requirements.txt
nano static/index.html
nano main.py
git add .
git commit -m "Update NextGen Fast Bingo WebApp with Beteseb UI"
git push origin main
nano main.py
git add .
git commit -m "Fix URL to my-fastbingo-app and update main logic"
git push origin main
nano main.py
git add .
git commit -m "Add Share Contact registration, User Account ID and Beteseb style menu"
git push origin main
nano main.py
git add .
git commit -m "Translate all bot menu texts and buttons to Amharic"
git push origin main
nano main.py
git add .
git commit -m "Add photo banner logic and setup interactive button responses"
git push origin main
nano main.py
git add .
git commit -m "Fix image error and stabilize contact handler"
git push origin main
nano main.py
git add .
git commit -m "Add SQLite database for permanent user account IDs and balance"
git push origin main
nano main.py
git add .
git commit -m "Add photo banner header"
git push origin main
nano main.py
git add .
git commit -m "Fix deploy error and build fallback"
git push origin main
nano main.py
git add .
git commit -m "Fix permanent ID and photo banner URL"
git push origin main
nano main.py
git add .
git commit -m "Full updated main.py with direct logo URL"
git push origin main
mkdir -p static
cp /sdcard/Pictures/Telegram/photo.jpg static/photo.jpg
nano main.py
git add .
git commit -m "Include photo.jpg in repository for bot banner"
git push origin main
nano main.py
git add .
git commit -m "Update photo sending logic and light banner URL"
git push origin main
mkdir -p static
cp /sdcard/Pictures/Telegram/logo.png.jpg static/logo.png
termux-setup-storage
mkdir -p static
cp /sdcard/Pictures/Telegram/logo.png.jpg static/logo.png
git add .
git commit -m "Add static logo.png file"
git push origin main
nano main.py
git add main.py
git commit -m "Use local static logo.png for welcome banner"
git push origin main
nano main.py
git add main.py
git commit -m "Optimize welcome message and separate user profile"
git push origin main
nano main.py
import os
import logging
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
# Logging setup
logging.basicConfig(
)
logger = logging.getLogger(__name__)
# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://my-fastbingo-app.onrender.com/static/index.html")
LOGO_URL = "https://raw.githubusercontent.com/wendewende717-pixel/FastBingo/main/static/logo.png"
# Initialize FastAPI app
app = FastAPI(title="Fast Bingo Bot & WebApp")
# Mount static folder for WebApp (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Initialize Telegram Application
tg_app = Application.builder().token(BOT_TOKEN).build()
# Start Command Handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# Register bot handlers
tg_app.add_handler(CommandHandler("start", start_command))
# Application Lifecycle / Webhook Setup
@app.on_event("startup")
async def on_startup():
@app.on_event("shutdown")
async def on_shutdown():
# Webhook Route for Telegram Updates
@app.post("/webhook")
async def telegram_webhook(request: Request):
# Root Endpoint Redirect to WebApp
@app.get("/")
async def root():
nano main.py
git add main.py
git commit -m "Fix main.py static mount"
git push origin main
