import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class CustomWebAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

def run_http_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), CustomWebAppHandler)
    print(f"Serving WebApp on port {port}...")
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name
    
    account_id = f"FB-{user_id}"
    web_app_url = "https://my-fastbingo-app.onrender.com"

    keyboard = [
        [InlineKeyboardButton("🎮 ቢንጎ ተጫወት (Play)", web_app=WebAppInfo(url=web_app_url)), InlineKeyboardButton("📝 ምዝገባ", callback_data="reg")],
        [InlineKeyboardButton("💵 ቀሪ ሂሳብ (Balance)", callback_data="bal"), InlineKeyboardButton("💳 ብር መሙያ (Deposit)", callback_data="dep")],
        [InlineKeyboardButton("☎️ እገዛ (Support)", callback_data="sup"), InlineKeyboardButton("📖 መመሪያ (Instruction)", callback_data="inst")],
        [InlineKeyboardButton("🎁 ብር ማስተላለፊያ", callback_data="trans"), InlineKeyboardButton("🤑 ብር ማውጫ (Withdraw)", callback_data="with")],
        [InlineKeyboardButton("🔗 ጓደኛ ጋብዝ (Invite)", callback_data="inv"), InlineKeyboardButton("🔄 ቦነስ ቀይር", callback_data="bon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_txt = (
        f"👋 እንኳን ወደ **Fast Bingo NextGen Pro** በደህና መጡ!\n\n"
        f"👤 **ስም:** {first_name}\n"
        f"🆔 **የእርስዎ ቋሚ ID:** `{account_id}`\n"
        f"💰 **የአካውንትዎ ቀሪ ሂሳብ:** 0.0 ብር\n\n"
        f"ከታች ካሉት አማራጮች አንዱን ይምረጡ፦"
    )

    photo_path = "static/logo.png"

    try:
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo_file,
                    caption=welcome_txt,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
        else:
            await update.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to send photo: {e}")
        await update.message.reply_text(welcome_txt, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    account_id = f"FB-{user.id}"

    data = query.data

    if data == "bal":
        await query.message.reply_text(f"💵 **የቀሪ ሂሳብ መረጃ**\n\n🆔 ID: `{account_id}`\n💰 ቀሪ ሂሳብ: **0.0 ብር**", parse_mode="Markdown")
    elif data == "dep":
        await query.message.reply_text("💳 **ብር መሙያ (Deposit)**\n\nበቴሌብር (Telebirr) ወይም ቻፓ (Chapa) ሂሳብዎን መሙላት ይችላሉ።\nለማስገባት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "with":
        await query.message.reply_text("🤑 **ብር ማውጫ (Withdraw)**\n\nዝቅተኛ የማውጫ መጠን: **50 ብር**\nለማውጣት የሚፈልጉትን የብር መጠን ይጻፉ፦", parse_mode="Markdown")
    elif data == "sup":
        await query.message.reply_text("☎ **የደንበኞች እገዛ (Support)**\n\nለማንኛውም ጥያቄ ወይም አቤቱታ በቴሌግራም ያውሩን፦ @wende4366", parse_mode="Markdown")
    elif data == "inst":
        await query.message.reply_text("📖 **የጨዋታ መመሪያ (Instruction)**\n\n1. 'ቢንጎ ተጫወት' የሚለውን በመጫን ቦርዱን ይክፈቱ።\n2. ከ 1-600 ካርቴላዎች ውስጥ የሚፈልጉትን ይምረጡ።\n3. ቁጥሮች ሲጠሩ በራሱ ወይም በእጅዎ ይመልከቱ።\n4. ቀድመው ቢንጎ ሲሰሩ ያሸንፋሉ!", parse_mode="Markdown")
    elif data == "reg":
        await query.message.reply_text(f"📝 **የምዝገባ መረጃ**\n\nተመዝግበዋል! የቋሚ መለያ ቁጥርዎ: `{account_id}` ነው::", parse_mode="Markdown")
    elif data == "trans":
        await query.message.reply_text("🎁 **ብር ማስተላለፊያ (Transfer)**\n\nለሌላ ተጫዋች ብር ለማስተላለፍ የያዙትን ID ያስገቡ፦", parse_mode="Markdown")
    elif data == "inv":
        await query.message.reply_text(f"🔗 **ጓደኛ ይጋብዙ**\n\nይህንን የጋበዛ ሊንክ ለጓደኞችዎ በመላክ ቦነስ ያግኙ፦\nhttps://t.me/FastBingoBot?start={account_id}", parse_mode="Markdown")
    elif data == "bon":
        await query.message.reply_text("🔄 **ቦነስ መመንዘሪያ**\n\nያለዎት የቦነስ ነጥብ: **0 Points** (100 Points = 10 ብር)", parse_mode="Markdown")

def main():
    threading.Thread(target=run_http_server, daemon=True).start()

    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        TOKEN = "8156382103:AAH..." # <--- የቦትህ Token

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Fast Bingo Bot running smoothly...")
    app.run_polling()

if __name__ == "__main__":
    main()
