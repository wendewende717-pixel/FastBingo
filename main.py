import os
import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler

logging.basicConfig(level=logging.INFO)

WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://fast-bingo-bot.onrender.com")
TOKEN = os.environ.get("BOT_TOKEN")

tg_app = None

if TOKEN:
    tg_app = Application.builder().token(TOKEN).build()

    async def start(update: Update, context):
        user = update.effective_user
        first_name = user.first_name if user else "ተጫዋች"

        inline_keyboard = [
            [InlineKeyboardButton("🎯 Fast Bingo ጀምር (Play Now)", web_app={"url": WEBAPP_URL})],
            [InlineKeyboardButton("📢 ቻናል (Channel)", url="https://t.me/A_ToolsX")]
        ]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        reply_keyboard = [
            [KeyboardButton("🕹️ ቢንጎ ተጫወት (Play Bingo)", web_app={"url": WEBAPP_URL})],
            [KeyboardButton("👤 ፕሮፋይል / ቀሪ ሂሳብ"), KeyboardButton("💳 ብር መሙያ (Deposit)")],
            [KeyboardButton("🤑 ብር ማውጫ (Withdraw)"), KeyboardButton("🎁 ብር ማስተላለፊያ")],
            [KeyboardButton("📖 መመሪያ (Instruction)"), KeyboardButton("☎ እገዛ (Support)")],
            [KeyboardButton("🔗 ጓደኛ ይጋብዙ (Invite)"), KeyboardButton("🔄 ሪቪው")]
        ]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

        welcome_text = (
            f"🔥 እንኳን ወደ Fast Bingo NextGen Pro በደህና መጡ!\n\n"
            f"ሰላም {first_name} 👋\n"
            f"በኢትዮጵያ የመጀመሪያው እና ዘመናዊው የኦንላይን የቢንጎ ጨዋታ መድረክ ላይ ይገኛሉ።\n\n"
            f"🎯 ለመጫወት፦ ከታች የሚገኘውን '🎯 ቢንጎ ተጫወት' የሚለውን ቁልፍ ይጫኑ።"
        )

        await update.message.reply_text(text=welcome_text, reply_markup=inline_markup)
        await update.message.reply_text(text="👇 ከታች ያሉትን አማራጮች ይጠቀሙ፦", reply_markup=reply_markup)

    tg_app.add_handler(CommandHandler("start", start))

@asynccontextmanager
async def lifespan(app: FastAPI):
    if tg_app:
        await tg_app.initialize()
        await tg_app.start()
        await tg_app.updater.start_polling()
        print("Bot Polling Started Successfully!")
    yield
    if tg_app:
        await tg_app.updater.stop()
        await tg_app.stop()
        await tg_app.shutdown()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

