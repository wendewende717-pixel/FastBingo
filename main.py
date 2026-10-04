import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://fast-bingo-bot.onrender.com")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.reply_text(
        text=welcome_text,
        reply_markup=inline_markup
    )
    
    await update.message.reply_text(
        text="👇 ከታች ያሉትን አማራጮች ይጠቀሙ፦",
        reply_markup=reply_markup
    )

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN environment variable not set.")
        return

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
