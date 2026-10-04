import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-render-url.onrender.com")

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
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("እባክዎን Render / Environment variables ላይ BOT_TOKEN ማስገባትዎን ያረጋግጡ!")
        return

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
