import os
import logging
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://my-fastbingo-app.onrender.com/static/index.html")
LOGO_URL = "https://raw.githubusercontent.com/wendewende717-pixel/FastBingo/main/static/logo.png"

app = FastAPI(title="Fast Bingo Bot & WebApp")
app.mount("/static", StaticFiles(directory="static"), name="static")

tg_app = Application.builder().token(BOT_TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_first_name = update.effective_user.first_name

    caption_text = (
        f"👋 ሰላም **{user_first_name}**! እንኳን ወደ **Fast Bingo** በደህና መጡ! 🎲\n\n"
        f"⚡️ ኢትዮጵያ ውስጥ የመጀመሪያው ፈጣን እና አስተማማኝ የኦንላይን ቢንጎ ጨዋታ።\n\n"
        f"👇 ጨዋታ ለመጀመር ወይም አገልግሎቶችን ለማግኘት ከታች ያሉትን አማራጮች ይጠቀሙ፦"
    )

    keyboard = [
        [
            InlineKeyboardButton("🎮 ቢንጎ ተጫወት (Play Bingo)", web_app={"url": WEBAPP_URL})
        ],
        [
            InlineKeyboardButton("👤 ፕሮፋይል / ቀሪ ሂሳብ", callback_data="profile"),
            InlineKeyboardButton("💳 ብር መሙያ (Deposit)", callback_data="deposit")
        ],
        [
            InlineKeyboardButton("🤑 ብር ማውጫ (Withdraw)", callback_data="withdraw"),
            InlineKeyboardButton("🎁 ብር ማስተላለፊያ", callback_data="transfer")
        ],
        [
            InlineKeyboardButton("📖 መመሪያ (Instruction)", callback_data="instructions"),
            InlineKeyboardButton("☎️ እገዛ (Support)", callback_data="support")
        ],
        [
            InlineKeyboardButton("🔗 ጓደኛ ጋብዝ (Invite)", callback_data="invite"),
            InlineKeyboardButton("🔄 ቦት መንከባከቢያ", callback_data="refresh")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=LOGO_URL,
            caption=caption_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error sending photo: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=caption_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

tg_app.add_handler(CommandHandler("start", start_command))

@app.on_event("startup")
async def on_startup():
    await tg_app.initialize()
    await tg_app.start()
    webhook_url = f"{WEBAPP_URL.rsplit('/', 2)[0]}/webhook"
    logger.info(f"Setting webhook to: {webhook_url}")
    await tg_app.bot.set_webhook(url=webhook_url)

@app.on_event("shutdown")
async def on_shutdown():
    await tg_app.stop()
    await tg_app.shutdown()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return Response(status_code=200)

@app.get("/")
async def root():
    return FileResponse("static/index.html")
