import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

@app.route('/')
def home():
    return "FastBingo Bot is Running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("እንኳን ወደ Fast Bingo በሰላም መጡ! ጨዋታ ለመጀመር ዝግጁ ነዎት።")

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN is missing!")
        return

    threading.Thread(target=run_flask, daemon=True).start()

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
