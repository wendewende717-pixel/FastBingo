import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://my-fastbingo-app.onrender.com")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# የ Fast Bingo ሎጎ ምስል URL
LOGO_URL = "https://raw.githubusercontent.com/wendewende717-pixel/FastBingo/main/static/logo.png"

app = FastAPI()
telegram_app = None

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
    
    try:
        # ሎጎውን ከነ ሙሉ መልእክቱ ይልካል
        await update.message.reply_photo(photo=LOGO_URL, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        await update.message.reply_text(caption, reply_markup=reply_markup, parse_mode="Markdown")

@app.on_event("startup")
async def startup_event():
    global telegram_app
    if BOT_TOKEN:
        telegram_app = Application.builder().token(BOT_TOKEN).build()
        telegram_app.add_handler(CommandHandler("start", start))
        await telegram_app.initialize()
        await telegram_app.start()
        webhook_url = f"{WEBAPP_URL}/webhook"
        await telegram_app.bot.set_webhook(url=webhook_url, drop_pending_updates=True)
        logging.info(f"Webhook set to {webhook_url}")

@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Fast Bingo Bot and WebApp is running smoothly with Logo Banner!"}
